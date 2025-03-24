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
from project_api.vespucciprjmng.domain.deployment import Application
from project_api.vespucciprjmng.repository.exceptions.resource_already_exist import (
    ResourceAlreadyExisting,
)
from datetime import datetime

logger = logging.getLogger(__name__)

def normalize_value(value):
    if value == '' or value == "":
        return None
    else:
        return value

def app_create_deployment_id(user, project_name, body: dict):
    if connexion.request.is_json:
        body = connexion.request.get_json()
        applications = body.get("applications")
        deployment = body.get("deployment")
        
        if not deployment:
            return response_error(msg="Missing deployment in the request body", status_code=400)
        
        project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
        project = project_repo.get_project(project_name=project_name)
        curr_app_uuids = {app.uuid: app for app in project.applications}

        uuid_mapping = {}
        new_apps = []

        if applications:
            for app in applications:
                existing_app = next(
                    (
                        _app for _app in project.applications
                        if (normalize_value(getattr(_app, 'device_template_id', None)) == normalize_value(app.get('device_template_id')))
                        and (normalize_value(getattr(_app, 'device_template_uri', None)) == normalize_value(app.get('device_template_uri')))
                        and (normalize_value(getattr(_app, 'device_manifest_uri', None)) == normalize_value(app.get('device_manifest_uri')))
                        and (normalize_value(getattr(_app, 'image_uri', None)) == normalize_value(app.get('image_uri')))
                        and (normalize_value(getattr(_app, 'module_id', None)) == normalize_value(app.get('module_id')))
                        and (normalize_value(getattr(_app, 'type', None)) == normalize_value(app.get('type')))
                        and (normalize_value(getattr(_app, 'binary_uri', None)) == normalize_value(app.get('binary_uri')))
                        and (normalize_value(getattr(_app, 'binary_id', None)) == normalize_value(app.get('binary_id')))
                        and (normalize_value(getattr(_app, 'protocol', None)) == normalize_value(app.get('protocol')))
                    ),
                    None
                )
                
                if existing_app:
                    # Use the UUID of the existing application
                    uuid_mapping[app['uuid']] = existing_app.uuid
                    logger.debug(f"Depl App Match found uuid: {existing_app.uuid}!")
                else:                    
                    # Generate a new UUID for the new application
                    new_uuid = str(uuid4())
                    uuid_mapping[app['uuid']] = new_uuid
                    app['uuid'] = new_uuid
                    logger.debug("Depl App Match not found, generating new uuid: {new_uuid}")
                    new_apps.append(app)
    
        # Replace UUIDs in deployment gateway and leaf devices
        for gateway in deployment['gateway']:
            if gateway['application'] in uuid_mapping:
                gateway['application'] = uuid_mapping[gateway['application']]
            elif gateway['application'] not in curr_app_uuids:
                return response_error(msg=f"Deployment references non-existing gw application UUID: {gateway['application']}", status_code=404)

        for leaf in deployment['leaf']:
            if 'datalogging' in leaf:
                if leaf['datalogging']['application'] in uuid_mapping:
                    leaf['datalogging']['application'] = uuid_mapping[leaf['datalogging']['application']]
                elif leaf['datalogging']['application'] not in curr_app_uuids:
                    return response_error(msg=f"Deployment references non-existing datalogging application UUID: {leaf['datalogging']['application']}", status_code=404)
            if 'inference' in leaf:
                if leaf['inference']['application'] in uuid_mapping:
                    leaf['inference']['application'] = uuid_mapping[leaf['inference']['application']]
                elif leaf['inference']['application'] not in curr_app_uuids:
                    return response_error(msg=f"Deployment references non-existing inference application UUID: {leaf['inference']['application']}", status_code=404)
        
        # Create new deployment object
        new_deployment = NewDeployment.from_dict(deployment)  # noqa: E501
        apps = []
        if new_apps:
            for app in new_apps:
                new_app = DeploymentApplication.from_dict(app)
                apps.append(new_app)

        try:
            project_repo.create_deployment(
                project_name=project_name,
                deployment_name=new_deployment.display_name,
                description=new_deployment.description,
                cloud_type=new_deployment.cloud_params.type,
                cloud_app_url=new_deployment.cloud_params.app_url,
                leaf_devices=new_deployment.leaf,
                gw_devices=new_deployment.gateway,
                applications=apps
            )
        except ResourceAlreadyExisting as e:
            return response_error(msg="Deployment resource already existing", status_code=400)
    
        return Response(status=201)
        
    return response_error(msg="JSON Body error", status_code=400)

def app_delete_deployment_id (user, project_name, deployment_id):
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_repo.dao_factory.get_deployment_dao_instance().delete(project_name=project_name, deployment_uuid_or_name=deployment_id)

    return Response(status=200)
    
