# ModelModelMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**ModelType**](ModelType.md) |  | [optional] 
**classes** | **List[str]** |  | [optional] 

## Example

```python
from project_api_client.models.model_model_metadata import ModelModelMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ModelModelMetadata from a JSON string
model_model_metadata_instance = ModelModelMetadata.from_json(json)
# print the JSON string representation of the object
print(ModelModelMetadata.to_json())

# convert the object into a dict
model_model_metadata_dict = model_model_metadata_instance.to_dict()
# create an instance of ModelModelMetadata from a dict
model_model_metadata_from_dict = ModelModelMetadata.from_dict(model_model_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


