#!/usr/bin/env python3
"""Validate H0 inventory evidence and final blocked checkpoint state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[4]
H0 = Path(__file__).resolve().parent
BASE_COMMIT = "d0b253158eac2c57748923f6484a794721e5c97f"
INVENTORY = H0 / "component-inventory.json"
SCHEMA = H0 / "component-inventory.schema.json"
MATRIX = H0 / "capability-matrix.json"
DEPENDENCIES = H0 / "dependency-map.json"
SOURCE_MAP = H0 / "source-of-truth-map.json"
LEAKAGE = H0 / "leakage-audit.json"
CHECKSUMS = H0 / "checksums.sha256"
CHECKPOINT = ROOT / ".pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json"
HARNESS_CHAIN = ROOT / ".pi/chains/pi-harness-incubation.chain.json"
CPN_CHAIN = ROOT / ".pi/chains/backend-neutral-kohn-sham-qe.chain.json"
H0_TASK = ROOT / ".pi/tasks/pi-harness-incubation-H0-inventory.md"
CLASSIFICATIONS = {
    "EXTRACTABLE",
    "SPLIT_GENERIC_AND_LOCAL",
    "KEEP_PROJECT_LOCAL",
    "RETIRE_AS_DUPLICATE",
    "DEFER",
}
AUTHORITIES = {
    "AUTHORITATIVE",
    "DERIVED",
    "ADVISORY",
    "HISTORICAL_EVIDENCE",
    "DUPLICATE",
    "UNRESOLVED",
}
SOURCE_OWNERS = {
    "python/src/ksdft2effmass/harness/pi/",
    "python/src/ksdft2effmass/harness/pi/local/",
    "harness/pi/",
    "harness/local/",
    ".pi/",
    "docs/harness/",
    "existing project-domain source",
    "historical evidence",
}
PROSPECTIVE = {
    "python/src/ksdft2effmass/harness/pi/",
    "python/src/ksdft2effmass/harness/pi/local/",
    "harness/pi/",
    "harness/local/",
}
ALLOWED_CHANGES = {
    ".pi/chains/pi-harness-incubation.chain.json",
    ".pi/tasks/pi-harness-incubation-H0-inventory.md",
    ".pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json",
}
LEAKAGE_TERMS = [
    ("ksdft2effmass", re.compile(r"ksdft2effmass")),
    ("SV-CPN", re.compile(r"SV-CPN")),
    ("P0", re.compile(r"\bP0\b")),
    ("P1", re.compile(r"\bP1\b")),
    ("P2", re.compile(r"\bP2\b")),
    ("QuantumEspresso", re.compile(r"QuantumEspresso|Quantum ESPRESSO", re.I)),
    ("Wannier90", re.compile(r"Wannier90")),
    ("SNAKES", re.compile(r"SNAKES")),
    ("backend-neutral-cpn", re.compile(r"backend-neutral-cpn")),
    (".pi/", re.compile(r"\.pi/")),
    ("docs/", re.compile(r"docs/")),
    ("python/src/", re.compile(r"python/src/")),
    (
        "repository-root discovery",
        re.compile(r"repository-root discovery|repository root|Path\.cwd\(\)|Git root"),
    ),
]


def load(path: Path) -> dict[str, Any]:
    """Load one required JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def fail(message: str) -> None:
    """Raise one deterministic H0 validation failure."""
    raise ValueError(message)


