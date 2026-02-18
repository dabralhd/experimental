import connexion
import six

from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util


def app_delete_project(project_name, as_org=None):  # noqa: E501
    """Delete project associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param as_org: sometimes a user will use org id credentials 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_project(project_name, as_org=None):  # noqa: E501
    """Get project associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: Project
    """
    return 'do some magic!'


def app_get_project_icon(project_name, as_org=None):  # noqa: E501
    """Get project icon associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param as_org: sometimes a user will use org id credentials 
    :type as_org: str

    :rtype: str
    """
    return 'do some magic!'


def app_get_template_project_icon(project_name):  # noqa: E501
    """Get project icon associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str

    :rtype: str
    """
    return 'do some magic!'
