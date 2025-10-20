#!/usr/bin/python

import os
import subprocess
import sys
import traceback

from project_api.vespucciprjmng.domain.job import Job, OperationType
from project_api.vespucciprjmng.repository.filesystem.job_file_repo import (
    JobFileRepo,
)


def resolve_operation_type(job_type:str):
    if job_type == OperationType.LOG_CONVERSION.value:
        return OperationType.LOG_CONVERSION
    if job_type == OperationType.LOG_UPLOADING.value:
        return OperationType.LOG_UPLOADING
    if job_type == OperationType.MODEL_ANALYSIS.value:
        return OperationType.MODEL_ANALYSIS
    if job_type == OperationType.OUTPUT_GENERATION.value:
        return OperationType.OUTPUT_GENERATION
    return OperationType.UNKNOWN

print(f"{os.path.basename(__file__)} ({os.getpid()}) started.")

jobs_folder_path   = sys.argv[1]
job_name           = sys.argv[2]
job_executer_id    = sys.argv[3]
job_type           = sys.argv[4]
resource_id        = str(os.getpid())
del sys.argv[0:5]

print("Tool executer started with arguments: " + str(sys.argv))
job_repo    = JobFileRepo(jobs_folder_path)
job: Job   = None

try:
    # operation_type = OperationType[job_type + ""]
    operation_type = resolve_operation_type(job_type)
    job = job_repo.start_job(uuid=resource_id,name=job_name, executer_id=job_executer_id, operation_type=operation_type)
    result = subprocess.run(sys.argv, check=True, cwd=os.path.dirname(sys.argv[1]))
    result_description = f"Terminated (return code: '{str(result.returncode)}'). '{job_name}' / '{job_executer_id}' / '{job_type}'"
    
    job_repo.stop_job(uuid=job.uuid, state_description=result_description, failure=False)
    print(result_description)
except subprocess.CalledProcessError:
    stack_trace = traceback.format_exc()
    state_description = f"[COVERSION PROCESS] {stack_trace}"
    print(state_description)
    job_repo.stop_job(uuid=job.uuid, state_description=state_description, failure=True)
except Exception:
    stack_trace = traceback.format_exc()
    state_description = f"[MAIN EXECUTER] {stack_trace}"
    print(state_description)
    if job:
        job_repo.stop_job(uuid=job.uuid, state_description=state_description, failure=True)