def schema_errors(instance: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Return stable Draft 2020-12 schema errors."""
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        f"{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            validator.iter_errors(instance),
            key=lambda item: (list(item.absolute_path), item.message),
        )
    ]


def git_paths() -> list[str]:
    """Return paths changed from the commit-derived H0 baseline."""
    output = subprocess.check_output(
        ["git", "diff", "--name-only", BASE_COMMIT, "--"], cwd=ROOT, text=True
    )
    return sorted(output.splitlines())


def validate_inventory() -> tuple[dict[str, Any], Counter[str], Counter[str]]:
    """Validate component schema, lexical order, paths, and cardinalities."""
    inventory = load(INVENTORY)
    errors = schema_errors(inventory, load(SCHEMA))
    if errors:
        fail("inventory schema errors: " + "; ".join(errors))
    components = inventory["components"]
    ids = [item["component_id"] for item in components]
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        fail("component IDs must be unique and lexically ordered")
    paths = [item["current_path"] for item in components]
    if len(paths) != len(set(paths)):
        fail("atomic inventory current_path values must be unique")
    if inventory["component_count"] != len(components):
        fail("component_count differs from components")
    for item in components:
        if item["classification"] not in CLASSIFICATIONS:
            fail(f"invalid classification: {item['component_id']}")
        if item["current_authority"] not in AUTHORITIES:
            fail(f"invalid authority: {item['component_id']}")
        path = item["current_path"]
        if path not in PROSPECTIVE and not (ROOT / path).is_file():
            fail(f"inventoried current path is not one file: {path}")
        for field in (
            "inputs",
            "outputs",
            "consumers",
            "direct_dependencies",
            "project_path_dependencies",
            "project_domain_dependencies",
            "control_plane_dependencies",
            "external_dependencies",
            "tests_or_evidence",
            "open_questions",
        ):
            if item[field] != sorted(item[field]):
                fail(f"{item['component_id']}.{field} is not lexically ordered")
    return (
        inventory,
        Counter(item["classification"] for item in components),
        Counter(item["current_authority"] for item in components),
    )


def validate_matrix(inventory: dict[str, Any]) -> None:
    """Require every component exactly once in the capability matrix."""
    matrix = load(MATRIX)
    rows = matrix.get("capabilities")
    if not isinstance(rows, list) or not rows:
        fail("capability matrix must contain rows")
    component_ids = [item["component_id"] for item in inventory["components"]]
    accounted = [component_id for row in rows for component_id in row["component_ids"]]
    if len(accounted) != len(set(accounted)):
        fail("capability matrix accounts for a component more than once")
    if set(accounted) != set(component_ids):
        fail("capability matrix component accounting differs from inventory")
    if matrix.get("accounted_component_count") != len(accounted):
        fail("capability matrix accounted count differs")
    if matrix.get("capability_count") != len(rows):
        fail("capability matrix capability count differs")
    by_id = {item["component_id"]: item for item in inventory["components"]}
    for row in rows:
        expected_paths = [by_id[item]["current_path"] for item in row["component_ids"]]
        if row["current_components"] != expected_paths:
            fail(f"capability matrix path accounting differs: {row['capability']}")
        expected_classifications = sorted(
            {by_id[item]["classification"] for item in row["component_ids"]}
        )
        if row["classification"] != expected_classifications:
            fail(f"capability classification summary differs: {row['capability']}")


def validate_source_map(inventory: dict[str, Any]) -> None:
    """Require one allowed future owner for every named reusable capability."""
    source_map = load(SOURCE_MAP)
    rows = source_map.get("capabilities")
    if not isinstance(rows, list) or not rows:
        fail("source-of-truth map must contain capabilities")
    names = [row["capability"] for row in rows]
    if len(names) != len(set(names)):
        fail("source-of-truth capability names must be unique")
    known = {item["component_id"] for item in inventory["components"]}
    assigned: list[str] = []
    for row in rows:
        if row.get("future_authoritative_owner") not in SOURCE_OWNERS:
            fail(f"invalid future source-of-truth owner: {row['capability']}")
        components = row.get("current_components")
        if not isinstance(components, list) or not components:
            fail(
                "source-of-truth capability lacks current components: "
                f"{row['capability']}"
            )
        if not set(components) <= known:
            fail(
                "source-of-truth map references unknown components: "
                f"{row['capability']}"
            )
        assigned.extend(components)
    if len(assigned) != len(set(assigned)):
        fail("one component is assigned to multiple future capability owners")
    inventory_ids = {item["component_id"] for item in inventory["components"]}
    if set(assigned) != inventory_ids:
        fail("source-of-truth map does not account for every inventory component")


def validate_dependencies(inventory: dict[str, Any]) -> None:
    """Validate dependency nodes, edges, candidates, and prohibited directions."""
    dependency = load(DEPENDENCIES)
    known = {item["component_id"] for item in inventory["components"]}
    node_ids = [node["component_id"] for node in dependency["nodes"]]
    if node_ids != sorted(known):
        fail("dependency node inventory differs from component inventory")
    edge_keys: set[tuple[str, str, str]] = set()
    for edge in dependency["edges"]:
        if edge["from"] not in known or edge["to"] not in known:
            fail(f"dependency edge references unknown component: {edge}")
        key = (edge["from"], edge["to"], edge["kind"])
        if key in edge_keys:
            fail(f"duplicate dependency edge: {key}")
        edge_keys.add(key)
    mapped_direct_dependencies = {
        (edge["from"], edge["to"])
        for edge in dependency["edges"]
    }
    expected_direct_dependencies = {
        (item["component_id"], target)
        for item in inventory["components"]
        for target in item["direct_dependencies"]
    }
    if mapped_direct_dependencies != expected_direct_dependencies:
        fail("dependency map differs from inventory-declared direct dependencies")
    expected_candidates = {
        item["component_id"]
        for item in inventory["components"]
        if item["classification"] in {"EXTRACTABLE", "SPLIT_GENERIC_AND_LOCAL"}
    }
    actual_candidates = {
        item["component_id"]
        for item in dependency["proposed_extraction_candidate_consumers"]
    }
    if actual_candidates != expected_candidates:
        fail("dependency candidate-consumer accounting differs")
    required = {
        ("generic", "local"),
        ("generic", "ksdft2effmass domain"),
        ("generic", "implicit .pi state"),
        ("generic", "repository-relative paths"),
        ("generic skill", "project task identity"),
    }
    actual = {
        (item["from"], item["to"])
        for item in dependency["prohibited_future_directions"]
    }
    if actual != required:
        fail("prohibited dependency-direction inventory differs")


def expected_leakage(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    """Rebuild every reported leakage-screening occurrence."""
    occurrences: list[dict[str, Any]] = []
    for component in inventory["components"]:
        if component["classification"] not in {
            "EXTRACTABLE",
            "SPLIT_GENERIC_AND_LOCAL",
        }:
            continue
        path = ROOT / component["current_path"]
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, 1):
            for term, pattern in LEAKAGE_TERMS:
                if not pattern.search(line):
                    continue
                if term in {
                    "ksdft2effmass",
                    "QuantumEspresso",
                    "Wannier90",
                    "SNAKES",
                }:
                    disposition = "PROJECT_DOMAIN_COUPLING"
                    consequence = (
                        "Keep in local extension or remove from generic candidate."
                    )
                elif term in {"SV-CPN", "P0", "P1", "P2", "backend-neutral-cpn"}:
                    disposition = "PROJECT_TASK_OR_EVIDENCE_IDENTITY"
                    consequence = "Represent only through local profile/runtime state."
                else:
                    disposition = "PROJECT_PATH_OR_DISCOVERY_COUPLING"
                    consequence = (
                        "Replace generic use with explicit caller-supplied "
                        "root/reference; retain local defaults only in adapter."
                    )
                occurrences.append(
                    {
                        "component_id": component["component_id"],
                        "path": component["current_path"],
                        "line": number,
                        "term": term,
                        "text": line.strip()[:240],
                        "semantic_disposition": disposition,
                        "consequence": consequence,
                    }
                )
    return sorted(
        occurrences,
        key=lambda item: (item["component_id"], item["line"], item["term"]),
    )


def _is_utf8_text(path: Path) -> bool:
    """Return whether one candidate file is readable UTF-8 text."""
    try:
        path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return True


def validate_leakage(inventory: dict[str, Any]) -> None:
    """Require complete reproducible leakage screening and semantic disposition."""
    leakage = load(LEAKAGE)
    expected = expected_leakage(inventory)
    expected_scanned = sorted(
        item["component_id"]
        for item in inventory["components"]
        if item["classification"] in {"EXTRACTABLE", "SPLIT_GENERIC_AND_LOCAL"}
        and (ROOT / item["current_path"]).is_file()
        and _is_utf8_text(ROOT / item["current_path"])
    )
    if leakage.get("candidate_files_scanned") != expected_scanned:
        fail("leakage candidate-file accounting differs")
    if leakage.get("occurrences") != expected:
        fail("leakage occurrence inventory differs from current candidates")
    if leakage.get("occurrence_count") != len(expected):
        fail("leakage occurrence count differs")
    if leakage.get("summary", {}).get("approved_generic_to_local_edges") != 0:
        fail("leakage audit must approve no generic-to-local dependency")


def validate_checksums(inventory: dict[str, Any], *, required: bool) -> None:
    """Validate the complete H0 evidence and inspected-input checksum catalog."""
    if not CHECKSUMS.is_file():
        if required:
            fail("required H0 checksum catalog is absent")
        return
    expected_paths = {
        str(path.relative_to(ROOT))
        for path in H0.rglob("*")
        if path.is_file()
        and path != CHECKSUMS
        and "__pycache__" not in path.parts
    }
    expected_paths.update(
        item["current_path"]
        for item in inventory["components"]
        if item["current_path"] not in PROSPECTIVE
    )
    expected_paths.update(
        {
            "AGENTS.md",
            ".pi/chains/pi-harness-incubation.chain.json",
            ".pi/chains/backend-neutral-kohn-sham-qe.chain.json",
            ".pi/tasks/pi-harness-incubation-H0-inventory.md",
            ".pi/tasks/pi-harness-incubation-H1-contract.md",
            ".pi/tasks/backend-neutral-cpn-P2-tools-provenance.md",
            ".pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json",
        }
    )
    observed: dict[str, str] = {}
    checksum_lines = CHECKSUMS.read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(checksum_lines, 1):
        parts = line.split("  ", 1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-f]{64}", parts[0]) is None:
            fail(f"malformed checksum line {number}")
        digest, relative = parts
        if relative in observed:
            fail(f"duplicate checksum path: {relative}")
        observed[relative] = digest
    if list(observed) != sorted(observed):
        fail("checksum paths are not lexically ordered")
    if set(observed) != expected_paths:
        fail("H0 checksum catalog path inventory differs")
    for relative, expected in observed.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"checksummed path is absent: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"checksum differs: {relative}")


def validate_state(require_checkpoint: bool, require_reviews: bool) -> None:
    """Require H0-only active state and optionally the final pending checkpoint."""
    harness = load(HARNESS_CHAIN)
    cpn = load(CPN_CHAIN)
    if harness.get("active_task") != "H0":
        fail("H0 is not the sole active harness task")
    records = {item["id"]: item for item in harness["task_sequence"]}
    if records["H0"]["status"] not in {
        "active_read_only_preflight",
        "active_blocked_at_H0-HC01",
    }:
        fail("H0 status is not active preflight/checkpoint blocked")
    blocked_harness_tasks = ("H1", "H2", "H3", "H4", "H5")
    if any(records[item]["status"] != "blocked" for item in blocked_harness_tasks):
        fail("H1-H5 must remain blocked")
    cpn_tasks = {item["id"]: item for item in cpn["task_sequence"]}
    if any(cpn_tasks[f"P{number}"]["status"] != "blocked" for number in range(2, 12)):
        fail("P2-P11 must remain blocked")
    if cpn_tasks["P2"]["prerequisites"] != [
        "P1:human_accepted",
        "H5:human_accepted",
        "explicit_activation:P2",
    ]:
        fail("P2 prerequisites differ")
    for path in PROSPECTIVE:
        if (ROOT / path).exists():
            fail(f"prohibited implementation/resource path exists: {path}")
    if require_checkpoint:
        checkpoint = load(CHECKPOINT)
        if (
            checkpoint.get("checkpoint_id") != "H0-HC01"
            or checkpoint.get("status") not in {"pending", "blocked"}
        ):
            fail("H0-HC01 is not the sole pending H0 checkpoint")
        if harness.get("pending_checkpoints") != ["H0-HC01"]:
            fail("harness chain pending checkpoint list differs")
        if "blocked at `H0-HC01`" not in H0_TASK.read_text(encoding="utf-8"):
            fail("H0 task does not record checkpoint block")
    if require_reviews:
        verdict_pattern = re.compile(
            r"(?im)^#{0,3}\s*(?:\*\*)?"
            r"(?:result|verdict|checkpoint technical-adequacy verdict)"
            r":\s*(?:\*\*)?(PASS|FAIL)(?:\*\*)?\s*$"
        )
        for name in (
            "review-inventory-completeness.md",
            "review-architecture-classification.md",
            "review-evidence-vvuq.md",
            "review-integration-control-plane.md",
        ):
            path = H0 / name
            if not path.is_file():
                fail(f"required review missing: {name}")
            verdicts = verdict_pattern.findall(path.read_text(encoding="utf-8"))
            if verdicts != ["PASS"]:
                fail(f"required review lacks one unambiguous PASS verdict: {name}")


def validate_nonmutation() -> None:
    """Fail when H0 changed a path outside its evidence/control-plane allowance."""
    concurrent_record = load(H0 / "concurrent-unrelated-worktree.json")
    concurrent_tracked = {
        item["path"]: item["sha256"]
        for item in concurrent_record.get("concurrent_unrelated_tracked_paths", [])
    }
    changed = git_paths()
    unexpected = [
        path
        for path in changed
        if path not in ALLOWED_CHANGES
        and not path.startswith(".pi/evidence/pi-harness-incubation/H0/")
        and path not in concurrent_tracked
    ]
    if unexpected:
        fail(f"H0 changed unauthorized tracked paths: {unexpected}")
    for relative in concurrent_tracked:
        path = ROOT / relative
        if not path.is_file():
            fail(f"recorded concurrent tracked path is absent: {relative}")
    untracked_output = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    )
    untracked = sorted(untracked_output.splitlines())
    concurrent = {
        item["path"]: item["sha256"]
        for item in concurrent_record["concurrent_unrelated_paths"]
    }
    unexpected_untracked = [
        path
        for path in untracked
        if not path.startswith(".pi/evidence/pi-harness-incubation/H0/")
        and path
        != ".pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json"
        and path not in concurrent
    ]
    if unexpected_untracked:
        fail(f"unaccounted untracked paths exist: {unexpected_untracked}")
    for relative in concurrent:
        path = ROOT / relative
        if not path.is_file():
            fail(f"recorded concurrent unrelated path is absent: {relative}")
    staged_output = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True
    )
    staged = set(staged_output.splitlines())
    concurrent_paths = set(concurrent) | set(concurrent_tracked)
    staged_concurrent = sorted(staged & concurrent_paths)
    if staged_concurrent:
        fail(f"concurrent unrelated paths are staged: {staged_concurrent}")
    for generated in ("docs/_build", "python/build", "python/dist"):
        if (ROOT / generated).exists():
            fail(f"generated output remains: {generated}")
    if any(H0.rglob("__pycache__")):
        fail("generated __pycache__ remains under H0 evidence")
    dependency_hashes = {
        "python/pyproject.toml": (
            "5d6318812c7db69b7b1d5d742bbd9be903419a2c5bd702ed90a240a73d661f6c"
        ),
        "python/uv.lock": (
            "186504b6dc24b054c15ef01ed3219c6829f83585a0d7c6a551d79ede37cb7368"
        ),
    }
    for relative, expected in dependency_hashes.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != expected:
            fail(f"dependency file changed: {relative}")


def main() -> int:
    """Run all H0 structural, accounting, state, and nonmutation gates."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-checkpoint", action="store_true")
    parser.add_argument("--require-reviews", action="store_true")
    args = parser.parse_args()
    try:
        inventory, classifications, authorities = validate_inventory()
        validate_matrix(inventory)
        validate_source_map(inventory)
        validate_dependencies(inventory)
        validate_leakage(inventory)
        validate_state(args.require_checkpoint, args.require_reviews)
        validate_nonmutation()
        validate_checksums(
            inventory,
            required=args.require_checkpoint or args.require_reviews,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"H0 validation failed: {error}", file=sys.stderr)
        return 1
    print("h0_inventory_validation=passed")
    print(f"components={inventory['component_count']}")
    print("classifications=" + json.dumps(dict(sorted(classifications.items()))))
    print("authorities=" + json.dumps(dict(sorted(authorities.items()))))
    print(f"checkpoint_required={args.require_checkpoint}")
    print(f"reviews_required={args.require_reviews}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
