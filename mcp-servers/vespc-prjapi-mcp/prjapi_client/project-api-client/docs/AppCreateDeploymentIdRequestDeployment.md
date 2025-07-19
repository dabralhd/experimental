# AppCreateDeploymentIdRequestDeployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**cloud_params** | [**AppCreateDeploymentIdRequestDeploymentCloudParams**](AppCreateDeploymentIdRequestDeploymentCloudParams.md) |  | [optional] 
**leaf** | [**List[AppCreateDeploymentIdRequestDeploymentLeafInner]**](AppCreateDeploymentIdRequestDeploymentLeafInner.md) |  | [optional] 
**gateway** | [**List[AppCreateDeploymentIdRequestDeploymentGatewayInner]**](AppCreateDeploymentIdRequestDeploymentGatewayInner.md) |  | [optional] 

## Example

```python
from project_api_client.models.app_create_deployment_id_request_deployment import AppCreateDeploymentIdRequestDeployment

# TODO update the JSON string below
json = "{}"
# create an instance of AppCreateDeploymentIdRequestDeployment from a JSON string
app_create_deployment_id_request_deployment_instance = AppCreateDeploymentIdRequestDeployment.from_json(json)
# print the JSON string representation of the object
print(AppCreateDeploymentIdRequestDeployment.to_json())

# convert the object into a dict
app_create_deployment_id_request_deployment_dict = app_create_deployment_id_request_deployment_instance.to_dict()
# create an instance of AppCreateDeploymentIdRequestDeployment from a dict
app_create_deployment_id_request_deployment_from_dict = AppCreateDeploymentIdRequestDeployment.from_dict(app_create_deployment_id_request_deployment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


