#!/usr/bin/env python3
"""
Script to get template project list using the project API client directly.
"""

import sys
import os

# Add the project-api-client to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prjapi_client/project-api-client'))

import project_api_client
from project_api_client.rest import ApiException
from pprint import pprint

# Configuration - using the same settings as the test file
remote_dev_url = 'https://dev.stm-vespucci.com:443/svc/project-api/3'

print(f"Using remote_dev_url: {remote_dev_url}")

# Configure Bearer authorization (JWT): bearerAuth
configuration = project_api_client.Configuration(
    host = remote_dev_url,
    access_token = 'eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiZDk4OTE1MzgtMjcyYy00NWM2LWFmNzQtZjJhN2UyNjI4ZjcyIiwiZXZlbnRfaWQiOiI1NWNmY2UxNi03ZWMzLTQzZWEtYTMyMi03ODQ3Nzg3YTgwMzEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTMyMDU4MDIsImV4cCI6MTc1MzI5MjIwMiwiaWF0IjoxNzUzMjA1ODAyLCJqdGkiOiI4NmMzMzA5ZS02NDhjLTQ5ZDAtOTIyMS0wYjJjODcwOWU5Y2UiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.kC0g3NSSUdMxRyjW6Bav-c-aibndM7T_3ayqxUd-KFA5hkFZHbwr7aCcTgYNdKz7Gt5EL0GWPr2Pq3Vn2HstJ6O_mglyquNWP-z_RjM9v59sKsDY-VtrnhcsZ7h3o_VQB9EvFdwq0f5AEYQJnrqHhQWicsjbn400EOVEraYti7oeX-oiyD8_FpPFbbqSBGBgHD9Du3SDBLQDyDylykGCo0mofr9G6iRq-uIkdElUwabTweX-sbDg_1fR6ejYkmJsHVH-KwpKxdS6rkoWss8cl8T1sWk5bcw2QGpn53_L2QAXrBRjI_J1zBNMAZirDeVm952zc0ZURB-qljm0-tkxXg'
)

def get_template_projects():
    """Get template projects using the ProjectTemplatesApi."""
    try:
        # Enter a context with an instance of the API client
        with project_api_client.ApiClient(configuration) as api_client:
            # Create an instance of the ProjectTemplatesApi class
            templates_api_instance = project_api_client.ProjectTemplatesApi(api_client)

            print("Fetching template projects...")
            template_projects = templates_api_instance.app_get_templates_projects()
            
            print(f"\nFound {len(template_projects)} template projects:")
            print("-" * 50)
            
            for i, project in enumerate(template_projects, 1):
                print(f"{i}. {project.ai_project_name}")
                if hasattr(project, 'description') and project.description:
                    print(f"   Description: {project.description}")
                if hasattr(project, 'version') and project.version:
                    print(f"   Version: {project.version}")
                print()
                
            return template_projects
            
    except ApiException as e:
        print(f"Exception when calling ProjectTemplatesApi->app_get_templates_projects: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    """Main function to get template projects."""
    template_projects = get_template_projects()
    
    if not template_projects:
        print("Failed to fetch template projects.")

if __name__ == "__main__":
    main() 