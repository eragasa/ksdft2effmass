#!/usr/bin/env python3
"""Validate the H1 contract/checkpoint evidence boundary without implementation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
H1 = ROOT / ".pi/evidence/pi-harness-incubation/H1"
START = "4b279115bf299ee86c74246828762dbe32b1286f"
ALLOWED_DISPOSITIONS = {
    "INCLUDE_IN_H1_PUBLIC_CONTRACT",
    "LOCAL_COMPATIBILITY_ONLY",
    "H3_RESOURCE_ONLY",
    "DEFER",
    "REJECT",
}
H0_CANDIDATES = {
    "ArtifactIdentity",
    "ResourceReference",
    "ResourceManifest",
    "ProjectProfile",
    "SkillDescriptor",
    "ValidationIssue",
    "ValidationResult",
    "OwnershipManifestView",
    "CheckpointRecord",
    "TaskReference",
    "ChainView",
    "ChecksumEntry",
    "ChecksumManifest",
    "DeterministicCommandSpecification",
    "DeterministicCommandResult",
    "DecisionBoundaryResult",
    "LoadProjectProfile",
    "ResolveResource",
    "ValidateResourceManifest",
    "ValidateOwnershipManifest",
    "ValidateCheckpointSet",
    "EvaluateChainState",
    "AuditEvidenceIdentifiers",
    "ValidateChecksumManifest",
    "ValidateSkillResources",
}
REQUIRED = {
    "activation.json",
    "contract-surface.md",
    "interface-decision-matrix.json",
    "field-and-wire-contract.md",
    "issue-code-and-ordering-contract.md",
    "path-and-resource-resolution-contract.md",
    "version-boundaries.md",
    "h3-h2-ownership-plan.json",
    "migration-and-compatibility-plan.md",
    "review-architecture.md",
    "review-public-contract.md",
    "review-evidence-vvuq.md",
    "review-integration.md",
    "validation-results.json",
    "checksums.sha256",
}
PROHIBITED_ROOTS = (
    "python/src/ksdft2effmass/harness/pi",
    "harness/pi",
    "harness/local",
)
PROTECTED_PREFIXES = (
    "python/src/",
    "python/tests/",
    "specification/",
    "fixtures/",
)
PROTECTED_EXACT = {"python/pyproject.toml", "python/uv.lock"}
GENERIC_PRIMARY_KINDS = {"class_owned", "artifact_owned"}


def run(*args: str) -> str:
    return subprocess.run(
        args, cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE
    ).stdout


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target_path = target.split("#", 1)[0]
        if target_path and not (path.parent / target_path).resolve().exists():
            fail(errors, f"broken Markdown link in {path.relative_to(ROOT)}: {target}")


def main() -> int:
    errors: list[str] = []

    missing = sorted(name for name in REQUIRED if not (H1 / name).is_file())
    if missing:
        fail(errors, f"missing required H1 artifacts: {missing}")

    for path in sorted(H1.glob("*.json")):
        try:
            load(path)
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    matrix = load(H1 / "interface-decision-matrix.json")
    assert isinstance(matrix, dict)
    dispositions = matrix.get("dispositions", [])
    names = [item.get("candidate") for item in dispositions]
    if len(names) != len(set(names)):
        fail(errors, "interface candidates are not unique")
    if not H0_CANDIDATES.issubset(set(names)):
        fail(errors, f"missing H0 candidates: {sorted(H0_CANDIDATES - set(names))}")
    for item in dispositions:
        if item.get("disposition") not in ALLOWED_DISPOSITIONS:
            fail(errors, f"invalid disposition: {item}")
        if not item.get("demonstrated_consumers"):
            fail(errors, f"candidate lacks demonstrated consumer: {item.get('candidate')}")
        for field in ("represented_meaning", "owner", "rationale"):
            if not item.get(field):
                fail(errors, f"candidate {item.get('candidate')} lacks {field}")
    for item in matrix.get("explicit_rejections", []):
        if item.get("disposition") != "REJECT" or not item.get("rationale"):
            fail(errors, f"invalid explicit rejection: {item}")

    contract = (H1 / "contract-surface.md").read_text(encoding="utf-8")
    fields = (H1 / "field-and-wire-contract.md").read_text(encoding="utf-8")
    included = {
        item["candidate"]
        for item in dispositions
        if item["disposition"] == "INCLUDE_IN_H1_PUBLIC_CONTRACT"
    }
    for name in sorted(included):
        if name not in contract and name not in fields:
            fail(errors, f"included interface absent from contract/field tables: {name}")
    traces = matrix.get("field_and_argument_consumer_evidence", {})
    for name in included:
        if name not in traces and name not in {
            "SerializeJsonRecord",
            "DeserializeJsonRecord",
            "LoadProjectProfile",
            "ResolveResource",
            "ValidateResourceManifest",
            "ValidateOwnershipManifest",
            "ValidateCheckpointSet",
            "EvaluateChainState",
            "AuditEvidenceIdentifiers",
            "ValidateChecksumManifest",
            "ValidateSkillResources",
        }:
            fail(errors, f"included record/result lacks field consumer trace: {name}")

    for required_phrase in (
        "class_owned",
        "artifact_owned",
        "local Python -> generic Python",
        "generic Python -/-> local Python",
        "H3",
        "H2",
        "H4",
    ):
        if required_phrase not in contract:
            fail(errors, f"contract lacks required phrase: {required_phrase}")
    kinds = set(re.findall(r"`(class_owned|artifact_owned|boundary_owned)`", contract))
    if not GENERIC_PRIMARY_KINDS.issubset(kinds):
        fail(errors, "generic evidence ownership kinds incomplete")
    if "third `boundary_owned` primary" not in contract:
        fail(errors, "legacy boundary_owned exclusion is not explicit")

    plan = load(H1 / "h3-h2-ownership-plan.json")
    assert isinstance(plan, dict)
    if plan.get("sequence") != ["H3", "H2", "H4"]:
        fail(errors, "successor sequence is not H3 -> H2 -> H4")
    tasks = {task["task_id"]: task for task in plan.get("tasks", [])}
    if set(tasks) != {"H3", "H2", "H4"}:
        fail(errors, "ownership plan task set is not exact")
    writer_scopes: list[tuple[str, str]] = []
    for task_id, task in tasks.items():
        for writer in task.get("writer_roles", []):
            if not isinstance(writer, dict) or not writer.get("future_agent_record"):
                fail(errors, f"{task_id} writer is not structured: {writer}")
                continue
            for scope in writer.get("owned_paths", []):
                writer_scopes.append((f"{task_id}:{writer['role']}", scope.rstrip("/")))
    for index, (owner, scope) in enumerate(writer_scopes):
        for other_owner, other_scope in writer_scopes[:index]:
            if scope == other_scope or scope.startswith(other_scope + "/") or other_scope.startswith(scope + "/"):
                fail(errors, f"writer scopes overlap: {owner}:{scope} and {other_owner}:{other_scope}")
    h2_text = json.dumps(tasks["H2"], sort_keys=True)
    if '"local_python_exception": null' not in h2_text or "no python/src/ksdft2effmass/harness/pi/local" not in h2_text:
        fail(errors, "H2 local-Python prohibition missing")

    chain = load(ROOT / ".pi/chains/pi-harness-incubation.chain.json")
    assert isinstance(chain, dict)
    if chain.get("active_task") != "H1":
        fail(errors, "H1 is not the sole active harness task")
    active = [task["id"] for task in chain["task_sequence"] if str(task["status"]).startswith("active")]
    if active != ["H1"]:
        fail(errors, f"active harness tasks are not exactly H1: {active}")
    for task in chain["task_sequence"]:
        if task["id"] in {"H3", "H2", "H4", "H5"} and task["status"] != "blocked":
            fail(errors, f"successor is not blocked: {task}")
    if chain.get("pending_checkpoints") != ["H1-HC01"]:
        fail(errors, "pending checkpoints are not exactly H1-HC01")

    backend = load(ROOT / ".pi/chains/backend-neutral-kohn-sham-qe.chain.json")
    assert isinstance(backend, dict)
    for task in backend["task_sequence"]:
        if task["id"] in {f"P{n}" for n in range(2, 12)} and task["status"] != "blocked":
            fail(errors, f"backend successor is not blocked: {task}")
    if backend.get("production_execution_authorized") is not False:
        fail(errors, "production execution flag is not false")

    checkpoint = load(ROOT / ".pi/checkpoints/H1-HC01-harness-contract.json")
    assert isinstance(checkpoint, dict)
    if checkpoint.get("status") != "pending" or checkpoint.get("checkpoint_id") != "H1-HC01":
        fail(errors, "H1 checkpoint is not pending")

    for root in PROHIBITED_ROOTS:
        if (ROOT / root).exists():
            fail(errors, f"prohibited implementation/resource root exists: {root}")

    changed = set(run("git", "diff", "--name-only", START).splitlines())
    for path in changed:
        if path in PROTECTED_EXACT or path.startswith(PROTECTED_PREFIXES):
            fail(errors, f"protected source/test/spec/fixture/dependency path changed: {path}")
    for protected in (
        ".pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json",
        ".pi/checkpoints/HARNESS-SEQ-HC01-h3-h2-h4-p2-h5-governance.json",
    ):
        if protected in changed:
            fail(errors, f"accepted governance checkpoint changed: {protected}")

    baseline = load(H1 / "unrelated-worktree-baseline.json")
    assert isinstance(baseline, dict)
    for item in baseline["paths"]:
        path = ROOT / item["path"]
        if not path.is_file():
            fail(errors, f"unrelated baseline file disappeared: {item['path']}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            fail(errors, f"unrelated baseline file changed during H1: {item['path']}")

    staged = set(run("git", "diff", "--cached", "--name-only").splitlines())
    unrelated = {item["path"] for item in baseline["paths"]}
    if staged & unrelated:
        fail(errors, f"unrelated paths staged: {sorted(staged & unrelated)}")

    for path in (
        H1 / "contract-surface.md",
        H1 / "field-and-wire-contract.md",
        H1 / "issue-code-and-ordering-contract.md",
        H1 / "path-and-resource-resolution-contract.md",
        H1 / "version-boundaries.md",
        ROOT / "docs/harness/ksdft2effmass.harness.00.md",
        ROOT / "docs/harness/ksdft2effmass.harness.02.md",
    ):
        check_links(path, errors)

    for review in (
        "review-architecture.md",
        "review-public-contract.md",
        "review-evidence-vvuq.md",
        "review-integration.md",
    ):
        text = (H1 / review).read_text(encoding="utf-8")
        if "PASS" not in text:
            fail(errors, f"final review is not PASS: {review}")

    checksum_path = H1 / "checksums.sha256"
    if checksum_path.is_file():
        catalog_paths: set[str] = set()
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if match is None:
                fail(errors, f"invalid checksum line: {line}")
                continue
            expected, relative = match.groups()
            if relative in catalog_paths:
                fail(errors, f"duplicate checksum path: {relative}")
                continue
            catalog_paths.add(relative)
            path = ROOT / relative
            if not path.is_file():
                fail(errors, f"checksum path missing: {relative}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                fail(errors, f"checksum mismatch: {relative}")
        required_catalog = {
            str(path.relative_to(ROOT))
            for path in H1.iterdir()
            if path.is_file() and path.name not in {"checksums.sha256", "validation-results.json"}
        }
        required_catalog.add(".pi/checkpoints/H1-HC01-harness-contract.json")
        if not required_catalog.issubset(catalog_paths):
            fail(errors, f"checksum catalog missing paths: {sorted(required_catalog - catalog_paths)}")

    generated = [
        path
        for path in ROOT.rglob("__pycache__")
        if ".venv" not in path.parts and ".git" not in path.parts
    ]
    if generated:
        fail(errors, f"generated caches remain: {[str(p.relative_to(ROOT)) for p in generated]}")

    print(f"h1_validation_errors={len(errors)}")
    print(f"included_interfaces={len(included)}")
    print(f"candidate_dispositions={len(dispositions)}")
    print("active_task=H1")
    print("unresolved_checkpoints=1")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
