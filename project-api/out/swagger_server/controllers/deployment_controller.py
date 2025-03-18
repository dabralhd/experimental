import connexion
import six

from swagger_server.models.deployments_deployment_id_body import DeploymentsDeploymentIdBody  # noqa: E501
from swagger_server.models.project_name_deployments_body import ProjectNameDeploymentsBody  # noqa: E501
from swagger_server import util


def app_create_deployment_id(body, project_name):  # noqa: E501
    """Create deployment of a project

     # noqa: E501

    :param body: The deployment to be added.
    :type body: dict | bytes
    :param project_name: 
    :type project_name: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = ProjectNameDeploymentsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_delete_deployment_id(project_name, deployment_id):  # noqa: E501
    """Delete the deployment ID of a project

     # noqa: E501

    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_deployment_gateway(device_id, project_name, deployment_id, resource):  # noqa: E501
    """Get files relating to a gateway device

     # noqa: E501

    :param device_id: 
    :type device_id: str
    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str
    :param resource: 
    :type resource: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_deployment_leaf(device_id, project_name, deployment_id, resource):  # noqa: E501
    """Get files relating to a leaf device

     # noqa: E501

    :param device_id: 
    :type device_id: str
    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str
    :param resource: 
    :type resource: str

    :rtype: None
    """
    return 'do some magic!'


def app_update_deployment_id(body, project_name, deployment_id):  # noqa: E501
    """Update deployment of a project

     # noqa: E501

    :param body: The deployment to be added.
    :type body: dict | bytes
    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = DeploymentsDeploymentIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
