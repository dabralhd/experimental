# NewTraining


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**configuration** | **str** |  | [optional] 
**artifacts** | **List[str]** |  | [optional] 
**reports** | **List[str]** |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**last_update_time** | **datetime** |  | [optional] 

## Example

```python
from project_api_client.models.new_training import NewTraining

# TODO update the JSON string below
json = "{}"
# create an instance of NewTraining from a JSON string
new_training_instance = NewTraining.from_json(json)
# print the JSON string representation of the object
print(NewTraining.to_json())

# convert the object into a dict
new_training_dict = new_training_instance.to_dict()
# create an instance of NewTraining from a dict
new_training_from_dict = NewTraining.from_dict(new_training_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


