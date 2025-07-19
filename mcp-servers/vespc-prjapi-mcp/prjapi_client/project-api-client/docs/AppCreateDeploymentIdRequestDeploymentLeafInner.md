# AppCreateDeploymentIdRequestDeploymentLeafInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gateway_id** | **str** |  | [optional] 
**device_id** | **str** |  | [optional] 
**application** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**datalogging** | [**AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging**](AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging.md) |  | [optional] 
**inference** | [**AppCreateDeploymentIdRequestDeploymentLeafInnerInference**](AppCreateDeploymentIdRequestDeploymentLeafInnerInference.md) |  | [optional] 

## Example

```python
from project_api_client.models.app_create_deployment_id_request_deployment_leaf_inner import AppCreateDeploymentIdRequestDeploymentLeafInner

# TODO update the JSON string below
json = "{}"
# create an instance of AppCreateDeploymentIdRequestDeploymentLeafInner from a JSON string
app_create_deployment_id_request_deployment_leaf_inner_instance = AppCreateDeploymentIdRequestDeploymentLeafInner.from_json(json)
# print the JSON string representation of the object
print(AppCreateDeploymentIdRequestDeploymentLeafInner.to_json())

# convert the object into a dict
app_create_deployment_id_request_deployment_leaf_inner_dict = app_create_deployment_id_request_deployment_leaf_inner_instance.to_dict()
# create an instance of AppCreateDeploymentIdRequestDeploymentLeafInner from a dict
app_create_deployment_id_request_deployment_leaf_inner_from_dict = AppCreateDeploymentIdRequestDeploymentLeafInner.from_dict(app_create_deployment_id_request_deployment_leaf_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


