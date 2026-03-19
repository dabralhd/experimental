#!/bin/bash
operation='remove_literal_statements'
cp_file_name="${operation}_$1"

echo "Copying $1 to $cp_file_name..."
cp "$1" "$cp_file_name"

echo "Obfuscating $cp_file_name by removing literal statements..."

obfuscated_file_name="obfuscated_$cp_file_name"

echo "Removing existing obfuscated file if it exists..."
rm -rf "$obfuscated_file_name"
# Use python_minifier (with underscore) or pyminify as the module name
poetry run python -m python_minifier --remove-literal-statements --remove-asserts "$cp_file_name" > "$obfuscated_file_name"

echo "Obfuscation complete. The obfuscated file is $obfuscated_file_name"