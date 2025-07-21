import project_api_client
from project_api_client.rest import ApiException
from pprint import pprint
# @hdtest_group_id = sp4n95r2rc4he7b4rpzdpqtj10
# @local_port = 9090
# @remote_port = 443
# @local_api_base_path = /3
# @remote_api_base_path = /svc/project-api
# @remote_api_base_path_3 = /svc/project-api/3
# @local_url = http://127.0.0.1:{{local_port}}{{local_api_base_path}}
# @remote_url = https://vespucci.st.com:{{remote_port}}{{remote_api_base_path}}
# @remote_dev_url = https://dev.stm-vespucci.com:{{remote_port}}{{remote_api_base_path_3}}
# @base_url = {{remote_dev_url}}
# @token-dummy = dev
# @token-dev = eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiYzhkYWZjMjQtZWY0ZS00YTYwLTlmNmQtODdiYjFlMTY0YzM0IiwiZXZlbnRfaWQiOiJlNzlmMTcwMy04MzQxLTRhOGYtYTI0ZS1hYmZjMTBmYjc5YjQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTI0NzQ2MTcsImV4cCI6MTc1MjU2MTAxNywiaWF0IjoxNzUyNDc0NjE3LCJqdGkiOiI2Mjg5MTNlMi00ZTA1LTQ1MzctYTM4NS1mNTUyMTExMGJlYjgiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.kEeRpoNBlNRg5HbQUGjShr7al7Mobr2cKJN0nja-E-UExb-nkwQiNFIXGh5ZQVnMSWrqTT_7fM1evbdU1BVcsp1w3ojshRCsBJthpT2zMnVV1CiE4Zqxxg_RAerLrwbPjAnYcP6yrMMnj7NcvzmPPIa4SksToE8hiubpsWguYnHSi6Z3ij0N_cGgx3SXg9dY6MgKiM_a3i1aip0rDJxJqaVbnSMwnea3YVjyRjUKaWpsvzusI1tlxeoby74nZoxGBh0i91v0lcsdXSfeQDJiBLIigjAuKa-9C2bW44CMAQDoiIVb_gywHbCmbXaWQcH8k_bBHokRc08PYkIq8AdbBA
# @token = {{token-dev}}

remote_dev_url = 'https://dev.stm-vespucci.com:443/svc/project-api/3'

print(f"Using remote_dev_url: {remote_dev_url}")

# Configure Bearer authorization (JWT): bearerAuth
configuration = project_api_client.Configuration(
    host = remote_dev_url,
    access_token = 'eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiODUyNDcyYWQtNjU2ZS00NjViLWEzY2MtMzY1MGE0MGFjN2I1IiwiZXZlbnRfaWQiOiIzZjNjNWEwZi05MGYxLTRiNzUtODliNS04ZmI0OTgwYjY0MDIiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTA2MDY5NTEsImV4cCI6MTc1MzAwNDMzMSwiaWF0IjoxNzUyOTE3OTMxLCJqdGkiOiIzNzE3NThiYy0zNDc1LTQ5YTYtYjRlNS05MzcxNDI5MWViMmUiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.A8Z8HyNRZBYhhO7AsZKJEF0I00z9ykBSPNft9RxHtmvpjmCQHwXaSsy8QvzYac9PwciEEo5bAN6VKDdZIu0VipopTG1-026CNVDADU_LUM8Iclza-lXDuSzl9tJ5FOsCxmP4Lfez3D8j8iBFBbFu5gVJWxZC4SBswqNzMVhtfY8BI3oZ2sag-FAANwRRTI2yLnRoscBt7qkNftDk2Du-TdsCDnSOvI17ZoYcV-7awLx0yeLWJiUZEGC7PwCdfi0-I5KVwjDuSkQlLuWEKhNnohbaoG_VSXPSEwhgEkk5AJOayIGWgBEF0UOji58Jl9aU63BHNmmdfnZsu1wTHpIPQg'
)


# Enter a context with an instance of the API client
with project_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    projects_api_instance = project_api_client.ProjectsApi(api_client)

    #api_instance = project_api_client.ActivityApi(api_client)
    # project_name = 'project_name_example' # str | Project `name` identifier
    # model_name = 'model_name_example' # str | Model `name` identifier
    # activity_type = 'activity_type_example' # str | Activity `name` identifier
    # new_training = project_api_client.NewTraining() # NewTraining | The activity to be added.
    # as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

    prjs = []
    try:
        # Create new Activity
        #api_instance.app_create_activity(project_name, model_name, activity_type, new_training, as_org=as_org)
        prjs = projects_api_instance.app_get_projects()
    except ApiException as e:
        print("Exception when calling ActivityApi->app_get_projects: %s\n" % e)
    except Exception as e:
        print("Exception when calling ActivityApi->app_get_projects: %s\n" % e)
    pprint(prjs)