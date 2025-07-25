# Project


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** |  | 
**ai_project_name** | **str** |  | 
**display_name** | **str** |  | [optional] 
**description** | **str** |  | 
**reference** | **str** |  | [optional] 
**version** | **str** |  | 
**creation_time** | **str** |  | 
**last_update_time** | **str** |  | 
**models** | [**List[Model]**](Model.md) |  | 
**deployments** | [**List[Deployment]**](Deployment.md) |  | [optional] 

## Example

```python
from project_api_client.models.project import Project

# TODO update the JSON string below
json = "{}"
# create an instance of Project from a JSON string
project_instance = Project.from_json(json)
# print the JSON string representation of the object
print(Project.to_json())

# convert the object into a dict
project_dict = project_instance.to_dict()
# create an instance of Project from a dict
project_from_dict = Project.from_dict(project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


