# Project Auditing & Cleanup

## Purpose
Conduct a comprehensive audit of your project portfolio to identify obsolete, redundant, or underutilized projects, and plan cleanup and optimization activities.

## Category
Maintenance

## Required Tools
- `fetch_usr_prjs()`
- `fetch_usr_prj_attr(attr)`
- `delete_usr_prj_using_name()` (optional, for actual deletion after planning)

## Base Prompt

Help me audit my project portfolio:

**Analysis Steps:**
1. List all projects with their complete metadata
2. Identify unused or outdated projects
3. Calculate and present project statistics
4. Recommend projects for deletion or archiving
5. Plan a comprehensive cleanup strategy

**Expected Output:**
- Complete project inventory with metadata
- Classification of projects by status (active, inactive, obsolete)
- Statistical analysis (total count, age distribution, update frequency)
- Risk assessment for each project
- Prioritized cleanup recommendations
- Phased cleanup execution plan
- Rollback considerations and safety measures

## Parameters (Optional)
- **include_metrics**: Include detailed project metrics (size, update frequency, etc.)
- **define_inactive**: Criteria for inactive projects (e.g., "no updates for 6 months")
- **define_obsolete**: Criteria for obsolete projects (e.g., "uses deprecated technology")
- **execution_phase**: Plan execution in phases or all at once

## Audit Dimensions
- **Activity**: Last update date, usage frequency
- **Technology**: Model versions, tool versions, framework versions
- **Redundancy**: Similar projects, duplicate functionality
- **Status**: Production, development, experimental, deprecated
- **Dependencies**: What other systems depend on this project
- **Documentation**: Is the project documented
- **Performance**: Is it meeting its objectives
- **Compliance**: Does it meet current standards

## Example Usage

> Help me audit my project portfolio. List all projects with metadata including: name, version, last update date, status, and description. Identify projects that haven't been updated in 6 months (inactive) and projects using deprecated models or tools (obsolete). Calculate statistics like total project count, average age, and update frequency distribution. Based on your analysis, recommend which projects should be deleted or archived, classify remaining projects by priority, and provide a phased cleanup strategy with safety considerations and rollback options.

## Tips
- Run quarterly or semi-annually for portfolio health
- Always backup/archive before deletion
- Identify and preserve critical dependencies first
- Plan cleanup in phases to minimize risk
- Document decisions for audit trail
- Consider data preservation requirements
- Communicate with stakeholders before cleanup
- Use dry-run analysis first before actual deletion
