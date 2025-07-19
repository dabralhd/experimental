# Model


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**Dataset**](Dataset.md) |  | 
**target** | [**Target**](Target.md) |  | 
**uuid** | **str** |  | 
**name** | **str** |  | 
**metadata** | [**ModelModelMetadata**](ModelModelMetadata.md) |  | 
**training** | [**Training**](Training.md) |  | 
**creation_time** | **str** |  | [optional] 
**last_update_time** | **str** |  | [optional] 
**model_owner_uuid** | **str** |  | 

## Example

```python
from project_api_client.models.model import Model

# TODO update the JSON string below
json = "{}"
# create an instance of Model from a JSON string
model_instance = Model.from_json(json)
# print the JSON string representation of the object
print(Model.to_json())

# convert the object into a dict
model_dict = model_instance.to_dict()
# create an instance of Model from a dict
model_from_dict = Model.from_dict(model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


