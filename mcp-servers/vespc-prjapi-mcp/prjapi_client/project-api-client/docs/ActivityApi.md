# project_api_client.ActivityApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_create_activity**](ActivityApi.md#app_create_activity) | **POST** /projects/{project_name}/models/{model_name}/{activity_type} | Create new Activity
[**app_delete_activity**](ActivityApi.md#app_delete_activity) | **DELETE** /projects/{project_name}/models/{model_name}/{activity_type} | Delete the activity associated to the given name.
[**app_get_activity**](ActivityApi.md#app_get_activity) | **GET** /projects/{project_name}/models/{model_name}/{activity_type} | Get the file contents of artifacts, reports or configuration of the activity
[**app_patch_activity**](ActivityApi.md#app_patch_activity) | **PATCH** /projects/{project_name}/models/{model_name}/{activity_type} | Update partial Activity JSON
[**app_update_activity**](ActivityApi.md#app_update_activity) | **PUT** /projects/{project_name}/models/{model_name}/{activity_type} | Update Activity JSON


# **app_create_activity**
> app_create_activity(project_name, model_name, activity_type, new_training, as_org=as_org)

Create new Activity



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.new_training import NewTraining
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
    api_instance = project_api_client.ActivityApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    new_training = project_api_client.NewTraining() # NewTraining | The activity to be added.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Create new Activity
        api_instance.app_create_activity(project_name, model_name, activity_type, new_training, as_org=as_org)
    except Exception as e:
        print("Exception when calling ActivityApi->app_create_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
 **new_training** | [**NewTraining**](NewTraining.md)| The activity to be added. | 
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
**201** | Created. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_delete_activity**
> app_delete_activity(project_name, model_name, activity_type, as_org=as_org)

Delete the activity associated to the given name.



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
    api_instance = project_api_client.ActivityApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Delete the activity associated to the given name.
        api_instance.app_delete_activity(project_name, model_name, activity_type, as_org=as_org)
    except Exception as e:
        print("Exception when calling ActivityApi->app_delete_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
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
**400** | Bad request |  -  |
**401** | Unathorized |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_get_activity**
> List[str] app_get_activity(project_name, model_name, activity_type, type=type, name=name, as_org=as_org)

Get the file contents of artifacts, reports or configuration of the activity



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
    api_instance = project_api_client.ActivityApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    type = 'type_example' # str | string corresponding to artifact to be GET artifacts, reports, runtime OR config (optional)
    name = 'name_example' # str | Filename of artifact for which GET is issued (optional)
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Get the file contents of artifacts, reports or configuration of the activity
        api_response = api_instance.app_get_activity(project_name, model_name, activity_type, type=type, name=name, as_org=as_org)
        print("The response of ActivityApi->app_get_activity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivityApi->app_get_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
 **type** | **str**| string corresponding to artifact to be GET artifacts, reports, runtime OR config | [optional] 
 **name** | **str**| Filename of artifact for which GET is issued | [optional] 
 **as_org** | **str**| sometimes a user will share a project with an org  | [optional] 

### Return type

**List[str]**

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Bad request |  -  |
**401** | Unathorized |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_patch_activity**
> app_patch_activity(project_name, model_name, activity_type, app_patch_activity_request, as_org=as_org)

Update partial Activity JSON



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.app_patch_activity_request import AppPatchActivityRequest
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
    api_instance = project_api_client.ActivityApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    app_patch_activity_request = project_api_client.AppPatchActivityRequest() # AppPatchActivityRequest | The activity to be patched.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Update partial Activity JSON
        api_instance.app_patch_activity(project_name, model_name, activity_type, app_patch_activity_request, as_org=as_org)
    except Exception as e:
        print("Exception when calling ActivityApi->app_patch_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
 **app_patch_activity_request** | [**AppPatchActivityRequest**](AppPatchActivityRequest.md)| The activity to be patched. | 
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
**201** | Created. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_update_activity**
> app_update_activity(project_name, model_name, activity_type, training, as_org=as_org)

Update Activity JSON



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.training import Training
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
    api_instance = project_api_client.ActivityApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    training = project_api_client.Training() # Training | The activity to be updated.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Update Activity JSON
        api_instance.app_update_activity(project_name, model_name, activity_type, training, as_org=as_org)
    except Exception as e:
        print("Exception when calling ActivityApi->app_update_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
 **training** | [**Training**](Training.md)| The activity to be updated. | 
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
**201** | Created. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

