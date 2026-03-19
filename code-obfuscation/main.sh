#!/bin/sh
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_PATH=$(dirname "$SCRIPT")

PYTHONHOME=/home/hemduttdabral/projects/experimental/code-obfuscation/.venv
export PYTHONHOME
NUITKA_PYTHONPATH="/home/hemduttdabral/projects/experimental/code-obfuscation:/home/hemduttdabral/.local/share/uv/python/cpython-3.14.3-linux-x86_64-gnu/lib/python3.14:/home/hemduttdabral/.local/share/uv/python/cpython-3.14.3-linux-x86_64-gnu/lib/python3.14/lib-dynload:/home/hemduttdabral/projects/experimental/code-obfuscation/.venv/lib/python3.14/site-packages"
export NUITKA_PYTHONPATH
PYTHONPATH="/home/hemduttdabral/projects/experimental/code-obfuscation:/home/hemduttdabral/.local/share/uv/python/cpython-3.14.3-linux-x86_64-gnu/lib/python3.14:/home/hemduttdabral/.local/share/uv/python/cpython-3.14.3-linux-x86_64-gnu/lib/python3.14/lib-dynload:/home/hemduttdabral/projects/experimental/code-obfuscation/.venv/lib/python3.14/site-packages"
export PYTHONPATH

"$SCRIPT_PATH/main.bin" $@

