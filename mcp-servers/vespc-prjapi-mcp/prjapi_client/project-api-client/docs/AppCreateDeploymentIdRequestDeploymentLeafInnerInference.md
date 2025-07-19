# AppCreateDeploymentIdRequestDeploymentLeafInnerInference


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application** | **str** |  | [optional] 
**firmware_update** | **bool** |  | [optional] 
**models** | [**List[AppCreateDeploymentIdRequestDeploymentLeafInnerInferenceModelsInner]**](AppCreateDeploymentIdRequestDeploymentLeafInnerInferenceModelsInner.md) |  | [optional] 

## Example

```python
from project_api_client.models.app_create_deployment_id_request_deployment_leaf_inner_inference import AppCreateDeploymentIdRequestDeploymentLeafInnerInference

# TODO update the JSON string below
json = "{}"
# create an instance of AppCreateDeploymentIdRequestDeploymentLeafInnerInference from a JSON string
app_create_deployment_id_request_deployment_leaf_inner_inference_instance = AppCreateDeploymentIdRequestDeploymentLeafInnerInference.from_json(json)
# print the JSON string representation of the object
print(AppCreateDeploymentIdRequestDeploymentLeafInnerInference.to_json())

# convert the object into a dict
app_create_deployment_id_request_deployment_leaf_inner_inference_dict = app_create_deployment_id_request_deployment_leaf_inner_inference_instance.to_dict()
# create an instance of AppCreateDeploymentIdRequestDeploymentLeafInnerInference from a dict
app_create_deployment_id_request_deployment_leaf_inner_inference_from_dict = AppCreateDeploymentIdRequestDeploymentLeafInnerInference.from_dict(app_create_deployment_id_request_deployment_leaf_inner_inference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


