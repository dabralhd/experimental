# Installed MCP Tools

Based on your current configuration and codebase, here are all the MCP tools you have installed:

## Currently Active MCP Server

### **prjapi-mcp** (STAIoT Craft Project API MCP Server)
- **Status**: ✅ Active (configured in `.cursor/mcp.json`)
- **Server File**: `tools_httpx_1.py`
- **Command**: `/Users/hemduttdabral/.local/bin/uv`
- **Arguments**: `--directory /Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp run tools_httpx_1.py`

## Available MCP Tools (11 Total)

### **1. Project Discovery Tools**

#### `fetch_usr_prjs()`
- **Purpose**: Fetch all user projects from STAIoT Craft workspace
- **Returns**: Complete project details for all user projects
- **Usage**: Get full project information including models and deployments

#### `fetch_template_prjs()`
- **Purpose**: Fetch all template/example projects from STAIoT Craft
- **Returns**: Complete project details for all template projects
- **Usage**: Get full template project information

#### `fetch_usr_prj_list()`
- **Purpose**: Get a list of user project names
- **Returns**: Array of project names (`ai_project_name`)
- **Usage**: Quick list of your project names

#### `fetch_template_prj_list()`
- **Purpose**: Get a list of template project names
- **Returns**: Array of template project names
- **Usage**: Quick list of available template names

### **2. Project Detail Tools**

#### `fetch_usr_prj_using_name(ai_project_name: str)`
- **Purpose**: Get detailed information about a specific user project
- **Parameters**: `ai_project_name` - name of the project to fetch
- **Returns**: Complete project details or None if not found
- **Usage**: Get detailed info about a specific project

#### `fetch_template_prj_using_name(ai_project_name: str)`
- **Purpose**: Get detailed information about a specific template project
- **Parameters**: `ai_project_name` - name of the template project to fetch
- **Returns**: Complete template project details or None if not found
- **Usage**: Get detailed info about a specific template

#### `fetch_usr_prj_attr(attr: str='ai_project_name')`
- **Purpose**: Fetch specific attributes for all user projects
- **Parameters**: `attr` - attribute name (default: 'ai_project_name')
- **Returns**: Array of attribute values for all projects
- **Usage**: Get specific attributes like descriptions, versions, etc.

### **3. Project Creation Tools**

#### `create_usr_prj(ai_project_name: str, description: str = "project description", version: str = '0.0.1')`
- **Purpose**: Create a new user project from scratch
- **Parameters**: 
  - `ai_project_name` - name of the new project
  - `description` - project description (optional)
  - `version` - project version (optional)
- **Returns**: Created project details
- **Usage**: Create new AI projects

### **4. Project Cloning Tools**

#### `clone_usr_prj(ai_project_name: str, project_name_to_clone: str)`
- **Purpose**: Clone an existing user project
- **Parameters**:
  - `ai_project_name` - name for the new cloned project
  - `project_name_to_clone` - name of the project to clone
- **Returns**: Cloned project details
- **Usage**: Copy existing user projects

#### `clone_template_prj(ai_project_name: str, project_name_to_clone: str)`
- **Purpose**: Clone a template/example project
- **Parameters**:
  - `ai_project_name` - name for the new cloned project
  - `project_name_to_clone` - name of the template project to clone
- **Returns**: Cloned project details
- **Usage**: Start with template projects

### **5. Project Deletion Tools**

#### `delete_usr_prj_using_name(ai_project_name: str)`
- **Purpose**: Delete a user project by name
- **Parameters**: `ai_project_name` - name of the project to delete
- **Returns**: None (success) or error message
- **Usage**: Remove unwanted projects

## Additional MCP Server Files (Not Currently Active)

### **tools.py** (6 tools)
- `create_project(prj_name: str)` - Create new project
- `list_projects_1()` - List all projects
- `clone_project(project_name: str)` - Clone project
- `delete_project(project_name: str)` - Delete project
- `describe_project(project_name: str)` - Describe project
- `list_models(project_name: str)` - List models

### **tools_project_api_client_based.py** (6 tools)
- `create_project(prj_name: str)` - Create new project
- `list_projects()` - List all projects
- `clone_project(project_name: str)` - Clone project
- `delete_project(project_name: str)` - Delete project
- `describe_project(project_name: str)` - Describe project
- `list_models(project_name: str)` - List models

## Configuration

### **Active Configuration** (`.cursor/mcp.json`)
```json
{
    "mcpServers": {
        "prjapi-mcp": {
            "command": "/Users/hemduttdabral/.local/bin/uv",
            "args": [
              "--directory",
              "/Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp",
              "run",
              "tools_httpx_1.py"
            ]
        }
    }
}
```

## Usage Examples

### **Basic Usage**
```python
# Get all your projects
user_projects = fetch_usr_prjs()

# Get template projects
template_projects = fetch_template_prjs()

# Create a new project
new_project = create_usr_prj("my_ai_project", "My AI project", "1.0.0")

# Clone a template
cloned_project = clone_template_prj("my_working_project", "example_classifier")
```

### **Advanced Usage**
```python
# Get project details
project_details = fetch_usr_prj_using_name("my_project")

# Get specific attributes
project_names = fetch_usr_prj_attr("ai_project_name")
project_descriptions = fetch_usr_prj_attr("description")

# Delete a project
delete_usr_prj_using_name("unwanted_project")
```

## Authentication

- **Base URL**: `https://dev.stm-vespucci.com:443/svc/project-api/3`
- **Authentication**: Bearer token (JWT)
- **Token**: Configured in the MCP server files

## Supported Operations

1. **Project Management**: Create, read, update, delete projects
2. **Template Access**: Access to example/template projects
3. **Project Cloning**: Copy existing projects
4. **Attribute Access**: Get specific project attributes
5. **STAIoT Craft Integration**: Full API integration

## Total Tools Available

- **Active Tools**: 11 (from `tools_httpx_1.py`)
- **Additional Tools**: 12 (from `tools.py` and `tools_project_api_client_based.py`)
- **Total MCP Tools**: 23 tools across 3 server files
- **Currently Active**: 11 tools from `tools_httpx_1.py` 