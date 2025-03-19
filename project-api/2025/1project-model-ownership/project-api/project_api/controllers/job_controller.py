
import connexion
from flask import Response

from project_api.globals import GlobalObjects
from project_api.models.job import Job  # noqa: E501
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)


def app_create_job(user, body, project_name, model_name):
    if connexion.request.is_json:
        new_job = Job.from_dict(connexion.request.get_json())  # noqa: E501

        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)
       
        project_repo.create_job(project_name=project_name, model_uuid_or_name=model_name, 
                                     name=new_job.name, version=new_job.version, template_id=new_job.template_id)

        return Response(status=201)

    return Response(status=400)

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