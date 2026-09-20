#!/usr/bin/env bash
set -euo pipefail
export MYPYPATH=python/src
python/.venv/bin/python -m ruff check .pi/task-ownership/generate_python_public_import_foundation.py
python/.venv/bin/python -m ruff format --check .pi/task-ownership/generate_python_public_import_foundation.py
python/.venv/bin/python -m mypy .pi/task-ownership/generate_python_public_import_foundation.py
