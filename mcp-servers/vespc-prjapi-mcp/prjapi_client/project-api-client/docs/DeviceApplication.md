# DeviceApplication


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_template_uri** | **str** |  | [optional] 
**device_template_id** | **str** |  | [optional] 
**protocol** | **float** |  | [optional] 
**firmware_uri** | **str** |  | [optional] 

## Example

```python
from project_api_client.models.device_application import DeviceApplication

# TODO update the JSON string below
json = "{}"
# create an instance of DeviceApplication from a JSON string
device_application_instance = DeviceApplication.from_json(json)
# print the JSON string representation of the object
print(DeviceApplication.to_json())

# convert the object into a dict
device_application_dict = device_application_instance.to_dict()
# create an instance of DeviceApplication from a dict
device_application_from_dict = DeviceApplication.from_dict(device_application_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


