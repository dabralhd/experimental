# Code obfuscation experiments

## Nuitka

1. using nuitka to create a module

uv run python -m nuitka --module main.py

2. using nuitka to create a standalone executable

uv run python -m nuitka --standalone --onefile main.py

3. to remove output after building binary

uv run python -m nuitka --remove-output main.py

## Reverse Engineering

1. simple experiments
strings <bin_name>
