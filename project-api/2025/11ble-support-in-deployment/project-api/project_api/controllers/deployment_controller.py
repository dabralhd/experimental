import os
import connexion
import json
import logging
from project_api.utils.func_dec import (default_except)
from flask import Response, send_file
from uuid import uuid4
from project_api.utils.func_dec import (not_supported_for_org)
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
from project_api.utils.error_helper import (get_prj_api_log_level)

logger = logging.getLogger(__name__)
logger.setLevel(get_prj_api_log_level())

def normalize_value(value):
    if value == '' or value == "":
        return None
    else:
        return value

@default_except
@not_supported_for_org
def app_create_deployment_id(user, project_name, body: dict):
    logger.info(f"app_create_deployment_id: user={user}, project={project_name}")
    if connexion.request.is_json:
        body = connexion.request.get_json()
        logger.debug(f"Incoming body keys: {list(body.keys())}")
        applications = body.get("applications")
        deployment = body.get("deployment")
        
        if not deployment:
            logger.warning("Missing 'deployment' in request body")
            return response_error(msg="Missing deployment in the request body", status_code=400)
        
        project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
        project = project_repo.get_project(project_name=project_name)
        curr_app_uuids = {app.uuid: app for app in project.applications}

        uuid_mapping = {}
        new_apps = []

        if applications:
            logger.debug(f"Applications received: {len(applications)}")
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
                    logger.debug(f"Depl App Match not found, generating new uuid: {new_uuid}")
                    new_apps.append(app)
        logger.info(f"UUID mapping created for {len(uuid_mapping)} apps; new apps to create: {len(new_apps)}")
    
        # Replace UUIDs in deployment gateway and leaf devices
        for gateway in deployment['gateway']:
            if gateway['application'] in uuid_mapping:
                gateway['application'] = uuid_mapping[gateway['application']]
            elif gateway['application'] not in curr_app_uuids:
                logger.warning(f"Non-existing gw application UUID referenced: {gateway['application']}")
                return response_error(msg=f"Deployment references non-existing gw application UUID: {gateway['application']}", status_code=404)

        for leaf in deployment['leaf']:
            if 'datalogging' in leaf:
                if leaf['datalogging']['application'] in uuid_mapping:
                    leaf['datalogging']['application'] = uuid_mapping[leaf['datalogging']['application']]
                elif leaf['datalogging']['application'] not in curr_app_uuids:
                    logger.warning(f"Non-existing datalogging application UUID referenced: {leaf['datalogging']['application']}")
                    return response_error(msg=f"Deployment references non-existing datalogging application UUID: {leaf['datalogging']['application']}", status_code=404)
            if 'inference' in leaf:
                if leaf['inference']['application'] in uuid_mapping:
                    leaf['inference']['application'] = uuid_mapping[leaf['inference']['application']]
                elif leaf['inference']['application'] not in curr_app_uuids:
                    logger.warning(f"Non-existing inference application UUID referenced: {leaf['inference']['application']}")
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
            logger.warning(f"Deployment already exists: {new_deployment.display_name}")
            return response_error(msg="Deployment resource already existing", status_code=400)
        logger.info(f"Deployment created: name={new_deployment.display_name}, apps_created={len(apps)}")
    
        return Response(status=201)
        
    return response_error(msg="JSON Body error", status_code=400)

@default_except
@not_supported_for_org
def app_delete_deployment_id (user, project_name, deployment_id):
    logger.info(f"app_delete_deployment_id: user={user}, project={project_name}, deployment_id={deployment_id}")
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_repo.dao_factory.get_deployment_dao_instance().delete(project_name=project_name, deployment_uuid_or_name=deployment_id)
    logger.info(f"Deployment deleted: {deployment_id}")
    return Response(status=200)

