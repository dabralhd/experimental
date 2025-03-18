import connexion
import six

from swagger_server import util


def app_get_public_projects_activity(project_name, model_name, activity_type, type=None, name=None):  # noqa: E501
    """Get the file contents of artifacts, reports or configuration of the activity for public projects

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str
    :param activity_type: Model &#x60;activity_type&#x60; identifier
    :type activity_type: str
    :param type: string corresponding to artifact to be GET artifacts, reports, runtime OR config
    :type type: str
    :param name: Filename of artifact for which GET is issued
    :type name: str

    :rtype: List[str]
    """
    return 'do some magic!'
