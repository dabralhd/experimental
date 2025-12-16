# STAIoT Craft Project API - MCP Prompt Templates

This directory contains 8 reusable prompt templates for working with your STAIoT Craft Project API MCP server.

## Quick Reference

| # | Template | Category | Purpose | Tools Used |
|---|----------|----------|---------|-----------|
| 1 | [Project Discovery](01_project_discovery.md) | Discovery | Understand your project portfolio | `fetch_usr_prjs()`, `fetch_template_prjs()` |
| 2 | [Project Cloning](02_project_cloning.md) | Creation | Create new project from template | `fetch_template_prj_list()`, `clone_template_prj()` |
| 3 | [Project Creation](03_project_creation.md) | Creation | Create new project from scratch | `create_usr_prj()` |
| 4 | [Project Comparison](04_project_comparison.md) | Analysis | Analyze projects across dimensions | `fetch_usr_prjs()`, `fetch_usr_prj_attr()` |
| 5 | [Project Details](05_project_details.md) | Inspection | Get detailed project information | `fetch_usr_prj_using_name()` |
| 6 | [Batch Operations](06_batch_operations.md) | Management | Manage multiple projects at once | `fetch_usr_prjs()`, `fetch_usr_prj_attr()` |
| 7 | [Template Exploration](07_template_exploration.md) | Learning | Learn from template projects | `fetch_template_prjs()`, `fetch_template_prj_using_name()` |
| 8 | [Project Audit](08_project_audit.md) | Maintenance | Audit and cleanup portfolio | `fetch_usr_prjs()`, `fetch_usr_prj_attr()` |

## How to Use These Templates

### In Cursor/Claude
Copy the base prompt from the template file and customize the parameters in brackets:

```
[Copy from template]
Replace [PARAMETERS] with your actual values
Submit to your AI assistant
```

### With MCP Tools
Each template includes:
- **Purpose** - What the template accomplishes
- **Required Tools** - Which MCP functions are called
- **Base Prompt** - The core prompt to use
- **Parameters** - Customize these fields
- **Example Usage** - Real-world usage example
- **Tips** - Best practices for this template

## Template Categories

### 🔍 Discovery (1)
Start here to understand what you have:
- Project Discovery & Inventory

### ✨ Creation (2)
Build new projects:
- Project Cloning (from templates)
- Project Creation (from scratch)

### 📊 Analysis (1)
Analyze and understand patterns:
- Project Comparison & Analysis

### 🔎 Inspection (1)
Deep dive into specifics:
- Project Details Investigation

### 🛠️ Management (1)
Manage multiple projects:
- Batch Project Operations

### 📚 Learning (1)
Learn from best practices:
- Template-Driven Development

### 🧹 Maintenance (1)
Keep portfolio healthy:
- Project Auditing & Cleanup

## Common Workflows

### Workflow 1: Getting Started
1. Run [Project Discovery](01_project_discovery.md) to see what exists
2. Run [Template Exploration](07_template_exploration.md) to learn patterns
3. Use [Project Cloning](02_project_cloning.md) or [Project Creation](03_project_creation.md) to build

### Workflow 2: Portfolio Management
1. Run [Project Audit](08_project_audit.md) for assessment
2. Run [Project Comparison](04_project_comparison.md) for analysis
3. Run [Batch Operations](06_batch_operations.md) for cleanup

### Workflow 3: Deep Dive
1. Run [Project Details](05_project_details.md) for one project
2. Run [Project Comparison](04_project_comparison.md) against templates
3. Plan updates or migration

## Tips for Success

✅ **Always start with Discovery** - Know your current state before making changes  
✅ **Use Comparison before major changes** - Understand patterns and dependencies  
✅ **Read Examples** - Each template has realistic usage examples  
✅ **Check Parameters** - Know which are required vs. optional  
✅ **Plan Batch Operations** - Use dry-run analysis before deletion  
✅ **Keep Learning** - Regularly explore templates for best practices  
✅ **Audit Periodically** - Run audit quarterly to maintain portfolio health

## Implementation Notes

- All templates work with the FastMCP server running
- Required configuration: Bearer token in `server_async.py`
- Each template can be used independently
- Templates can be chained for complex workflows
- Copy-paste the base prompt and customize parameters

## Need Help?

Each template file includes:
- Detailed parameter explanations
- Common examples
- Optional enhancements
- Best practices and tips

Start with the template that matches your current need, customize the parameters, and submit to your AI assistant along with these tools activated.
