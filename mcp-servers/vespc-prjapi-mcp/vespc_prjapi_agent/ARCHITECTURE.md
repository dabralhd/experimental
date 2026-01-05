# STAIoT Craft MCP Server Architecture

## System Architecture Diagram

```mermaid
graph TB
    subgraph "MCP Client Layer"
        VSCode[VS Code / Cursor<br/>MCP Client]
        Config[.vscode/mcp.json<br/>Configuration]
    end

    subgraph "MCP Server Layer"
        FastMCP[FastMCP Server<br/>staiotcraft_server<br/>Transport: stdio]
        EntryPoint[server_async.py<br/>Entry Point]
    end

    subgraph "MCP Tools Layer (11 tools)"
        Tool1[fetch_usr_prjs<br/>@time_tool]
        Tool2[fetch_usr_prj_list<br/>@time_tool]
        Tool3[fetch_usr_prj_using_name<br/>@time_tool]
        Tool4[fetch_usr_prj_attr<br/>@time_tool]
        Tool5[create_usr_prj<br/>@time_tool]
        Tool6[clone_usr_prj<br/>@time_tool]
        Tool7[delete_usr_prj_using_name<br/>@time_tool]
        Tool8[fetch_template_prjs<br/>@time_tool]
        Tool9[fetch_template_prj_list<br/>@time_tool]
        Tool10[fetch_template_prj_using_name<br/>@time_tool]
        Tool11[clone_template_prj<br/>@time_tool]
    end

    subgraph "MCP Prompts Layer (3 prompts)"
        Prompt1[explore_staiotcraft_templates<br/>@time_prompt]
        Prompt2[delete_projects_with_confirmation<br/>@time_prompt]
        Prompt3[clone_example_project_with_filtering<br/>@time_prompt]
    end

    subgraph "Business Logic Layer"
        GetProjects[get_projects]
        GetTemplateProjects[get_template_projects]
        CreateProject[create_project]
        CloneProject[clone_project]
        DeleteProject[delete_project]
    end

    subgraph "HTTP Client Layer"
        InvokeURL[invoke_url_with_http_method]
        MakeHTTP[make_http_request<br/>GET/POST/DELETE]
        Headers[get_headers<br/>Bearer Token]
        HTTPX[httpx.AsyncClient]
    end

    subgraph "Configuration & Utilities"
        Endpoints[prjapi_endpoints.py<br/>API Endpoints]
        Logger[setup_logger<br/>logger_staiotcraft_server<br/>DEBUG level]
        TimeDecorator[time_tool<br/>time_prompt<br/>Timing Decorators]
        ConfigVars[BASE_URL<br/>BEARER_TOKEN]
    end

    subgraph "External API"
        STAPI[STAIoT Craft Project API<br/>https://dev.stm-vespucci.com<br/>/svc/project-api/3]
        Endpoint1[/projects<br/>GET/POST/DELETE]
        Endpoint2[/templates/projects<br/>GET]
    end

    subgraph "Logging & Monitoring"
        StreamHandler[StreamHandler<br/>stdout/stderr]
        TimingLogs[Timing Logs<br/>TOOL_TIMING<br/>PROMPT_TIMING<br/>HTTP_TIMING]
    end

    %% Client to Server connections
    VSCode -->|stdio| FastMCP
    Config -->|config| VSCode
    EntryPoint -->|runs| FastMCP

    %% Server to Tools/Prompts
    FastMCP --> Tool1
    FastMCP --> Tool2
    FastMCP --> Tool3
    FastMCP --> Tool4
    FastMCP --> Tool5
    FastMCP --> Tool6
    FastMCP --> Tool7
    FastMCP --> Tool8
    FastMCP --> Tool9
    FastMCP --> Tool10
    FastMCP --> Tool11
    FastMCP --> Prompt1
    FastMCP --> Prompt2
    FastMCP --> Prompt3

    %% Tools to Business Logic
    Tool1 --> GetProjects
    Tool2 --> GetProjects
    Tool3 --> GetProjects
    Tool4 --> GetProjects
    Tool5 --> CreateProject
    Tool6 --> CloneProject
    Tool7 --> DeleteProject
    Tool8 --> GetTemplateProjects
    Tool9 --> GetTemplateProjects
    Tool10 --> GetTemplateProjects
    Tool11 --> CloneProject

    %% Business Logic to HTTP Layer
    GetProjects --> InvokeURL
    GetTemplateProjects --> InvokeURL
    CreateProject --> InvokeURL
    CloneProject --> InvokeURL
    DeleteProject --> InvokeURL

    %% HTTP Layer connections
    InvokeURL --> MakeHTTP
    MakeHTTP --> Headers
    MakeHTTP --> HTTPX
    Headers --> ConfigVars
    Endpoints --> InvokeURL

    %% HTTP to External API
    HTTPX -->|HTTPS| STAPI
    STAPI --> Endpoint1
    STAPI --> Endpoint2

    %% Configuration & Utilities
    ConfigVars --> MakeHTTP
    TimeDecorator --> Tool1
    TimeDecorator --> Tool2
    TimeDecorator --> Prompt1
    Logger --> StreamHandler
    Logger --> TimingLogs
    MakeHTTP --> TimingLogs
    TimeDecorator --> TimingLogs

    %% Styling
    classDef clientLayer fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef serverLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef toolsLayer fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef promptsLayer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef businessLayer fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef httpLayer fill:#e0f2f1,stroke:#004d40,stroke-width:2px
    classDef externalLayer fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef configLayer fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef loggingLayer fill:#fafafa,stroke:#424242,stroke-width:2px

    class VSCode,Config clientLayer
    class FastMCP,EntryPoint serverLayer
    class Tool1,Tool2,Tool3,Tool4,Tool5,Tool6,Tool7,Tool8,Tool9,Tool10,Tool11 toolsLayer
    class Prompt1,Prompt2,Prompt3 promptsLayer
    class GetProjects,GetTemplateProjects,CreateProject,CloneProject,DeleteProject businessLayer
    class InvokeURL,MakeHTTP,Headers,HTTPX httpLayer
    class STAPI,Endpoint1,Endpoint2 externalLayer
    class Endpoints,Logger,TimeDecorator,ConfigVars configLayer
    class StreamHandler,TimingLogs loggingLayer
```

