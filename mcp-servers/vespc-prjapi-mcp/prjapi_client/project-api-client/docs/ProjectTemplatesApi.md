# project_api_client.ProjectTemplatesApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_get_templates_projects**](ProjectTemplatesApi.md#app_get_templates_projects) | **GET** /templates/projects | Project templates list


# **app_get_templates_projects**
> List[Project] app_get_templates_projects()

Project templates list



### Example


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


# Enter a context with an instance of the API client
with project_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = project_api_client.ProjectTemplatesApi(api_client)

    try:
        # Project templates list
        api_response = api_instance.app_get_templates_projects()
        print("The response of ProjectTemplatesApi->app_get_templates_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectTemplatesApi->app_get_templates_projects: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Project]**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

