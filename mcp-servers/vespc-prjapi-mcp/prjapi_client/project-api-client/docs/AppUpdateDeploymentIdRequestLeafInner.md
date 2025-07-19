# AppUpdateDeploymentIdRequestLeafInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_id** | **str** |  | [optional] 
**device_id** | **str** |  | [optional] 
**gateway_id** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**datalogging** | [**AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging**](AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging.md) |  | [optional] 
**inference** | [**AppCreateDeploymentIdRequestDeploymentLeafInnerInference**](AppCreateDeploymentIdRequestDeploymentLeafInnerInference.md) |  | [optional] 

## Example

```python
from project_api_client.models.app_update_deployment_id_request_leaf_inner import AppUpdateDeploymentIdRequestLeafInner

# TODO update the JSON string below
json = "{}"
# create an instance of AppUpdateDeploymentIdRequestLeafInner from a JSON string
app_update_deployment_id_request_leaf_inner_instance = AppUpdateDeploymentIdRequestLeafInner.from_json(json)
# print the JSON string representation of the object
print(AppUpdateDeploymentIdRequestLeafInner.to_json())

# convert the object into a dict
app_update_deployment_id_request_leaf_inner_dict = app_update_deployment_id_request_leaf_inner_instance.to_dict()
# create an instance of AppUpdateDeploymentIdRequestLeafInner from a dict
app_update_deployment_id_request_leaf_inner_from_dict = AppUpdateDeploymentIdRequestLeafInner.from_dict(app_update_deployment_id_request_leaf_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


