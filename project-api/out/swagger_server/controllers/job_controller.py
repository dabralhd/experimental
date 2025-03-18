import connexion
import six

from swagger_server.models.job import Job  # noqa: E501
from swagger_server import util


def app_create_job_for_activity(body, project_name, model_name, activity_type):  # noqa: E501
    """Create new Activity Job and add a job json object to the model activity in Project JSON file

     # noqa: E501

    :param body: The activity to be added.
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
        body = Job.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
