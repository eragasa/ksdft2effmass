r"""Software verification of migrated validation command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owners.

Facet and represented meaning

Software verification of explicit repository command adapters over internal reusable
validation owners.

Intrinsic and cross-object scope

Explicit arguments, deterministic rendering, exit status, nonrepository working
directory behavior, and nonmutation of selected authoritative inputs are in scope.

VVUQ and scientific exclusions

Passing establishes structural command agreement only. It does not establish
scientific validation, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification

ROOT = Path(__file__).resolve().parents[7]
CLI_MODULE = "ksdft2effmass.harness.cli"


def snapshot_identities(paths: Iterable[Path]) -> dict[str, str]:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-177 through 181.

    Requirement: Command tests require exact selected-input identities.

    Method: Hash every regular explicit input by absolute path.

    Oracle: SHA-256 byte identity is exact.

    Acceptance: Return a stable path-to-digest mapping.

    Interpretation: Failure identifies test setup drift.

    Limitations: Only explicitly supplied paths are included.
    """
    return {
        path.as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(paths)
        if path.is_file()
    }


def run_command(
    name: str, arguments: list[str], cwd: Path
) -> subprocess.CompletedProcess[str]:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-177 through 181.

    Requirement: Tests invoke exact maintained command paths and explicit arguments.

    Method: Run one script with the selected venv interpreter and working directory.

    Oracle: The R2.6 inventory fixes the command root.

    Acceptance: Return the captured completed process.

    Interpretation: Failure identifies command setup drift.

    Limitations: The helper makes no behavioral assertion.
    """
    return subprocess.run(
        [sys.executable, "-m", CLI_MODULE, name, *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )


def test_artifact__architecture_cases_command__agrees_from_nonrepository_cwd(
    tmp_path: Path,
) -> None:
    """Evidence ID: ``SV-HARNESS-177``.

    Requirement: Architecture-case validation is an explicit-root, deterministic,
    read-only command over its reusable owner.

    Method: Snapshot all three authoritative inputs and execute the maintained script
    from a nonrepository working directory with the absolute repository root.

    Oracle: The closed fixture contract fixes the exact structured result.

    Acceptance: Exit is zero, JSON equals the exact PASS projection, and inputs retain
    byte identities.

    Interpretation: Failure indicates argument, adapter, projection, CWD, or mutation
    drift.

    Limitations: This verifies controlled structural cases, not architecture quality.
    """
    inputs = [
        ROOT / "harness/pi/fixtures/architecture-decision/cases.json",
        ROOT / "harness/pi/skills/develop-architecture-decision/SKILL.md",
        ROOT / "harness/pi/skills/develop-architecture-decision/references/"
        "architecture-decision-conventions.md",
    ]
    before = snapshot_identities(inputs)
    completed = run_command(
        "validate-architecture-decision-cases",
        ["--repository-root", str(ROOT)],
        tmp_path,
    )
    assert completed.returncode == 0
    assert json.loads(completed.stdout) == {
        "applicable_cases": 3,
        "fixture_scope": "harness-phase-six-only-controlled-fixture",
        "issues": [],
        "non_applicable_cases": 5,
        "schema_version": 1,
        "status": "PASS",
    }
    assert completed.stderr == ""
    assert snapshot_identities(inputs) == before


def test_artifact__checkpoint_command__agrees_from_nonrepository_cwd(
    tmp_path: Path,
) -> None:
    """Evidence ID: ``SV-HARNESS-178``.

    Requirement: Checkpoint validation accepts an explicit root and preserves every
    checkpoint and fixture byte while reporting all declared dry-run stages.

    Method: Snapshot the checkpoint JSON tree and run the maintained script with the
    fixture and dry-run flags from a nonrepository working directory.

    Oracle: The accepted schema and deterministic dry-run transformations fix the text
    fields and zero-error exit.

    Acceptance: Exit is zero; every stage and count line is present exactly once; no
    error line appears; all input bytes are unchanged.

    Interpretation: Failure indicates schema, transformation, rendering, CWD, or
    mutation drift.

    Limitations: Passing does not resolve checkpoints or authorize work.
    """
    inputs = list((ROOT / ".pi/checkpoints").rglob("*.json"))
    before = snapshot_identities(inputs)
    completed = run_command(
        "validate-checkpoints",
        [
            "--repository-root",
            str(ROOT),
            "--include-fixtures",
            "--dry-run",
        ],
        tmp_path,
    )
    assert completed.returncode == 0
    lines = completed.stdout.splitlines()
    assert lines[:4] == [
        "dry_run_checkpoint_schema=passed",
        "dry_run_checkpoint_resolution=passed",
        "dry_run_task_resumption=passed",
        "dry_run_deterministic_correction=passed",
    ]
    assert lines[-2:] == ["unresolved_checkpoints=0", "duplicate_resolved_decisions=0"]
    assert lines[4].startswith("checkpoint_records_validated=")
    assert "ERROR:" not in completed.stdout
    assert completed.stderr == ""
    assert snapshot_identities(inputs) == before


def test_artifact__skill_capability_command__agrees_from_nonrepository_cwd(
    tmp_path: Path,
) -> None:
    """Evidence ID: ``SV-HARNESS-179``.

    Requirement: Skill-capability validation uses an explicit root and inventory and
    is deterministic and read-only.

    Method: Snapshot the inventory and maintained skill files, then execute the script
    from a nonrepository working directory.

    Oracle: The closed capability inventory fixes exact summary lines and zero errors.

    Acceptance: Exit is zero, stdout is the exact five-line PASS summary, stderr is
    empty, and selected authoritative bytes remain identical.

    Interpretation: Failure indicates inventory, discovery, output, CWD, or mutation
    drift.

    Limitations: Passing does not execute skills or establish human acceptance.
    """
    inputs = (
        [ROOT / ".pi/skills/skill-capability-inventory.json"]
        + list((ROOT / ".pi/skills").rglob("SKILL.md"))
        + list((ROOT / ".agents/skills").rglob("SKILL.md"))
    )
    before = snapshot_identities(inputs)
    completed = run_command(
        "validate-skill-capabilities",
        [
            "--repository-root",
            str(ROOT),
            "--inventory",
            ".pi/skills/skill-capability-inventory.json",
        ],
        tmp_path,
    )
    assert completed.returncode == 0
    assert completed.stdout == (
        "skill_records=10\n"
        "filesystem_skills=10\n"
        "cpn_review_blocks=13\n"
        "deterministic_tool_blocks=13\n"
        "validation_errors=0\n"
    )
    assert completed.stderr == ""
    assert snapshot_identities(inputs) == before


def write_legacy_task_record(path: Path) -> Path:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-180 and 181.

    Requirement: Projection tests require the accepted version-1 Task shape.

    Method: Remove only later-version fields from the corresponding current Task.

    Oracle: The version-1 schema fixes the retained field set.

    Acceptance: Write and return one controlled temporary record.

    Interpretation: Failure identifies support-input drift.

    Limitations: The temporary record is synthetic test data.
    """
    task = json.loads(
        (
            ROOT
            / "harness/local/fixtures/task-control-reference/input/"
            "harness.simplification.docs-json.schema-projection-v3.json"
        ).read_text()
    )
    task["schema_version"] = 1
    task["authority_reference_paths"] = sorted(
        value.replace(
            "harness/archive/task-control-v1/chains/",
            ".pi/chains/",
        )
        for value in task["authority_reference_paths"]
    )
    task.pop("status_detail")
    task.pop("superseded_by_task_ids")
    path.write_text(json.dumps(task))
    return path


