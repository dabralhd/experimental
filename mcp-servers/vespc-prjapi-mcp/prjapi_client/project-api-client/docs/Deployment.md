# Deployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** |  | 
**display_name** | **str** |  | 
**description** | **str** |  | [optional] 
**last_deploy_time** | **datetime** |  | [optional] 
**last_deploy_result** | **str** |  | [optional] 
**cloud_params** | [**DeploymentCloudParams**](DeploymentCloudParams.md) |  | 
**configuration** | [**DeploymentConfiguration**](DeploymentConfiguration.md) |  | 

## Example

```python
from project_api_client.models.deployment import Deployment

# TODO update the JSON string below
json = "{}"
# create an instance of Deployment from a JSON string
deployment_instance = Deployment.from_json(json)
# print the JSON string representation of the object
print(Deployment.to_json())

# convert the object into a dict
deployment_dict = deployment_instance.to_dict()
# create an instance of Deployment from a dict
deployment_from_dict = Deployment.from_dict(deployment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


