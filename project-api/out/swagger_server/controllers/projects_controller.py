import connexion
import six

from swagger_server.models.new_project import NewProject  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util


def app_create_project(body=None, is_user_project=None):  # noqa: E501
    """Create new project

     # noqa: E501

    :param body: New project model
    :type body: dict | bytes
    :param is_user_project: Boolean flag which indicates whether &#x27;project_name_to_clone&#x27; is a user project
    :type is_user_project: bool

    :rtype: None
    """
    if connexion.request.is_json:
        body = NewProject.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_get_projects():  # noqa: E501
    """Projects list

     # noqa: E501


    :rtype: List[Project]
    """
    return 'do some magic!'
