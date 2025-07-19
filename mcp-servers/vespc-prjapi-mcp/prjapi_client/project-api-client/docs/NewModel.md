# NewModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_name_to_clone** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**model_type** | [**ModelType**](ModelType.md) |  | [optional] 
**dataset** | [**Dataset**](Dataset.md) |  | [optional] 
**classes** | **List[str]** |  | [optional] 
**training_type** | [**TrainingType**](TrainingType.md) |  | [optional] 
**target** | [**Target**](Target.md) |  | [optional] 
**creation_time** | **str** |  | [optional] 
**last_update_time** | **str** |  | [optional] 
**model_owner_uuid** | **str** |  | [optional] 

## Example

```python
from project_api_client.models.new_model import NewModel

# TODO update the JSON string below
json = "{}"
# create an instance of NewModel from a JSON string
new_model_instance = NewModel.from_json(json)
# print the JSON string representation of the object
print(NewModel.to_json())

# convert the object into a dict
new_model_dict = new_model_instance.to_dict()
# create an instance of NewModel from a dict
new_model_from_dict = NewModel.from_dict(new_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


