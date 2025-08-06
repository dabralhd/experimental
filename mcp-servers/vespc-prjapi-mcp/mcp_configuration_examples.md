# How to Add Another MCP Server to mcp.json

## Current Configuration

Your current `.cursor/mcp.json` has one MCP server:

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

## How to Add Another MCP Server

### **Method 1: Add a Python-based MCP Server**

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
        },
        "my-new-server": {
            "command": "/usr/bin/python3",
            "args": [
                "/path/to/your/mcp/server.py"
            ]
        }
    }
}
```

### **Method 2: Add a Node.js-based MCP Server**

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
        },
        "filesystem-server": {
            "command": "npx",
            "args": [
                "@modelcontextprotocol/server-filesystem",
                "/path/to/your/files"
            ]
        }
    }
}
```

### **Method 3: Add Multiple Python Servers**

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
        },
        "tools-server": {
            "command": "/Users/hemduttdabral/.local/bin/uv",
            "args": [
              "--directory",
              "/Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp",
              "run",
              "tools.py"
            ]
        },
        "project-api-server": {
            "command": "/Users/hemduttdabral/.local/bin/uv",
            "args": [
              "--directory",
              "/Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp",
              "run",
              "tools_project_api_client_based.py"
            ]
        }
    }
}
```

## Configuration Parameters

### **Required Parameters**
- **`command`**: The executable to run (e.g., `python3`, `node`, `uv`)
- **`args`**: Array of arguments to pass to the command

### **Optional Parameters**
- **`env`**: Environment variables (optional)
```json
"my-server": {
    "command": "python3",
    "args": ["server.py"],
    "env": {
        "API_KEY": "your-api-key",
        "DEBUG": "true"
    }
}
```

## Examples for Your Project

### **Add Your Other MCP Server Files**

Since you have multiple MCP server files, here's how to add them:

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
        },
        "basic-tools": {
            "command": "/Users/hemduttdabral/.local/bin/uv",
            "args": [
              "--directory",
              "/Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp",
              "run",
              "tools.py"
            ]
        },
        "api-client-tools": {
            "command": "/Users/hemduttdabral/.local/bin/uv",
            "args": [
              "--directory",
              "/Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp",
              "run",
              "tools_project_api_client_based.py"
            ]
        }
    }
}
```

### **Add External MCP Servers**

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
        },
        "filesystem": {
            "command": "npx",
            "args": [
                "@modelcontextprotocol/server-filesystem",
                "/Users/hemduttdabral/projects"
            ]
        },
        "github": {
            "command": "npx",
            "args": [
                "@modelcontextprotocol/server-github",
                "--token",
                "your-github-token"
            ]
        }
    }
}
```

## Steps to Add a New Server

1. **Edit the mcp.json file**:
   ```bash
   nano .cursor/mcp.json
   # or
   code .cursor/mcp.json
   ```

2. **Add the new server configuration**:
   ```json
   "new-server-name": {
       "command": "path/to/executable",
       "args": ["arg1", "arg2", "arg3"]
   }
   ```

3. **Save the file**

4. **Restart your IDE/editor** to load the new configuration

## Validation

After adding a server, you can validate it by:

1. **Checking the MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Testing the server**:
   - The server should appear in the MCP inspector
   - Tools from the server should be available

## Troubleshooting

### **Common Issues**
- **Server not starting**: Check the command path and arguments
- **Tools not available**: Ensure the server is properly configured
- **Permission errors**: Make sure the executable has proper permissions

### **Debug Tips**
- Use absolute paths for commands
- Test the command manually first
- Check server logs for errors
- Verify the server implements the MCP protocol correctly

## Best Practices

1. **Use descriptive server names**
2. **Use absolute paths for commands**
3. **Test servers individually before combining**
4. **Keep configurations organized and documented**
5. **Use environment variables for sensitive data** 