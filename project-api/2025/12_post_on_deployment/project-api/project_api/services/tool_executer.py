
from __future__ import annotations

import json
import os
import shutil
import sys
import time
import traceback
import uuid
from tempfile import TemporaryFile
from typing import IO, Any, List, Mapping, Sequence
from zipfile import ZipFile

import requests

from project_api.globals import (
    CONVERSION_JOB_MAX_CONSECUTIVE_POLLING_ERRORS,
    CONVERSION_JOB_TEMPLATE_ID,
    JOBCONTROL_API_BASE_URL,
)
from project_api.services.models.tools import ToolDescriptor, ToolSection
from project_api.utils import threads
from project_api.vespucciprjmng.domain.input import InputType
from project_api.vespucciprjmng.domain.model import ModelType
from project_api.vespucciprjmng.domain.output import OutputType


def create_conversion_job(
    auth_token: str,
    template_id: str,
    log_folder_path: str,
    runtime: str,
    tool_uri: str,
    params: Mapping[str, str]
) -> Mapping[str, Any]:

    temp_file_name = f"/tmp/{uuid.uuid4()}"
    archive_filename = shutil.make_archive(temp_file_name, "zip", log_folder_path)

    with open(archive_filename, "rb") as file:
        fet = requests.post(
            JOBCONTROL_API_BASE_URL + "/jobs",
            headers={
                "Authorization": f"Bearer {auth_token}"
            },
            data={
                "templateId": template_id,
                "runtimeInput": json.dumps({
                    "conversionParams": {
                        "runtime": runtime,
                        "script": tool_uri,
                        "argv": params
                    }
                })
            },
            files={ "file": ("datalog", file) }
        ).json()
    
    os.remove(archive_filename)

    return fet

_max_consecutive_errors = int(CONVERSION_JOB_MAX_CONSECUTIVE_POLLING_ERRORS)

# This function blocks the current thread, it needs to be run in a thread pool
def await_job_ready(auth_token: str, job_id: str) -> Mapping[str, Any]:

    consecutive_error_status = 0

    while True:
        res = requests.get(
            f"{JOBCONTROL_API_BASE_URL}/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

        if not res.ok:
            consecutive_error_status += 1
            if consecutive_error_status >= _max_consecutive_errors:
                msg = (
                    "Too many failed request while waiting "
                    f"for job {job_id} job to become ready"
                )
                raise Exception(msg)
            else:
                continue
        else:
            consecutive_error_status = 0

        job = res.json()

        if job["status"] not in ("Pending", "Running"):
            return job

        time.sleep(1.5)

def deliver_dataset(dataset_folder: str, archive_bytes: IO[bytes]) -> None:
    os.makedirs(dataset_folder, exist_ok=True)

    with ZipFile(archive_bytes, "r") as archive:
        archive.extractall(dataset_folder)

def finalize_conversion_fallible(
    token_info: Mapping[str, Any],
    dataset_folder: str,
    job_id: str
) -> None:
    
    auth_token = token_info["token_string"]

    done = await_job_ready(auth_token, job_id)

    status = done["status"]
    if status != "Succeeded":
        msg = f"Conversion job {job_id} has unexpected status: {status}"
        raise Exception(msg)

    with TemporaryFile("w+b") as file:

        artifacts: Sequence[Any] = done["outputs"]["artifacts"]
        dataset = next(
            (item for item in artifacts if item["name"] == "dataset")
        )

        with requests.get(
            dataset["authorizedGetUrl"],
            stream=True
        ) as res:
            if not res.ok:
                msg = (
                    "Request to artifact repository returned"
                    f" unexpected status: {res.status_code}"
                )
                raise Exception(msg)
            
            for chunk in res.iter_content():
                file.write(chunk)

        file.seek(0)
        deliver_dataset(dataset_folder, file)
        requests.delete(
            f"{JOBCONTROL_API_BASE_URL}/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

        
def finalize_conversion(
    token_info: Mapping[str, Any],
    dataset_folder: str,
    job_id: str
) -> None:
    try:
        finalize_conversion_fallible(
            token_info,
            dataset_folder,
            job_id
        )
    except Exception:
        print(f"Error finalizing conversion job {job_id}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

# For now, a single template is sufficient to handle all tools. If this changes,
# this mapping may be updated
def map_tool_template_id(tool: Any) -> str:
    return CONVERSION_JOB_TEMPLATE_ID

TOOL_EXECUTER_FILE_PATH = os.path.join(os.path.dirname(__file__), "main_executer.py")

class ToolExecuter():

    @property
    def assets_folder_path_placeholder_name(self) -> str:
        return self.__assets_folder_path_placeholder_name

    @property
    def assets_folder_path(self) -> str:
        return self.__assets_folder_path
    
    @property
    def tools(self) -> List[ToolDescriptor]:
        return self.__tools
    
    def __init__(self, assets_folder_path_placeholder_name: str, assets_folder_path: str, tools: List[ToolDescriptor]):
        self.__assets_folder_path_placeholder_name = assets_folder_path_placeholder_name
        self.__assets_folder_path = assets_folder_path
        self.__tools = tools
        pass

    def execute(self, jobs_folder_path: str, model_name: str, log_name: str, tool_name: str, tool_version: str, input_type: InputType, model_type: ModelType, output_type: OutputType, keyword_value_pairs: dict, section: ToolSection, token_info: Mapping[str, Any]) -> Mapping[str, Any]:
        selected_tool_details: ToolDescriptor = None
        tool_details: ToolDescriptor = None
        for tool_details in self.tools:
            if tool_details.name == tool_name and input_type == tool_details.input_type and model_type == tool_details.model_type and output_type == tool_details.output_type and tool_details.section == section:
                selected_tool_details = tool_details

        if not selected_tool_details:
            raise Exception("Tool '"+ tool_name +":"+ tool_version +"' not found")
        
        tool_parameters_resolved = self.__substitute_parameters_placeholders(selected_tool_details.parameters, keyword_value_pairs) 
        tool_uri_resolved = selected_tool_details.uri.replace(self.assets_folder_path_placeholder_name, self.assets_folder_path)
        tool_parameters_resolved = [selected_tool_details.runtime, tool_uri_resolved] + tool_parameters_resolved

        # Resolve log folder path
        logs_folder_path = self.__substitute_parameters_placeholders(
            {'': selected_tool_details.parameters['']},
            keyword_value_pairs
        )[0]

        dataset_folder_path = self.__substitute_parameters_placeholders(
            {'-o': selected_tool_details.parameters['-o']},
            keyword_value_pairs
        )[0][2:]

        created_job = create_conversion_job(
            token_info["token_string"],
            map_tool_template_id(selected_tool_details),
            logs_folder_path,
            selected_tool_details.runtime,
            selected_tool_details.uri,
            selected_tool_details.parameters,
        )

        threads.executor.submit(
            finalize_conversion_fallible,
            token_info,
            dataset_folder_path,
            created_job["id"]
        )

        return created_job

    def __substitute_parameters_placeholders(self, parameters, keyword_value_pairs):
        resolved_parameters = []
        for parameter_key in parameters:
            resolved_parameter_value = parameters[parameter_key]
            for keyword_pair in keyword_value_pairs:
                keyword_k = keyword_pair[0]
                keyword_v = keyword_pair[1]
                resolved_parameter_value = resolved_parameter_value.replace(keyword_k, keyword_v)
            resolved_parameters.append(parameter_key + "" + resolved_parameter_value)
        return resolved_parameters