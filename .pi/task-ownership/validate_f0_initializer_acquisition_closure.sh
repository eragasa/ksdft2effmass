#!/usr/bin/env bash
set -euo pipefail
export MYPYPATH=python/src:.pi/task-ownership
python/.venv/bin/python -m ruff check .pi/task-ownership/public_import_foundation/source_observation.py
python/.venv/bin/python -m ruff format --check .pi/task-ownership/public_import_foundation/source_observation.py
python/.venv/bin/python -m mypy .pi/task-ownership/public_import_foundation/source_observation.py
