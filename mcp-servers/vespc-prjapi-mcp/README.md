# README

## Usage with Cursor

1. Windows
```
cd C:\projects\experimental\mcp-servers\vespc-prjapi-mcp

# Activate python dev env on windows
.venv\Scripts\activate

# Activate python dev env on Mac

# For mcp-inspector based debugging
npx @modelcontextprotocol/inspector uv run server.py
```

2. run the server using following command

```
uv run tools_httpx_1.py
```

3. 

This MCP server that provides STAIoT Craft Project-API capabilities. 

## Supported Tools
- list_projects
- clone an example project
- delete project
- describe project
- list_models

## Helper commands

1. installing prjapi-api-client library
- first build the prjapi client library
cd experimental\mcp-servers\vespc-prjapi-mcp\prjapi_client\project-api-client\setup.py
```
python setup.py install --user
```


1. running a python script
```
uv run python 1simple_test_get_projects.py
```

2. using mcp inspector
```
npx @modelcontextprotocol/inspector

2. command: 
/Users/hemduttdabral/.local/bin/uv
OR
C:\Users\hem\.local\bin\uv.exe
3. 
arguments: --directory /Users/hemduttdabral/projects/experimental/mcp-servers/vespc-prjapi-mcp run tools.py
OR
arguments: --directory C:\\projects\\experimental\\mcp-servers\\vespc-prjapi-mcp run tools.py