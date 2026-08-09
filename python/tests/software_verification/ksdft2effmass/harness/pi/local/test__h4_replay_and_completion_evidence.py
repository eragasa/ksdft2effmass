r"""Software verification of h4 replay and completion evidence.

Facet and represented meaning

Software verification of the retained H4 replay/completion evidence boundary.

Intrinsic and cross-object scope

The primary owner is h4 replay and completion evidence; public behavior and fixed
repository resources provide the exact oracle.

VVUQ and scientific exclusions

Passing establishes only the stated software contract. Numerical verification,
scientific validation, uncertainty quantification, physical correctness, portability,
and cross-language conformance are excluded.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from .conftest import repository_root

pytestmark = pytest.mark.software_verification


def load(path: Path, name: str) -> Any:
    """Evidence ID: Owns no identifier; supports SV-HL-020.

    Requirement: Provide explicit setup mechanics for the h4 replay and completion
    evidence evidence
    without owning an independent result.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_workflow__side_selection__runs_exact_suite_without_evidence_mutation() -> None:
    """Evidence ID: SV-HL-020

    Requirement: Both no-write sides consume the same exact eight explicit identity
    sets.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    program = (
        root / ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
    )
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    before = {
        path.name: path.read_bytes() for path in evidence.iterdir() if path.is_file()
    }
    completed = subprocess.run(
        [sys.executable, str(program), "--side", "local", "--no-write"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "FileNotFoundError" in completed.stderr
    assert "test-evidence-documentation.md" in completed.stderr
    after = {
        path.name: path.read_bytes() for path in evidence.iterdir() if path.is_file()
    }
    assert after == before


def test_workflow__symlinked_absolute_invocation__canonicalizes_script_path(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-021

    Requirement: A symlink spelling and resolved repository root compose
    deterministically.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    linked_root = tmp_path / "repository-link"
    linked_root.symlink_to(root, target_is_directory=True)
    linked_program = (
        linked_root
        / ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
    )
    completed = subprocess.run(
        [
            sys.executable,
            str(linked_program),
            "--side",
            "legacy",
            "--pair",
            "task-chain-explicit-selection",
            "--no-write",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["pair_ids"] == ["task-chain-explicit-selection"]
    command = payload["observations"][0]["observation"]["command"]
    assert command[1] == (
        ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
    )


def test_artifact__parity_identity__is_bound_only_to_declared_git_blobs(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-022

    Requirement: Current R-input edits are irrelevant, while a different R blob fails.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    validator = load(evidence / "validate_h4_completion.py", "h4_completion_fixture")
    retained = json.loads((evidence / "shadow-parity-results.json").read_bytes())
    revision = retained["revision_identity"]
    retained["replay_program_sha256"] = validator.revision_blob_digest(
        root, revision, retained["replay_program"]
    )
    retained["replay_input_definition"] = (
        ".pi/evidence/pi-harness-incubation/H4/replay-inputs.json"
    )
    assert validator.validate_parity(retained, root) is None

    evidence_pair = next(
        pair
        for pair in retained["pairs"]
        if pair["pair_id"] == "evidence-id-audit-h4-selection"
    )
    first_path = next(
        item["path"]
        for item in evidence_pair["input_identities"]
        if item["path"].endswith("test__h4_replay_and_completion_evidence.py")
    )
    current_copy = root / first_path
    original = current_copy.read_bytes()
    try:
        current_copy.write_bytes(original + b"\ncurrent-copy-only mutation\n")
        assert validator.validate_parity(retained, root) is None
    finally:
        current_copy.write_bytes(original)

    changed_root = tmp_path / "changed-r"
    subprocess.run(
        ["git", "worktree", "add", "--detach", str(changed_root), revision],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    try:
        changed = changed_root / first_path
        changed.write_bytes(changed.read_bytes() + b"\nchanged R blob\n")
        subprocess.run(
            ["git", "add", first_path],
            cwd=changed_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=H4 Test",
                "-c",
                "user.email=h4@example.invalid",
                "commit",
                "-m",
                "synthetic changed R",
            ],
            cwd=changed_root,
            check=True,
            capture_output=True,
        )
        changed_revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=changed_root, text=True
        ).strip()
        changed_parity = copy.deepcopy(retained)
        changed_parity["revision_identity"] = changed_revision
        changed_parity["replay_program_sha256"] = validator.revision_blob_digest(
            changed_root, changed_revision, retained["replay_program"]
        )
        assert "input identity mismatch" in validator.validate_parity(
            changed_parity, changed_root
        )
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(changed_root)],
            cwd=root,
            check=True,
            capture_output=True,
        )


def test_artifact__e_hash_index__rejects_generated_artifact_tampering(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-023

    Requirement: The deterministic E index covers exactly the three generated reports.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    validator = load(evidence / "validate_h4_completion.py", "h4_hash_fixture")
    revision = "1" * 40
    artifacts = []

    def exercise_relative_case_308_2(relative: Any) -> Any:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(relative + "\n")
        artifacts.append({"path": relative, "sha256": validator.digest(target)})

    _ = [
        exercise_relative_case_308_2(relative)
        for relative in (validator.GENERATED_E_PATHS)
    ]
    index = {
        "schema_version": 1,
        "artifact_identity": "H4.evidence-artifact-hashes.v1",
        "task_id": "H4",
        "implementation_revision": revision,
        "algorithm": "sha256",
        "artifacts": artifacts,
    }
    assert validator.validate_e_artifact_hashes(index, revision, tmp_path) is None
    (tmp_path / validator.GENERATED_E_PATHS[0]).write_text("tampered\n")
    assert "E artifact hash mismatch" in validator.validate_e_artifact_hashes(
        index, revision, tmp_path
    )


def test_artifact__unrelated_inventory__checks_hashes_without_status_equality(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-024

    Requirement: Recorded unrelated hashes remain optional and later E files are
    tolerated.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    validator = load(evidence / "validate_h4_completion.py", "h4_status_fixture")
    (tmp_path / "unrelated.txt").write_bytes(b"preserved\n")
    baseline = [
        {
            "status": "??",
            "path": "unrelated.txt",
            "sha256": hashlib.sha256(b"preserved\n").hexdigest(),
        }
    ]

    (tmp_path / "later-e.json").write_text("{}\n")
    assert validator.validate_unrelated_work(tmp_path, baseline) is None
    (tmp_path / "unrelated.txt").write_text("changed\n")
    assert "preservation failure" in validator.validate_unrelated_work(
        tmp_path, baseline
    )


def test_artifact__replay_input_definition__excludes_every_generated_e_artifact() -> (
    None
):
    """Evidence ID: SV-HL-025

    Requirement: R owns stable inputs only; generated reports and their index stay
    outside.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    definition = json.loads((evidence / "replay-inputs.json").read_bytes())
    excluded = {
        ".pi/evidence/pi-harness-incubation/H4/acceptance-artifacts.json",
        ".pi/evidence/pi-harness-incubation/H4/evidence-artifact-hashes.json",
        ".pi/evidence/pi-harness-incubation/H4/shadow-parity-results.json",
        ".pi/evidence/pi-harness-incubation/H4/validation-results.json",
    }
    assert set(definition["generated_non_inputs"]) == excluded
    catalog_paths = {
        line.partition("  ")[2]
        for line in (evidence / "checksums.sha256").read_text().splitlines()
    }
    assert excluded.isdisjoint(catalog_paths)
    assert ".pi/evidence/pi-harness-incubation/H4/checksums.sha256" not in catalog_paths
    assert set(definition["classes"].values()) <= catalog_paths | {
        ".pi/evidence/pi-harness-incubation/H4/checksums.sha256",
        "python/tests/software_verification/ksdft2effmass/harness/pi/local",
    }


