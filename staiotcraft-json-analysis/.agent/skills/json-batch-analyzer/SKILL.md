---
name: json-batch-analyzer
description: Analyzes, validates, and structurally categorizes up to 100 JSON files simultaneously. Trigger this skill when a user provides a directory, a compressed archive, or a list of raw JSON files requiring schema extraction, consistency validation, anomalies detection, or semantic sorting.
compatibility: Python 3.10+, CLI access
allowed-tools: fs_read fs_write execute_bash
---

# JSON Batch Analyzer & Organizer

This skill guides the agent through a high-performance, systematic pipeline to parse, validate, and organize up to 100 JSON files without blowing out the LLM context window.

## Execution Steps

1. **Discovery and Inventory**
   * Scan the target directory for files ending in `.json`.
   * Count total files. If count exceeds 100, truncate the list to the first 100 files and log a warning to the user.
   * Generate an internal manifest array containing `file_name`, `file_path`, and `file_size`.

2. **Batch Script Execution**
   * Instead of reading all JSON contents directly into the LLM context, execute the provided Python script `scripts/process_jsons.py` via CLI.
   * The script performs schema extraction, null-value tracking, and structural hash generation natively.

3. **Analysis & Schema Aggregation**
   * Parse the output metrics from the script execution.
   * Group JSON files matching identical structural hashes into "Schema Buckets".
   * Identify structural anomalies (e.g., missing mandatory keys, data type mismatches across files).

4. **Organization and Physical Sorting**
   * Create an organized output directory structure based on the extracted schemas or user-defined categories.
   * Physically move or copy files into their designated sub-directories.
   * Write a consolidated `summary_report.json` in the root output folder.

## Edge Cases and Guardrails

* **Corrupted/Invalid JSON:** If a file contains invalid JSON, log it in an `errors` object, skip it, and proceed with the remaining batch. Do not halt execution.
* **Empty Files:** Treat 0-byte files as invalid JSON; log and isolate them in a `corrupted/` sub-folder.
* **Massive Structural Divergence:** If all 100 files have unique schemas, abort auto-sorting, output the schema definitions to `references/`, and prompt the user for sorting rules.

## Output Structure Template

When the skill finishes, ensure the output mirrors this pattern:
```text
organized_output/
├── summary_report.json
├── schema_type_a/
│   ├── file001.json
│   └── file002.json
└── corrupted/
    └── broken_file.json