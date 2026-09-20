#!/usr/bin/env bash
set -euo pipefail
export MYPYPATH=python/src:.pi/task-ownership
export PYTHONPATH=.pi/task-ownership:python/src
paths=(
  .pi/task-ownership/python_public_import_foundation_model.py
  .pi/task-ownership/generate_python_public_import_foundation.py
  .pi/task-ownership/public_import_foundation/__init__.py
  .pi/task-ownership/public_import_foundation/input_snapshot.py
  .pi/task-ownership/public_import_foundation/source_observation.py
  .pi/task-ownership/public_import_foundation/runtime_observation.py
  .pi/task-ownership/public_import_foundation/architecture_conformance_adapter.py
  .pi/task-ownership/public_import_foundation/foundation_assembly.py
  .pi/task-ownership/public_import_foundation/command.py
)
python/.venv/bin/python -m ruff check "${paths[@]}"
python/.venv/bin/python -m ruff format --check "${paths[@]}"
python/.venv/bin/python -m mypy "${paths[@]}"
json_returns=$(rg -n --glob '*.py' -- '-> .*Json(?:Value|Record)' \
  .pi/task-ownership/public_import_foundation/source_observation.py \
  .pi/task-ownership/public_import_foundation/runtime_observation.py \
  .pi/task-ownership/public_import_foundation/architecture_conformance_adapter.py \
  .pi/task-ownership/public_import_foundation/foundation_assembly.py \
  | grep -v 'foundation_assembly.py:.*def _required' || true)
if [[ -n "$json_returns" ]]; then
  printf '%s\n' "$json_returns" >&2
  echo 'generated-domain callable returns recursive JSON' >&2
  exit 1
fi
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
grep -v '^#' harness/reports/public-import-boundaries/phase3/foundation-selection.tsv > "$scratch/selection.unsorted.tsv"
for path in \
  .pi/task-ownership/public_import_foundation/__init__.py \
  .pi/task-ownership/public_import_foundation/input_snapshot.py \
  .pi/task-ownership/public_import_foundation/source_observation.py \
  .pi/task-ownership/public_import_foundation/runtime_observation.py \
  .pi/task-ownership/public_import_foundation/architecture_conformance_adapter.py \
  .pi/task-ownership/public_import_foundation/foundation_assembly.py \
  .pi/task-ownership/public_import_foundation/command.py
do
  printf 'task_tool\t%s\n' "$path" >> "$scratch/selection.unsorted.tsv"
done
LC_ALL=C sort -u "$scratch/selection.unsorted.tsv" > "$scratch/selection.tsv"
before_manifest=$(shasum -a 256 harness/reports/public-import-boundaries/phase3/foundation-inputs.json | awk '{print $1}')
before_foundation=$(shasum -a 256 harness/reports/public-import-boundaries/phase3/foundation.json | awk '{print $1}')
python/.venv/bin/python .pi/task-ownership/generate_python_public_import_foundation.py prepare \
  --repository-root "$PWD" \
  --selection "$scratch/selection.tsv" \
  --output "$scratch/foundation-inputs.json"
python/.venv/bin/python .pi/task-ownership/generate_python_public_import_foundation.py generate \
  --repository-root "$PWD" \
  --manifest "$scratch/foundation-inputs.json" \
  --accepted-inventory "$PWD/harness/reports/python-architecture-inventory.json" \
  --output "$scratch/foundation.json" \
  --python-executable "$PWD/python/.venv/bin/python"
