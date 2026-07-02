import os
import json
import sys

def infer_schema(data):
    """Recursively infers the JSON schema type from python data primitives."""
    if isinstance(data, dict):
        properties = {}
        required = list(data.keys())
        for k, v in data.items():
            properties[k] = infer_schema(v)
        return {"type": "object", "properties": properties, "required": required}
    elif isinstance(data, list):
        if not data:
            return {"type": "array"}
        # Merge types inside array items
        item_schemas = [infer_schema(item) for item in data]
        distinct_schemas = [dict(t) for t in {tuple(d.items()) for d in item_schemas if 'type' in d}]
        if len(distinct_schemas) == 1:
            return {"type": "array", "items": distinct_schemas[0]}
        return {"type": "array", "items": {"anyOf": distinct_schemas}}
    elif isinstance(data, bool):
        return {"type": "boolean"}
    elif isinstance(data, int):
        return {"type": "integer"}
    elif isinstance(data, float):
        return {"type": "number"}
    elif data is None:
        return {"type": "null"}
    else:
        return {"type": "string"}

def merge_schemas(s1, s2):
    """Merges two deduced schema structures together, optimizing requirements."""
    if s1 == s2:
        return s1
    if s1.get("type") != s2.get("type"):
        return {"anyOf": [s1, s2]}
    
    if s1.get("type") == "object":
        p1, p2 = s1.get("properties", {}), s2.get("properties", {})
        merged_props = {}
        all_keys = set(p1.keys()).union(p2.keys())
        
        for k in all_keys:
            if k in p1 and k in p2:
                merged_props[k] = merge_schemas(p1[k], p2[k])
            elif k in p1:
                merged_props[k] = p1[k]
            else:
                merged_props[k] = p2[k]
                
        req1, req2 = set(s1.get("required", [])), set(s2.get("required", []))
        return {
            "type": "object",
            "properties": merged_props,
            "required": sorted(list(req1.intersection(req2)))
        }
    return s1

def main(target_dir):
    files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith('.json')]
    if not files:
        print(json.dumps({"error": "No JSON files detected"}, indent=2))
        return

    base_schema = {"$schema": "https://json-schema.org/draft/2020-12/schema"}
    unified_body = None

    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                content = json.load(f)
                current_schema = infer_schema(content)
                if unified_body is None:
                    unified_body = current_schema
                else:
                    unified_body = merge_schemas(unified_body, current_schema)
        except Exception:
            continue # Soft skip on bad files

    if unified_body:
        base_schema.update(unified_body)
        with open("unified_schema.json", "w") as out:
            json.dump(base_schema, out, indent=2)
        print(json.dumps({"status": "success", "output": "unified_schema.json"}))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])