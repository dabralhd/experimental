import connexion
import six

from swagger_server.models.patch_inference_model_reference import PatchInferenceModelReference  # noqa: E501
from swagger_server import util


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
