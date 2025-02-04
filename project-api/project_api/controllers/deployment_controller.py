import os
import connexion
import json
import logging

from flask import Response, send_file
from uuid import uuid4

from project_api.globals import STORAGE_PATH, GlobalObjects, USER_WORKSPACE_SUBPATH
from project_api.models.new_deployment import NewDeployment
from project_api.models.deployment_application import DeploymentApplication
from project_api.util import response_error
from project_api.utils.vespucci_to_controller_model_converters import convert_project
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name

from datetime import datetime

logger = logging.getLogger(__name__)

def app_create_deployment_id (user, project_name, body : dict):
    if connexion.request.is_json:
        body = connexion.request.get_json()
        applications = body.get("applications")
        deployment = body.get("deployment")
        
        uuid_mapping = {app['uuid']: str(uuid4()) for app in applications}

        # Replace UUIDs in applications
        for app in applications:
            app['uuid'] = uuid_mapping[app['uuid']]

        # Replace UUIDs in deployment gateway and leaf devices
        for gateway in deployment['gateway']:
            gateway['application'] = uuid_mapping[gateway['application']]

        for leaf in deployment['leaf']:
            if 'datalogging' in leaf:
                leaf['datalogging']['application'] = uuid_mapping[leaf['datalogging']['application']]
            if 'inference' in leaf:
                leaf['inference']['application'] = uuid_mapping[leaf['inference']['application']]
        
        new_deployment = NewDeployment.from_dict(deployment)  # noqa: E501
        apps = []
        for app in applications:
            new_app = DeploymentApplication.from_dict(app)
            apps.append(new_app)

        # Create deployment
        project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
            
        project_repo.create_deployment(project_name=project_name, deployment_name=new_deployment.display_name, description=new_deployment.description,
                                        cloud_type=new_deployment.cloud_params.type, cloud_app_url=new_deployment.cloud_params.app_url,
                                        leaf_devices=new_deployment.leaf, gw_devices=new_deployment.gateway, applications=apps)
        
        return Response(status=201)
        
    return response_error(msg="Input error", status_code=400)

def app_delete_deployment_id (user, project_name, deployment_id):
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_repo.dao_factory.get_deployment_dao_instance().delete(project_name=project_name, deployment_uuid_or_name=deployment_id)

    return Response(status=200)
    
# TODO handle FS exception
def app_update_deployment_id (user, project_name, deployment_id, body : dict):
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)     # get_started_motor_classification
    j = os.path.join(workspace, project_path)
    
    try:
        with open(j, 'rt') as jf:
            project = json.load(jf)
            deploys : list = project["deployments"]                         # uuid_to_replace_deployment1
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            # Weirdo list comprehension, see https://www.w3schools.com/python/python_lists_comprehension.asp
            # I hate that syntax
            if deploy is None:
                return Response(status=404)

            update_flag = False

            if body.get("display_name") is not None:
                deploy["display_name"] = body["display_name"]
                update_flag = True

            if body.get("last_deploy_result") is not None:
                deploy["last_deploy_result"] = body["last_deploy_result"]
                update_flag = True

            if body.get("cloud_params") is not None:
                    if body.get("cloud_params").get("app_url") is not None:
                        deploy["cloud_params"]["app_url"] = body["cloud_params"]["app_url"]
                    if body.get("cloud_params").get("type") is not None:
                        deploy["cloud_params"]["type"] = body["cloud_params"]["type"]
                    update_flag = True

            if "leaf" in deploy:
                deployLeaves : list = deploy["leaf"]
                if body.get("leaf") is not None:
                    for inLeaf in body["leaf"]:

                        myLeaf = next((el for el in deployLeaves if el["device_id"] == inLeaf["_device_id"]), None)
                        if myLeaf is not None:
                            myLeaf["device_id"] = inLeaf["device_id"]
                            if not update_flag:
                                update_flag = True
                        else:
                            return Response(status=404)

            if "gateway" in deploy:        
                gateways : list = deploy["gateway"]

                if body.get("gateway") is not None:
                    for inGateway in body["gateway"]:

                        myGateway = next((el for el in gateways if el["device_id"] == inGateway["_device_id"]), None)
                        if myGateway is not None:
                            myGateway["device_id"] = inGateway["device_id"]
                            if not update_flag:
                                update_flag = True
                    
                            for myLeaf in deployLeaves:
                                if myLeaf["gateway_id"] == inGateway["_device_id"]:
                                    myLeaf["gateway_id"] = inGateway["device_id"]
                        else:
                            return Response(status=404)
                
            # if deployment object has been updated set the timestamp
            if update_flag:
                deploy["last_update_time"] = str(datetime.now())
                
    except OSError as e:
        return Response(status=400)
    
    # Now actually write the file
    try:
        with open(j, 'wt') as jf:
            json.dump(project, jf, indent=4)
    except OSError as e:
        return Response(status=400)

    return Response(status=200)

