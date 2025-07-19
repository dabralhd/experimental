# AppPatchActivityRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**configuration** | **str** |  | [optional] 
**artifacts** | **List[str]** |  | [optional] 
**reports** | **List[str]** |  | [optional] 

## Example

```python
from project_api_client.models.app_patch_activity_request import AppPatchActivityRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AppPatchActivityRequest from a JSON string
app_patch_activity_request_instance = AppPatchActivityRequest.from_json(json)
# print the JSON string representation of the object
print(AppPatchActivityRequest.to_json())

# convert the object into a dict
app_patch_activity_request_dict = app_patch_activity_request_instance.to_dict()
# create an instance of AppPatchActivityRequest from a dict
app_patch_activity_request_from_dict = AppPatchActivityRequest.from_dict(app_patch_activity_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


