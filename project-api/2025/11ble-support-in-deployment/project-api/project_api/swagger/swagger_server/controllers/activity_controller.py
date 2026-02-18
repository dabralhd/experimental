import connexion
import six

from swagger_server.models.model_name_activity_type_body import ModelNameActivityTypeBody  # noqa: E501
from swagger_server.models.new_training import NewTraining  # noqa: E501
from swagger_server.models.training import Training  # noqa: E501
from swagger_server import util


def app_create_activity(body, project_name, model_name, activity_type, as_org=None):  # noqa: E501
    """Create new Activity

     # noqa: E501

    :param body: The activity to be added.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Activity &#x60;name&#x60; identifier
    :type activity_type: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = NewTraining.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_delete_activity(project_name, model_name, activity_type, as_org=None):  # noqa: E501
    """Delete the activity associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Activity &#x60;name&#x60; identifier
    :type activity_type: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_activity(project_name, model_name, activity_type, type=None, name=None, as_org=None):  # noqa: E501
    """Get the file contents of artifacts, reports or configuration of the activity

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Activity &#x60;name&#x60; identifier
    :type activity_type: str
    :param type: string corresponding to artifact to be GET artifacts, reports, runtime OR config
    :type type: str
    :param name: Filename of artifact for which GET is issued
    :type name: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: List[str]
    """
    return 'do some magic!'


def app_patch_activity(body, project_name, model_name, activity_type, as_org=None):  # noqa: E501
    """Update partial Activity JSON

     # noqa: E501

    :param body: The activity to be patched.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Activity &#x60;name&#x60; identifier
    :type activity_type: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = ModelNameActivityTypeBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_update_activity(body, project_name, model_name, activity_type, as_org=None):  # noqa: E501
    """Update Activity JSON

     # noqa: E501

    :param body: The activity to be updated.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Activity &#x60;name&#x60; identifier
    :type activity_type: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = Training.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
