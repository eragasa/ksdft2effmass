#!/usr/bin/env python3
"""Deterministic, non-mutating completion validator for active H2."""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CLASS_NAMES = (
    "ArtifactIdentity",
    "ResourceReference",
    "ResourceManifest",
    "ProjectProfile",
    "SkillDescriptor",
    "OwnershipScope",
    "AgentDescriptorView",
    "EvidenceIdentifierOccurrence",
    "OwnershipManifestView",
    "CheckpointRecord",
    "TaskReference",
    "ChainView",
    "ChecksumEntry",
    "ChecksumManifest",
    "ValidationIssue",
    "ValidationResult",
    "ProjectProfileLoadResult",
    "ResourceResolutionResult",
    "ChainEvaluationResult",
    "EvidenceAuditResult",
    "JsonSerializationResult",
    "JsonDeserializationResult",
    "WireRecordKind",
    "HarnessInternalError",
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
)
ARTIFACT_MODULES = (
    "test__harness_pi_public_api.py",
    "test__harness_pi_h3_resource_contract.py",
    "test__harness_pi_generic_local_dependency_direction.py",
    "test__harness_pi_path_confinement_contract.py",
)
HEADINGS = (
    "Evidence class and represented meaning",
    "Owned contract, oracle, and scope",
    "VVUQ and scientific exclusions",
)
FIELDS = (
    "Evidence ID",
    "Requirement",
    "Method",
    "Oracle",
    "Acceptance",
    "Interpretation",
    "Limitations",
)
SOURCE_FILES = (
    "__init__.py",
    "identity.py",
    "resources.py",
    "profiles.py",
    "validation.py",
    "ownership.py",
    "checkpoints.py",
    "chains.py",
    "checksums.py",
    "evidence.py",
)


def fail(message: str) -> None:
    raise SystemExit(f"H2 completion: FAIL: {message}")


def check_structure(repo: Path, tests: Path) -> tuple[int, int]:
    expected = {f"test__{name}.py" for name in CLASS_NAMES} | set(ARTIFACT_MODULES)
    actual = {p.name for p in tests.glob("test__*.py")}
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        fail(f"test inventory differs: missing={missing}, extra={extra}")
    evidence_ids: list[str] = []
    collected_functions = 0
    for path in sorted(tests.glob("test__*.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        module_doc = ast.get_docstring(tree, clean=False) or ""
        positions = [module_doc.find(heading) for heading in HEADINGS]
        if any(position < 0 for position in positions) or positions != sorted(
            positions
        ):
            fail(f"module headings missing/out of order: {path}")
        if any(module_doc.count(heading) != 1 for heading in HEADINGS):
            fail(f"module heading multiplicity: {path}")
        class_stem = path.stem.removeprefix("test__")
        if class_stem in CLASS_NAMES:
            assignments = [
                node
                for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "SUT" for t in node.targets)
            ]
            if (
                len(assignments) != 1
                or not isinstance(assignments[0].value, ast.Name)
                or assignments[0].value.id != class_stem
            ):
                fail(f"exact SUT assignment absent: {path}")
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("test_"):
                collected_functions += 1
                parts = node.name.split("__")
                if len(parts) != 3 or not parts[0].startswith("test_"):
                    fail(f"nonsemantic test name: {path}:{node.name}")
            doc = ast.get_docstring(node, clean=False) or ""
            if node.name.startswith("test_") or not node.name.startswith("_"):
                positions = [doc.find(field) for field in FIELDS]
                if any(position < 0 for position in positions) or positions != sorted(
                    positions
                ):
                    fail(f"evidence fields missing/out of order: {path}:{node.name}")
                if any(doc.count(field) != 1 for field in FIELDS):
                    fail(f"evidence field multiplicity: {path}:{node.name}")
                start = doc.index("Evidence ID") + len("Evidence ID")
                end = doc.index("Requirement", start)
                eid = doc[start:end].strip()
                if node.name.startswith("test_"):
                    if not eid.startswith("H2-SV-"):
                        fail(f"invalid evidence ID: {path}:{node.name}:{eid}")
                    evidence_ids.append(eid)
    if len(evidence_ids) != len(set(evidence_ids)):
        fail("duplicate H2 evidence identifiers")
    return len(expected), len(evidence_ids)


def check_inputs(repo: Path) -> None:
    handoff = json.loads(
        (
            repo / ".pi/evidence/pi-harness-incubation/H3/h3-to-h2-handoff.json"
        ).read_text()
    )
    for item in handoff["accepted_input_contract"]["inputs"]:
        digest = hashlib.sha256((repo / item["path"]).read_bytes()).hexdigest()
        if digest != item["content_identity"]["digest"]:
            fail(f"accepted H3 input identity changed: {item['path']}")
    source = repo / "python/src/ksdft2effmass/harness/pi"
    if {p.name for p in source.glob("*.py")} != set(SOURCE_FILES):
        fail("H2 production-source inventory differs from accepted ten files")
    if (source / "local").exists():
        fail("generic source contains prohibited local package")
    pyproject = (repo / "python/pyproject.toml").read_text()
    for forbidden in ("requests", "pydantic", "orjson"):
        if forbidden in pyproject:
            fail(f"unexpected dependency text: {forbidden}")


def run(repo: Path, command: list[str], label: str) -> None:
    result = subprocess.run(
        command, cwd=repo, text=True, capture_output=True, check=False
    )
    if result.returncode:
        output = (result.stdout + result.stderr).strip()
        fail(f"{label} returned {result.returncode}\n{output}")
    print(f"H2 completion: PASS: {label}")


def main() -> None:
    repo = Path(__file__).resolve().parents[6]
    tests = repo / "python/tests/software_verification/ksdft2effmass/harness/pi"
    check_inputs(repo)
    module_count, evidence_count = check_structure(repo, tests)
    test_arg = str(tests.relative_to(repo))
    source_arg = "python/src/ksdft2effmass/harness/pi"
    run(
        repo,
        [sys.executable, "harness/pi/validation/validate_h3_resources.py"],
        "accepted H3 resource replay",
    )
    run(
        repo,
        [
            sys.executable,
            ".pi/task-ownership/validate_task_ownership.py",
            "--task",
            "H2",
            "--chain",
            ".pi/chains/pi-harness-incubation.chain.json",
        ],
        "H2 ownership replay",
    )
    run(
        repo,
        [sys.executable, "-m", "pytest", "--collect-only", "-q", test_arg],
        "H2 pytest collection",
    )
    run(
        repo,
        [sys.executable, "-m", "pytest", "-q", test_arg],
        "H2 software verification",
    )
    run(
        repo,
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            source_arg,
            test_arg,
        ],
        "ruff lint",
    )
    run(
        repo,
        [sys.executable, "-m", "ruff", "format", "--check", source_arg, test_arg],
        "ruff format",
    )
    run(
        repo,
        [sys.executable, "-m", "mypy", "--no-incremental", source_arg, test_arg],
        "mypy",
    )
    with tempfile.TemporaryDirectory(prefix="h2-sphinx-") as output:
        run(
            repo,
            [sys.executable, "-m", "sphinx", "-W", "-b", "html", "docs", output],
            "Sphinx warnings-as-errors",
        )
    print(f"H2 completion: PASS: modules={module_count} evidence_ids={evidence_count}")


if __name__ == "__main__":
    main()
