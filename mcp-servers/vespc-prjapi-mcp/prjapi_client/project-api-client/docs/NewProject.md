# NewProject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_name_to_clone** | **str** |  | [optional] 
**ai_project_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**reference** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**creation_time** | **str** |  | [optional] 
**last_update_time** | **str** |  | [optional] 

## Example

```python
from project_api_client.models.new_project import NewProject

# TODO update the JSON string below
json = "{}"
# create an instance of NewProject from a JSON string
new_project_instance = NewProject.from_json(json)
# print the JSON string representation of the object
print(NewProject.to_json())

# convert the object into a dict
new_project_dict = new_project_instance.to_dict()
# create an instance of NewProject from a dict
new_project_from_dict = NewProject.from_dict(new_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


