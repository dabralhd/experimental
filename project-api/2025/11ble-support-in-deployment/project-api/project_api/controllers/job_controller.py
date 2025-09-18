
import connexion
from flask import Response
from project_api.utils.func_dec import (ws_userid, with_model_owner_uuid, default_except)

from project_api.globals import GlobalObjects
from project_api.models.job import Job  # noqa: E501
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
from project_api.utils.error_helper import (model_exists, get_prj_api_log_level)

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(get_prj_api_log_level())

@default_except
@with_model_owner_uuid
def app_create_job(user, body, project_name, model_name):
    logger.debug(f'user: {user}')
    if connexion.request.is_json:
        new_job = Job.from_dict(connexion.request.get_json())  # noqa: E501

        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)
        logger.debug(f'Creating job for user: {user}, project: {project_name}, model: {model_name}, job name: {new_job.name}')
        project_repo.create_job(project_name=project_name, model_uuid_or_name=model_name, 
                                     name=new_job.name, version=new_job.version, template_id=new_job.template_id)

        return Response(status=201)

    return Response(status=400)

@ws_userid
def app_get_jobs(user, body, project_name, model_name):  # noqa: E501
    """Job list


    :rtype: List[Job] 
    """
    # user_jobs_folder_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    # os.makedirs(user_jobs_folder_path, exist_ok=True)
    # job_repo = JobFileRepo(user_jobs_folder_path)
    # job_doman_objs = job_repo.get_jobs()
    jobs = []
    # for job_domain_obj in job_doman_objs:
    #     jobs.append(convert_job(job=job_domain_obj))
    return jobs