# Project Creation from Scratch

## Purpose
Create a new AI project from scratch with custom specifications and receive guidance on setup and configuration.

## Category
Creation

## Required Tools
- `create_usr_prj(ai_project_name, description, version)`

## Base Prompt

Create a new AI project with these specifications:

- **Project Name:** [YOUR PROJECT NAME]
- **Description:** [YOUR DESCRIPTION]
- **Version:** [VERSION NUMBER, default: 0.0.1]
- **Purpose:** [WHAT YOU'LL USE IT FOR]

**Then provide guidance on:**
1. Project structure and organization
2. Available tools and models you can use
3. Configuration steps and initial setup
4. Best practices for this project type

**Expected Output:**
- Confirmation of project creation with details
- Project structure overview
- Configuration checklist
- Recommended tools and models for your use case
- Quick start guide

## Parameters (Required)
- **project_name** (REQUIRED): Name for your new project (e.g., "my_classification_model")
- **description** (REQUIRED): What this project does (e.g., "Binary classifier for email spam detection")
- **purpose** (REQUIRED): What you'll use it for (e.g., "Production email filtering system")
- **version** (OPTIONAL): Starting version (default: "0.0.1")

## Example Usage

> Create a new AI project with these specifications:
> - Project name: email_spam_detector
> - Description: A machine learning system to identify and classify spam emails
> - Version: 0.0.1
> - Purpose: Deploy as a production email filter for our enterprise platform
> 
> Then provide guidance on project structure, available tools and models I can integrate, configuration steps, and best practices for building a reliable email classifier.

## Tips
- Use when you have a specific, unique project idea
- You'll have complete control over structure and configuration
- Good for experimental or innovative projects
- Requires more setup than cloning templates