def app_update_deployment_id(user, project_name, deployment_id, body: dict):
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)
    j = os.path.join(workspace, project_path)
    
    try:
        with open(j, 'rt') as jf:
            project = json.load(jf)
            deploys: list = project.get("deployments", [])
            applications: list = project.get("applications", [])
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            curr_app_uuids = [app["uuid"] for app in applications]
            logger.debug(f"Current apps: {curr_app_uuids}")
            
            if deploy is None:
                return response_error(msg="Deployment not found", status_code=404)

            update_flag = False

            # Update display_name
            if body.get("display_name") is not None:
                deploy["display_name"] = body["display_name"]
                update_flag = True

            # Update last_deploy_result
            if body.get("last_deploy_result") is not None:
                deploy["last_deploy_result"] = body["last_deploy_result"]
                update_flag = True

            # Update cloud_params
            if body.get("cloud_params") is not None:
                if body["cloud_params"].get("app_url") is not None:
                    deploy["cloud_params"]["app_url"] = body["cloud_params"]["app_url"]
                if body["cloud_params"].get("type") is not None:
                    deploy["cloud_params"]["type"] = body["cloud_params"]["type"]
                update_flag = True

            if "leaf" in deploy:
                deploy_leaves: list = deploy["leaf"]

            # Update gateway devices
            if "gateway" in deploy:
                gateways: list = deploy["gateway"]
                if body.get("gateway") is not None:
                    for in_gateway in body["gateway"]:
                        my_gateway = next((el for el in gateways if el["device_id"] == in_gateway.get("_device_id")), None)
                        if my_gateway is not None:
                            # Update all relevant fields for gateway devices
                            if in_gateway.get("device_id") is not None:
                                my_gateway["device_id"] = in_gateway["device_id"]
                            if in_gateway.get("application") is not None:
                                appl = in_gateway["application"]
                                if appl not in curr_app_uuids:
                                    return response_error(msg=f"Deployment references non-existing gateway application UUID: {appl}", status_code=404)
                                my_gateway["application"] = appl
                            if in_gateway.get("description") is not None:
                                my_gateway["description"] = in_gateway["description"]
                            if in_gateway.get("display_name") is not None:
                                my_gateway["display_name"] = in_gateway["display_name"]
                            if in_gateway.get("wifi_mode") is not None:
                                my_gateway["wifi_mode"] = in_gateway["wifi_mode"]
                            update_flag = True

                            # Update gateway_id in leaf devices which used this GW
                            for my_leaf in deploy_leaves:
                                if my_leaf["gateway_id"] == in_gateway.get("device_id"):
                                    my_leaf["gateway_id"] = in_gateway["device_id"]
                        else:
                            return response_error(msg="Gateway device not found", status_code=404)
                        
            # Update leaf devices
            if "leaf" in deploy:
                if body.get("leaf") is not None:
                    for in_leaf in body["leaf"]:
                        my_leaf = next((el for el in deploy_leaves if el["device_id"] == in_leaf.get("_device_id")), None)
                        if my_leaf is not None:
                            # Update all relevant fields for leaf devices
                            if in_leaf.get("device_id") is not None:
                                my_leaf["device_id"] = in_leaf["device_id"]
                            if in_leaf.get("description") is not None:
                                my_leaf["description"] = in_leaf["description"]
                            if in_leaf.get("display_name") is not None:
                                my_leaf["display_name"] = in_leaf["display_name"]
                            if in_leaf.get("gateway_id") is not None:
                                gws = [gwi["device_id"] for gwi in deploy["gateway"]]
                                if in_leaf["gateway_id"] not in gws:
                                    return response_error(msg=f"Deployment leaf references non-existing gateway device ID: {in_leaf['gateway_id']}", status_code=404)
                                my_leaf["gateway_id"] = in_leaf["gateway_id"]
                            if in_leaf.get("datalogging") is not None:
                                if my_leaf.get("datalogging") is None:
                                    my_leaf["datalogging"] = {}
                                if in_leaf["datalogging"].get("application") is not None:
                                    appl = in_leaf["datalogging"]["application"]
                                    if appl not in curr_app_uuids:
                                        return response_error(msg=f"Deployment references non-existing datalogging application UUID: {appl}", status_code=404)
                                    my_leaf["datalogging"]["application"] = appl
                                if in_leaf["datalogging"].get("firmware_update") is not None:
                                    my_leaf["datalogging"]["firmware_update"] = in_leaf["datalogging"]["firmware_update"]
                            if in_leaf.get("inference") is not None:
                                if my_leaf.get("inference") is None:
                                    my_leaf["inference"] = {}
                                if in_leaf["inference"].get("application") is not None:
                                    appl = in_leaf["inference"]["application"]
                                    if appl not in curr_app_uuids:
                                        return response_error(msg=f"Deployment references non-existing inference application UUID: {appl}", status_code=404)
                                    my_leaf["inference"]["application"] = appl
                                if in_leaf["inference"].get("firmware_update") is not None:
                                    my_leaf["inference"]["firmware_update"] = in_leaf["inference"]["firmware_update"]
                                if in_leaf["inference"].get("models") is not None:
                                    my_leaf["inference"]["models"] = in_leaf["inference"]["models"] # The whole models list is updated currently
                            update_flag = True
                        else:
                            return response_error(msg="Leaf Device not found", status_code=404)            
                
            # If deployment object has been updated, set the timestamp
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

def app_delete_application_id (user, project_name, application_id):
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_repo.dao_factory.get_deployment_app_dao_instance().delete(project_name=project_name, application_uuid_or_name=application_id)

    return Response(status=200)

def get_artifacts (project_name, deployment_name, device_id, log_uuid):
    # Unused
    return Response(status=501)

