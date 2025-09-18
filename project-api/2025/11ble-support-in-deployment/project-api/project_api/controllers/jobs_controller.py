import os
from project_api.utils.func_dec import (ws_userid)

from project_api.globals import GlobalObjects
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_job,
)
from project_api.vespucciprjmng.repository.filesystem.job_file_repo import (
    JobFileRepo,
)


@ws_userid
def app_get_jobs(user):  # noqa: E501
    """Job list


    :rtype: List[Job] 
    """
    user_jobs_folder_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    os.makedirs(user_jobs_folder_path, exist_ok=True)
    job_repo = JobFileRepo(user_jobs_folder_path)
    job_doman_objs = job_repo.get_jobs()
    jobs = []
    for job_domain_obj in job_doman_objs:
        jobs.append(convert_job(job=job_domain_obj))
    return jobs
