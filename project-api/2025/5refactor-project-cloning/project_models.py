import json
import os
import re
import shutil
from datetime import datetime
from uuid import uuid4
import json
from project_api.globals import GlobalObjects
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def generate_project_uuid(project_file_path: str):
    txt = None
    with open(project_file_path, "r") as f:
        txt = f.read()
        occurs = re.findall(r"uuid_to_replace_\w+", txt)
        occurs = list(dict.fromkeys(occurs))
        for occ in occurs:
            txt = txt.replace(occ, str(uuid4()))

    with open(project_file_path, "w") as f:
        project_json_obj = json.loads(txt)
        json.dump(project_json_obj, f)
        
def generate_project_uuid_custom_project(project_file_path: str):
    obj = None
    with open(project_file_path, "r") as f:
        obj = json.load(f)
        obj['uuid'] = str(uuid4())
        for model in obj['models']:
            model['uuid'] = str(uuid4())
        for app in obj['applications']:
            app['uuid'] = str(uuid4())
        for deployment in obj['deployments']:
            deployment['uuid'] = str(uuid4())

    with open(project_file_path, "w") as f:
        json.dump(obj, f)


def set_model_owner_uuid(project_file_path: str, model_owner_uuid: str):
    with open(project_file_path, "r") as f:
        project_json_obj = json.load(f)
        for model in project_json_obj["models"]:
            model["model_owner_uuid"] = model_owner_uuid
    with open(project_file_path, "w") as f:
        json.dump(project_json_obj, f)


def substitute_artifacts_project_name(project_folder_path: str, project_file_path: str, new_project_name: str):
    with open(project_file_path, "r") as f:
        project_json_obj = json.load(f)

    project_json_obj["ai_project_name"] = new_project_name
    project_json_obj["creation_time"] = str(datetime.now())
    project_json_obj["last_update_time"] = project_json_obj["creation_time"]

    for model in project_json_obj["models"]:
        model["creation_time"] = str(datetime.now())
        model["last_update_time"] = model["creation_time"]
        
    for deployment in project_json_obj["models"]:
        deployment.update({"last_update_time": str(datetime.now())})
    
    with open(project_file_path, "w") as f:
        json.dump(project_json_obj, f)

def create_model_fs_copy(model_name_to_copy: str, new_model_name: str, dest_folder: str):
    # Prepare folder/file paths
    user_project_model_clone_folder = os.path.join(dest_folder, model_name_to_copy)
    user_project_model_dest_folder = os.path.join(dest_folder, new_model_name)

    # Copy recursively project folder and rename it
    shutil.copytree(user_project_model_clone_folder, user_project_model_dest_folder)
    
    return user_project_model_dest_folder

def generate_script_artifacts(script_path: str, script_config_path: str, schema_config_path: str, project_name: str, model_name: str, experiment_name: str, classes):

    new_jupyter = None
    configuration = None
    with open(script_path, 'r') as jupyter_f:
        with open(script_config_path, 'r') as configuration_f:
            jupyter = json.load(jupyter_f)
            configuration = json.load(configuration_f)
            
            if script_config_path:
                configuration["$schema"] = schema_config_path

            configuration["general"]["project"] = project_name
            configuration["general"]["model"] = model_name
            configuration["general"]["experiment"] = experiment_name

            if classes:
                configuration["general"]["classes"] = classes
            
            new_jupyter = _substitute_conf_cell(jupyter=jupyter, configuration=configuration)
    
    if new_jupyter:
        with open(script_path, "w") as json_file:
            # Substitute conf cell
            for cell in new_jupyter["cells"]:
                if "# Auto-generated configuration cell" in cell["source"][0]:
                    if configuration:
                        conf_cell = ["# Auto-generated configuration cell (do not delete this line).\n", "\n"]
                        for majorkey, subdict in configuration.items():
                            try:
                                items = subdict.items()
                                conf_cell.append("# " + majorkey + ".\n")
                                for subkey, value in items:
                                    if type(value) is str:
                                        conf_cell.append(subkey.upper() + " = \"" + value + "\"\n")
                                    if type(value) is int:
                                        conf_cell.append(subkey.upper() + " = " + str(value) + "\n")
                                    if type(value) is float:
                                        conf_cell.append(subkey.upper() + " = " + str(value) + "\n")
                                    if type(value) is bool:
                                        if value == False:
                                            conf_cell.append(subkey.upper() + " = False\n")
                                        else:
                                            conf_cell.append(subkey.upper() + " = True\n")
                                    if type(value) is list:
                                        conf_cell.append(subkey.upper() + " = " + str(value) + "\n")
                                    if value is None:
                                        conf_cell.append(subkey.upper() + " = None\n")
                                conf_cell.append("\n")
                            except Exception as e:
                                print(e)
                        cell["source"] = conf_cell
            # Write JN
            json_file.write(json.dumps(new_jupyter, indent=4))

        with open(script_config_path, "w") as json_file:
            json_file.write(json.dumps(configuration, indent=4))  



def _substitute_conf_cell(configuration, jupyter):
    configuration_cell = None
    for cell in jupyter["cells"]:
        if "metadata" in cell:
            if "is_configuration_cell" in cell["metadata"]:
                configuration_cell = cell

    if configuration_cell:
        configuration_cell["source"] = []
        for k in configuration.keys():
            configuration_topic = configuration[k]

            if isinstance(configuration_topic, dict):
                first = False
                for j in configuration_topic.keys():
                    try:
                        if first:
                            configuration_cell["source"].append(" ")
                            title = k.replace("_", " ")
                            configuration_cell["source"].append("# " + title + ".")
                            first = False
                    except:
                        pass
                    
                    row = "" + j.upper() + " = "

                    if isinstance(configuration_topic[j], str):
                        row += "\"" + configuration_topic[j].replace('"', '\"') + "\""
                    elif isinstance(configuration_topic[j], dict):
                        row += json.dumps(configuration_topic[j]).replace('"', '\"')
                    elif isinstance(configuration_topic[j], list):
                        row += json.dumps(configuration_topic[j]).replace('"', '\"')
                    elif configuration_topic[j] == True:
                        row += "True"
                    elif configuration_topic[j] == False:
                        row += "False"
                    elif configuration_topic[j] == None:
                        row += "None"
                    else:
                        row += str(configuration_topic[j])

                    configuration_cell["source"].append(row)
    
    return jupyter
    
