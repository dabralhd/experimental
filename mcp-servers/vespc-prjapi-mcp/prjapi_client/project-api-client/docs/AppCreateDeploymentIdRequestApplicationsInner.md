# AppCreateDeploymentIdRequestApplicationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_manifest_uri** | **str** |  | [optional] 
**device_template_id** | **str** |  | [optional] 
**device_template_uri** | **str** |  | [optional] 
**image_uri** | **str** |  | [optional] 
**module_id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**protocol** | **int** |  | [optional] 
**binary_id** | **int** |  | [optional] 
**binary_uri** | **str** |  | [optional] 

## Example

```python
from project_api_client.models.app_create_deployment_id_request_applications_inner import AppCreateDeploymentIdRequestApplicationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of AppCreateDeploymentIdRequestApplicationsInner from a JSON string
app_create_deployment_id_request_applications_inner_instance = AppCreateDeploymentIdRequestApplicationsInner.from_json(json)
# print the JSON string representation of the object
print(AppCreateDeploymentIdRequestApplicationsInner.to_json())

# convert the object into a dict
app_create_deployment_id_request_applications_inner_dict = app_create_deployment_id_request_applications_inner_instance.to_dict()
# create an instance of AppCreateDeploymentIdRequestApplicationsInner from a dict
app_create_deployment_id_request_applications_inner_from_dict = AppCreateDeploymentIdRequestApplicationsInner.from_dict(app_create_deployment_id_request_applications_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