after_manifest=$(shasum -a 256 harness/reports/public-import-boundaries/phase3/foundation-inputs.json | awk '{print $1}')
after_foundation=$(shasum -a 256 harness/reports/public-import-boundaries/phase3/foundation.json | awk '{print $1}')
test "$before_manifest" = "$after_manifest"
test "$before_foundation" = "$after_foundation"
probe_source=$(cat <<'PY'
from __future__ import annotations

import sys
from pathlib import Path

from python_public_import_foundation_model import (
    ClosedFoundationParser,
    DeepImportCandidate,
    FoundationJsonCodec,
    PackageBindingCandidate,
    PublicImportFoundation,
)


class TypedConstructionDeltaProbe:
    """Validate the exact temporary C2 candidate delta boundary."""

    __slots__ = ()

    def execute(self, maintained_path: Path, candidate_path: Path) -> None:
        parser = ClosedFoundationParser()
        codec = FoundationJsonCodec()
        maintained = parser.execute(codec.decode(maintained_path.read_bytes()))
        candidate = parser.execute(codec.decode(candidate_path.read_bytes()))
        for attribute in (
            "accepted_inventory",
            "predecessor_routes",
            "package_surfaces",
            "zero_route_surfaces",
            "documentation_citations",
            "phase2_lineage_inputs",
            "production_fact_outputs",
            "dependency_graph_views",
            "runtime_environment",
            "runtime_observations",
            "claim_boundaries",
        ):
            if getattr(maintained, attribute) != getattr(candidate, attribute):
                raise SystemExit(f"unexpected C2 candidate delta: {attribute}")
        added_tools = {
            ".pi/task-ownership/public_import_foundation/__init__.py",
            ".pi/task-ownership/public_import_foundation/input_snapshot.py",
            ".pi/task-ownership/public_import_foundation/source_observation.py",
            ".pi/task-ownership/public_import_foundation/runtime_observation.py",
            ".pi/task-ownership/public_import_foundation/architecture_conformance_adapter.py",
            ".pi/task-ownership/public_import_foundation/foundation_assembly.py",
            ".pi/task-ownership/public_import_foundation/command.py",
        }
        allowed_changed = {
            ".pi/task-ownership/generate_python_public_import_foundation.py",
            ".pi/task-ownership/python_public_import_foundation_model.py",
            "harness/intake/python-architecture-review-refactor.md",
            "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.json",
        }
        maintained_inputs = {item.path: item for item in maintained.inputs}
        candidate_inputs = {item.path: item for item in candidate.inputs}
        if set(candidate_inputs) - set(maintained_inputs) != added_tools:
            raise SystemExit("temporary candidate has unexpected added inputs")
        if set(maintained_inputs) - set(candidate_inputs):
            raise SystemExit("temporary candidate removed an input")
        changed = {
            path
            for path in set(maintained_inputs) & set(candidate_inputs)
            if maintained_inputs[path] != candidate_inputs[path]
        }
        if changed != allowed_changed:
            raise SystemExit(f"unexpected changed input identities: {sorted(changed)}")
        old_tool_paths = {
            ".pi/task-ownership/generate_python_public_import_foundation.py"
        }
        new_tool_paths = old_tool_paths | added_tools
        self._require_observation_delta(
            maintained, candidate, old_tool_paths, new_tool_paths
        )
        allowed_authority_paths = {
            "harness/intake/python-architecture-review-refactor.md",
            "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.json",
        }
        old_authority = tuple(
            item
            for item in maintained.authority_citations
            if item.path not in allowed_authority_paths
        )
        new_authority = tuple(
            item
            for item in candidate.authority_citations
            if item.path not in allowed_authority_paths
        )
        if old_authority != new_authority:
            raise SystemExit("authority delta escaped authorized administrative paths")
        self._require_summary_counts(candidate)

    @staticmethod
    def _require_observation_delta(
        maintained: PublicImportFoundation,
        candidate: PublicImportFoundation,
        old_tool_paths: set[str],
        new_tool_paths: set[str],
    ) -> None:
        old_consumers = tuple(
            item
            for item in maintained.consumer_imports
            if item.consumer_path not in old_tool_paths
        )
        new_consumers = tuple(
            item
            for item in candidate.consumer_imports
            if item.consumer_path not in new_tool_paths
        )
        if old_consumers != new_consumers:
            raise SystemExit("consumer delta escaped decomposed task-tool paths")
        old_deep = tuple(
            item
            for item in maintained.deep_imports
            if item.consumer_path not in old_tool_paths
        )
        new_deep = tuple(
            item
            for item in candidate.deep_imports
            if item.consumer_path not in new_tool_paths
        )
        if old_deep != new_deep:
            raise SystemExit("deep-import delta escaped decomposed task-tool paths")
        old_packages = tuple(
            item
            for item in maintained.supplemental_candidates
            if type(item) is PackageBindingCandidate
        )
        new_packages = tuple(
            item
            for item in candidate.supplemental_candidates
            if type(item) is PackageBindingCandidate
        )
        if old_packages != new_packages:
            raise SystemExit("package-binding candidates changed")
        old_deep_candidates = {
            item.candidate_key: item
            for item in maintained.supplemental_candidates
            if type(item) is DeepImportCandidate
        }
        new_deep_candidates = {
            item.candidate_key: item
            for item in candidate.supplemental_candidates
            if type(item) is DeepImportCandidate
        }
        if set(old_deep_candidates) != set(new_deep_candidates):
            raise SystemExit("deep candidate keys changed")
        for key, old in old_deep_candidates.items():
            new = new_deep_candidates[key]
            if (
                old.candidate_kind,
                old.support_status,
                old.imported_module,
                old.imported_name,
            ) != (
                new.candidate_kind,
                new.support_status,
                new.imported_module,
                new.imported_name,
            ):
                raise SystemExit(f"deep candidate meaning changed: {key}")
            if old.consumer_path != new.consumer_path and (
                old.consumer_path not in old_tool_paths
                or new.consumer_path not in new_tool_paths
            ):
                raise SystemExit(f"deep candidate path changed outside tools: {key}")

    @staticmethod
    def _require_summary_counts(candidate: PublicImportFoundation) -> None:
        summary = candidate.summary
        expected = (
            len(candidate.inputs),
            len(candidate.predecessor_routes),
            len(candidate.package_surfaces),
            len(candidate.zero_route_surfaces),
            len(candidate.consumer_imports),
            len(candidate.deep_imports),
            len(candidate.documentation_citations),
            len(candidate.authority_citations),
            len(candidate.phase2_lineage_inputs),
            len(candidate.production_fact_outputs),
            len(candidate.dependency_graph_views),
            len(candidate.supplemental_candidates),
            len(candidate.runtime_observations),
        )
        actual = (
            summary.input_count,
            summary.predecessor_route_count,
            summary.package_surface_count,
            summary.zero_route_surface_count,
            summary.consumer_import_count,
            summary.deep_non_initializer_module_import_count,
            summary.documentation_citation_count,
            summary.authority_citation_count,
            summary.phase2_lineage_input_count,
            summary.production_fact_output_count,
            summary.dependency_graph_view_count,
            summary.supplemental_candidate_count,
            summary.runtime_package_observation_count,
        )
        if actual != expected:
            raise SystemExit("candidate summary is not mechanically derived")


TypedConstructionDeltaProbe().execute(Path(sys.argv[1]), Path(sys.argv[2]))
PY
)
python/.venv/bin/python -m mypy --strict -c "$probe_source"
python/.venv/bin/python -c "$probe_source" \
  harness/reports/public-import-boundaries/phase3/foundation.json \
  "$scratch/foundation.json"
printf 'typed-domain candidate manifest and foundation passed without maintained writes\n'
