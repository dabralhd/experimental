# Code obfuscation experiments

## Nuitka

1. using nuitka to create a module

uv run python -m nuitka --module main.py

2. using nuitka to create a standalone executable

uv run python -m nuitka --standalone --onefile main.py

3. to remove output after building binary

- install patchself first, required by option '--standalone' of Nuitka
sudo apt update
sudo apt install patchelf

- run command
uv run python -m nuitka --standalone --onefile --remove-output main.py
uv run python -m nuitka --standalone --onefile --unstripped --remove-output main.py

## docker 

sudo systemctl status docker

sudo systemctl start docker

## Reverse Engineering

1. simple experiments
strings <bin_name>

### Reverse Engineering tools

To unpack pyinstaller generated image use 'pyinstxtractor'

- save docker images as tars
sudo docker save 303868523198.dkr.ecr.eu-west-1.amazonaws.com/project-api:poetryrel-debug-build1 -o my_app.tar

- install undocker
uv add undocker

- undocker -o rootfs my_app.tar

- objdump
objdump -d ./main.bin

- Ghidra SRE
sudo snap install ghidra

- pyminifier
pyminifier is not actively supported 
https://pypi.org/search/?q=pyminifier

- python-minifier
https://pypi.org/project/python-minifier/

uv run python -m python_minifier --in-place --remove-literal-statements --remove-asserts main_1.py

poetry run python -m python_minifier --in-place --remove-literal-statements --remove-asserts secure_logic_cp.py

poetry run python -m nuitka --standalone --onefile --unstripped --remove-output secure_logic.py

1. readelf --symbols obfuscated_remove_literal_statements_secure_logic.bin 

2. strings -n 25 obfuscated_remove_literal_statements_secure_logic.bin 