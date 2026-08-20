r"""Software verification of sole Harness command dispatcher.

Evidence profile: claim_bearing

Bounded artifact scope: ``ksdft2effmass.harness.cli`` command inventory and dispatch.

Facet and represented meaning

The module verifies exact command discovery, lazy selection, argument forwarding, and
closed rejection at the one maintained Harness command namespace.

Intrinsic and cross-object scope

Dispatcher behavior is primary; individual command argument and rendering contracts
remain with their focused command/API evidence.

VVUQ and scientific exclusions

Passing establishes command-dispatch software behavior only. It does not establish
domain validation, scientific validation, uncertainty quantification, execution
authority, or human acceptance.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from ksdft2effmass.harness.cli import main

pytestmark = pytest.mark.software_verification

_EXPECTED_COMMANDS = (
    "harness-projection",
    "inspect-task-state",
    "refresh-resource-manifest",
    "validate-agent-definitions",
    "validate-architecture-decision-cases",
    "validate-checkpoints",
    "validate-documentation-projection",
    "validate-evidence-repository-conformance",
    "validate-harness",
    "validate-local-harness-resources",
    "validate-python-conformance",
    "validate-skill-capabilities",
    "validate-task-ownership",
)


def test_artifact__help__lists_exact_command_inventory(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.cli.exact-inventory

    Requirement: The sole dispatcher publishes every maintained Harness command once
    and exposes no retired command surface.

    Method: Request dispatcher help and compare its command lines with a literal tuple.

    Oracle: The accepted command architecture fixes the complete inventory.

    Acceptance: Help exits zero, stderr is empty, and command lines equal the exact
    sorted inventory.

    Interpretation: Failure identifies missing, unexpected, duplicated, or renamed
    command dispatch.

    Limitations: Individual command semantics are verified separately.
    """
    assert main.run(["--help"]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert (
        tuple(
            line.strip() for line in captured.out.splitlines() if line.startswith("  ")
        )
        == _EXPECTED_COMMANDS
    )


def test_artifact__dispatch__loads_only_selected_owner_and_forwards_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: software-verification.harness.cli.lazy-dispatch

    Requirement: Dispatch imports only the selected adapter and forwards remaining
    arguments without reinterpretation.

    Method: Replace the import seam with one literal module result and dispatch a
    command with two opaque arguments.

    Oracle: The accepted command map and supplied argument tuple fix the exact call.

    Acceptance: Exactly the selected module is imported, exact arguments reach
    ``run``, and its exit status is returned unchanged.

    Interpretation: Failure identifies eager imports, routing drift, argument mutation,
    or exit translation in the dispatcher.

    Limitations: The selected adapter itself is synthetic test data.
    """
    observed: list[object] = []

    def run_literal(arguments: list[str]) -> int:
        observed.append(arguments)
        return 7

    def import_literal(name: str) -> object:
        observed.append(name)
        return SimpleNamespace(run=run_literal)

    monkeypatch.setattr(main, "import_module", import_literal)
    assert main.run(["validate-harness", "--opaque", "value"]) == 7
    assert observed == [
        "ksdft2effmass.harness.cli.validate_harness",
        ["--opaque", "value"],
    ]


def test_artifact__dispatch__rejects_missing_and_unknown_commands(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.cli.closed-selection

    Requirement: Missing and unknown commands fail closed without importing an owner.

    Method: Invoke both invalid selection partitions.

    Oracle: Command-line usage semantics reserve exit two for selection errors.

    Acceptance: Both calls return two and emit usage on stderr only.

    Interpretation: Failure identifies ambient/default dispatch or an open command set.

    Limitations: Selected-command input validation belongs to each adapter.
    """
    assert main.run([]) == 2
    missing = capsys.readouterr()
    assert missing.out == ""
    assert "Usage: python3 -m ksdft2effmass.harness.cli" in missing.err

    assert main.run(["not-a-command"]) == 2
    unknown = capsys.readouterr()
    assert unknown.out == ""
    assert "unknown Harness command: not-a-command" in unknown.err
