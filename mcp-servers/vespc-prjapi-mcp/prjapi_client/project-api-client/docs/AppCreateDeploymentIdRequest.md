# AppCreateDeploymentIdRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**applications** | [**List[AppCreateDeploymentIdRequestApplicationsInner]**](AppCreateDeploymentIdRequestApplicationsInner.md) |  | 
**deployment** | [**AppCreateDeploymentIdRequestDeployment**](AppCreateDeploymentIdRequestDeployment.md) |  | 

## Example

```python
from project_api_client.models.app_create_deployment_id_request import AppCreateDeploymentIdRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AppCreateDeploymentIdRequest from a JSON string
app_create_deployment_id_request_instance = AppCreateDeploymentIdRequest.from_json(json)
# print the JSON string representation of the object
print(AppCreateDeploymentIdRequest.to_json())

# convert the object into a dict
app_create_deployment_id_request_dict = app_create_deployment_id_request_instance.to_dict()
# create an instance of AppCreateDeploymentIdRequest from a dict
app_create_deployment_id_request_from_dict = AppCreateDeploymentIdRequest.from_dict(app_create_deployment_id_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


