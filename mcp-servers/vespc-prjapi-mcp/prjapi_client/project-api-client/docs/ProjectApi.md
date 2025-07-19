# project_api_client.ProjectApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_delete_project**](ProjectApi.md#app_delete_project) | **DELETE** /projects/{project_name} | Delete project associated to the given name.
[**app_get_project**](ProjectApi.md#app_get_project) | **GET** /projects/{project_name} | Get project associated to the given name.
[**app_get_project_icon**](ProjectApi.md#app_get_project_icon) | **GET** /projects/{project_name}/icon | Get project icon associated to the given name.
[**app_get_template_project_icon**](ProjectApi.md#app_get_template_project_icon) | **GET** /templates/projects/{project_name}/icon | Get project icon associated to the given name.


# **app_delete_project**
> app_delete_project(project_name, as_org=as_org)

Delete project associated to the given name.



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
    api_instance = project_api_client.ProjectApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will use org id credentials  (optional)

    try:
        # Delete project associated to the given name.
        api_instance.app_delete_project(project_name, as_org=as_org)
    except Exception as e:
        print("Exception when calling ProjectApi->app_delete_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **as_org** | **str**| sometimes a user will use org id credentials  | [optional] 

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
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_get_project**
> Project app_get_project(project_name, as_org=as_org)

Get project associated to the given name.



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.project import Project
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
    api_instance = project_api_client.ProjectApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Get project associated to the given name.
        api_response = api_instance.app_get_project(project_name, as_org=as_org)
        print("The response of ProjectApi->app_get_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectApi->app_get_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **as_org** | **str**| sometimes a user will share a project with an org  | [optional] 

### Return type

[**Project**](Project.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_get_project_icon**
> bytearray app_get_project_icon(project_name, as_org=as_org)

Get project icon associated to the given name.



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
    api_instance = project_api_client.ProjectApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will use org id credentials  (optional)

    try:
        # Get project icon associated to the given name.
        api_response = api_instance.app_get_project_icon(project_name, as_org=as_org)
        print("The response of ProjectApi->app_get_project_icon:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectApi->app_get_project_icon: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **as_org** | **str**| sometimes a user will use org id credentials  | [optional] 

### Return type

**bytearray**

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: image/*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_get_template_project_icon**
> bytearray app_get_template_project_icon(project_name)

Get project icon associated to the given name.



### Example


```python
import project_api_client
from project_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /3
# See configuration.py for a list of all supported configuration parameters.
configuration = project_api_client.Configuration(
    host = "/3"
)


# Enter a context with an instance of the API client
with project_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = project_api_client.ProjectApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier

    try:
        # Get project icon associated to the given name.
        api_response = api_instance.app_get_template_project_icon(project_name)
        print("The response of ProjectApi->app_get_template_project_icon:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectApi->app_get_template_project_icon: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: image/*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