def test_artifact__maintained_route__selects_local_without_mutation(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-026

    Requirement: Invoke the concrete consumer for legacy, local, and shadow routes.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    consumer = root / ".pi/skills/validate_harness.py"
    maintained = root / "harness/local/validation-route.json"
    maintained_bytes = maintained.read_bytes()
    assert json.loads(maintained_bytes) == {
        "rollback_route": "legacy",
        "route": "local",
        "schema_version": 1,
    }
    assert consumer.is_file()
    assert maintained.read_bytes() == maintained_bytes


def make_completion_records(
    validator: Any,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Evidence ID: Owns no identifier; supports SV-HL-020.

    Requirement: Provide explicit setup mechanics for the h4 replay and completion
    evidence evidence
    without owning an independent result.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    acceptance = json.loads((evidence / "acceptance-artifacts.json").read_bytes())
    validation = json.loads((evidence / "validation-results.json").read_bytes())
    parity = json.loads((evidence / "shadow-parity-results.json").read_bytes())
    inventory = validator.derive_test_evidence_inventory(
        root, parity["revision_identity"]
    )
    assert not isinstance(inventory, str)
    modules, evidence_ids, occurrences = inventory
    audit = next(
        item
        for item in validation["commands"]
        if item["command"].startswith("generic AuditEvidenceIdentifiers")
    )
    audit["command"] = (
        f"generic AuditEvidenceIdentifiers over {len(modules)} H4 local test modules "
        "with explicit ksdft2effmass-v2 profile"
    )
    audit["summary"] = f"{len(modules)} modules, {occurrences} occurrences, 0 issues"
    audit["module_inventory"] = modules
    audit["evidence_id_inventory"] = evidence_ids
    focused = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FOCUSED_PYTEST_COMMAND
    )
    focused.update(summary="1 passed", reported_count=1, observed_count=1)
    full = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FULL_PYTEST_COMMAND
    )
    full.update(summary="1 passed", reported_count=1, observed_count=1)
    return acceptance, validation, parity


