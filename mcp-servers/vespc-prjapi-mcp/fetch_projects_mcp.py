#!/usr/bin/env python3
"""
Script to fetch STAIoT Craft user projects using MCP server.
"""

import subprocess
import json
import sys

def fetch_projects_using_mcp():
    """Fetch STAIoT Craft user projects using MCP server."""
    print("🔍 Fetching your STAIoT Craft user projects using MCP...")
    print("=" * 60)
    
    try:
        # Run the MCP server command to get projects
        print("📡 Starting MCP server...")
        
        # Command from your mcp.json configuration
        command = [
            "/Users/hemduttdabral/.local/bin/uv",
            "--directory",
            "/Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp",
            "run",
            "tools_httpx_1.py"
        ]
        
        print(f"🔧 Running command: {' '.join(command)}")
        print("-" * 50)
        
        # Run the MCP server
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ MCP server started successfully")
            print("📋 Server output:")
            print(result.stdout)
        else:
            print("❌ MCP server failed to start")
            print("🔧 Error output:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ MCP server timed out")
    except FileNotFoundError:
        print("❌ MCP server executable not found")
        print("💡 Make sure uv is installed at: /Users/hemduttdabral/.local/bin/uv")
    except Exception as e:
        print(f"❌ Error running MCP server: {str(e)}")

def test_mcp_tools_directly():
    """Test MCP tools by importing them directly."""
    print("\n🔧 Testing MCP tools directly...")
    print("-" * 40)
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Import the MCP tools
        from tools_httpx_1 import (
            fetch_usr_prjs,
            fetch_usr_prj_list,
            fetch_template_prj_list
        )
        
        print("✅ Successfully imported MCP tools")
        
        # Test fetching user projects
        print("\n👤 Fetching your user projects...")
        user_projects = fetch_usr_prjs()
        
        if user_projects:
            print(f"✅ Found {len(user_projects)} user projects:")
            for i, project in enumerate(user_projects, 1):
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
            print("❌ No user projects found")
            
        # Test fetching project names
        print("\n📋 Fetching project names...")
        user_names = fetch_usr_prj_list()
        if user_names:
            print("👤 Your Project Names:")
            for i, name in enumerate(user_names, 1):
                print(f"   {i}. {name}")
        else:
            print("   No user project names found")
            
        # Test fetching template projects
        print("\n📋 Fetching template projects...")
        template_names = fetch_template_prj_list()
        if template_names:
            print("📋 Template Project Names:")
            for i, name in enumerate(template_names, 1):
                print(f"   {i}. {name}")
        else:
            print("   No template project names found")
            
    except ImportError as e:
        print(f"❌ Error importing MCP tools: {str(e)}")
        print("🔧 Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error testing MCP tools: {str(e)}")

def show_mcp_configuration():
    """Show the current MCP configuration."""
    print("\n📋 Current MCP Configuration:")
    print("-" * 40)
    
    try:
        with open('.cursor/mcp.json', 'r') as f:
            config = json.load(f)
            
        print("✅ MCP Configuration loaded:")
        print(json.dumps(config, indent=2))
        
        # Count servers
        servers = config.get('mcpServers', {})
        print(f"\n📊 Configuration Summary:")
        print(f"   📡 Total MCP Servers: {len(servers)}")
        for server_name, server_config in servers.items():
            command = server_config.get('command', 'Unknown')
            args = server_config.get('args', [])
            print(f"   🔧 {server_name}: {command} {' '.join(args)}")
            
    except FileNotFoundError:
        print("❌ MCP configuration file not found: .cursor/mcp.json")
    except json.JSONDecodeError:
        print("❌ Invalid JSON in MCP configuration file")
    except Exception as e:
        print(f"❌ Error reading MCP configuration: {str(e)}")

def main():
    """Main function to fetch projects using MCP."""
    print("🚀 STAIoT Craft Project Fetcher using MCP")
    print("=" * 60)
    
    # Show MCP configuration
    show_mcp_configuration()
    
    # Test MCP tools directly
    test_mcp_tools_directly()
    
    # Try running MCP server
    fetch_projects_using_mcp()
    
    print("\n💡 MCP Usage Tips:")
    print("-" * 30)
    print("   # Get all your projects")
    print("   user_projects = fetch_usr_prjs()")
    print()
    print("   # Get project names")
    print("   user_names = fetch_usr_prj_list()")
    print()
    print("   # Get template projects")
    print("   template_names = fetch_template_prj_list()")
    print()
    print("🚀 MCP tools are ready to use!")

if __name__ == "__main__":
    main() 