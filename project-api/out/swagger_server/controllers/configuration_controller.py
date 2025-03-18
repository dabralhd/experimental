import connexion
import six

from swagger_server.models.activity_type_configuration_body import ActivityTypeConfigurationBody  # noqa: E501
from swagger_server.models.activity_type_configuration_body1 import ActivityTypeConfigurationBody1  # noqa: E501
from swagger_server import util


def app_create_activity_configuration(body, project_name, model_name, activity_type):  # noqa: E501
    """Create activity configuration file of the project/model/activity

     # noqa: E501

    :param body: Create activity configuration file of the project/model/activity
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
        body = ActivityTypeConfigurationBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_patch_activity_configuration(body, project_name, model_name, activity_type):  # noqa: E501
    """Update activity configuration file of the project/model/activity

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
        body = ActivityTypeConfigurationBody1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