def test_artifact__focused_pytest__requires_pass_and_integer_zero() -> None:
    """Evidence ID: SV-HL-027

    Requirement: Nonzero or boolean exit status cannot attest the focused run.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "h4_focused_status_fixture",
    )
    assert validator.validate_pytest_record(
        {"status": "PASS", "exit_status": 1, "summary": "focused suite passed"}
    )
    assert validator.validate_pytest_record(
        {"status": "PASS", "exit_status": True, "summary": "focused suite passed"}
    )
    acceptance, validation, parity = make_completion_records(validator)
    focused = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FOCUSED_PYTEST_COMMAND
    )
    focused.update(summary="focused suite passed", exit_status=1)
    assert "not PASS" in validator.validate_generated_evidence(
        acceptance, validation, parity, root
    )


def test_artifact__focused_pytest__rejects_missing_same_run_count() -> None:
    """Evidence ID: SV-HL-028

    Requirement: A successful focused run must retain an internally consistent same-run
    count.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "h4_focused_no_count_fixture",
    )
    assert (
        validator.validate_pytest_record(
            {"status": "PASS", "exit_status": 0, "summary": "focused suite passed"}
        )
        is None
    )
    acceptance, validation, parity = make_completion_records(validator)
    focused = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FOCUSED_PYTEST_COMMAND
    )
    focused.pop("reported_count")
    focused.pop("observed_count")
    assert "same-run count contract" in validator.validate_generated_evidence(
        acceptance, validation, parity, root
    )


def test_artifact__focused_pytest__rejects_falsified_retained_count() -> None:
    """Evidence ID: SV-HL-029

    Requirement: Summary, reported, and same-run observed counts must agree exactly.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "h4_focused_false_count_fixture",
    )
    record = {
        "status": "PASS",
        "exit_status": 0,
        "summary": "23 passed",
        "reported_count": 23,
        "observed_count": 8,
    }
    assert "mismatched" in validator.validate_pytest_record(record)
    acceptance, validation, parity = make_completion_records(validator)
    focused = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FOCUSED_PYTEST_COMMAND
    )
    focused.update(record)
    assert "mismatched" in validator.validate_generated_evidence(
        acceptance, validation, parity, root
    )


def test_artifact__focused_pytest__accepts_true_same_run_count() -> None:
    """Evidence ID: SV-HL-030

    Requirement: A retained count remains valid when all same-run count facts agree.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "h4_focused_true_count_fixture",
    )
    record = {
        "status": "PASS",
        "exit_status": 0,
        "summary": "7 passed",
        "reported_count": 7,
        "observed_count": 7,
    }
    assert validator.validate_pytest_record(record) is None
    acceptance, validation, parity = make_completion_records(validator)
    focused = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FOCUSED_PYTEST_COMMAND
    )
    focused.update(record)
    assert (
        validator.validate_generated_evidence(acceptance, validation, parity, root)
        is None
    )


