#!/usr/bin/env bash
# Reproduce the bounded P0A installation, wheel, documentation, and tooling gates.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
EVIDENCE="$ROOT/.pi/evidence/backend-neutral-cpn-P0A-packaging-configuration"
BASE=$(mktemp -d "${TMPDIR:-/tmp}/ksdft2effmass-p0a-verify.XXXXXX")
export UV_CACHE_DIR="$BASE/uv-cache"
trap 'rm -rf "$BASE"' EXIT
uv venv --python 3.14 "$BASE/evidence-python"
PYTHON="$BASE/evidence-python/bin/python"

# Build from a disposable source copy so setuptools cannot leave build/ or
# egg-info state in the repository.
mkdir -p "$BASE/build-source"
cp "$ROOT/python/pyproject.toml" "$BASE/build-source/"
cp -R "$ROOT/python/src" "$BASE/build-source/"
find "$BASE/build-source" -type d -name __pycache__ -prune -exec rm -rf {} +
find "$BASE/build-source" -type f -name '*.pyc' -delete
uv build --wheel --out-dir "$BASE/project-wheel" "$BASE/build-source"
WHEEL=$(find "$BASE/project-wheel" -maxdepth 1 \
    -name 'ksdft2effmass-*.whl' -print -quit)
test -n "$WHEEL"

cd "$ROOT/python"
env -u VIRTUAL_ENV UV_PROJECT_ENVIRONMENT="$BASE/core" \
    uv sync --locked --no-dev --no-install-project
env -u VIRTUAL_ENV UV_PROJECT_ENVIRONMENT="$BASE/workflow" \
    uv sync --locked --no-dev --no-install-project --extra workflow
env -u VIRTUAL_ENV UV_PROJECT_ENVIRONMENT="$BASE/docs" \
    uv sync --locked --no-dev --no-install-project --extra docs
uv pip install --python "$BASE/core/bin/python" --no-deps "$WHEEL"
uv pip install --python "$BASE/workflow/bin/python" --no-deps "$WHEEL"
uv pip install --python "$BASE/docs/bin/python" --no-deps "$WHEEL"

"$BASE/core/bin/python" - <<'PY'
import importlib.util
import ksdft2effmass

if importlib.util.find_spec("snakes") is not None:
    raise SystemExit("core environment unexpectedly contains snakes")
if importlib.util.find_spec("myst_parser") is not None:
    raise SystemExit("core environment unexpectedly contains myst_parser")
PY
"$BASE/workflow/bin/python" - <<'PY'
import importlib.metadata as metadata
import importlib.util
import ksdft2effmass
import snakes

if metadata.version("SNAKES") != "0.9.33":
    raise SystemExit("unexpected SNAKES version")
if importlib.util.find_spec("myst_parser") is not None:
    raise SystemExit("workflow environment unexpectedly contains myst_parser")
PY
"$BASE/docs/bin/python" - <<'PY'
import importlib.metadata as metadata
import importlib.util
import ksdft2effmass
import myst_parser
import sphinx

if metadata.version("myst-parser") != "5.1.0":
    raise SystemExit("unexpected MyST version")
if metadata.version("Sphinx") != "9.1.0":
    raise SystemExit("unexpected locked Sphinx version")
if importlib.util.find_spec("snakes") is not None:
    raise SystemExit("docs environment unexpectedly contains snakes")
PY

uv venv --python 3.14 "$BASE/wheel-install"
uv pip install --python "$BASE/wheel-install/bin/python" "$WHEEL"
"$BASE/wheel-install/bin/python" - <<'PY'
import importlib.metadata as metadata
import ksdft2effmass

if metadata.version("ksdft2effmass") != "0.1.0.dev0":
    raise SystemExit("unexpected project-wheel version")
PY

cd "$ROOT"
"$PYTHON" "$EVIDENCE/collect_locked_artifacts.py" --lock python/uv.lock \
    --output "$BASE/locked-artifacts.json"
cmp "$BASE/locked-artifacts.json" "$EVIDENCE/locked-artifacts.json"
"$PYTHON" "$EVIDENCE/verify_packaging_configuration.py" --repository . \
    --wheel "$WHEEL" --output "$BASE/verification-result.json"
cmp "$BASE/verification-result.json" "$EVIDENCE/verification-result.json"

# Confirm that optimized Python cannot bypass an intentionally failed gate.
mkdir -p "$BASE/invalid/python" "$BASE/invalid/docs"
cp python/pyproject.toml python/uv.lock "$BASE/invalid/python/"
cp docs/conf.py docs/index.rst "$BASE/invalid/docs/"
cp -R docs/user-guide "$BASE/invalid/docs/"
cp THIRD_PARTY_NOTICES.md "$BASE/invalid/"
"$PYTHON" - "$BASE/invalid/python/pyproject.toml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace("SNAKES>=0.9.33,<0.10", "SNAKES>=0.9,<0.10"))
PY
if "$PYTHON" -O "$EVIDENCE/verify_packaging_configuration.py" \
    --repository "$BASE/invalid" --output "$BASE/invalid-result.json" \
    >"$BASE/invalid.stdout" 2>"$BASE/invalid.stderr"; then
    echo "optimized invalid-input self-test unexpectedly passed" >&2
    exit 1
fi

"$BASE/docs/bin/python" -m sphinx -W --keep-going -b html \
    -d "$BASE/sphinx/doctrees" docs "$BASE/sphinx/html"
uv venv --python 3.14 "$BASE/docs8"
uv pip install --python "$BASE/docs8/bin/python" "${WHEEL}[docs]" 'Sphinx>=8,<9'
"$BASE/docs8/bin/python" -m sphinx -W --keep-going -b html \
    -d "$BASE/sphinx8/doctrees" docs "$BASE/sphinx8/html"

cd "$ROOT/python"
uv lock --check
env -u VIRTUAL_ENV UV_PROJECT_ENVIRONMENT="$BASE/tooling" \
    uv sync --locked --extra dev --no-install-project
uv pip install --python "$BASE/tooling/bin/python" --no-deps "$WHEEL"
"$BASE/tooling/bin/ruff" format --check --no-cache \
    ../docs/conf.py "$EVIDENCE"/*.py
"$BASE/tooling/bin/ruff" check --no-cache ../docs/conf.py "$EVIDENCE"/*.py
"$BASE/tooling/bin/mypy" --cache-dir "$BASE/mypy-cache"
"$BASE/tooling/bin/pytest" -q -p no:cacheprovider

cd "$ROOT"
git diff --check
printf 'P0A reproducible verification: PASS\n'
