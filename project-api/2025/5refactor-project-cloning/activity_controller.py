
import connexion
from flask import Response
from project_api.util import response_error
from project_api.utils.activity_name import Activity_Name
from . import data_sufficiency_controller, job_controller, training_controller
from project_api.utils.resource_allocation import (
    is_efs_size_ok
)
from project_api.globals import VESPUCCI_ENVIRONMENT
import logging
from project_api.utils.orgs_api_wrapper import(check_orgs_membership, is_user_org_member)
from project_api.utils.error_types import (client_side_error, ErrorType)

from project_api.utils.error_helper import (model_exists)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def app_create_activity(user, body, project_name, model_name, activity_type):  # noqa: E501
    """Create new activity or update whole activity section

    :param body: The activity to be added/updated.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """
    as_org = connexion.request.args.get('as_org')  
    effective_user_id = user        
    if as_org: 
        logger.debug(f'attempting POST using as_org credentials.\n as_org: {as_org}')
        if is_user_org_member(user, as_org):
            effective_user_id = as_org
            logger.debug(f'switched effective_user_id to the organization: {as_org}')
        else:
            logger.error(f'user {user} is not a member of org {as_org}')
            return Response(status=client_side_error(ErrorType.FORBIDDEN))   

    if is_efs_size_ok(effective_user_id) == False:
        logger.error(f'EFS size limit has been breached for this user: {effective_user_id}')
        if VESPUCCI_ENVIRONMENT != "dev":
            logger.error('Refusing this request')
            return response_error(msg="Storage limit exceeded", status_code=507) # 507 == Insufficient Storage

    if connexion.request.is_json and model_exists(effective_user_id, project_name, model_name):
        logger.debug(f'app_create_activity: user: {effective_user_id}\n, project_name: {project_name}\n, model_name: {model_name}\n, activity_type: {activity_type}\n')
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return training_controller.app_create_training(effective_user_id, body, project_name, model_name)
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400) # bad request

def app_update_activity(user, body, project_name, model_name, activity_type):  # noqa: E501
    """Create new activity or update whole activity section

    :param body: The activity to be added/updated.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """ 
    if connexion.request.is_json:
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return training_controller.app_create_training(user, body, project_name, model_name)
        elif activity_type ==  Activity_Name.Activity_Name_Data_Sufficiency.value:
            pass
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400) # bad request

def app_patch_activity(user, body, project_name, model_name, activity_type):  # noqa: E501
    """Create new activity

    :param body: The activity to be added.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """ 
    
    if connexion.request.is_json:
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return training_controller.app_patch_training(user, body, project_name, model_name)
        elif activity_type ==  Activity_Name.Activity_Name_Data_Sufficiency.value:
            return data_sufficiency_controller.app_patch_datasuff(user, body, project_name, model_name)
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400)


def app_get_activity(user: str, project_name: str, model_name: str, activity_type: str):  # noqa: E501
    """Get model activity

    Return selected project model activity from user workspace  # noqa: E501

    :param project_name: Project identifier
    :type project_name: str
    :param model_name: model identifier
    :type model_name: str

    :rtype: Activity
    """
    
    if activity_type ==  Activity_Name.Activity_Name_Training.value:
        print('training activity detecting. forwarding request')
        return training_controller.app_get_training(user, project_name, model_name)
    elif activity_type ==  Activity_Name.Activity_Name_Data_Sufficiency.value:
        return data_sufficiency_controller.app_get_datasuff(user, project_name, model_name)

    return Response(status=501) # not implemented

    
def app_delete_activity(user, project_name, model_name, activity_type):  # noqa: E501
    """Delete activity associated to the given name

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param experiment_name: Experiment &#x60;name&#x60; identifier
    :type experiment_name: str
    :param test_name: Test &#x60;name&#x60; identifier
    :type test_name: str

    :rtype: None
    """
    
    if activity_type ==  Activity_Name.Activity_Name_Training.value:
        return training_controller.app_delete_training(user, project_name, model_name)

    return Response(status=501) # not implemented


def app_download_activity_artifacts(user, body, project_name, model_name, activity_type):
    # print('- app_download_activity_artifacts')
    
    if connexion.request.is_json:
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return training_controller.app_download_training_artifacts(user, body, project_name, model_name)
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400)

def app_create_activity_configuration(user, body, project_name, model_name, activity_type):

    if connexion.request.is_json:
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return training_controller.app_create_training_configuration(user, body, project_name, model_name)
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400)

def app_patch_activity_configuration(user, body, project_name, model_name, activity_type):

    if connexion.request.is_json:
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return training_controller.app_patch_training_configuration(user, body, project_name, model_name)
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400)

def app_get_public_projects_activity(project_name: str, model_name: str, activity_type: str):
    if activity_type ==  Activity_Name.Activity_Name_Training.value:
        return training_controller.app_get_public_projects_training(project_name, model_name)
    elif activity_type ==  Activity_Name.Activity_Name_Data_Sufficiency.value:
        return data_sufficiency_controller.app_get_public_projects_datasuff(project_name, model_name)

    return Response(status=501) # not implemented

    
def app_create_job_for_activity(user, body, project_name: str, model_name: str, activity_type: str):
    if connexion.request.is_json:
        if activity_type ==  Activity_Name.Activity_Name_Training.value:
            return job_controller.app_create_job(user, body, project_name, model_name)
        else:
            return Response(status=501) # not implemented

    return response_error(msg="Connexion request not a JSON", status_code=400)
