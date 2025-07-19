# project_api_client.ApplicationsApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_delete_application_id**](ApplicationsApi.md#app_delete_application_id) | **DELETE** /projects/{project_name}/applications/{application_id} | Delete the application ID of a project
[**app_update_application_id**](ApplicationsApi.md#app_update_application_id) | **PATCH** /projects/{project_name}/applications/{application_id} | Patch the application ID of a project


# **app_delete_application_id**
> app_delete_application_id(project_name, application_id, as_org=as_org)

Delete the application ID of a project



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
    api_instance = project_api_client.ApplicationsApi(api_client)
    project_name = 'project_name_example' # str | 
    application_id = 'application_id_example' # str | 
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Delete the application ID of a project
        api_instance.app_delete_application_id(project_name, application_id, as_org=as_org)
    except Exception as e:
        print("Exception when calling ApplicationsApi->app_delete_application_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **application_id** | **str**|  | 
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

# **app_update_application_id**
> app_update_application_id(project_name, application_id, app_create_deployment_id_request_applications_inner, as_org=as_org)

Patch the application ID of a project



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.app_create_deployment_id_request_applications_inner import AppCreateDeploymentIdRequestApplicationsInner
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
    api_instance = project_api_client.ApplicationsApi(api_client)
    project_name = 'project_name_example' # str | 
    application_id = 'application_id_example' # str | 
    app_create_deployment_id_request_applications_inner = project_api_client.AppCreateDeploymentIdRequestApplicationsInner() # AppCreateDeploymentIdRequestApplicationsInner | The application to be patched.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Patch the application ID of a project
        api_instance.app_update_application_id(project_name, application_id, app_create_deployment_id_request_applications_inner, as_org=as_org)
    except Exception as e:
        print("Exception when calling ApplicationsApi->app_update_application_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **application_id** | **str**|  | 
 **app_create_deployment_id_request_applications_inner** | [**AppCreateDeploymentIdRequestApplicationsInner**](AppCreateDeploymentIdRequestApplicationsInner.md)| The application to be patched. | 
 **as_org** | **str**| sometimes a user will share a project with an org  | [optional] 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

