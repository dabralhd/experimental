---
name: json-schema-generator
description: Analyzes a cluster of JSON files, merges their shapes, and infers a single unified, minimal JSON Schema. Trigger this skill when a user provides multiple JSON samples and needs an overarching structural contract or validation schema.
compatibility: Python 3.10+, CLI access
allowed-tools: fs_read fs_write execute_bash
---

# Minimal JSON Schema Generator

This skill automates the extraction and synthesis of structural types from multiple JSON files into a singular, unified JSON schema template.

## Execution Steps

1. **Locate Target JSON Files**
   * Scan the designated input directory for all valid `.json` files.
   * If zero files are found, halt execution and prompt the user for a valid path.

2. **Run Schema Synthesis Engine**
   * Execute the standalone Python script `scripts/generate_schema.py` via CLI, passing the target directory as an argument.
   * The underlying script maps primitive types, resolves structural variations, and unifies optional/required properties across files.

3. **Format and Store Output**
   * Capture the generated JSON schema string output by the script.
   * Save the completed draft to a root file named `unified_schema.json`.
   * Return a concise structural summary map to the user.

## Edge Cases and Guardrails

* **Heterogeneous Arrays:** If an array contains mixed data types across different files (e.g., `[1, "string"]`), fallback to a generic `"anyOf"` array validation schema.
* **Conflicting Object Keys:** If a key is a `string` in file A but an `object` in file B, register the type mismatch as `"anyOf": [{"type": "string"}, {"type": "object"}]`.
* **Missing Keys:** If a property appears in one file but is absent in another, it must not be listed in the schema's `"required"` array property block.

## Schema Output Target Format

The generated `unified_schema.json` file must strictly adhere to this minimal structural pattern:
```json
{
  "$schema": "[https://json-schema.org/draft/2020-12/schema](https://json-schema.org/draft/2020-12/schema)",
  "type": "object",
  "properties": {},
  "required": []
}