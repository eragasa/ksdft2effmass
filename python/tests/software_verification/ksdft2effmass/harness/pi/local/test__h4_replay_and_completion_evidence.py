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


def test_artifact__completion_gate__rejects_hand_authored_and_accepts_exact_fixture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reject the old summary and accept an exact constructed replay fixture."""
    root = repository_root()
    evidence = root / ".pi/evidence/pi-harness-incubation/H4"
    replay = load(evidence / "replay_selected_validators.py", "h4_replay_fixture")
    validator = load(evidence / "validate_h4_completion.py", "h4_completion_fixture")
    old = json.loads((evidence / "shadow-parity-results.json").read_bytes())
    assert validator.validate_parity(old) is not None

    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    monkeypatch.setattr(replay, "durable_revision", lambda: (revision, []))
    # The active worktree checksum catalog is intentionally stale until the
    # implementation-boundary commit.  For this schema fixture only, force the
    # deterministic command oracle to PASS; hashes and observations remain real.
    original = replay.base_status

    def passing_checksum(pair_id: str, command: list[str]) -> tuple[int, str]:
        if pair_id == "accepted-checksum-catalogs":
            return 0, ""
        return original(pair_id, command)

    monkeypatch.setattr(replay, "base_status", passing_checksum)
    monkeypatch.setattr(
        replay,
        "revision_blob_digest",
        lambda selected_revision, path: replay.sha256((root / path).read_bytes()),
    )
    fixture = replay.retained()
    monkeypatch.setattr(
        replay, "revision_blob_digest", lambda selected_revision, path: "0" * 64
    )
    with pytest.raises(RuntimeError, match="differs from durable revision"):
        replay.retained()
    monkeypatch.setattr(
        validator,
        "revision_blob_digest",
        lambda selected_root, selected_revision, path: validator.digest(
            selected_root / path
        ),
    )
    assert validator.validate_parity(fixture) is None

    wrong_hash = copy.deepcopy(fixture)
    wrong_hash["pairs"][0]["input_set_hash"] = "0" * 64
    assert "input set hash mismatch" in validator.validate_parity(wrong_hash)

    original_blob_digest = validator.revision_blob_digest
    first_path = fixture["pairs"][0]["input_identities"][0]["path"]
    monkeypatch.setattr(
        validator,
        "revision_blob_digest",
        lambda selected_root, selected_revision, path: (
            "0" * 64
            if path == first_path
            else original_blob_digest(selected_root, selected_revision, path)
        ),
    )
    assert "input identity mismatch" in validator.validate_parity(fixture)

    monkeypatch.setattr(
        validator,
        "revision_blob_digest",
        lambda selected_root, selected_revision, path: validator.digest(
            selected_root / path
        ),
    )
    malformed_issue = copy.deepcopy(fixture)
    malformed_issue["pairs"][0]["legacy"]["issue_facts"] = [
        ["CODE", "ERROR", None, None, ["z", "a"]]
    ]
    assert "incomplete normalized observation" in validator.validate_parity(
        malformed_issue
    )
    malformed_state = copy.deepcopy(fixture)
    malformed_state["pairs"][0]["legacy"]["state"] = [["state", [1]]]
    assert "incomplete normalized observation" in validator.validate_parity(
        malformed_state
    )


def test_artifact__unrelated_inventory__rejects_unrecorded_dirty_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No dirty path outside the H4 boundary or exact baseline can escape."""
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

    class Result:
        returncode = 0
        stdout = b"?? unrelated.txt\x00?? escaped.txt\x00"

    monkeypatch.setattr(validator.subprocess, "run", lambda *args, **kwargs: Result())
    assert "dirty paths escape" in validator.validate_unrelated_work(
        tmp_path, baseline, set()
    )
    assert (
        validator.validate_unrelated_work(tmp_path, baseline, {"escaped.txt"}) is None
    )


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
