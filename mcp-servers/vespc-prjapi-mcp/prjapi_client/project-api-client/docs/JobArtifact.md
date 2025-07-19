# JobArtifact


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**s3_url** | **str** |  | [optional] 
**job** | [**Job**](Job.md) |  | [optional] 
**artifacts** | **List[str]** |  | [optional] 
**reports** | **List[str]** |  | [optional] 

## Example

```python
from project_api_client.models.job_artifact import JobArtifact

# TODO update the JSON string below
json = "{}"
# create an instance of JobArtifact from a JSON string
job_artifact_instance = JobArtifact.from_json(json)
# print the JSON string representation of the object
print(JobArtifact.to_json())

# convert the object into a dict
job_artifact_dict = job_artifact_instance.to_dict()
# create an instance of JobArtifact from a dict
job_artifact_from_dict = JobArtifact.from_dict(job_artifact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


