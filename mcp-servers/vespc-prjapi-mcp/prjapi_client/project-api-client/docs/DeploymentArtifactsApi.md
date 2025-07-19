# project_api_client.DeploymentArtifactsApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_artifacts**](DeploymentArtifactsApi.md#get_artifacts) | **GET** /projects/{project_name}/deployments/{deployment_name}/devices/{device_id}/artifacts | Get deployment artifacts of a project


# **get_artifacts**
> get_artifacts(project_name, deployment_name, device_id, log_uuid, as_org=as_org)

Get deployment artifacts of a project

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /3
# See configuration.py for a list of all supported configuration parameters.
configuration = project_api_client.Configuration(
    host = "/3"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = project_api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with project_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = project_api_client.DeploymentArtifactsApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    deployment_name = 'deployment_name_example' # str | Deployment `name` identifier
    device_id = 'device_id_example' # str | Device `ID` identifier
    log_uuid = 'log_uuid_example' # str | Existing input source uuid reference
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Get deployment artifacts of a project
        api_instance.get_artifacts(project_name, deployment_name, device_id, log_uuid, as_org=as_org)
    except Exception as e:
        print("Exception when calling DeploymentArtifactsApi->get_artifacts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **deployment_name** | **str**| Deployment &#x60;name&#x60; identifier | 
 **device_id** | **str**| Device &#x60;ID&#x60; identifier | 
 **log_uuid** | **str**| Existing input source uuid reference | 
 **as_org** | **str**| sometimes a user will share a project with an org  | [optional] 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

