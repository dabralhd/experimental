# project_api_client.PublicProjectsActivityApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_get_public_projects_activity**](PublicProjectsActivityApi.md#app_get_public_projects_activity) | **GET** /templates/projects/{project_name}/models/{model_name}/{activity_type} | Get the file contents of artifacts, reports or configuration of the activity for public projects


# **app_get_public_projects_activity**
> List[str] app_get_public_projects_activity(project_name, model_name, activity_type, type=type, name=name)

Get the file contents of artifacts, reports or configuration of the activity for public projects



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
    api_instance = project_api_client.PublicProjectsActivityApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Model `activity_type` identifier
    type = 'type_example' # str | string corresponding to artifact to be GET artifacts, reports, runtime OR config (optional)
    name = 'name_example' # str | Filename of artifact for which GET is issued (optional)

    try:
        # Get the file contents of artifacts, reports or configuration of the activity for public projects
        api_response = api_instance.app_get_public_projects_activity(project_name, model_name, activity_type, type=type, name=name)
        print("The response of PublicProjectsActivityApi->app_get_public_projects_activity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PublicProjectsActivityApi->app_get_public_projects_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Model &#x60;activity_type&#x60; identifier | 
 **type** | **str**| string corresponding to artifact to be GET artifacts, reports, runtime OR config | [optional] 
 **name** | **str**| Filename of artifact for which GET is issued | [optional] 

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Bad request |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

