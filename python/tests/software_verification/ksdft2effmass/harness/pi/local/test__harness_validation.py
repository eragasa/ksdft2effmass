r"""Software verification of Harness repository-validation command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: Harness repository-validation command/API agreement.

Facet and represented meaning

The module owns deterministic check ordering, aggregation, claim boundaries, and
command/API exit and rendering agreement for repository structural validation.

Intrinsic and cross-object scope

The public project-local records and Action are exercised together; command partitions
replace only the public Action result at the renderer seam.

VVUQ and scientific exclusions

This is structural software verification only. It does not establish pytest, Ruff,
mypy, Sphinx, numerical, scientific, uncertainty, protected-execution, or human
acceptance claims.
"""

import json
import subprocess
from operator import attrgetter
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidationResult,
    HarnessValidator,
)
from ksdft2effmass.harness.pi.local._commands import validate_harness

pytestmark = pytest.mark.software_verification

_PASS_CHECKS = (
    HarnessValidationCheck("python_evidence", "PASS", ()),
    HarnessValidationCheck("resources", "PASS", ()),
    HarnessValidationCheck("task_graph", "PASS", ()),
    HarnessValidationCheck("checkpoints", "PASS", ()),
    HarnessValidationCheck("skills", "PASS", ()),
    HarnessValidationCheck("ownership", "PASS", ()),
    HarnessValidationCheck("control_state", "PASS", ()),
    HarnessValidationCheck("external_gates", "PASS", ()),
)
_WARN_CHECKS = (
    *_PASS_CHECKS[:5],
    HarnessValidationCheck(
        "ownership", "WARN", (("ownership.not_declared", None, "not declared"),)
    ),
    *_PASS_CHECKS[6:],
)
_FAIL_CHECKS = (
    *_PASS_CHECKS[:6],
    HarnessValidationCheck(
        "control_state", "FAIL", (("control.changed", None, "drift"),)
    ),
    _PASS_CHECKS[7],
)
_COMMAND_CASES = (
    pytest.param(HarnessValidationResult("PASS", _PASS_CHECKS), 0, id="pass_exit_zero"),
    pytest.param(HarnessValidationResult("WARN", _WARN_CHECKS), 0, id="warn_exit_zero"),
    pytest.param(HarnessValidationResult("FAIL", _FAIL_CHECKS), 1, id="fail_exit_one"),
)


def test_method__execute_maintained_repository__returns_stable_structural_checks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.action.maintained-structure

    Requirement: Repository validation invokes existing owners directly, returns every
    check in stable semantic order, records explicit claim boundaries, and executes no
    development-tool subprocess.

    Method: Reject any subprocess invocation and execute the public Action on the exact
    maintained repository root after synchronized control state.

    Oracle: The accepted R2.7 check order and claim-boundary contract are fixed literals;
    current ownership and external final gates are expected warnings.

    Acceptance: Status is WARN, check names are exact, no check or result contains a
    duration field, claim boundaries are complete, and no subprocess is invoked.

    Interpretation: Failure identifies nested tool execution, unstable composition, or
    an overclaimed validation result.

    Limitations: Separately required development tools and documentation builds are not
    executed by this test or the Action.
    """  # noqa: E501
    repository = Path(__file__).resolve().parents[7]

    def reject_subprocess(
        *args: object, **kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        raise AssertionError("HarnessValidator must not execute subprocesses")

    monkeypatch.setattr(subprocess, "run", reject_subprocess)
    result = HarnessValidator().execute(HarnessValidationRequest(repository))
    assert result.status == "WARN"
    assert tuple(map(attrgetter("name"), result.checks)) == (
        "python_evidence",
        "resources",
        "task_graph",
        "checkpoints",
        "skills",
        "ownership",
        "control_state",
        "external_gates",
    )
    assert "duration" not in repr(result).lower()
    assert result.claim_boundaries[-1] == "does not establish human acceptance"


@pytest.mark.parametrize(("result", "expected_exit"), _COMMAND_CASES)
def test_artifact__command__expected_results_preserve_output_and_exit_status(
    result: HarnessValidationResult,
    expected_exit: int,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.command.expected-status

    Requirement: PASS and WARN return zero, expected FAIL returns one, and the renderer
    preserves the complete deterministic public result without durations.

    Method: Supply one literal public result for each aggregate status and invoke the
    reusable command owner with one absolute existing repository root.

    Oracle: The accepted R2.7 exit table and literal result independently define output.

    Acceptance: Exit status matches the case, JSON status and ordered check names agree
    with the public result, and rendered JSON has no duration key.

    Interpretation: Failure identifies command/API or expected-status translation drift.

    Limitations: Invalid input and unexpected exceptions are separate partitions.
    """  # noqa: E501
    monkeypatch.setattr(HarnessValidator, "execute", lambda self, request: result)
    exit_status = validate_harness.run(["--repository-root", str(tmp_path.resolve())])
    payload = json.loads(capsys.readouterr().out)
    assert exit_status == expected_exit
    assert payload["status"] == result.status
    assert tuple(map(lambda check: check["name"], payload["checks"])) == tuple(
        map(attrgetter("name"), result.checks)
    )
    assert "duration" not in json.dumps(payload).lower()


def test_artifact__command__invalid_request_returns_exit_two(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.command.invalid-input

    Requirement: Invalid request construction is translated only at the CLI boundary to
    exit status two.

    Method: Invoke the command owner with a relative repository path.

    Oracle: ``HarnessValidationRequest`` requires an absolute path.

    Acceptance: Exit status is two and JSON status is ``INVALID_INPUT``.

    Interpretation: Failure identifies weakened request validation or wrong translation.

    Limitations: Expected domain findings use a valid request and exit one.
    """  # noqa: E501
    assert validate_harness.run(["--repository-root", "."]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "INVALID_INPUT"


def test_artifact__command__unexpected_exception_returns_exit_three(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.command.unexpected-exception

    Requirement: Unexpected implementation exceptions propagate from the Action and are
    translated to exit status three only by the command boundary.

    Method: Inject one runtime exception at the public Action seam and invoke the command.

    Oracle: The accepted R2.7 exit table assigns unexpected boundary failures to three.

    Acceptance: Exit status is three and JSON status is ``INTERNAL_ERROR``.

    Interpretation: Failure identifies swallowed exceptions or wrong exit translation.

    Limitations: The injected exception represents no expected domain finding.
    """  # noqa: E501

    def fail(self: object, request: object) -> HarnessValidationResult:
        raise RuntimeError("injected unexpected failure")

    monkeypatch.setattr(HarnessValidator, "execute", fail)
    assert validate_harness.run(["--repository-root", str(tmp_path.resolve())]) == 3
    assert json.loads(capsys.readouterr().out)["status"] == "INTERNAL_ERROR"
