#!/usr/bin/env python3
"""
Simple script to fetch STAIoT Craft user projects using MCP tools.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fetch_user_projects_mcp():
    """Fetch user projects using MCP tools."""
    print("🔍 Fetching your STAIoT Craft user projects using MCP...")
    print("=" * 60)
    
    try:
        # Import MCP tools
        print("📡 Importing MCP tools...")
        from tools_httpx_1 import fetch_usr_prjs, fetch_usr_prj_list
        print("✅ MCP tools imported successfully")
        
        # Get all user projects
        print("\n👤 Fetching your user projects...")
        user_projects = fetch_usr_prjs()
        
        if user_projects:
            print(f"✅ Found {len(user_projects)} user projects:")
            print("-" * 50)
            
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
        
        # Get just the project names
        print("\n📋 Project Names Only:")
        print("-" * 30)
        user_names = fetch_usr_prj_list()
        if user_names:
            print("👤 Your Project Names:")
            for i, name in enumerate(user_names, 1):
                print(f"   {i}. {name}")
        else:
            print("   No user project names found.")
        
        # Summary
        print("\n📊 Summary:")
        print("-" * 20)
        print(f"   👤 Total User Projects: {len(user_projects) if user_projects else 0}")
        
        print("\n🚀 MCP tools working correctly!")
        
    except ImportError as e:
        print(f"❌ Error importing MCP tools: {str(e)}")
        print("🔧 Try running with uv:")
        print("   uv run python get_user_projects_mcp.py")
    except Exception as e:
        print(f"❌ Error fetching projects: {str(e)}")
        print("🔧 Check your connection and authentication")

if __name__ == "__main__":
    fetch_user_projects_mcp() 