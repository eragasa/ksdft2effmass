r"""Software verification of validate Harness command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: validate Harness command/API agreement.

Facet and represented meaning

The module verifies deterministic rendering, exit mapping, and direct API agreement for
the ``validate-harness`` command adapter.

Intrinsic and cross-object scope

The command/API relation is primary; ``HarnessValidator`` supplies controlled public
results and repository-check integration.

VVUQ and scientific exclusions

Passing establishes command-boundary software verification only, not numerical or
scientific validation, uncertainty quantification, execution authority, or acceptance.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.harness.cli import validate_harness
from ksdft2effmass.harness.pi.conformance.python import PythonConformanceValidator
from ksdft2effmass.harness.pi.local import (
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidationResult,
    HarnessValidator,
)
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionVerificationResult,
)
from ksdft2effmass.harness.pi.local.dbcontrol.verification import (
    _HarnessProjectionVerifier,
)

pytestmark = pytest.mark.software_verification

_PASS_CHECKS = (
    HarnessValidationCheck("python_conformance", "PASS", ()),
    HarnessValidationCheck("resources", "PASS", ()),
    HarnessValidationCheck("task_graph", "PASS", ()),
    HarnessValidationCheck("checkpoints", "PASS", ()),
    HarnessValidationCheck("skills", "PASS", ()),
    HarnessValidationCheck("control_state", "PASS", ()),
)
_WARN_CHECKS = (
    _PASS_CHECKS[0],
    HarnessValidationCheck(
        "resources", "WARN", (("resource.warning", None, "real warning"),)
    ),
    *_PASS_CHECKS[2:],
)
_FAIL_CHECKS = (
    *_PASS_CHECKS[:5],
    HarnessValidationCheck(
        "control_state", "FAIL", (("control.changed", None, "drift"),)
    ),
)
_COMMAND_CASES = (
    pytest.param(HarnessValidationResult("PASS", _PASS_CHECKS), 0, id="pass_exit_zero"),
    pytest.param(HarnessValidationResult("WARN", _WARN_CHECKS), 0, id="warn_exit_zero"),
    pytest.param(HarnessValidationResult("FAIL", _FAIL_CHECKS), 1, id="fail_exit_one"),
)
_BOUNDARIES = [
    "does not execute or establish pytest success",
    "does not execute or establish Ruff conformance",
    "does not execute or establish mypy conformance",
    "does not execute or establish Sphinx conformance",
    "does not establish numerical verification",
    "does not establish scientific validation",
    "does not establish uncertainty quantification",
    "does not authorize protected execution",
    "does not establish human acceptance",
]
_PASS_PAYLOAD: dict[str, object] = {
    "status": "PASS",
    "checks": [
        {"name": "python_conformance", "status": "PASS", "findings": []},
        {"name": "resources", "status": "PASS", "findings": []},
        {"name": "task_graph", "status": "PASS", "findings": []},
        {"name": "checkpoints", "status": "PASS", "findings": []},
        {"name": "skills", "status": "PASS", "findings": []},
        {"name": "control_state", "status": "PASS", "findings": []},
    ],
    "claim_boundaries": _BOUNDARIES,
}
_WARN_PAYLOAD = deepcopy(_PASS_PAYLOAD)
_WARN_PAYLOAD["status"] = "WARN"
cast(list[dict[str, object]], _WARN_PAYLOAD["checks"])[1] = {
    "name": "resources",
    "status": "WARN",
    "findings": [["resource.warning", None, "real warning"]],
}
_FAIL_PAYLOAD = deepcopy(_PASS_PAYLOAD)
_FAIL_PAYLOAD["status"] = "FAIL"
cast(list[dict[str, object]], _FAIL_PAYLOAD["checks"])[-1] = {
    "name": "control_state",
    "status": "FAIL",
    "findings": [["control.changed", None, "drift"]],
}
_EXPECTED_PAYLOADS = {
    "PASS": _PASS_PAYLOAD,
    "WARN": _WARN_PAYLOAD,
    "FAIL": _FAIL_PAYLOAD,
}


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
    assert payload == _EXPECTED_PAYLOADS[result.status]
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


def test_artifact__python_conformance__direct_owner_preserves_controlled_finding(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: SV-HRV-PE-001

    Requirement: Python conformance is obtained directly from
    PythonConformanceValidator and preserves its exact code, path, and message.

    Method: Copy the maintained repository, introduce one invalid evidence name, wrap
    the Python owner to capture its result, and make the control verifier conform.

    Oracle: The captured Python-conformance finding is independent of control state.

    Acceptance: The conformance check and aggregate fail with the exact captured
    triple.

    Interpretation: Failure identifies indirect conformance ownership or lossy
    mapping.

    Limitations: The mutation is synthetic software-verification data.
    """
    repository = Path(__file__).resolve().parents[7]
    import shutil

    root = tmp_path / "repository"
    shutil.copytree(repository, root)
    module = (
        root
        / "python/tests/software_verification/ksdft2effmass/harness/pi/local"
        / "test__HarnessValidationRequest.py"
    )
    module.write_text(module.read_text().replace("test_constructor__", "test_bad__", 1))
    captured: list[tuple[tuple[str, str, str], ...]] = []
    execute = PythonConformanceValidator.execute

    def observe(self: object, request: object) -> object:
        result = execute(self, request)  # type: ignore[arg-type]
        captured.append(
            tuple((item.code, item.path, item.message) for item in result.findings)
        )
        return result

    monkeypatch.setattr(PythonConformanceValidator, "execute", observe)
    monkeypatch.setattr(
        _HarnessProjectionVerifier,
        "execute",
        lambda self, repository_root: _HarnessProjectionVerificationResult(
            "ok", 0, "digest", "digest", "raw", "candidate", True
        ),
    )
    result = HarnessValidator().execute(HarnessValidationRequest(root.resolve()))
    assert captured and captured[0]
    assert result.status == "FAIL"
    expected = tuple(sorted(captured[0]))
    assert result.checks[0] == HarnessValidationCheck(
        "python_conformance", "FAIL", expected
    )
    assert validate_harness.run(["--repository-root", str(root.resolve())]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "FAIL"
    assert payload["checks"][0] == {
        "name": "python_conformance",
        "status": "FAIL",
        "findings": [list(finding) for finding in expected],
    }
