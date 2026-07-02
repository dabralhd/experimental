import os
import json
import hashlib
import sys

def get_structural_hash(d):
    """Generates a unique signature for a JSON schema structure."""
    if isinstance(d, dict):
        return hashlib.md5(str(sorted([(k, get_structural_hash(v)) for k, v in d.items()])).encode()).hexdigest()
    elif isinstance(d, list):
        if len(d) > 0:
            return f"array_{get_structural_hash(d[0])}"
        return "array_empty"
    return type(d).__name__

def process_batch(directory_path):
    results = {"buckets": {}, "errors": []}
    # Limit to 100 files
    files = [f for f in os.listdir(directory_path) if f.endswith('.json')][:100]
    
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                s_hash = get_structural_hash(data)
                if s_hash not in results["buckets"]:
                    results["buckets"][s_hash] = []
                results["buckets"][s_hash].append(file_path)
        except Exception as e:
            results["errors"].append({"file": file_name, "error": str(e)})
            
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_batch(sys.argv[1])