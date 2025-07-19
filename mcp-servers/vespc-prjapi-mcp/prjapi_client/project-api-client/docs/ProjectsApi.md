# project_api_client.ProjectsApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_create_project**](ProjectsApi.md#app_create_project) | **POST** /projects | Create new project
[**app_get_projects**](ProjectsApi.md#app_get_projects) | **GET** /projects | Projects list


# **app_create_project**
> app_create_project(is_user_project=is_user_project, as_org=as_org, new_project=new_project)

Create new project



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.new_project import NewProject
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
    api_instance = project_api_client.ProjectsApi(api_client)
    is_user_project = True # bool | Boolean flag which indicates whether 'project_name_to_clone' is a user project (optional)
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)
    new_project = project_api_client.NewProject() # NewProject | New project model (optional)

    try:
        # Create new project
        api_instance.app_create_project(is_user_project=is_user_project, as_org=as_org, new_project=new_project)
    except Exception as e:
        print("Exception when calling ProjectsApi->app_create_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **is_user_project** | **bool**| Boolean flag which indicates whether &#39;project_name_to_clone&#39; is a user project | [optional] 
 **as_org** | **str**| sometimes a user will share a project with an org  | [optional] 
 **new_project** | [**NewProject**](NewProject.md)| New project model | [optional] 

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_get_projects**
> List[Project] app_get_projects(as_org=as_org)

Projects list



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
    api_instance = project_api_client.ProjectsApi(api_client)
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Projects list
        api_response = api_instance.app_get_projects(as_org=as_org)
        print("The response of ProjectsApi->app_get_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->app_get_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **as_org** | **str**| sometimes a user will share a project with an org  | [optional] 

### Return type

[**List[Project]**](Project.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

