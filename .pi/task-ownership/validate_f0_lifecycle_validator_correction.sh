#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.pi/task-ownership:python/src
export MYPYPATH=.pi/task-ownership:python/src
python/.venv/bin/python .pi/task-ownership/validate_python_public_import_foundation.py
scratch=$(mktemp -d "${TMPDIR:-/tmp}/f0-lifecycle-correction.XXXXXX")
trap 'rm -rf "$scratch"' EXIT
git show 8170ccb8b191bfd5c88a8298ee3a81edd318e42d:harness/reports/public-import-boundaries/phase3/foundation.json > "$scratch/c5-foundation.json"
git show 8170ccb8b191bfd5c88a8298ee3a81edd318e42d:harness/task-selection.json > "$scratch/c5-selection.json"
git show 8170ccb8b191bfd5c88a8298ee3a81edd318e42d:tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.aggregate-verification.json > "$scratch/c5-c6-task.json"
probe_source=$(cat <<'PY'
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import TypeAlias

from python_public_import_foundation_model import (
    ClosedFoundationParser,
    FoundationJsonCodec,
)

JsonScalar: TypeAlias = None | bool | int | float | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonRecord: TypeAlias = dict[str, JsonValue]


class LifecycleValidatorCorrectionProbe:
    """Verify the exact C5 lifecycle boundary and correction delta."""

    __slots__ = ()

    def execute(
        self,
        old_foundation_path: Path,
        new_foundation_path: Path,
        old_selection_path: Path,
        old_c6_task_path: Path,
    ) -> None:
        codec = FoundationJsonCodec()
        parser = ClosedFoundationParser()
        old = parser.execute(codec.decode(old_foundation_path.read_bytes()))
        new = parser.execute(codec.decode(new_foundation_path.read_bytes()))
        selection = self._record(codec.decode(old_selection_path.read_bytes()), "selection")
        c6 = self._record(codec.decode(old_c6_task_path.read_bytes()), "C6 task")
        if (
            selection.get("active_task_id") is not None
            or selection.get("explicit_activation_receipt_ids") != []
            or selection.get("automatic_successor_activation") is not False
        ):
            raise SystemExit("accepted C5 selection boundary is not inactive and manual")
        if c6.get("status") != "inactive":
            raise SystemExit("accepted C5 boundary did not retain C6 inactive")
        if hashlib.sha256(old_foundation_path.read_bytes()).hexdigest() != (
            "21ef8af5230d0623fd0dd69abbca0253719d603a03d50d960b1a97468c815e3c"
        ):
            raise SystemExit("accepted C5 foundation identity changed")
        for attribute in (
            "accepted_inventory",
            "predecessor_routes",
            "package_surfaces",
            "zero_route_surfaces",
            "consumer_imports",
            "deep_imports",
            "documentation_citations",
            "authority_citations",
            "phase2_lineage_inputs",
            "production_fact_outputs",
            "dependency_graph_views",
            "runtime_environment",
            "runtime_observations",
            "supplemental_candidates",
            "claim_boundaries",
            "summary",
        ):
            if getattr(old, attribute) != getattr(new, attribute):
                raise SystemExit(f"lifecycle correction changed {attribute}")
        old_inputs = {item.path: item for item in old.inputs}
        new_inputs = {item.path: item for item in new.inputs}
        if set(old_inputs) != set(new_inputs):
            raise SystemExit("lifecycle correction changed selected paths")
        changed = {
            path
            for path in old_inputs
            if old_inputs[path] != new_inputs[path]
        }
        if changed != {
            ".pi/task-ownership/validate_python_public_import_foundation.py"
        }:
            raise SystemExit(
                f"lifecycle correction changed unexpected identities: {sorted(changed)}"
            )
        print("lifecycle-validator correction delta passed")

    @staticmethod
    def _record(value: JsonValue, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise SystemExit(f"{label} must be an object")
        return value


LifecycleValidatorCorrectionProbe().execute(
    Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
)
PY
)
python/.venv/bin/python -m mypy --strict -c "$probe_source"
python/.venv/bin/python -c "$probe_source" \
  "$scratch/c5-foundation.json" \
  harness/reports/public-import-boundaries/phase3/foundation.json \
  "$scratch/c5-selection.json" \
  "$scratch/c5-c6-task.json"
PYTHONPATH=python/src python/.venv/bin/python -m ksdft2effmass.harness.cli harness-projection --repository-root "$PWD" check
PYTHONPATH=python/src python/.venv/bin/python -m ksdft2effmass.harness.cli validate-harness --repository-root "$PWD"
git diff --check
