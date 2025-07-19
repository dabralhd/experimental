# AppUpdateDeploymentIdRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**last_update_time** | **datetime** |  | [optional] 
**last_deploy_result** | **str** |  | [optional] 
**cloud_params** | [**AppCreateDeploymentIdRequestDeploymentCloudParams**](AppCreateDeploymentIdRequestDeploymentCloudParams.md) |  | [optional] 
**leaf** | [**List[AppUpdateDeploymentIdRequestLeafInner]**](AppUpdateDeploymentIdRequestLeafInner.md) |  | [optional] 
**gateway** | [**List[AppUpdateDeploymentIdRequestGatewayInner]**](AppUpdateDeploymentIdRequestGatewayInner.md) |  | [optional] 

## Example

```python
from project_api_client.models.app_update_deployment_id_request import AppUpdateDeploymentIdRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AppUpdateDeploymentIdRequest from a JSON string
app_update_deployment_id_request_instance = AppUpdateDeploymentIdRequest.from_json(json)
# print the JSON string representation of the object
print(AppUpdateDeploymentIdRequest.to_json())

# convert the object into a dict
app_update_deployment_id_request_dict = app_update_deployment_id_request_instance.to_dict()
# create an instance of AppUpdateDeploymentIdRequest from a dict
app_update_deployment_id_request_from_dict = AppUpdateDeploymentIdRequest.from_dict(app_update_deployment_id_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


