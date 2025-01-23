import json
import os
import shutil

from project_api.globals import (
    EXPERIMENT_TEMPLATES_PATH,
    GET_STARTED_PROJECTS_PATH,
)
from project_api.services.models.templates import (
    TemplateDescriptor,
    TemplateType,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

def get_started_projects():
    get_started_project_names = os.listdir(GET_STARTED_PROJECTS_PATH)
    project_jsons = []

    for folder_name in get_started_project_names:
        project_name = folder_name
        project_file = os.path.join(GET_STARTED_PROJECTS_PATH, folder_name, f'ai_{project_name}.json')
        with open(project_file) as f:
            project_json_str = f.read()
            project_jsons.append(json.loads(project_json_str))

    return project_jsons

def experiment_templates():
    templates = []
    entries = os.listdir(EXPERIMENT_TEMPLATES_PATH)

    for entry in entries:
        if ("template_for" in entry) and (".ipynb" in entry):
            name = entry.replace("template_for_", "").replace(".ipynb", "")
            template_type = TemplateType.EXPERIMENT_MODEL_DEV_FILE
            template_path = os.path.join(EXPERIMENT_TEMPLATES_PATH, "template_for_" + name + ".ipynb")
            template_config_path = os.path.join(EXPERIMENT_TEMPLATES_PATH, "instance_for_" + name + ".json")
            schema_template_config_path = os.path.join(EXPERIMENT_TEMPLATES_PATH, "schema_for_" + name + ".json")
            template = TemplateDescriptor(name, template_type, template_path, template_config_path, schema_template_config_path)
            templates.append(template)

    return templates

def get_started_projects_artifacts(project_name: str, model_name: str, experiment_name: str, test_name: str, artifact_name: bool):
    bytes = None
    artifact_path = os.path.join(GET_STARTED_PROJECTS_PATH, project_name, "models", model_name, "experiments", experiment_name, "tests", test_name, artifact_name)
    with open(artifact_path) as f:
        bytes = f.buffer.read()
    return bytes

def extract_get_started_project(get_started_project_name: str, new_project_name: str, dest_folder: str):

    # Prepare folder/file paths
    get_started_project_folder_path = os.path.join(GET_STARTED_PROJECTS_PATH, get_started_project_name)
    if not os.path.isdir(get_started_project_folder_path):
            logger.error(f'source project does not exists - {get_started_project_folder_path}')
            return [None, None, 400]
    project_folder = os.path.join(dest_folder, new_project_name)

    get_started_project_file_path = os.path.join(project_folder, f'ai_{get_started_project_name}.json')
    project_file_path = os.path.join(project_folder, f'ai_{new_project_name}.json')

    # Copy recursively project folder and rename it
    shutil.copytree(get_started_project_folder_path, project_folder)
    shutil.move(get_started_project_file_path, project_file_path)
    
    return [project_folder, project_file_path, 200]

import os
import shutil

def extract_user_project(src_project_name: str, new_project_name: str, user_ws_folder: str):
    """
    Extracts a user project by copying and renaming the project folder and JSON file.

    Args:
        src_project_name (str): The name of the source project.
        new_project_name (str): The name of the new project.
        user_ws_folder (str): The path to the user's workspace folder.

    Returns:
        list: A list containing the destination project folder path and the destination project JSON file path.
    """
    # Prepare folder/file paths
    src_project_folder_path = os.path.join(user_ws_folder, src_project_name)
    if not os.path.isdir(src_project_folder_path):
            logger.error(f'source project does not exists - {src_project_folder_path}')
            return [None, None, 400]

    dest_project_folder_path = os.path.join(user_ws_folder, new_project_name)

    src_project_json_file_path = os.path.join(dest_project_folder_path, f'ai_{src_project_name}.json')
    dest_project_json_file_path = os.path.join(dest_project_folder_path, f'ai_{new_project_name}.json')

    # Copy recursively project folder and rename it
    shutil.copytree(src_project_folder_path, dest_project_folder_path)
    logger.info(f'moving {src_project_json_file_path} to {dest_project_json_file_path}')
    shutil.move(src_project_json_file_path, dest_project_json_file_path)
    
    return [dest_project_folder_path, dest_project_json_file_path, 200]


def project_name_substitution(config_file_path: str, script_file_path: str, original_project_name: str, new_project_name: str):
    # Config file substitution 
    with open(config_file_path, "r") as f:
        config_json_obj = json.load(f)
    config_json_obj["general"]["project"] = new_project_name
    with open(config_file_path, "w") as f:
        json.dump(config_json_obj, f)   
    # Jupyter notebook substitution
    with open(script_file_path, "r") as f:
        model_dev_file_str = f.read()
    model_dev_file_str = model_dev_file_str.replace(f'PROJECT = \\"{original_project_name}\\"', f'PROJECT = \\"{new_project_name}\\"')
  
    with open(script_file_path, "w") as f:
        f.write(model_dev_file_str) 
    