# AppUpdateDeploymentIdRequestGatewayInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_id** | **str** |  | [optional] 
**device_id** | **str** |  | [optional] 
**application** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**wifi_mode** | **str** |  | [optional] 

## Example

```python
from project_api_client.models.app_update_deployment_id_request_gateway_inner import AppUpdateDeploymentIdRequestGatewayInner

# TODO update the JSON string below
json = "{}"
# create an instance of AppUpdateDeploymentIdRequestGatewayInner from a JSON string
app_update_deployment_id_request_gateway_inner_instance = AppUpdateDeploymentIdRequestGatewayInner.from_json(json)
# print the JSON string representation of the object
print(AppUpdateDeploymentIdRequestGatewayInner.to_json())

# convert the object into a dict
app_update_deployment_id_request_gateway_inner_dict = app_update_deployment_id_request_gateway_inner_instance.to_dict()
# create an instance of AppUpdateDeploymentIdRequestGatewayInner from a dict
app_update_deployment_id_request_gateway_inner_from_dict = AppUpdateDeploymentIdRequestGatewayInner.from_dict(app_update_deployment_id_request_gateway_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


