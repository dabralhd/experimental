# Runtime


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**jobs** | [**List[Job]**](Job.md) |  | [optional] 

## Example

```python
from project_api_client.models.runtime import Runtime

# TODO update the JSON string below
json = "{}"
# create an instance of Runtime from a JSON string
runtime_instance = Runtime.from_json(json)
# print the JSON string representation of the object
print(Runtime.to_json())

# convert the object into a dict
runtime_dict = runtime_instance.to_dict()
# create an instance of Runtime from a dict
runtime_from_dict = Runtime.from_dict(runtime_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


