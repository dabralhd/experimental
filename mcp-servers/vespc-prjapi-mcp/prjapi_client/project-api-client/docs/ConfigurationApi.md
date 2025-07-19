# project_api_client.ConfigurationApi

All URIs are relative to */3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_create_activity_configuration**](ConfigurationApi.md#app_create_activity_configuration) | **POST** /projects/{project_name}/models/{model_name}/{activity_type}/configuration | Create activity configuration file of the project/model/activity
[**app_patch_activity_configuration**](ConfigurationApi.md#app_patch_activity_configuration) | **PATCH** /projects/{project_name}/models/{model_name}/{activity_type}/configuration | Update activity configuration file of the project/model/activity


# **app_create_activity_configuration**
> app_create_activity_configuration(project_name, model_name, activity_type, training_mlc_configuration, as_org=as_org)

Create activity configuration file of the project/model/activity



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.training_mlc_configuration import TrainingMLCConfiguration
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
    api_instance = project_api_client.ConfigurationApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    training_mlc_configuration = project_api_client.TrainingMLCConfiguration() # TrainingMLCConfiguration | Create activity configuration file of the project/model/activity
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Create activity configuration file of the project/model/activity
        api_instance.app_create_activity_configuration(project_name, model_name, activity_type, training_mlc_configuration, as_org=as_org)
    except Exception as e:
        print("Exception when calling ConfigurationApi->app_create_activity_configuration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
 **training_mlc_configuration** | [**TrainingMLCConfiguration**](TrainingMLCConfiguration.md)| Create activity configuration file of the project/model/activity | 
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

# **app_patch_activity_configuration**
> app_patch_activity_configuration(project_name, model_name, activity_type, training_mlc_configuration, as_org=as_org)

Update activity configuration file of the project/model/activity



### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import project_api_client
from project_api_client.models.training_mlc_configuration import TrainingMLCConfiguration
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
    api_instance = project_api_client.ConfigurationApi(api_client)
    project_name = 'project_name_example' # str | Project `name` identifier
    model_name = 'model_name_example' # str | Model `name` identifier
    activity_type = 'activity_type_example' # str | Activity `name` identifier
    training_mlc_configuration = project_api_client.TrainingMLCConfiguration() # TrainingMLCConfiguration | The job artifact to be downloaded to user workspace.
    as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    try:
        # Update activity configuration file of the project/model/activity
        api_instance.app_patch_activity_configuration(project_name, model_name, activity_type, training_mlc_configuration, as_org=as_org)
    except Exception as e:
        print("Exception when calling ConfigurationApi->app_patch_activity_configuration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**| Project &#x60;name&#x60; identifier | 
 **model_name** | **str**| Model &#x60;name&#x60; identifier | 
 **activity_type** | **str**| Activity &#x60;name&#x60; identifier | 
 **training_mlc_configuration** | [**TrainingMLCConfiguration**](TrainingMLCConfiguration.md)| The job artifact to be downloaded to user workspace. | 
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