@default_except
@not_supported_for_org
def app_update_deployment_id(user, project_name, deployment_id, body: dict):
    logger.info(f"app_update_deployment_id: user={user}, project={project_name}, deployment_id={deployment_id}")
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)
    j = os.path.join(workspace, project_path)
    logger.debug(f"Project file path: {j}")
    
    try:
        with open(j, 'rt') as jf:
            project = json.load(jf)
            deploys: list = project.get("deployments", [])
            applications: list = project.get("applications", [])
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            curr_app_uuids = [app["uuid"] for app in applications]
            logger.debug(f"Current apps: {curr_app_uuids}")
            
            if deploy is None:
                logger.warning(f"Deployment not found: {deployment_id}")
                return response_error(msg="Deployment not found", status_code=404)

            update_flag = False

            # Update display_name
            if body.get("display_name") is not None:
                deploy["display_name"] = body["display_name"]
                update_flag = True
                logger.debug("Updated deployment display_name")

            # Update last_deploy_result
            if body.get("last_deploy_result") is not None:
                deploy["last_deploy_result"] = body["last_deploy_result"]
                update_flag = True
                logger.debug("Updated last_deploy_result")

            # Update cloud_params
            if body.get("cloud_params") is not None:
                if body["cloud_params"].get("app_url") is not None:
                    deploy["cloud_params"]["app_url"] = body["cloud_params"]["app_url"]
                if body["cloud_params"].get("type") is not None:
                    deploy["cloud_params"]["type"] = body["cloud_params"]["type"]
                update_flag = True
                logger.debug("Updated cloud_params")

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
                            logger.debug(f"Updated gateway device: {in_gateway.get('device_id')}")

                            # Update gateway_id in leaf devices which used this GW
                            for my_leaf in deploy_leaves:
                                if my_leaf["gateway_id"] == in_gateway.get("device_id"):
                                    my_leaf["gateway_id"] = in_gateway["device_id"]
                        else:
                            logger.warning("Gateway device not found for update")
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
                            logger.debug(f"Updated leaf device: {in_leaf.get('device_id')}")
                        else:
                            logger.warning("Leaf Device not found for update")
                            return response_error(msg="Leaf Device not found", status_code=404)            
                
            # If deployment object has been updated, set the timestamp
            if update_flag:
                deploy["last_update_time"] = str(datetime.now())
                logger.info(f"Deployment updated: {deployment_id}")
                
    except OSError as e:
        logger.exception("Failed reading project file for update")
        return Response(status=400)

    # Now actually write the file
    try:
        with open(j, 'wt') as jf:
            json.dump(project, jf, indent=4)
    except OSError as e:
        logger.exception("Failed writing updated project file")
        return Response(status=400)

    return Response(status=200)

@default_except
@not_supported_for_org
def app_get_deployment_leaf (user, project_name, deployment_id, device_id, resource):
    logger.info(f"app_get_deployment_leaf: user={user}, project={project_name}, deployment_id={deployment_id}, device_id={device_id}, resource={resource}")
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)         # get_started_motor_classification

    j = os.path.join(workspace, project_path)
    logger.debug(f"Project file path: {j}")

    try:
        with open(j, 'r') as jf:
            project = json.load(jf)
            deploys : list = project["deployments"]                         # uuid_to_replace_deployment1
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            if deploy is None:
                logger.warning(f"Deployment not found: {deployment_id}")
                return Response(status=404)
            device = next((el for el in deploy["leaf"] if el["device_id"] == device_id), None)
            if device is None:
                logger.warning(f"Leaf device not found: {device_id}")
                return Response(status=404)
    except OSError:
        logger.exception("Failed reading project file for leaf resource")
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
        logger.debug(f"Resolved leaf resource path: {path}")
        if (os.path.isfile(path)):
            return send_file(path)
        else:
            return target

    target = "NOT AVAILABLE" if target is None else target
    return Response(status=404, response=target)

@default_except
@not_supported_for_org
def app_get_deployment_gateway (user, project_name, deployment_id, device_id, resource):
    logger.debug(f"app_get_deployment_gateway: user={user}, project={project_name}, deployment_id={deployment_id}, device_id={device_id}, resource={resource}")
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)         # get_started_motor_classification

    j = os.path.join(workspace, project_path)
    logger.debug(f"Project file path: {j}")
    
    try:
        with open(j, 'r') as jf:
            project = json.load(jf)
            deploys : list = project["deployments"]                         # uuid_to_replace_deployment1
            deploy = next((el for el in deploys if el["uuid"] == deployment_id), None)
            if deploy is None:
                logger.warning(f"Deployment not found: {deployment_id}")
                return Response(status=404)
            device = next((el for el in deploy["gateway"] if el["device_id"] == device_id), None)
            if device is None:
                logger.warning(f"Gateway device not found: {device_id}")
                return Response(status=404)
    except OSError:
        logger.exception("Failed reading project file for gateway resource")
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
        logger.debug(f"Resolved gateway resource path: {path}")
        if (os.path.isfile(path)):
            return send_file(path)
        else:
            return target

    target = "NOT AVAILABLE" if target is None else target
    return Response(status=404, response=target)

