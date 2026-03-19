STAIoT Craft Project API MCP Server
===================================

This MCP server (`staiotcraft_server`) exposes tools and prompt templates for
interacting with the STAIoT Craft (STm Vespucci) Project API. It lets an AI
assistant list, inspect, create, clone, and delete AI projects, as well as
explore example/template projects to understand the capabilities of the
STAIoT Craft online platform.

This server is implemented using `mcp.server.fastmcp.FastMCP` in
`server_async.py`.


Features
--------

- **User project management**
  - `fetch_usr_prjs`: fetch all user projects.
  - `fetch_usr_prj_list`: fetch only the list of project names.
  - `fetch_usr_prj_using_name(ai_project_name)`: fetch details of a single project.
  - `fetch_usr_prj_attr(attr='ai_project_name')`: fetch a specific attribute
    (e.g. `ai_project_id`, `description`, `models`, `deployments`) across all projects.
  - `create_usr_prj(ai_project_name, description, version)`: create a new user project.
  - `clone_usr_prj(ai_project_name, project_name_to_clone)`: clone an existing
    user project.
  - `delete_usr_prj_using_name(ai_project_name)`: delete a user project by name.

- **Template / example project exploration**
  - `fetch_template_prjs`: fetch all template/example projects.
  - `fetch_template_prj_list`: fetch the list of template project names.
  - `fetch_template_prj_using_name(ai_project_name)`: fetch details for a
    specific template project.
  - `clone_template_prj(ai_project_name, project_name_to_clone)`: clone a
    template/example project into the user workspace.

- **High-level prompt templates (for MCP clients)**
  - `explore_staiotcraft_templates()`
    - Guides the model to call `fetch_template_prjs` and explain what the
      available templates reveal about the capabilities and use-cases of the
      STAIoT Craft platform.
  - `delete_projects_with_confirmation()`
    - Guides the model through a safe, one-by-one deletion workflow:
      list projects, ask the user which to delete, get explicit confirmation,
      then call `delete_usr_prj_using_name` only after confirmation.
  - `clone_example_project_with_filtering(application_area, project_description)`
    - Guides the model to use `fetch_template_prjs` to filter templates based
      on the provided application/target area and/or desired description,
      present the best candidates to the user, and (after explicit confirmation)
      call `clone_template_prj` to create a new user project.


File overview
-------------

- `server_async.py`
  - Defines the `FastMCP` server instance `staiotcraft_server`.
  - Configures logging and HTTP helpers (`make_http_request`,
    `invoke_url_with_http_method`).
  - Implements higher-level API helpers:
    - `get_projects`, `get_template_projects`,
      `create_project`, `clone_project`, `delete_project`.
  - Registers all MCP tools and prompt templates via decorators.

- `prompts/*.md`
  - Human-readable prompt designs (project discovery, cloning, comparison,
    details, template exploration, batch operations, audit, etc.). These are
    reference documents for how the MCP prompts are intended to behave.


Running the server
------------------

The MCP server entry point is at the bottom of `server_async.py`:

- It creates `staiotcraft_server = FastMCP('staiotcraft_server')`.
- It starts the server with:

  ```python
  if __name__ == "__main__":
      staiotcraft_server.run(transport="stdio")
  ```

This means the server is intended to be launched by an MCP-compatible client
over stdio (for example, from an IDE or an LLM runner that supports MCP).


Running with `uv`
-----------------

This project is configured to use the `uv` package manager (see `pyproject.toml`).

- **Install dependencies** (from the `vespc_prjapi_agent` directory):

  ```bash
  uv sync
  ```

- **Run the MCP server directly with `uv`**:

  ```bash
  uv run server_async.py
  ```

  This starts the `staiotcraft_server` over stdio, which is what MCP clients expect.


Using with VS Code (MCP)
------------------------

This repo includes a VS Code MCP configuration at `.vscode/mcp.json`:

```json
{
  "servers": {
    "staiotcraft_server": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "server_async.py"
      ]
    }
  },
  "inputs": []
}
```

To use this server in VS Code:

1. Make sure you have `uv` installed and available on your PATH.
2. From the `vespc_prjapi_agent` directory, run:

   ```bash
   uv sync
   ```

3. Open this folder in VS Code.
4. Ensure your VS Code MCP / AI extension is configured to read `.vscode/mcp.json`.
5. The extension should then be able to start the `staiotcraft_server` by invoking:

   ```bash
   uv run server_async.py
   ```

   over stdio, exposing all tools and prompt templates to the AI assistant.


Authentication / configuration
------------------------------

The server currently uses:

- `BASE_URL`: the STAIoT Craft Project API base URL.
- `BEARER_TOKEN`: a bearer token for authenticating HTTP requests.

These are defined near the top of `server_async.py`. For production use you
should externalize these into environment variables or a secure config
mechanism rather than hard-coding them.


How clients should use this MCP server
--------------------------------------

- **Direct tool use**
  - Call tools like `fetch_usr_prjs`, `fetch_template_prjs`,
    `create_usr_prj`, `clone_template_prj`, `delete_usr_prj_using_name`
    directly when you want low-level control over the workspace.

- **Prompt-template driven workflows**
  - Use `explore_staiotcraft_templates` when the user wants a high-level
    overview of what STAIoT Craft can do, grounded in real template projects.
  - Use `delete_projects_with_confirmation` when the user wants help safely
    cleaning up their workspace, ensuring each deletion is explicitly confirmed.
  - Use `clone_example_project_with_filtering` when the user wants to find
    and clone an example project matching a particular application area and/or
    description, with an explicit confirmation step before cloning.


Notes
-----

- All network calls are made asynchronously using `httpx.AsyncClient`.
- Logging is enabled via a dedicated logger (`logger_staiotcraft_server`) to
  help debug API calls and tool behavior.
