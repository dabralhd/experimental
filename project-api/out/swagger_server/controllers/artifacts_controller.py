import connexion
import six

from swagger_server.models.job_artifact import JobArtifact  # noqa: E501
from swagger_server import util


def app_download_activity_artifacts(body, project_name, model_name, activity_type):  # noqa: E501
    """Download Activity Job Artifacts

     # noqa: E501

    :param body: The job artifact to be downloaded to user workspace.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Activity &#x60;name&#x60; identifier
    :type activity_type: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = JobArtifact.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