@default_except
@not_supported_for_org
def app_delete_application_id (user, project_name, application_id):
    logger.info(f"app_delete_application_id: user={user}, project={project_name}, application_id={application_id}")
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_repo.dao_factory.get_deployment_app_dao_instance().delete(project_name=project_name, application_uuid_or_name=application_id)
    logger.info(f"Application deleted: {application_id}")
    return Response(status=200)

@default_except
@not_supported_for_org
def app_update_application_id (user, project_name, application_id, body: dict):
    if connexion.request.is_json:
        body = connexion.request.get_json()
        updated_app = DeploymentApplication.from_dict(body)  # noqa: E501
        logger.info(f"app_update_application_id: user={user}, project={project_name}, application_id={application_id}")
        logger.debug(f"Patch body keys: {list(body.keys())}")
        project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
        project_repo.dao_factory.get_deployment_app_dao_instance().patch(project_name=project_name, application_uuid_or_name=application_id, app = updated_app)
        logger.info(f"Application updated: {application_id}")
        return Response(status=200)
    return response_error(msg="JSON Body error", status_code=400)

@default_except
@not_supported_for_org
def get_artifacts (project_name, deployment_name, device_id, log_uuid):
    # Unused
    return Response(status=501)


@default_except
@not_supported_for_org
def app_patch_deployment_leaf(user, project_name, deployment_id, device_id, resource_type = None, resource_name = None):  # noqa: E501
    """Get files relating to a leaf device

     # noqa: E501

    :param device_id: 
    :type device_id: str
    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str
    :param resource_type: string identifying resource to patch
    :type resource_type: str
    :param resource_name: identify resource_name within the category resource_type, at present
    :type resource_name: str

    :rtype: None
    """
    logger.debug(f"> app_patch_deployment_leaf:\n user={user}\n, project={project_name}\n, deployment_id={deployment_id}\n, device_id={device_id}\n, resource_type={resource_type}\n, resource_name={resource_name}\n")
    workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    project_path = get_project_file_name(project_name=project_name)         # get_started_motor_classification

    j = os.path.join(workspace, project_path)
    logger.debug(f"Project file path: {j}")
    
    if connexion.request.is_json:
        body = connexion.request.get_json()
        logger.debug(f'requestBody: {body}')    
    
    try:
        project = None
        found_and_patched = False
        with open(j, 'r') as jf:
            project = json.load(jf)
        deploys : list = project["deployments"]
        for deploy in deploys: 
            if deployment_id == deploy.get("uuid"):
                for lf in deploy["leaf"]:
                    if lf.get("device_id") == device_id:
                        logger.debug(f"resource_type: {resource_type}, resource_name: {resource_name}")    
                        if resource_type == "datalogging" and resource_name == "application":
                            dtlg = lf.get("datalogging")
                            dtlg["application"] = body.get("application")
                            found_and_patched = True
                            break
                        elif resource_type == "datalogging" and resource_name != "application":
                            lf["datalogging"] = dict()
                            found_and_patched = True
                            break
                        elif resource_type == "inference" and resource_name == "application":
                            infr = lf.get("inference")
                            if infr and infr["application"]:
                                logger.debug(f"setting infr.application")
                                infr["application"] = body.get("application")
                                found_and_patched = True
                                break
                        elif resource_type == "inference" and resource_name == "model_name_reference":
                            infr = lf.get("inference")
                            models = infr.get("models")
                            if len(models)==1:
                                models[0]["model_name_reference"] = body.get("model_name_reference")
                                found_and_patched = True
                                break                            
                        else:
                            logger.debug(f"Device found, but invalid query param combination")  
                            return Response(status=404)                
                        
                if found_and_patched:
                    break
            
        if not found_and_patched:
            logger.warning(f"Device with id '{device_id}' not found in project '{project_name}'.")
            return Response(status=404) # Not Found                
                
            logger.info(f"-writing back ai project json\n: project: {project} ")
            
        with open(j, 'w') as jf:     
            json.dump(project, jf)            
    except OSError:
        logger.exception("Failed reading project file for device resource")
        return Response(status=400)
    logger.info(f"< app_patch_deployment_leaf\npatch operation completed")
    return Response(status=200)                                
                                    

