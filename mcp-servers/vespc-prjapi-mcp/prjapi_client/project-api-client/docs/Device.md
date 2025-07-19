# Device


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_id** | **str** |  | 
**description** | **str** |  | 
**gateway_id** | **str** |  | [optional] 
**selected_model_name** | **str** |  | [optional] 
**module_id** | **str** |  | [optional] 
**configuration_uri** | **str** |  | [optional] 
**device_manifest_uri** | **str** |  | [optional] 
**device_template_uri** | **str** |  | [optional] 
**device_template_id** | **str** |  | [optional] 
**wifi_mode** | **str** |  | [optional] 
**models** | [**List[DeviceModelsInner]**](DeviceModelsInner.md) |  | [optional] 

## Example

```python
from project_api_client.models.device import Device

# TODO update the JSON string below
json = "{}"
# create an instance of Device from a JSON string
device_instance = Device.from_json(json)
# print the JSON string representation of the object
print(Device.to_json())

# convert the object into a dict
device_dict = device_instance.to_dict()
# create an instance of Device from a dict
device_from_dict = Device.from_dict(device_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


