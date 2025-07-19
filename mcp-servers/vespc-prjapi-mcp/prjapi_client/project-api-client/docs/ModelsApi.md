# project_api_client.ModelsApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_create_model**](ModelsApi.md#app_create_model) | **POST** /projects/{project_name}/models | Create new model
[**app_patch_model**](ModelsApi.md#app_patch_model) | **PATCH** /projects/{project_name}/models/{model_name} | Patch a model


# **app_create_model**
> app_create_model(project_name, new_model, as_org=as_org)

Create new model



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.new_model import NewModel
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
    api_instance = project_api_client.ModelsApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    new_model = project_api_client.NewModel() # NewModel | The model to be added (or cloned).
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will copy a model, using rights of an organization  (optional)

    try:
        # Create new model
        api_instance.app_create_model(project_name, new_model, as_org=as_org)
    except Exception as e:
        print("Exception when calling ModelsApi->app_create_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **new_model** | [**NewModel**](NewModel.md)| The model to be added (or cloned). | 
 **as_org** | **str**| sometimes a user will copy a model, using rights of an organization  | [optional] 

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
**201** | OK. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_patch_model**
> app_patch_model(project_name, model_name, new_model, as_org=as_org)

Patch a model



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.new_model import NewModel
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
    api_instance = project_api_client.ModelsApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    new_model = project_api_client.NewModel() # NewModel | The model to be patched.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Patch a model
        api_instance.app_patch_model(project_name, model_name, new_model, as_org=as_org)
    except Exception as e:
        print("Exception when calling ModelsApi->app_patch_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **new_model** | [**NewModel**](NewModel.md)| The model to be patched. | 
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
**201** | OK. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthorized. |  -  |
**404** | Not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

