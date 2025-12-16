# Template-Driven Development

## Purpose
Explore and understand available template projects to identify best practices, reference implementations, and learning resources for your development.

## Category
Learning

## Required Tools
- `fetch_template_prjs()`
- `fetch_template_prj_list()`
- `fetch_template_prj_using_name(ai_project_name)`

## Base Prompt

I need to understand template projects to:

1. **Identify best practices** used in reference implementations
2. **See reference implementations** for [YOUR DOMAIN/USE CASE]
3. **Learn available features** and capabilities
4. **Decide which templates to clone** for: **[YOUR SPECIFIC GOAL]**

**Please show me:**
- All available template projects
- Detailed analysis with focus on: **[FOCUS AREA]**
- Best practices exemplified in each template
- Feature inventory and capabilities
- Recommendations for your use case

**Expected Output:**
- Comprehensive list of all templates
- Detailed breakdown of each template's purpose and architecture
- Feature comparison matrix
- Best practices documented in templates
- Learning resources and code patterns
- Personalized recommendations based on your goal

## Parameters (Required)
- **specific_goal** (REQUIRED): What you want to achieve (e.g., "build a production-grade NLP pipeline", "implement real-time predictions")
- **focus_area** (REQUIRED): What aspect to emphasize (e.g., "model architecture", "data pipeline", "deployment", "scalability")

## Optional Parameters
- **include_code_samples**: Show code snippets from templates
- **compare_approaches**: Compare different templates' approaches
- **difficulty_level**: Filter by complexity (basic, intermediate, advanced)

## Common Focus Areas
- Model architecture and design patterns
- Data pipeline and preprocessing
- Deployment and scaling strategies
- Testing and validation approaches
- API design and integration patterns
- Configuration management
- Monitoring and observability
- Performance optimization

## Example Usage

> I need to understand template projects. My specific goal is to build a production-grade machine learning pipeline that can handle real-time predictions at scale. Show me all available template projects with particular focus on:
> - Model architecture patterns
> - Data pipeline design
> - Deployment and scaling strategies
> 
> For each relevant template, explain best practices, show feature capabilities, and recommend which ones would be best to clone and customize for my production use case.

## Tips
- Excellent for learning from proven patterns
- Great resource before starting new projects
- Use to understand architectural best practices
- Identify tools and libraries used across templates
- Learn from optimization techniques
- Discover integration patterns for common tasks
