# Project Cloning Workflow

## Purpose
Create a new project by cloning an existing template project, enabling quick bootstrapping with proven configurations.

## Category
Creation

## Required Tools
- `fetch_template_prj_list()`
- `fetch_template_prj_using_name()` (optional, for exploration)
- `clone_template_prj(ai_project_name, project_name_to_clone)`

## Base Prompt

I want to start a new AI project based on an existing template.

**Steps:**
1. Show me all available template projects
2. Help me understand which template fits my use case: **[YOUR USE CASE]**
3. Clone the selected template with my project name: **[YOUR PROJECT NAME]**
4. Provide next steps for customization

**Expected Output:**
- List of available templates with descriptions
- Recommendation for best-fit template
- Confirmation of successful clone
- Guidance on customization and configuration
- Links to relevant documentation

## Parameters (Required)
- **use_case** (REQUIRED): Description of what you want to build (e.g., "sentiment analysis classifier", "image detection model")
- **project_name** (REQUIRED): Name for your new cloned project
- **template_name** (OPTIONAL): Specific template to clone (if you already know it)

## Example Usage

> I want to start a new AI project based on an existing template. My use case is building a sentiment analysis classifier for customer reviews. Show me all available template projects that might fit this need. Then clone the most suitable template with my project name: "sentiment_classifier_v1". Finally, provide next steps for customizing it to my specific requirements.

## Tips
- Use this when you want to leverage proven project structures
- Much faster than creating from scratch
- Good for learning best practices from example projects
- Templates typically include pre-configured tools and models
