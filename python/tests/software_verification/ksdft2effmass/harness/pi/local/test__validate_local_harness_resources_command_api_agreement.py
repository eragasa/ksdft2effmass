r"""Software verification of validate local harness resources command API agreement.

Facet and represented meaning

Software verification of one explicit-input command over current harness resources.

Intrinsic and cross-object scope

The artifact owner is the command boundary joining maintained context loading and
resource resolution Actions without repository discovery.

VVUQ and scientific exclusions

Passing establishes only the declared software interface. It does not establish general
harness correctness, numerical verification, scientific validation, or UQ.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from .conftest import repository_root

pytestmark = pytest.mark.software_verification


def command(root: Path, script_root: Path | None = None) -> list[str]:
    """Evidence ID: Owns no identifier; supports SV-HL-046 through SV-HL-049.

    Requirement: Provide explicit command arguments without owning an independent claim.

    Method: Construct absolute selected repository, resource, profile, and manifest
    paths.

    Oracle: The command contract fixes the six required explicit path inputs.

    Acceptance: The returned argument list names every required input exactly once.

    Interpretation: Failure identifies test setup drift.

    Limitations: This helper does not execute validation or establish a result.
    """
    return [
        sys.executable,
        str(
            (script_root or root)
            / "harness/local/validation/validate_local_harness_resources.py"
        ),
        "--repository-root",
        str(root),
        "--generic-resource-root",
        str(root / "harness/pi"),
        "--local-resource-root",
        str(root / "harness/local"),
        "--profile",
        str(root / "harness/local/profiles/ksdft2effmass-v2.json"),
        "--generic-manifest",
        str(root / "harness/pi/resource-manifest.json"),
        "--local-manifest",
        str(root / "harness/local/resource-manifest.json"),
    ]


def test_artifact__command__validates_explicit_current_resources() -> None:
    """Evidence ID: SV-HL-046

    Requirement: The command validates the explicitly selected current resource closure.

    Method: Invoke it with six absolute repository/resource/profile/manifest paths.

    Oracle: The selected manifests independently declare every resource ID and digest.

    Acceptance: Exit status is zero; structured status is PASS; resource IDs are sorted,
    unique, and all nested statuses are PASS.

    Interpretation: Failure identifies command, Action composition, manifest, or
    resource drift.

    Limitations: This does not authorize resources or establish semantic or scientific
    correctness.
    """
    root = repository_root()
    completed = subprocess.run(
        command(root), capture_output=True, text=True, check=False
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["status"] == "PASS"
    assert payload["stage"] == "resources"
    identifiers = [item["resource_id"] for item in payload["resources"]]
    assert identifiers == sorted(set(identifiers))
    assert all(item["status"] == "PASS" for item in payload["resources"])


@pytest.mark.parametrize(
    "defect",
    [
        pytest.param("relative_root", id="relative_root"),
        pytest.param("parent_traversal", id="parent_traversal"),
        pytest.param("symlinked_ancestor", id="symlinked_ancestor"),
    ],
)
def test_artifact__command__distinguishes_invalid_explicit_input(
    tmp_path: Path, defect: str
) -> None:
    """Evidence ID: SV-HL-047

    Requirement: Invalid or filesystem-escaping command inputs are distinct from
    validation and internal failure.

    Method: Supply a relative root, a parent-traversing profile path, or a profile path
    below a symlinked ancestor while keeping every argument explicit.

    Oracle: Explicit roots and selected files must be absolute, resolved, nonsymlinked,
    and filesystem-contained before any resource Action runs.

    Acceptance: Every case exits two with `INVALID_INPUT`, input stage, no resources,
    and a diagnostic identifying the rejected root or selected path.

    Interpretation: Failure identifies ambient-root acceptance, filesystem escape, or
    exit/status drift.

    Limitations: The cases cover root spelling, parent traversal, and symlinked
    ancestry; resource-level confinement remains independently owned by
    `ResourceResolver`.
    """
    source = repository_root()
    if defect == "relative_root":
        args = command(source)
        args[args.index("--repository-root") + 1] = "."
        expected = "repository root must be an absolute path"
    else:
        root = tmp_path / "repository"
        generic = root / "harness/pi"
        local = root / "harness/local"
        generic.mkdir(parents=True)
        local.mkdir(parents=True)
        (generic / "profile.json").write_text("{}", encoding="utf-8")
        args = command(root, source)
        profile_index = args.index("--profile") + 1
        if defect == "parent_traversal":
            args[profile_index] = str(local / ".." / "pi" / "profile.json")
            expected = "profile path must not contain parent traversal"
        else:
            (local / "linked").symlink_to(generic, target_is_directory=True)
            args[profile_index] = str(local / "linked" / "profile.json")
            expected = "profile path must resolve below its explicit resource root"
    completed = subprocess.run(args, capture_output=True, text=True, check=False)
    payload = json.loads(completed.stdout)
    assert completed.returncode == 2
    assert payload["status"] == "INVALID_INPUT"
    assert payload["stage"] == "input"
    assert payload["resources"] == []
    assert payload["error"] == expected


def test_artifact__command__propagates_nested_resource_failure(tmp_path: Path) -> None:
    """Evidence ID: SV-HL-048

    Requirement: A nested selected-resource failure makes the aggregate fail without
    suppressing its diagnostic.

    Method: Copy the two explicit resource roots, alter one declared generic resource,
    and invoke the command against those copies.

    Oracle: The copied manifest retains the original SHA-256 while the selected bytes
    differ.

    Acceptance: Exit status is one, aggregate status is FAIL, and exactly the altered
    resource reports `PIH.ARTIFACT.HASH_MISMATCH`.

    Interpretation: Failure identifies missing nested-failure propagation or hash
    selection drift.

    Limitations: The copy is synthetic software-verification input, not provenance data.
    """
    source = repository_root()
    root = tmp_path / "repository"
    shutil.copytree(source / "harness/pi", root / "harness/pi")
    shutil.copytree(source / "harness/local", root / "harness/local")
    target = root / "harness/pi/schemas/records/common.schema.json"
    target.write_bytes(target.read_bytes() + b"\n")
    completed = subprocess.run(
        command(root), capture_output=True, text=True, check=False
    )
    assert completed.returncode == 1
    payload = json.loads(completed.stdout)
    assert payload["status"] == "FAIL"
    failed = [item for item in payload["resources"] if item["status"] == "FAIL"]
    assert len(failed) == 1
    assert [issue["code"] for issue in failed[0]["issues"]] == [
        "PIH.ARTIFACT.HASH_MISMATCH"
    ]


def test_artifact__command__distinguishes_unexpected_internal_failure(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID: SV-HL-049

    Requirement: Unexpected Action-boundary failures are not rendered as invalid input
    or ordinary validation failure.

    Method: Replace only the selected resolver constructor with one that raises at
    execution, then invoke the command with valid explicit inputs.

    Oracle: The command contract reserves exit three and `INTERNAL_ERROR` for unexpected
    boundary exceptions.

    Acceptance: Exit status is three with internal stage, structured error text, and no
    resource results.

    Interpretation: Failure identifies exception translation or status-partition drift.

    Limitations: The synthetic exception does not claim a production resolver defect.
    """
    root = repository_root()
    path = root / "harness/local/validation/validate_local_harness_resources.py"
    spec = importlib.util.spec_from_file_location("local_harness_command", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class ExplodingResolver:
        def execute(self, *_: Any) -> None:
            raise RuntimeError("controlled internal failure")

    monkeypatch.setattr(module, "ResourceResolver", ExplodingResolver)
    result = module.main(command(root)[2:])
    payload = json.loads(capsys.readouterr().out)
    assert result == 3
    assert payload == {
        "error": "RuntimeError: controlled internal failure",
        "resources": [],
        "schema_version": 1,
        "stage": "internal",
        "status": "INTERNAL_ERROR",
    }
