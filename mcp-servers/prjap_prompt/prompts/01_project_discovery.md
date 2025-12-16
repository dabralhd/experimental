# Project Discovery & Inventory

## Purpose
Understand your current STAIoT Craft project portfolio and compare it with available template projects.

## Category
Discovery

## Required Tools
- `fetch_usr_prjs()`
- `fetch_template_prjs()`

## Base Prompt

Help me understand my current STAIoT Craft projects.

**Steps:**
1. Fetch all my user projects
2. Provide a comprehensive summary including:
   - Total project count
   - Project names and descriptions
   - Version information
   - Key metadata and status
3. Compare with available template projects

**Expected Output:**
- Organized list of all user projects with metadata
- Template projects available for reference
- Analysis comparing user projects with templates
- Recommendations for next steps

## Parameters (Optional)
- **Focus Area**: Specify a particular domain (e.g., "ML models", "NLP projects", "Computer Vision")
- **Include Statistics**: True/False (provides metrics like project age, update frequency)
- **Comparison Focus**: What to emphasize in template comparison (e.g., "deployment status", "model types")

## Example Usage

### Basic Discovery
> Help me discover my STAIoT Craft projects. Fetch all my user projects and available templates, then provide a summary and comparison.

### With Focus Area
> Help me understand my current STAIoT Craft projects. I'm particularly interested in Accelerometer and machine learning projects. Use the MCP tools to fetch my user projects and template projects, then focus the comparison on NLP capabilities and ML frameworks.

### With Statistics
> Give me a detailed portfolio discovery. Fetch my user projects and templates, then provide statistics on project distribution, comparison analysis, and recommendations prioritized by relevance.

### Complete Example
> Use the #mcp.st-aiot-craft-mcp-server-cff49d3d MCP tools to:
> 1. Fetch all my user projects via fetch_usr_prjs()
> 2. Fetch available templates via fetch_template_prjs()
> 3. Create a detailed summary with total counts, names, descriptions, and versions
> 4. Compare my projects with templates, highlighting which templates I'm already using and which could be beneficial
> 5. Provide specific recommendations for optimization
> Focus on data science and ML projects specifically.

## Tips for Success

✅ **Server Running**: Ensure `uv run server_async.py` is running before using  
✅ **Tool Reference**: Use full MCP tool reference (`#mcp.st-aiot-craft-mcp-server-cff49d3d.function_name()`)  
✅ **Start Simple**: Begin with basic discovery before adding parameters  
✅ **Review Results**: Use results to plan next steps (cloning, creation, cleanup)  
✅ **Next Steps**: After discovery, consider using Project Cloning (02), Project Creation (03), or Project Comparison (04)  

## Common Follow-up Actions

After discovery, you might want to:
- **Clone a Template**: Use [02_project_cloning.md](02_project_cloning.md) to create from a template
- **Create New Project**: Use [03_project_creation.md](03_project_creation.md) for custom projects
- **Compare Projects**: Use [04_project_comparison.md](04_project_comparison.md) for deeper analysis
- **Get Details**: Use [05_project_details.md](05_project_details.md) for specific project info

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Tool not found" error | Ensure MCP server is running: `uv run server_async.py` |
| No projects returned | Check API authentication token in `server_async.py` |
| Incomplete results | Try fetching again; API may be temporarily unavailable |
| Need project details | Use `fetch_usr_prj_using_name(project_name)` for deeper info |
