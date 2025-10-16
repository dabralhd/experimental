import connexion
import six

from swagger_server.models.new_model import NewModel  # noqa: E501
from swagger_server import util


def app_create_model(body, project_name, as_org=None):  # noqa: E501
    """Create new model

     # noqa: E501

    :param body: The model to be added (or cloned).
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param as_org: sometimes a user will copy a model, using rights of an organization 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = NewModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_patch_model(body, project_name, model_name, as_org=None):  # noqa: E501
    """Patch a model

     # noqa: E501

    :param body: The model to be patched.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = NewModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