def app_get_deployment_leaf (user, project_name, deployment_id, device_id, resource):
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)         # get_started_motor_classification

    j = os.path.join(workspace, project_path)

    try:
        with open(j, 'r') as jf:
            project = json.load(jf)
            deploys : list = project["deployments"]                         # uuid_to_replace_deployment1
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            if deploy is None:
                return Response(status=404)
            device = next((el for el in deploy["leaf"] if el["device_id"] == device_id), None)
            if device is None:
                return Response(status=404)
    except OSError:
        return Response(status=400)

    # selected = next((el for el in device["models"] if el["name"] == device["selected_model_name"]), None)

    apps : list = project["applications"]
    target : str = "ERROR"

    if resource == "datalogging_device_config_uri":
        target = "NOT AVAILABLE"

    elif resource == "datalogging_device_template_uri":
        selected_app = device["datalogging"]["application"]
        app = next((el for el in apps if el["uuid"] == selected_app), None)
        if app is None:
            return Response(status=404)
        target = app["device_template_uri"]

    elif resource == "datalogging_firmware_uri":
        selected_app = device["datalogging"]["application"]
        app = next((el for el in apps if el["uuid"] == selected_app), None)
        if app is None:
            return Response(status=404)
        target = app["binary_uri"]

    elif resource == "inference_device_template_uri":
        selected_app = device["inference"]["application"]
        app = next((el for el in apps if el["uuid"] == selected_app), None)
        if app is None:
            return Response(status=404)
        target = app["device_template_uri"]

    elif resource == "inference_firmware_uri":
        selected_app = device["inference"]["application"]
        app = next((el for el in apps if el["uuid"] == selected_app), None)
        if app is None:
            return Response(status=404)
        target = app["binary_uri"]

    elif resource == "inference_ml_uri":
        target = "NOT AVAILABLE"
    else:
        return Response(status=400)
    
    if (target is not None):
        workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        path = os.path.join(workspace, project_name, target)
        if (os.path.isfile(path)):
            return send_file(path)
        else:
            return target

    target = "NOT AVAILABLE" if target is None else target
    return Response(status=404, response=target)

def app_get_deployment_gateway (user, project_name, deployment_id, device_id, resource):
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)         # get_started_motor_classification

    j = os.path.join(workspace, project_path)
    
    try:
        with open(j, 'r') as jf:
            project = json.load(jf)
            deploys : list = project["deployments"]                         # uuid_to_replace_deployment1
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            if deploy is None:
                return Response(status=404)
            device = next((el for el in deploy["gateway"] if el["device_id"] == device_id), None)
            if device is None:
                return Response(status=404)
    except OSError:
        return Response(status=400)

    apps : list = project["applications"]
    selected_app = device["application"]
    app = next((el for el in apps if el["uuid"] == selected_app), None)
    if app is None:
        return Response(status=404)
    target : str = "ERROR"
    # This is atrocious, but upgrading to Python 3.10 to get match-case syntax is broken, so...

    if resource == "configuration_uri":
        target = "NOT AVAILABLE"
    
    elif resource == "image_uri":
        target = app["image_uri"]

    elif resource == "device_manifest_uri":
        target = app["device_manifest_uri"]
        
    elif resource == "device_template_uri":
        target = app["device_template_uri"]

    else:
        return Response(status=400)
    
    if (target is not None):
        workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        path = os.path.join(workspace, project_name, target)
        if (os.path.isfile(path)):
            return send_file(path)
        else:
            return target

    target = "NOT AVAILABLE" if target is None else target
    return Response(status=404, response=target)

def get_artifacts (project_name, deployment_name, device_id, log_uuid):
    # Unused
    return Response(status=501)