def write_legacy_chain(path: Path) -> Path:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-180 and 181.

    Requirement: Projection tests require the accepted version-1 chain context.

    Method: Select the retained completed-task activation projection.

    Oracle: The expected Markdown fixture fixes the four activation facts.

    Acceptance: Write and return one controlled temporary chain.

    Interpretation: Failure identifies support-input drift.

    Limitations: The temporary chain cannot activate work.
    """
    chain = json.loads(
        (
            ROOT
            / "harness/archive/task-control-v1/chains/harness-simplification.chain.json"
        ).read_text()
    )
    chain["active_task"] = None
    chain["explicitly_activated_task_ids"] = [
        "harness.simplification.agents.delegation-validation",
        "harness.simplification.control.task-catalog-reconciliation",
        "harness.simplification.docs-json.schema-projection",
        "harness.simplification.resources.h3-validator-retirement",
    ]
    path.write_text(json.dumps(chain))
    return path


def test_artifact__documentation_projection_command__agrees_on_explicit_inputs(
    tmp_path: Path,
) -> None:
    """Evidence ID: ``SV-HARNESS-181``.

    Requirement: Documentation projection accepts explicit schema, profile, context,
    expected, and generated paths and performs no mutation.

    Method: Derive a controlled context from the maintained Task and chain, write it
    beneath a temporary root, and invoke the migrated script outside the repository.

    Oracle: The accepted expected/generated bytes fix the exact PASS projection.

    Acceptance: Exit is zero, JSON is exact, stderr is empty, and controlled input
    bytes remain unchanged.

    Interpretation: Failure indicates explicit-input, rendering, drift, or CWD
    disagreement.

    Limitations: Passing establishes byte agreement, not documentation completeness.
    """
    task_path = write_legacy_task_record(tmp_path / "task.json")
    task = json.loads(task_path.read_text())
    task["intake_path"] = Path(task["intake_path"]).name
    chain_path = write_legacy_chain(tmp_path / "chain.json")
    chain = json.loads(chain_path.read_text())
    context = tmp_path / "context.json"
    context.write_text(json.dumps({"task": task, "chain": chain}))
    inputs = [
        ROOT / "harness/pi/schemas/documentation-projection-profile.schema.json",
        ROOT / "harness/local/projections/task-control-reference-v1.json",
        task_path,
        context,
        ROOT / "harness/local/fixtures/task-control-reference/expected/"
        "harness.simplification.docs-json.schema-projection.md",
        ROOT / "harness/local/fixtures/task-control-reference/expected/"
        "harness.simplification.docs-json.schema-projection.md",
    ]
    before = snapshot_identities(inputs)
    completed = run_command(
        "validate-documentation-projection",
        [
            "--schema",
            str(ROOT / "harness/local/schemas/task-record.schema.json"),
            "--instance",
            str(task_path),
            "--profile-schema",
            str(inputs[0]),
            "--profile",
            str(inputs[1]),
            "--context",
            str(context),
            "--expected",
            str(inputs[4]),
            "--generated",
            str(inputs[5]),
        ],
        tmp_path,
    )
    assert completed.returncode == 0
    assert completed.stdout == (
        '{"diagnostics":[],"schema_version":1,"status":"PASS"}\n'
    )
    assert completed.stderr == ""
    assert snapshot_identities(inputs) == before
