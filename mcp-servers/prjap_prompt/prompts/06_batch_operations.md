# Batch Project Operations

## Purpose
Manage multiple projects efficiently by identifying, extracting data from, and planning operations on groups of projects matching specific criteria.

## Category
Management

## Required Tools
- `fetch_usr_prjs()`
- `fetch_usr_prj_attr(attr)`
- `delete_usr_prj_using_name()` (optional, if cleanup is needed)

## Base Prompt

Help me manage multiple projects efficiently:

**Steps:**
1. List all my projects
2. Identify projects matching these criteria: **[YOUR CRITERIA]**
3. For each matching project, extract these attributes: **[ATTRIBUTES]**
4. Suggest bulk operations I could perform
5. Help me plan migrations or consolidations

**Expected Output:**
- Filtered list of projects matching criteria
- Extracted attributes in organized format (table or structured list)
- Analysis of patterns in matching projects
- Recommended bulk operations with impact assessment
- Migration/consolidation planning guidance
- Risk assessment for proposed operations

## Parameters (Required)
- **criteria** (REQUIRED): What projects to select (e.g., "inactive for >6 months", "using outdated models", "not in production")
- **attributes** (REQUIRED): What data to extract (e.g., "name, version, status, last_updated")

## Optional Parameters
- **operation_type**: Type of bulk operation to plan (e.g., "cleanup", "migration", "consolidation")
- **dry_run**: True/False (plan without executing)
- **priority**: How to prioritize projects for operations

## Common Criteria Examples
- Inactive for more than X days/months
- Projects with outdated model versions
- Projects not deployed to production
- Projects with similar names or descriptions
- Projects created before a certain date
- Projects without recent updates
- Projects using deprecated tools

## Example Usage

> Help me manage multiple projects. First, list all my projects. Then identify all projects that haven't been updated in the last 6 months. For each matching project, extract: name, last_updated, version, status, and associated models. Finally, suggest bulk operations I could perform (like archiving, consolidating, or migrating) and help me plan the execution safely.

## Tips
- Enables efficient portfolio management
- Good for scheduled maintenance routines
- Use dry_run mode first to assess impact
- Plan migrations carefully with consolidation strategy
- Archive before deletion as safety measure
