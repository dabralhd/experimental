# Project Comparison & Analysis

## Purpose
Analyze your projects across multiple dimensions to identify improvement opportunities, consolidation needs, and migration candidates.

## Category
Analysis

## Required Tools
- `fetch_usr_prjs()`
- `fetch_usr_prj_attr(attr)`

## Base Prompt

Compare my projects across these dimensions:

- **Dimension 1:** [METRIC TO COMPARE]
- **Dimension 2:** [METRIC TO COMPARE]
- **Dimension 3:** [METRIC TO COMPARE]

**Then suggest which projects might benefit from:**
1. Consolidation or archiving
2. Updates or refactoring
3. Migration to newer templates
4. Resource optimization

**Expected Output:**
- Comparison matrix of projects by specified dimensions
- Statistical analysis and patterns identified
- Projects grouped by characteristics
- Recommendations for consolidation
- Refactoring suggestions
- Migration roadmap

## Parameters (Required)
- **dimension_1** (REQUIRED): First comparison metric (e.g., "deployment status", "model version", "update frequency")
- **dimension_2** (RECOMMENDED): Second comparison metric
- **dimension_3** (OPTIONAL): Third comparison metric

## Common Dimensions to Compare
- Deployment status (active, inactive, beta)
- Model versions (current vs. outdated)
- Update frequency (recently updated vs. stale)
- Project size/complexity
- Dependencies and integrations
- Usage patterns
- Performance metrics

## Example Usage

> Compare my projects across these dimensions:
> - Deployment status (active, inactive, beta)
> - Last update date (to identify stale projects)
> - Associated model versions (to identify outdated implementations)
> 
> Then suggest which projects might benefit from consolidation or archiving, which need updates or refactoring, and which could migrate to newer templates for better performance.

## Tips
- Helps identify technical debt and redundancy
- Use periodically to maintain portfolio health
- Informs prioritization decisions
- Data-driven basis for cleanup initiatives
