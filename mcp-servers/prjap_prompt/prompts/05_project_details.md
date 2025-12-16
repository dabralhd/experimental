# Project Details Investigation

## Purpose
Retrieve comprehensive information about a specific project including configuration, models, deployments, and how it compares to similar templates.

## Category
Inspection

## Required Tools
- `fetch_usr_prj_using_name(ai_project_name)`
- `fetch_template_prj_using_name(ai_project_name)` (for template comparison)

## Base Prompt

Get detailed information about the project **'[PROJECT NAME]'**:

**Retrieve and explain:**
1. Complete project configuration
2. Associated models and their details
3. Deployment status and configurations
4. Recent activities and modifications
5. Comparison with similar template projects
6. Recommendations for optimization

**Expected Output:**
- Full project details and metadata
- Model inventory with versions
- Deployment information
- Activity timeline
- Template comparison analysis
- Optimization recommendations

## Parameters (Required)
- **project_name** (REQUIRED): Name of the specific project to investigate

## Optional Enhancements
- **include_comparison**: Compare with specific template(s)
- **show_history**: Include project modification history
- **highlight_config**: Focus on particular configuration aspects
- **performance_metrics**: Include performance data if available

## Example Usage

> Get detailed information about the project 'sentiment_classifier_v1':
> - Show me its complete configuration
> - List all associated models and their versions
> - Show deployment status and details
> - Provide a timeline of recent activities
> - Compare it with relevant template projects
> - Suggest any optimizations based on current trends

## Tips
- Use before major project changes or updates
- Helps understand project dependencies
- Good for troubleshooting issues
- Useful for documentation and knowledge transfer
- Identifies upgrade opportunities