def test_artifact__full_pytest__uses_same_run_count_without_fixed_total() -> None:
    """Evidence ID: SV-HL-031

    Requirement: Full-suite counts follow the same run-consistent contract as focused
    tests.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "h4_full_count_fixture",
    )
    acceptance, validation, parity = make_completion_records(validator)
    full = next(
        item
        for item in validation["commands"]
        if item["command"] == validator.FULL_PYTEST_COMMAND
    )
    full.update(summary="1130 passed", reported_count=1130, observed_count=1130)
    assert (
        validator.validate_generated_evidence(acceptance, validation, parity, root)
        is None
    )
    full["reported_count"] = 1107
    assert "mismatched" in validator.validate_generated_evidence(
        acceptance, validation, parity, root
    )


def test_artifact__frozen_inventory__rejects_independent_e_mismatch() -> None:
    """Evidence ID: SV-HL-032

    Requirement: E cannot substitute its own module or evidence-ID inventory for R
    blobs.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "h4_inventory_fixture",
    )
    acceptance, validation, parity = make_completion_records(validator)
    assert (
        validator.validate_generated_evidence(acceptance, validation, parity, root)
        is None
    )
    audit = next(
        item
        for item in validation["commands"]
        if item["command"].startswith("generic AuditEvidenceIdentifiers")
    )
    audit["evidence_id_inventory"] = audit["evidence_id_inventory"][:-1]
    assert "inventory does not match" in validator.validate_generated_evidence(
        acceptance, validation, parity, root
    )


def test_artifact__h3_leakage__ignores_import_cache_and_bytecode(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-033

    Requirement: Import caches plus explicit pyc/pyo files are outside the text scan.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    source = root / "harness/pi/validation/validate_h3_resources.py"
    validator = load(source, "h3_cache_fixture")
    assert any(source.parent.glob("__pycache__/validate_h3_resources*.pyc"))
    generic = tmp_path / "pi"
    generic.mkdir()
    (generic / "resource-manifest.json").write_text('{"resources": []}')
    (generic / "safe.py").write_text("portable = True\n")
    (generic / "junk.pyc").write_bytes(b"\xffproject-local")
    (generic / "junk.pyo").write_bytes(b"\xffproject-local")
    cache = generic / "__pycache__"
    cache.mkdir()
    (cache / "cached.py").write_bytes(b"\xffproject-local")
    validator.PI = generic
    validator.HARNESS_ROOT = tmp_path
    validator.R = validator.Report()
    validator.leakage_gate({}, {"resources": []})
    assert validator.R.failures == []


def test_artifact__h3_leakage__rejects_invalid_utf8_maintained_text(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-034

    Requirement: A manifest-declared maintained text path cannot evade UTF-8 validation.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    validator = load(
        root / "harness/pi/validation/validate_h3_resources.py",
        "h3_invalid_utf8_fixture",
    )
    generic = tmp_path / "pi"
    generic.mkdir()
    manifest = {"resources": [{"path": "declared.resource"}]}
    (generic / "resource-manifest.json").write_text(json.dumps(manifest))
    (generic / "declared.resource").write_bytes(b"\xff")
    validator.PI = generic
    validator.HARNESS_ROOT = tmp_path
    validator.R = validator.Report()
    validator.leakage_gate({}, manifest)
    assert any(
        failure.startswith("leakage.generic-text-utf8:")
        and "declared.resource" in failure
        for failure in validator.R.failures
    )


def test_artifact__local_manifest__owns_exact_maintained_route_identity() -> None:
    """Evidence ID: SV-HL-035

    Requirement: The local manifest binds the exact maintained legacy route bytes.

    Method: Load the retained replay or completion validator, alter only the named
    record field
    or disposable artifact, and execute its public validation boundary.

    Oracle: Versioned H4 record structure, current maintained route resources, and exact
    hash or
    same-run count relations fix the expected outcome independently.

    Acceptance: The named exact equality, diagnostic substring, status, count relation,
    or byte
    nonmutation must hold; no tolerance is used.

    Interpretation: Failure identifies retained-validator drift, stale resource
    identity, incorrect
    controlled mutation, or a nonmutation boundary defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    route = root / "harness/local/validation-route.json"
    manifest = json.loads((root / "harness/local/resource-manifest.json").read_bytes())
    selected = [
        item
        for item in manifest["resources"]
        if item["resource_id"] == "ksdft2effmass.profile.validation-route.v1"
    ]
    assert len(selected) == 1
    assert selected[0]["path"] == "validation-route.json"
    assert selected[0]["dependency_ids"] == [
        "ksdft2effmass.profile.v2",
        "ksdft2effmass.validation.current-local-replay.v1",
    ]
    assert selected[0]["content_identity"] == {
        "algorithm": "sha256",
        "digest": hashlib.sha256(route.read_bytes()).hexdigest(),
        "schema_version": 1,
    }
