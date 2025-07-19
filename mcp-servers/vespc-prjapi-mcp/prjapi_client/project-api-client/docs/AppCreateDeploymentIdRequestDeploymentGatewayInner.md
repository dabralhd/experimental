# AppCreateDeploymentIdRequestDeploymentGatewayInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**device_id** | **str** |  | [optional] 
**wifi_mode** | **str** |  | [optional] 

## Example

```python
from project_api_client.models.app_create_deployment_id_request_deployment_gateway_inner import AppCreateDeploymentIdRequestDeploymentGatewayInner

# TODO update the JSON string below
json = "{}"
# create an instance of AppCreateDeploymentIdRequestDeploymentGatewayInner from a JSON string
app_create_deployment_id_request_deployment_gateway_inner_instance = AppCreateDeploymentIdRequestDeploymentGatewayInner.from_json(json)
# print the JSON string representation of the object
print(AppCreateDeploymentIdRequestDeploymentGatewayInner.to_json())

# convert the object into a dict
app_create_deployment_id_request_deployment_gateway_inner_dict = app_create_deployment_id_request_deployment_gateway_inner_instance.to_dict()
# create an instance of AppCreateDeploymentIdRequestDeploymentGatewayInner from a dict
app_create_deployment_id_request_deployment_gateway_inner_from_dict = AppCreateDeploymentIdRequestDeploymentGatewayInner.from_dict(app_create_deployment_id_request_deployment_gateway_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


