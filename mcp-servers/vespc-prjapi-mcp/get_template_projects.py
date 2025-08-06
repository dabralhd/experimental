#!/usr/bin/env python3
"""
Script to get template project list from the STAIoT Craft tool's workspace.
"""

import sys
import os

# Add the current directory to the path so we can import the tools module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools_httpx_1 import fetch_template_prj_list, get_template_projects

def main():
    """Get and display the template project list."""
    print("Fetching template project list...")
    
    # Get the full template projects data
    template_projects = get_template_projects()
    
    if template_projects:
        print(f"\nFound {len(template_projects)} template projects:")
        print("-" * 50)
        
        for i, project in enumerate(template_projects, 1):
            print(f"{i}. {project.get('ai_project_name', 'Unknown')}")
            if 'description' in project:
                print(f"   Description: {project['description']}")
            if 'version' in project:
                print(f"   Version: {project['version']}")
            print()
    else:
        print("No template projects found or failed to fetch projects.")
    
    # Also get just the project names using the existing tool
    print("\nTemplate project names:")
    print("-" * 30)
    project_names = fetch_template_prj_list()
    if project_names:
        for i, name in enumerate(project_names, 1):
            print(f"{i}. {name}")
    else:
        print("No template project names found.")

if __name__ == "__main__":
    main() 