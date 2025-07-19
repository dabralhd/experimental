# project_api_client.DeploymentApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_create_deployment_id**](DeploymentApi.md#app_create_deployment_id) | **POST** /projects/{project_name}/deployments | Create deployment of a project
[**app_delete_deployment_id**](DeploymentApi.md#app_delete_deployment_id) | **DELETE** /projects/{project_name}/deployments/{deployment_id} | Delete the deployment ID of a project
[**app_get_deployment_gateway**](DeploymentApi.md#app_get_deployment_gateway) | **GET** /projects/{project_name}/deployments/{deployment_id}/gateway/{device_id} | Get files relating to a gateway device
[**app_get_deployment_leaf**](DeploymentApi.md#app_get_deployment_leaf) | **GET** /projects/{project_name}/deployments/{deployment_id}/leaf/{device_id} | Get files relating to a leaf device
[**app_update_deployment_id**](DeploymentApi.md#app_update_deployment_id) | **PUT** /projects/{project_name}/deployments/{deployment_id} | Update deployment of a project


# **app_create_deployment_id**
> app_create_deployment_id(project_name, app_create_deployment_id_request, as_org=as_org)

Create deployment of a project



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.app_create_deployment_id_request import AppCreateDeploymentIdRequest
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
    api_instance = project_api_client.DeploymentApi(api_client)
    project_name = 'project_name_example' # str | 
    app_create_deployment_id_request = project_api_client.AppCreateDeploymentIdRequest() # AppCreateDeploymentIdRequest | The deployment to be added.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Create deployment of a project
        api_instance.app_create_deployment_id(project_name, app_create_deployment_id_request, as_org=as_org)
    except Exception as e:
        print("Exception when calling DeploymentApi->app_create_deployment_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **app_create_deployment_id_request** | [**AppCreateDeploymentIdRequest**](AppCreateDeploymentIdRequest.md)| The deployment to be added. | 
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

# **app_delete_deployment_id**
> app_delete_deployment_id(project_name, deployment_id, as_org=as_org)

Delete the deployment ID of a project



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
    api_instance = project_api_client.DeploymentApi(api_client)
    project_name = 'project_name_example' # str | 
    deployment_id = 'deployment_id_example' # str | 
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Delete the deployment ID of a project
        api_instance.app_delete_deployment_id(project_name, deployment_id, as_org=as_org)
    except Exception as e:
        print("Exception when calling DeploymentApi->app_delete_deployment_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **deployment_id** | **str**|  | 
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

# **app_get_deployment_gateway**
> app_get_deployment_gateway(device_id, project_name, deployment_id, resource, as_org=as_org)

Get files relating to a gateway device



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
    api_instance = project_api_client.DeploymentApi(api_client)
    device_id = 'device_id_example' # str | 
    project_name = 'project_name_example' # str | 
    deployment_id = 'deployment_id_example' # str | 
    resource = 'resource_example' # str | 
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Get files relating to a gateway device
        api_instance.app_get_deployment_gateway(device_id, project_name, deployment_id, resource, as_org=as_org)
    except Exception as e:
        print("Exception when calling DeploymentApi->app_get_deployment_gateway: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **project_name** | **str**|  | 
 **deployment_id** | **str**|  | 
 **resource** | **str**|  | 
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

# **app_get_deployment_leaf**
> app_get_deployment_leaf(device_id, project_name, deployment_id, resource, as_org=as_org)

Get files relating to a leaf device



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
    api_instance = project_api_client.DeploymentApi(api_client)
    device_id = 'device_id_example' # str | 
    project_name = 'project_name_example' # str | 
    deployment_id = 'deployment_id_example' # str | 
    resource = 'resource_example' # str | 
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Get files relating to a leaf device
        api_instance.app_get_deployment_leaf(device_id, project_name, deployment_id, resource, as_org=as_org)
    except Exception as e:
        print("Exception when calling DeploymentApi->app_get_deployment_leaf: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **project_name** | **str**|  | 
 **deployment_id** | **str**|  | 
 **resource** | **str**|  | 
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

# **app_update_deployment_id**
> app_update_deployment_id(project_name, deployment_id, app_update_deployment_id_request, as_org=as_org)

Update deployment of a project



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.app_update_deployment_id_request import AppUpdateDeploymentIdRequest
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
    api_instance = project_api_client.DeploymentApi(api_client)
    project_name = 'project_name_example' # str | 
    deployment_id = 'deployment_id_example' # str | 
    app_update_deployment_id_request = project_api_client.AppUpdateDeploymentIdRequest() # AppUpdateDeploymentIdRequest | The deployment to be added.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Update deployment of a project
        api_instance.app_update_deployment_id(project_name, deployment_id, app_update_deployment_id_request, as_org=as_org)
    except Exception as e:
        print("Exception when calling DeploymentApi->app_update_deployment_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **deployment_id** | **str**|  | 
 **app_update_deployment_id_request** | [**AppUpdateDeploymentIdRequest**](AppUpdateDeploymentIdRequest.md)| The deployment to be added. | 
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

