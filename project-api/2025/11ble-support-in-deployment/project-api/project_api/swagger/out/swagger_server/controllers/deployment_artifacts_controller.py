import connexion
import six

from swagger_server import util


def get_artifacts(project_name, deployment_name, device_id, log_uuid, as_org=None):  # noqa: E501
    """Get deployment artifacts of a project

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param deployment_name: Deployment &#x60;name&#x60; identifier
    :type deployment_name: str
    :param device_id: Device &#x60;ID&#x60; identifier
    :type device_id: str
    :param log_uuid: Existing input source uuid reference
    :type log_uuid: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'
