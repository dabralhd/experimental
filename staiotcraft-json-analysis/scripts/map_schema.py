import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path


def extract_schema_features(value, prefix=""):
	"""Collect structural features from JSON value as path:type tokens."""
	features = set()
	if isinstance(value, dict):
		for key in sorted(value.keys()):
			child = value[key]
			path = f"{prefix}.{key}" if prefix else key
			features.add(f"{path}:dict" if isinstance(child, dict) else f"{path}:{type_name(child)}")
			features |= extract_schema_features(child, path)
	elif isinstance(value, list):
		path = f"{prefix}[]" if prefix else "[]"
		features.add(f"{path}:list")
		if value:
			features |= extract_schema_features(value[0], path)
		else:
			features.add(f"{path}:empty")
	return features


def type_name(value):
	if value is None:
		return "null"
	if isinstance(value, bool):
		return "bool"
	if isinstance(value, int):
		return "int"
	if isinstance(value, float):
		return "float"
	if isinstance(value, str):
		return "str"
	if isinstance(value, list):
		return "list"
	if isinstance(value, dict):
		return "dict"
	return type(value).__name__


def jaccard_distance(a, b):
	if not a and not b:
		return 0.0
	union = len(a | b)
	if union == 0:
		return 0.0
	intersection = len(a & b)
	return 1.0 - (intersection / union)


def read_feature_map(input_dir):
	feature_map = {}
	for file_path in sorted(input_dir.glob("*.json")):
		with file_path.open("r", encoding="utf-8") as f:
			payload = json.load(f)
		feature_map[file_path] = extract_schema_features(payload)
	return feature_map


def agglomerative_merge_to_k(feature_map, target_k):
	"""Merge nearest singleton clusters until exactly target_k remain."""
	clusters = []
	for file_path, feats in feature_map.items():
		clusters.append({"files": [file_path], "features": set(feats)})

	while len(clusters) > target_k:
		best_i = None
		best_j = None
		best_dist = None

		for i in range(len(clusters)):
			for j in range(i + 1, len(clusters)):
				dist = jaccard_distance(clusters[i]["features"], clusters[j]["features"])
				if best_dist is None or dist < best_dist:
					best_dist = dist
					best_i = i
					best_j = j

		left = clusters[best_i]
		right = clusters[best_j]
		merged = {
			"files": left["files"] + right["files"],
			"features": left["features"] | right["features"],
		}

		for idx in sorted([best_i, best_j], reverse=True):
			clusters.pop(idx)
		clusters.append(merged)

	return clusters


def write_grouped_output(clusters, output_dir):
	output_dir.mkdir(parents=True, exist_ok=True)

	# Sort by descending size for deterministic group numbering.
	clusters_sorted = sorted(clusters, key=lambda c: (-len(c["files"]), str(c["files"][0])))
	manifest = []

	for i, cluster in enumerate(clusters_sorted, start=1):
		group_dir = output_dir / f"group_{i}"
		group_dir.mkdir(exist_ok=True)

		sorted_files = sorted(cluster["files"])
		for file_path in sorted_files:
			shutil.copy2(file_path, group_dir / file_path.name)

		manifest.append(
			{
				"group": i,
				"file_count": len(sorted_files),
				"files": [p.name for p in sorted_files],
			}
		)

	with (output_dir / "grouping_manifest.json").open("w", encoding="utf-8") as f:
		json.dump(manifest, f, indent=2)


def main():
	parser = argparse.ArgumentParser(description="Organize JSON files into 4 schema-based groups.")
	parser.add_argument("--input-dir", required=True, help="Folder containing JSON files")
	parser.add_argument("--output-dir", required=True, help="Folder where grouped files are written")
	parser.add_argument("--groups", type=int, default=4, help="Target number of groups")
	args = parser.parse_args()

	input_dir = Path(args.input_dir)
	output_dir = Path(args.output_dir)

	feature_map = read_feature_map(input_dir)
	if len(feature_map) < args.groups:
		raise ValueError(
			f"Requested {args.groups} groups but found only {len(feature_map)} JSON files."
		)

	clusters = agglomerative_merge_to_k(feature_map, args.groups)
	write_grouped_output(clusters, output_dir)

	counts = sorted([len(c["files"]) for c in clusters], reverse=True)
	print(f"Organized {len(feature_map)} files into {args.groups} groups: {counts}")
	print(f"Output written to: {output_dir}")


if __name__ == "__main__":
	main()