## Component Details

### 1. MCP Client Layer
- **VS Code / Cursor**: MCP-compatible IDE client
- **Configuration**: `.vscode/mcp.json` defines server startup via `uv run server_async.py`

### 2. MCP Server Layer
- **FastMCP Server**: Core MCP server instance (`staiotcraft_server`)
- **Transport**: stdio (standard input/output)
- **Entry Point**: `server_async.py` main execution

### 3. MCP Tools Layer (11 Tools)
All tools are decorated with `@time_tool` for performance monitoring:

**User Project Management:**
- `fetch_usr_prjs`: Fetch all user projects
- `fetch_usr_prj_list`: Fetch project names list
- `fetch_usr_prj_using_name`: Fetch single project by name
- `fetch_usr_prj_attr`: Fetch specific attribute across projects
- `create_usr_prj`: Create new project
- `clone_usr_prj`: Clone existing user project
- `delete_usr_prj_using_name`: Delete project by name

**Template Project Management:**
- `fetch_template_prjs`: Fetch all template projects
- `fetch_template_prj_list`: Fetch template names list
- `fetch_template_prj_using_name`: Fetch single template by name
- `clone_template_prj`: Clone template to user workspace

### 4. MCP Prompts Layer (3 Prompts)
All prompts are decorated with `@time_prompt` for performance monitoring:

- `explore_staiotcraft_templates`: Guide exploration of template capabilities
- `delete_projects_with_confirmation`: Safe deletion workflow with confirmation
- `clone_example_project_with_filtering`: Filtered template cloning workflow

### 5. Business Logic Layer
- `get_projects`: Fetch user projects from API
- `get_template_projects`: Fetch template projects from API
- `create_project`: Create new project via API
- `clone_project`: Clone project (user or template) via API
- `delete_project`: Delete project via API

### 6. HTTP Client Layer
- `invoke_url_with_http_method`: URL construction and request orchestration
- `make_http_request`: Core HTTP request handler (GET/POST/DELETE)
- `get_headers`: Bearer token authentication header construction
- `httpx.AsyncClient`: Async HTTP client for API calls

### 7. Configuration & Utilities
- `prjapi_endpoints.py`: API endpoint definitions
- `setup_logger`: Logger configuration (DEBUG level)
- `time_tool` / `time_prompt`: Timing decorators for performance monitoring
- `BASE_URL`: API base URL configuration
- `BEARER_TOKEN`: Authentication token

### 8. External API
- **STAIoT Craft Project API**: RESTful API at `https://dev.stm-vespucci.com/svc/project-api/3`
- **Endpoints**:
  - `/projects`: User project CRUD operations
  - `/templates/projects`: Template project listing

### 9. Logging & Monitoring
- **StreamHandler**: Logs to stdout/stderr
- **Timing Logs**: Performance metrics for:
  - Tool execution (`[TOOL_TIMING]`)
  - Prompt execution (`[PROMPT_TIMING]`)
  - HTTP requests (`[TIMING]`)

## Data Flow

1. **Client Request**: MCP client (VS Code) sends request via stdio
2. **Server Processing**: FastMCP server receives and routes to appropriate tool/prompt
3. **Tool Execution**: Tool function executes with timing decorator
4. **Business Logic**: Business logic functions prepare API requests
5. **HTTP Request**: HTTP client makes async request to external API
6. **Response Processing**: Response flows back through layers
7. **Logging**: All operations logged with timing information
8. **Client Response**: Final result returned to MCP client

## Key Design Patterns

- **Decorator Pattern**: `@time_tool` and `@time_prompt` for cross-cutting concerns
- **Layered Architecture**: Clear separation between tools, business logic, and HTTP
- **Async/Await**: All HTTP operations use async/await for non-blocking I/O
- **Dependency Injection**: Configuration and endpoints externalized
- **Single Responsibility**: Each layer has distinct responsibilities

## Security Considerations

- Bearer token authentication for all API requests
- Token currently hardcoded (should be externalized for production)
- HTTPS communication with external API
- No sensitive data logged in timing metrics

