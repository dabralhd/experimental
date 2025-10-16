import connexion
import six

from swagger_server import util


def app_delete_model(project_name, model_name, as_org=None):  # noqa: E501
    """Delete model associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param as_org: sometimes a user will use org id credentials 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'
