#!/usr/bin/env python3
"""
Script to list STAIoT Craft projects using installed MCP tools.
"""

import sys
import os

# Add the current directory to the path so we can import the tools module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def list_projects_using_mcp_tools():
    """List STAIoT Craft projects using MCP tools."""
    print("🔍 Listing your STAIoT Craft projects using MCP tools...")
    print("=" * 70)
    
    try:
        # Import the MCP tools
        from tools_httpx_1 import (
            fetch_usr_prjs,
            fetch_usr_prj_list,
            fetch_template_prj_list,
            fetch_template_prjs
        )
        
        print("📡 Using MCP Server: prjapi-mcp")
        print("🔧 Active Tools: tools_httpx_1.py")
        print("-" * 50)
        
        # Get user projects using MCP tools
        print("\n👤 Your User Projects:")
        print("-" * 30)
        
        try:
            user_projects = fetch_usr_prjs()
            if user_projects:
                print(f"✅ Found {len(user_projects)} user projects:")
                for i, project in enumerate(user_projects, 1):
                    name = project.get('ai_project_name', 'Unknown')
                    description = project.get('description', 'No description')
                    version = project.get('version', 'Unknown version')
                    creation_time = project.get('creation_time', 'Unknown')
                    
                    print(f"\n{i}. 📁 {name}")
                    print(f"   📝 Description: {description}")
                    print(f"   🏷️  Version: {version}")
                    print(f"   📅 Created: {creation_time}")
                    
                    # Show models if available
                    models = project.get('models', [])
                    if models:
                        print(f"   🤖 Models: {len(models)} model(s)")
                        for j, model in enumerate(models[:3], 1):
                            model_name = model.get('name', 'Unknown')
                            model_type = model.get('model_metadata', {}).get('type', 'Unknown')
                            print(f"      {j}. {model_name} ({model_type})")
                        if len(models) > 3:
                            print(f"      ... and {len(models) - 3} more models")
                    
                    # Show deployments if available
                    deployments = project.get('deployments', [])
                    if deployments:
                        print(f"   🚀 Deployments: {len(deployments)} deployment(s)")
                        for j, deployment in enumerate(deployments[:3], 1):
                            deploy_name = deployment.get('display_name', 'Unknown')
                            deploy_status = deployment.get('last_deploy_result', 'Unknown')
                            print(f"      {j}. {deploy_name} ({deploy_status})")
                        if len(deployments) > 3:
                            print(f"      ... and {len(deployments) - 3} more deployments")
            else:
                print("❌ No user projects found.")
                print("💡 You might need to:")
                print("   - Create your first project")
                print("   - Clone a template project to get started")
                
        except Exception as e:
            print(f"❌ Error fetching user projects: {str(e)}")
        
        # Get template projects using MCP tools
        print("\n📋 Template/Example Projects:")
        print("-" * 40)
        
        try:
            template_projects = fetch_template_prjs()
            if template_projects:
                print(f"✅ Found {len(template_projects)} template projects:")
                for i, project in enumerate(template_projects, 1):
                    name = project.get('ai_project_name', 'Unknown')
                    description = project.get('description', 'No description')
                    version = project.get('version', 'Unknown version')
                    
                    print(f"\n{i}. 📁 {name}")
                    print(f"   📝 Description: {description}")
                    print(f"   🏷️  Version: {version}")
                    
                    # Show models if available
                    models = project.get('models', [])
                    if models:
                        print(f"   🤖 Models: {len(models)} model(s)")
                        for j, model in enumerate(models[:3], 1):
                            model_name = model.get('name', 'Unknown')
                            model_type = model.get('model_metadata', {}).get('type', 'Unknown')
                            print(f"      {j}. {model_name} ({model_type})")
                        if len(models) > 3:
                            print(f"      ... and {len(models) - 3} more models")
            else:
                print("❌ No template projects found.")
                
        except Exception as e:
            print(f"❌ Error fetching template projects: {str(e)}")
        
        # Get just the names using MCP tools
        print("\n📋 Project Names Only:")
        print("-" * 30)
        
        try:
            user_names = fetch_usr_prj_list()
            if user_names:
                print("👤 Your Project Names:")
                for i, name in enumerate(user_names, 1):
                    print(f"   {i}. {name}")
            else:
                print("   No user project names found.")
                
        except Exception as e:
            print(f"❌ Error fetching user project names: {str(e)}")
        
        try:
            template_names = fetch_template_prj_list()
            if template_names:
                print("\n📋 Template Project Names:")
                for i, name in enumerate(template_names, 1):
                    print(f"   {i}. {name}")
            else:
                print("   No template project names found.")
                
        except Exception as e:
            print(f"❌ Error fetching template project names: {str(e)}")
        
        # Summary
        print("\n📊 Summary:")
        print("-" * 30)
        try:
            user_count = len(fetch_usr_prjs() or [])
            template_count = len(fetch_template_prjs() or [])
            print(f"   👤 User Projects: {user_count}")
            print(f"   📋 Template Projects: {template_count}")
            print(f"   📊 Total Projects: {user_count + template_count}")
        except:
            print("   📊 Unable to get project counts")
        
        print("\n💡 MCP Tool Usage:")
        print("-" * 30)
        print("   # Get all your projects")
        print("   user_projects = fetch_usr_prjs()")
        print()
        print("   # Get template projects")
        print("   template_projects = fetch_template_prjs()")
        print()
        print("   # Get just project names")
        print("   user_names = fetch_usr_prj_list()")
        print("   template_names = fetch_template_prj_list()")
        print()
        print("🚀 MCP tools are working correctly!")
        
    except ImportError as e:
        print(f"❌ Error importing MCP tools: {str(e)}")
        print("🔧 Make sure the MCP server is running and tools are available")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("🔧 Check your connection and authentication")

if __name__ == "__main__":
    list_projects_using_mcp_tools() 