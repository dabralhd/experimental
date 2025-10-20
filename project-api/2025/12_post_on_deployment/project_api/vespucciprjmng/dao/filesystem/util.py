
from os import path
from re import search


def get_project_file_name(project_name: str) -> str:
    return path.join(project_name, "ai_" + project_name + ".json")

def is_project_file(filename: str) -> bool:
    matched = search("^ai_[A-Za-z0-9#@_]+.json$", filename)
    return bool(matched)

def get_project_name_from_filename(filename: str) -> str:
    return filename[3:].replace(".json", "")