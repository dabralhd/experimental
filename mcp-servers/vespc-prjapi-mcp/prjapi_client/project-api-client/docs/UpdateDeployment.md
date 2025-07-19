# UpdateDeployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cloud_credentials** | [**UpdateDeploymentCloudCredentials**](UpdateDeploymentCloudCredentials.md) |  | [optional] 
**leaf_devices** | [**UpdateDevice**](UpdateDevice.md) |  | [optional] 
**gateways** | [**UpdateDevice**](UpdateDevice.md) |  | [optional] 

## Example

```python
from project_api_client.models.update_deployment import UpdateDeployment

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateDeployment from a JSON string
update_deployment_instance = UpdateDeployment.from_json(json)
# print the JSON string representation of the object
print(UpdateDeployment.to_json())

# convert the object into a dict
update_deployment_dict = update_deployment_instance.to_dict()
# create an instance of UpdateDeployment from a dict
update_deployment_from_dict = UpdateDeployment.from_dict(update_deployment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


