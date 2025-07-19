# DeploymentCloudParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**app_url** | **str** |  | 

## Example

```python
from project_api_client.models.deployment_cloud_params import DeploymentCloudParams

# TODO update the JSON string below
json = "{}"
# create an instance of DeploymentCloudParams from a JSON string
deployment_cloud_params_instance = DeploymentCloudParams.from_json(json)
# print the JSON string representation of the object
print(DeploymentCloudParams.to_json())

# convert the object into a dict
deployment_cloud_params_dict = deployment_cloud_params_instance.to_dict()
# create an instance of DeploymentCloudParams from a dict
deployment_cloud_params_from_dict = DeploymentCloudParams.from_dict(deployment_cloud_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


