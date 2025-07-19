# project_api_client.ModelApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_delete_model**](ModelApi.md#app_delete_model) | **DELETE** /projects/{project_name}/models/{model_name} | Delete model associated to the given name.


# **app_delete_model**
> app_delete_model(project_name, model_name, as_org=as_org)

Delete model associated to the given name.



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
    api_instance = project_api_client.ModelApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will use org id credentials  (optional)

    try:
        # Delete model associated to the given name.
        api_instance.app_delete_model(project_name, model_name, as_org=as_org)
    except Exception as e:
        print("Exception when calling ModelApi->app_delete_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
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

