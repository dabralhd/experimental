# DeviceModelsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**datalogging** | [**DeviceApplication**](DeviceApplication.md) |  | [optional] 
**inference** | [**DeviceApplication**](DeviceApplication.md) |  | [optional] 

## Example

```python
from project_api_client.models.device_models_inner import DeviceModelsInner

# TODO update the JSON string below
json = "{}"
# create an instance of DeviceModelsInner from a JSON string
device_models_inner_instance = DeviceModelsInner.from_json(json)
# print the JSON string representation of the object
print(DeviceModelsInner.to_json())

# convert the object into a dict
device_models_inner_dict = device_models_inner_instance.to_dict()
# create an instance of DeviceModelsInner from a dict
device_models_inner_from_dict = DeviceModelsInner.from_dict(device_models_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


