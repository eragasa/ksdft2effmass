"""Software verification of the retained H4 replay/completion evidence boundary."""

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
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_workflow__side_selection__runs_exact_suite_without_evidence_mutation() -> None:
    """Both no-write sides consume the same exact eight explicit identity sets."""
    root = repository_root()
    program = (
        root / ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
    )
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    before = {
        path.name: path.read_bytes() for path in evidence.iterdir() if path.is_file()
    }
    results = {}
    for side in ("legacy", "local"):
        completed = subprocess.run(
            [sys.executable, str(program), "--side", side, "--no-write"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        results[side] = json.loads(completed.stdout)
    assert tuple(results["legacy"]["pair_ids"]) == (
        "task-chain-explicit-selection",
        "checkpoint-validator",
        "ownership-validator-h4",
        "ownership-validator-legacy-p1-boundary-owned",
        "evidence-id-audit-h4-selection",
        "accepted-checksum-catalogs",
        "skill-capability-and-explicit-descriptor-selection",
        "h3-resource-validator",
    )
    for left, right in zip(
        results["legacy"]["observations"],
        results["local"]["observations"],
        strict=True,
    ):
        assert left["pair_id"] == right["pair_id"]
        assert left["input_identities"] == right["input_identities"]
        expected_hash = hashlib.sha256(
            (
                json.dumps(
                    left["input_identities"],
                    ensure_ascii=True,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode()
        ).hexdigest()
        assert left["input_set_hash"] == right["input_set_hash"] == expected_hash
        assert set(left["observation"]) == {
            "command",
            "status",
            "exit_status",
            "issue_facts",
            "paths",
            "related_identities",
            "state",
            "inventory",
            "report_identity",
        }
    after = {
        path.name: path.read_bytes() for path in evidence.iterdir() if path.is_file()
    }
    assert after == before


def test_workflow__symlinked_absolute_invocation__canonicalizes_script_path(
    tmp_path: Path,
) -> None:
    """A symlink spelling and resolved repository root compose deterministically."""
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
    """Current R-input edits are irrelevant, while a different R blob fails."""
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
    """The deterministic E index covers exactly the three generated reports."""
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    validator = load(evidence / "validate_h4_completion.py", "h4_hash_fixture")
    revision = "1" * 40
    artifacts = []
    for relative in validator.GENERATED_E_PATHS:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(relative + "\n")
        artifacts.append({"path": relative, "sha256": validator.digest(target)})
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
    """Recorded unrelated hashes remain optional and later E files are tolerated."""
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
    """R owns stable inputs only; generated reports and their index stay outside."""
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


def test_workflow__concrete_consumer__passes_all_explicit_routes(
    tmp_path: Path,
) -> None:
    """Invoke the concrete consumer for legacy, local, and shadow routes."""
    root = repository_root()
    consumer = root / ".pi/skills/validate_harness.py"
    maintained = root / "harness/local/validation-route.json"
    maintained_bytes = maintained.read_bytes()
    assert json.loads(maintained_bytes) == {
        "rollback_route": "legacy",
        "route": "legacy",
        "schema_version": 1,
    }
    for route in ("legacy", "local", "shadow"):
        config = tmp_path / f"{route}.json"
        config.write_text(
            json.dumps(
                {"rollback_route": "legacy", "route": route, "schema_version": 1}
            )
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(consumer),
                "--repository-root",
                str(root),
                "--route-config",
                str(config.resolve()),
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        result = json.loads(completed.stdout)
        assert result["status"] == "PASS"
        assert result["selected_route"] == route
        assert result["rollback_route"] == "legacy"
        assert result["routes"][0]["status"] == "PASS"
    assert maintained.read_bytes() == maintained_bytes


def test_artifact__local_manifest__owns_exact_maintained_route_identity() -> None:
    """The local manifest binds the exact maintained legacy route bytes."""
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
    assert selected[0]["dependency_ids"] == ["ksdft2effmass.profile.v2"]
    assert selected[0]["content_identity"] == {
        "algorithm": "sha256",
        "digest": hashlib.sha256(route.read_bytes()).hexdigest(),
        "schema_version": 1,
    }
