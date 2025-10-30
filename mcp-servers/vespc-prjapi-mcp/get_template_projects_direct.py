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
    access_token = ''
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