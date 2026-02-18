import connexion
import six

from swagger_server.models.applications_application_id_body import ApplicationsApplicationIdBody  # noqa: E501
from swagger_server import util


def app_delete_application_id(project_name, application_id, as_org=None):  # noqa: E501
    """Delete the application ID of a project

     # noqa: E501

    :param project_name: 
    :type project_name: str
    :param application_id: 
    :type application_id: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'


def app_update_application_id(body, project_name, application_id, as_org=None):  # noqa: E501
    """Patch the application ID of a project

     # noqa: E501

    :param body: The application to be patched.
    :type body: dict | bytes
    :param project_name: 
    :type project_name: str
    :param application_id: 
    :type application_id: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = ApplicationsApplicationIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
