import connexion
import six

from swagger_server.models.deployments_deployment_id_body import DeploymentsDeploymentIdBody  # noqa: E501
from swagger_server.models.leaf_device_id_body import LeafDeviceIdBody  # noqa: E501
from swagger_server.models.patch_inference_model_reference import PatchInferenceModelReference  # noqa: E501
from swagger_server.models.project_name_deployments_body import ProjectNameDeploymentsBody  # noqa: E501
from swagger_server import util


def app_create_deployment_id(body, project_name, as_org=None):  # noqa: E501
    """Create deployment of a project

     # noqa: E501

    :param body: The deployment to be added.
    :type body: dict | bytes
    :param project_name: 
    :type project_name: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = ProjectNameDeploymentsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_delete_deployment_id(project_name, deployment_id, as_org=None):  # noqa: E501
    """Delete the deployment ID of a project

     # noqa: E501

    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_deployment_gateway(device_id, project_name, deployment_id, resource, as_org=None):  # noqa: E501
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
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_deployment_leaf(device_id, project_name, deployment_id, resource, as_org=None):  # noqa: E501
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
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    return 'do some magic!'


def app_patch_deployment_leaf(body, device_id, project_name, deployment_id, as_org=None, resource_type=None, resource_name=None):  # noqa: E501
    """Get files relating to a leaf device

     # noqa: E501

    :param body: requestbody for patching leaf device
    :type body: dict | bytes
    :param device_id: 
    :type device_id: str
    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str
    :param resource_type: string identifying resource to patch
    :type resource_type: str
    :param resource_name: identify resource_name within the category resource_type, at present
    :type resource_name: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = LeafDeviceIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_patch_leaf_inference_model(body, project_name, deployment_id, device_id):  # noqa: E501
    """Patch inference model reference for a leaf device

    Updates the &#x27;model_name_reference&#x27; in the leaf device&#x27;s inference configuration. The resource must exist, otherwise a 404 error is returned.  # noqa: E501

    :param body: Partial payload to update the model reference.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param deployment_id: Deployment &#x60;id&#x60; identifier
    :type deployment_id: str
    :param device_id: Leaf Device &#x60;id&#x60; identifier
    :type device_id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = PatchInferenceModelReference.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_update_deployment_id(body, project_name, deployment_id, as_org=None):  # noqa: E501
    """Update deployment of a project

     # noqa: E501

    :param body: The deployment to be added.
    :type body: dict | bytes
    :param project_name: 
    :type project_name: str
    :param deployment_id: 
    :type deployment_id: str
    :param as_org: sometimes a user will share a project with an org 
    :type as_org: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = DeploymentsDeploymentIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
