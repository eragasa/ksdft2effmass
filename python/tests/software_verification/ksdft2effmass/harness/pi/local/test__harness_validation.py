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
from copy import deepcopy
from operator import attrgetter
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.harness.pi.evidence import PythonConformanceValidator
from ksdft2effmass.harness.pi.local import (
    HarnessTaskDeserializer,
    HarnessTaskGraphValidator,
    HarnessTaskSerializer,
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidationResult,
    HarnessValidator,
)
from ksdft2effmass.harness.pi.local._commands import validate_harness
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionVerificationFinding,
    _HarnessProjectionVerificationResult,
)
from ksdft2effmass.harness.pi.local.dbcontrol.verification import (
    _HarnessProjectionVerifier,
)

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification

_PASS_CHECKS = (
    HarnessValidationCheck("python_evidence", "PASS", ()),
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
        {"name": "python_evidence", "status": "PASS", "findings": []},
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
    the synchronized maintained repository is expected to conform.

    Acceptance: Status is PASS, check names are exact, no check or result contains a
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
    assert result.status == "PASS"
    assert tuple(map(attrgetter("name"), result.checks)) == (
        "python_evidence",
        "resources",
        "task_graph",
        "checkpoints",
        "skills",
        "control_state",
    )
    assert tuple(
        (check.name, check.status, check.findings) for check in result.checks
    ) == (
        ("python_evidence", "PASS", ()),
        ("resources", "PASS", ()),
        ("task_graph", "PASS", ()),
        ("checkpoints", "PASS", ()),
        ("skills", "PASS", ()),
        ("control_state", "PASS", ()),
    )
    assert result.claim_boundaries == (
        "does not execute or establish pytest success",
        "does not execute or establish Ruff conformance",
        "does not execute or establish mypy conformance",
        "does not execute or establish Sphinx conformance",
        "does not establish numerical verification",
        "does not establish scientific validation",
        "does not establish uncertainty quantification",
        "does not authorize protected execution",
        "does not establish human acceptance",
    )
    assert "duration" not in repr(result).lower()


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


def test_artifact__task_check__deserializes_complete_discovered_catalog(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.task-check.complete-catalog

    Requirement: Every discovered live Task is passed through the maintained
    deserializer and every successfully deserialized Task reaches graph validation.

    Method: Write two independent version-3 Tasks and observe public collaborator calls
    while invoking the repository Task check.

    Oracle: The two literal Task IDs define both complete expected call sets.

    Acceptance: Deserializer and graph observations both equal ``alpha,beta`` and the
    check passes.

    Interpretation: Failure identifies a silently skipped Task or incomplete graph.

    Limitations: Repository discovery is isolated from other HarnessValidator checks.
    """  # noqa: E501
    task_root = tmp_path / "harness/tasks"
    task_root.mkdir(parents=True)
    serializer = HarnessTaskSerializer()
    (task_root / "alpha.json").write_bytes(
        serializer.execute(
            make_task(
                task_id="alpha",
                intake_path="harness/intake/alpha.md",
                documentation_path="docs/tasks/alpha.md",
            )
        )
    )
    (task_root / "beta.json").write_bytes(
        serializer.execute(
            make_task(
                task_id="beta",
                intake_path="harness/intake/beta.md",
                documentation_path="docs/tasks/beta.md",
            )
        )
    )
    deserialized: list[str] = []
    graphed: list[tuple[str, ...]] = []
    deserialize = HarnessTaskDeserializer.execute
    graph = HarnessTaskGraphValidator.execute

    def observe_deserialization(self: object, payload: bytes) -> object:
        task = deserialize(self, payload)  # type: ignore[arg-type]
        deserialized.append(task.task_id)
        return task

    def observe_graph(self: object, tasks: tuple[object, ...]) -> object:
        graphed.append(tuple(task.task_id for task in tasks))  # type: ignore[attr-defined]
        return graph(self, tasks)  # type: ignore[arg-type]

    monkeypatch.setattr(HarnessTaskDeserializer, "execute", observe_deserialization)
    monkeypatch.setattr(HarnessTaskGraphValidator, "execute", observe_graph)
    result = HarnessValidator()._task_check(tmp_path.resolve())
    assert result == HarnessValidationCheck("task_graph", "PASS", ())
    assert deserialized == ["alpha", "beta"]
    assert graphed == [("alpha", "beta")]


def test_artifact__task_check__unsupported_version_reports_invalid_record(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.task-check.unsupported-version

    Requirement: An unsupported live Task version produces ``task.invalid_record``
    rather than disappearing from repository validation.

    Method: Write one otherwise valid Task with schema version 2 and invoke the bounded
    Task check.

    Oracle: ``HarnessTaskDeserializer`` accepts exactly schema version 3.

    Acceptance: The result fails with one exact invalid-record finding naming the Task.

    Interpretation: Failure identifies silent version filtering.

    Limitations: Version-3 graph behavior is covered by the complete-catalog partition.
    """  # noqa: E501
    task_root = tmp_path / "harness/tasks"
    task_root.mkdir(parents=True)
    payload = (
        HarnessTaskSerializer()
        .execute(make_task())
        .replace(b'"schema_version": 3', b'"schema_version": 2')
    )
    (task_root / "example.task.json").write_bytes(payload)
    result = HarnessValidator()._task_check(tmp_path.resolve())
    assert result.status == "FAIL"
    assert result.findings == (
        (
            "task.invalid_record",
            "harness/tasks/example.task.json",
            "schema_version must equal integer 3",
        ),
    )


def test_artifact__python_evidence__direct_owner_preserves_controlled_finding(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: SV-HRV-PE-001

    Requirement: Python evidence is obtained directly from PythonConformanceValidator
    and preserves its exact code, path, and message.

    Method: Copy the maintained repository, introduce one invalid evidence name, wrap
    the Python owner to capture its result, and make the control verifier conform.

    Oracle: The captured Python-conformance finding is independent of control state.

    Acceptance: The evidence check and aggregate fail with the exact captured triple.

    Interpretation: Failure identifies indirect evidence ownership or lossy mapping.

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
        "python_evidence", "FAIL", expected
    )
    assert validate_harness.run(["--repository-root", str(root.resolve())]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "FAIL"
    assert payload["checks"][0] == {
        "name": "python_evidence",
        "status": "FAIL",
        "findings": [list(finding) for finding in expected],
    }


def test_artifact__control_state__does_not_contaminate_python_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: SV-HRV-CS-001

    Requirement: Control-only disagreement, including a finding without a path, does
    not become Python evidence.

    Method: Verify the maintained conforming evidence corpus while replacing only the
    control verifier result with one pathless source-input failure.

    Oracle: PythonConformanceValidator owns evidence; the private projection verifier
    owns drift.

    Acceptance: Evidence passes, control fails with its exact finding, aggregate fails.

    Interpretation: Failure identifies path-based cross-domain inference.

    Limitations: The injected control result represents no maintained drift claim.
    """
    repository = Path(__file__).resolve().parents[7]
    finding = _HarnessProjectionVerificationFinding(
        "source_input_failure", None, "controlled control-only disagreement"
    )
    monkeypatch.setattr(
        _HarnessProjectionVerifier,
        "execute",
        lambda self, repository_root: _HarnessProjectionVerificationResult(
            "not_checked",
            0,
            "",
            "",
            "raw",
            "",
            False,
            False,
            False,
            False,
            (finding,),
        ),
    )
    result = HarnessValidator().execute(HarnessValidationRequest(repository))
    assert result.status == "FAIL"
    assert result.checks[0] == HarnessValidationCheck("python_evidence", "PASS", ())
    assert result.checks[-1].status == "FAIL"
    assert result.checks[-1].findings == (
        (
            "control.source_input_failure",
            None,
            "controlled control-only disagreement",
        ),
    )
