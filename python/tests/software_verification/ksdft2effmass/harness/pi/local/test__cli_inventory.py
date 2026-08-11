r"""Software verification of the maintained harness CLI inventory.

Evidence profile: claim_bearing

Bounded artifact scope: maintained harness CLI placement and inventory agreement.

Facet and represented meaning

The module owns the repository agreement that maintained operational Python commands
reside directly under ``python/src/cli`` while retained evidence commands remain
historical.

Intrinsic and cross-object scope

Exact paths, nonpackage placement, nonrepository-CWD startup, and the durable R2.7
handoff inventory are in scope. Individual command semantics remain owned by focused
command/API evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no numerical verification,
scientific validation, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification
ROOT = Path(__file__).resolve().parents[7]
CLI_ROOT = ROOT / "python/src/cli"
INVENTORY = ROOT / ".pi/evidence/harness-simplify-2/r2.6-cli-inventory.json"
R2_6_COMMANDS = {
    "audit_evidence_identifiers.py",
    "harness_control.py",
    "inspect_task_state.py",
    "refresh_resource_manifest.py",
    "validate_architecture_decision_cases.py",
    "validate_checkpoints.py",
    "validate_documentation_projection.py",
    "validate_evidence_repository_conformance.py",
    "validate_local_harness_resources.py",
    "validate_python_conformance.py",
    "validate_skill_capabilities.py",
    "validate_task_ownership.py",
    "validate_task_schema_projection.py",
}
EXPECTED_COMMANDS = (R2_6_COMMANDS - {"audit_evidence_identifiers.py"}) | {
    "validate_harness.py"
}
HELP_CASES = (
    pytest.param("harness_control.py", id="harness_control"),
    pytest.param("inspect_task_state.py", id="inspect_task_state"),
    pytest.param("refresh_resource_manifest.py", id="refresh_resource_manifest"),
    pytest.param(
        "validate_architecture_decision_cases.py",
        id="validate_architecture_decision_cases",
    ),
    pytest.param("validate_checkpoints.py", id="validate_checkpoints"),
    pytest.param("validate_harness.py", id="validate_harness"),
    pytest.param(
        "validate_documentation_projection.py", id="validate_documentation_projection"
    ),
    pytest.param(
        "validate_evidence_repository_conformance.py",
        id="validate_evidence_repository_conformance",
    ),
    pytest.param("validate_local_harness_resources.py", id="validate_local_resources"),
    pytest.param("validate_python_conformance.py", id="validate_python_conformance"),
    pytest.param("validate_skill_capabilities.py", id="validate_skill_capabilities"),
    pytest.param("validate_task_ownership.py", id="validate_task_ownership"),
    pytest.param("validate_task_schema_projection.py", id="validate_task_schema"),
)


def defines_command(path: Path) -> bool:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-175.

    Requirement: Placement evidence needs an exact static command-boundary predicate.

    Method: Parse one module and inspect only top-level ``main`` definitions and
    ``__name__`` guards.

    Oracle: The maintained repository command grammar uses those two explicit forms.

    Acceptance: Return true exactly when either form occurs.

    Interpretation: Failure identifies test scan implementation drift.

    Limitations: Dynamically generated external entry points are outside repository
    scope.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
    defines_main = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "main"
        for node in tree.body
    )
    has_main_guard = any(
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
        for node in tree.body
    )
    return defines_main or has_main_guard


def test_artifact__inventory__classifies_exact_maintained_and_historical_commands() -> (
    None
):
    """Evidence ID: SV-HARNESS-174.

    Requirement: The durable R2.7 handoff must classify every discovered maintained
    and historical executable Python command without overlap.

    Method: Parse the handoff and compare maintained destinations with the exact direct
    CLI directory while checking retained entries remain beneath the evidence root.

    Oracle: The Task-authorized final CLI root and tracked historical evidence boundary
    define the exact two path partitions.

    Acceptance: The thirteen completed R2.6 names remain historically exact, the
    current CLI replaces the retired identifier audit with ``validate_harness.py``,
    every other implementation owner remains live, and retained historical commands
    stay under ``.pi/evidence``.

    Interpretation: Failure indicates incomplete inventory, misplaced live commands,
    or accidental historical migration.

    Limitations: Individual argument and result behavior is covered by command/API
    evidence.
    """
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    migrated = [
        item
        for item in payload["entries"]
        if item["classification"] == "migrated_maintained"
    ]
    retained = [
        item
        for item in payload["entries"]
        if item["classification"] == "retained_historical_reproduction"
    ]
    assert {Path(item["path"]).name for item in migrated} == R2_6_COMMANDS
    assert len({item["old_path"] for item in migrated}) == len(migrated) == 13
    assert all(
        (ROOT / item["implementation_owner"]).is_file()
        for item in migrated
        if Path(item["path"]).name != "audit_evidence_identifiers.py"
    )
    assert not (
        ROOT / "python/src/ksdft2effmass/harness/pi/local/_commands/"
        "audit_evidence_identifiers.py"
    ).exists()
    assert retained
    retained_paths = {item["path"] for item in retained}
    discovered_historical = {
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / ".pi/evidence").rglob("*.py"))
        if defines_command(path)
    }
    assert retained_paths == discovered_historical
    assert {path.name for path in CLI_ROOT.glob("*.py")} == EXPECTED_COMMANDS
    assert (
        "audit_evidence_identifiers.py"
        not in (ROOT / ".pi/skills/skill-capability-inventory.json").read_text()
    )
    assert (
        "python/src/cli/audit_evidence_identifiers.py"
        not in (ROOT / "docs/architecture/cpn-skill-capability-audit.md").read_text()
    )
    assert any(
        item.get("path") == "python/src/cli/audit_evidence_identifiers.py"
        for item in payload["entries"]
    )


def test_artifact__placement__leaves_no_maintained_command_outside_cli() -> None:
    """Evidence ID: SV-HARNESS-175.

    Requirement: No maintained operational command may remain under the package,
    harness resource roots, or live ``.pi`` control roots after consolidation.

    Method: Parse every Python file in the three maintained roots while excluding the
    explicitly retained evidence and archive trees.

    Oracle: Top-level ``main`` definitions and ``__name__`` guards are exact command
    boundary syntax for the current repository inventory.

    Acceptance: The scan finds no command boundary outside ``python/src/cli`` and that
    directory is not an importable package.

    Interpretation: Failure identifies an incomplete wrapper retirement or competing
    live CLI root.

    Limitations: Dynamically generated external commands are outside repository scope.
    """
    candidates = [
        *sorted((ROOT / "python/src/ksdft2effmass").rglob("*.py")),
        *sorted((ROOT / "harness").rglob("*.py")),
        *sorted((ROOT / ".pi").rglob("*.py")),
    ]
    maintained = [
        path
        for path in candidates
        if ".pi/evidence" not in path.as_posix()
        and "harness/archive" not in path.as_posix()
        and "__pycache__" not in path.parts
    ]
    assert [
        path.relative_to(ROOT).as_posix()
        for path in maintained
        if defines_command(path)
    ] == []
    assert not (CLI_ROOT / "__init__.py").exists()


@pytest.mark.parametrize("command", HELP_CASES)
def test_artifact__adapters__are_thin_and_owners_not_executable(
    command: str,
) -> None:
    """Evidence ID: SV-HARNESS-182.

    Requirement: Repository CLI scripts are thin adapters while reusable package
    owners contain no competing ``main`` function or executable guard.

    Method: Parse every maintained CLI and its corresponding internal owner and inspect
    their top-level command shape plus the adapter function body.

    Oracle: The accepted adapter pattern is one explicit-argv delegate call; owner
    modules are non-executable implementation surfaces.

    Acceptance: Every adapter function has one return-call statement and every owner
    lacks both ``main`` and a ``__name__`` guard.

    Interpretation: Failure identifies domain behavior in a script or a competing
    package CLI.

    Limitations: Focused command/API tests own behavioral agreement.
    """
    owner_root = ROOT / "python/src/ksdft2effmass/harness/pi/local/_commands"
    adapter_path = CLI_ROOT / command
    adapter_tree = ast.parse(adapter_path.read_text(encoding="utf-8"))
    adapter = next(
        node
        for node in adapter_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "cli_main"
    )
    assert len(adapter.body) == 2
    assert isinstance(adapter.body[0], ast.Expr)
    assert isinstance(adapter.body[1], ast.Return)
    assert isinstance(adapter.body[1].value, ast.Call)

    owner_path = owner_root / command
    owner_tree = ast.parse(owner_path.read_text(encoding="utf-8"))
    assert not any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "main"
        for node in owner_tree.body
    )
    assert not any(
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
        for node in owner_tree.body
    )


@pytest.mark.parametrize("command", HELP_CASES)
def test_artifact__startup__works_from_nonrepository_cwd(
    command: str, tmp_path: Path
) -> None:
    """Evidence ID: SV-HARNESS-176.

    Requirement: Maintained argument-parsing commands must start through the canonical
    interpreter without repository-CWD authority.

    Method: Invoke each help-capable script from an isolated temporary directory.

    Oracle: Standard ``argparse`` help handling exits zero after loading the real script
    and package imports.

    Acceptance: Every semantic command partition exits zero, writes help to stdout,
    and writes nothing to stderr.

    Interpretation: Failure indicates CWD-dependent imports, invalid script placement,
    or argument-parser startup drift.

    Limitations: Full semantic behavior remains owned by focused command/API tests.
    """
    completed = subprocess.run(
        (sys.executable, str(CLI_ROOT / command), "--help"),
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert completed.stdout.startswith("usage:")
    assert completed.stderr == ""
