# EFSUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**efs_usage_breached** | **bool** |  | [optional] 

## Example

```python
from project_api_client.models.efs_usage import EFSUsage

# TODO update the JSON string below
json = "{}"
# create an instance of EFSUsage from a JSON string
efs_usage_instance = EFSUsage.from_json(json)
# print the JSON string representation of the object
print(EFSUsage.to_json())

# convert the object into a dict
efs_usage_dict = efs_usage_instance.to_dict()
# create an instance of EFSUsage from a dict
efs_usage_from_dict = EFSUsage.from_dict(efs_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


