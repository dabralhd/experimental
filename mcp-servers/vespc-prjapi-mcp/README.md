# README

## Usage with Cursor

1. Windows
```
cd C:\projects\experimental\mcp-servers\vespc-prjapi-mcp

# Activate python dev env

when using uv activating python virtual env is not necessary, just run uv run command. However if you still want to activate uv. Use command  '.venv\Scripts\activate'

# Activate python dev env on Mac

# For mcp-inspector based debugging
npx @modelcontextprotocol/inspector uv run server_async.py
```

2. run the server using following command

```
uv run server.py
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

4. ollama serve

5. ngrok setup 
    1. follow instructions at https://ngrok.com/downloads/mac-os

    2. to read ollama port use command (generally ollama port is 11434)
    ```
    ollama serve
    ```

    3. ngrok run <llm-port>
