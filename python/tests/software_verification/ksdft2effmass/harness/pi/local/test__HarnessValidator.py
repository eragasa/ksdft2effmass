r"""Software verification of ``HarnessValidator``.

Evidence profile: claim_bearing

Bounded artifact scope: ``HarnessValidator``.

Facet and represented meaning

The module verifies repository-check ordering, configuration forwarding, Task catalog
validation, Python-conformance ownership, and control-state separation.

Intrinsic and cross-object scope

``HarnessValidator`` is the sole system under test; its configured domain collaborators
provide controlled cross-object results.

VVUQ and scientific exclusions

Passing establishes structural software verification only. It does not establish pytest,
Ruff, mypy, Sphinx, numerical, scientific, uncertainty, protected-execution, or human
acceptance claims.
"""

import subprocess
from dataclasses import replace
from operator import attrgetter
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessTaskDeserializer,
    HarnessTaskGraphValidator,
    HarnessTaskSerializer,
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidator,
)
from ksdft2effmass.harness.pi.local.control.configuration_inputs import (
    _HarnessConfigurationInputResolver,
    _HarnessConfigurationInputs,
)
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionVerificationFinding,
    _HarnessProjectionVerificationResult,
)
from ksdft2effmass.harness.pi.local.dbcontrol.verification import (
    _HarnessProjectionVerifier,
)
from ksdft2effmass.harness.pi.local.validation import (
    _PythonConformanceRepositoryValidator,
)

from .task_model_examples import make_task

SUT = HarnessValidator
pytestmark = pytest.mark.software_verification

_PASS_CHECKS = (
    HarnessValidationCheck("python_conformance", "PASS", ()),
    HarnessValidationCheck("resources", "PASS", ()),
    HarnessValidationCheck("task_graph", "PASS", ()),
    HarnessValidationCheck("checkpoints", "PASS", ()),
    HarnessValidationCheck("skills", "PASS", ()),
    HarnessValidationCheck("control_state", "PASS", ()),
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
    result = SUT().execute(HarnessValidationRequest(repository))
    assert result.status == "PASS"
    assert tuple(map(attrgetter("name"), result.checks)) == (
        "python_conformance",
        "resources",
        "task_graph",
        "checkpoints",
        "skills",
        "control_state",
    )
    assert tuple(
        (check.name, check.status, check.findings) for check in result.checks
    ) == (
        ("python_conformance", "PASS", ()),
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


def test_method__execute__forwards_resolved_configuration_to_all_configured_checks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.action.configuration-cutover

    Requirement: Maintained repository validation consumes the one resolved
    HarnessConfiguration for conformance, resource, Task, and checkpoint inputs.

    Method: Replace canonical resolution with an immutable aggregate containing
    non-default paths and observe each check-owner argument while returning literal
    passing checks.

    Oracle: The non-default configuration fields independently define every expected
    forwarded value.

    Acceptance: Validation passes and each observed argument equals its exact nested
    configuration value or configured catalog path.

    Interpretation: Failure identifies fallback path authority or loss at composition.

    Limitations: Each domain owner's path reading is verified in its focused evidence.
    """  # noqa: E501
    repository = Path(__file__).resolve().parents[7]
    original = _HarnessConfigurationInputResolver().execute(repository).configuration
    conformance = replace(
        original.python_conformance,
        pyproject_path="alternate/python/pyproject.toml",
        test_root="alternate/python/tests",
        profile_matrix_path="alternate/evidence/profile.json",
        migration_map_path="alternate/evidence/migration.json",
    )
    resources = replace(
        original.resources,
        project_profile_path="alternate/local/profile.json",
        generic_manifest_path="alternate/generic/manifest.json",
        generic_root="alternate/generic",
        local_manifest_path="alternate/local/manifest.json",
        local_root="alternate/local",
    )
    catalogs = replace(
        original.catalogs,
        task_root="alternate/tasks",
        checkpoint_roots=("alternate/checkpoints",),
    )
    configuration = replace(
        original,
        python_conformance=conformance,
        resources=resources,
        catalogs=catalogs,
    )
    observed: dict[str, object] = {}
    monkeypatch.setattr(
        _HarnessConfigurationInputResolver,
        "execute",
        lambda self, root: _HarnessConfigurationInputs(configuration),
    )
    monkeypatch.setattr(
        _PythonConformanceRepositoryValidator,
        "execute",
        lambda self, root, value: (
            observed.__setitem__("conformance", value),
            _PASS_CHECKS[0],
        )[1],
    )

    monkeypatch.setattr(
        HarnessValidator,
        "_resource_check",
        lambda self, root, value: (
            observed.__setitem__("resources", value),
            (None, _PASS_CHECKS[1]),
        )[1],
    )
    monkeypatch.setattr(
        HarnessValidator,
        "_task_check",
        lambda self, root, value: (
            observed.__setitem__("task_root", value),
            _PASS_CHECKS[2],
        )[1],
    )
    monkeypatch.setattr(
        HarnessValidator,
        "_checkpoint_check",
        lambda self, root, value: (
            observed.__setitem__("catalogs", value),
            _PASS_CHECKS[3],
        )[1],
    )
    monkeypatch.setattr(
        HarnessValidator,
        "_skill_check",
        lambda self, root, context: _PASS_CHECKS[4],
    )
    monkeypatch.setattr(
        _HarnessProjectionVerifier,
        "execute",
        lambda self, root: _HarnessProjectionVerificationResult(
            "ok", 0, "same", "same", "raw", "raw", True, True, True, True, ()
        ),
    )

    result = SUT().execute(HarnessValidationRequest(repository))

    assert result.status == "PASS"
    assert observed == {
        "conformance": conformance,
        "resources": resources,
        "task_root": Path("alternate/tasks"),
        "catalogs": catalogs,
    }


def test_method__task_check__deserializes_complete_discovered_catalog(
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
    result = SUT()._task_check(tmp_path.resolve(), Path("harness/tasks"))
    assert result == HarnessValidationCheck("task_graph", "PASS", ())
    assert deserialized == ["alpha", "beta"]
    assert graphed == [("alpha", "beta")]


def test_method__task_check__unsupported_version_reports_invalid_record(
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
    result = SUT()._task_check(tmp_path.resolve(), Path("harness/tasks"))
    assert result.status == "FAIL"
    assert result.findings == (
        (
            "task.invalid_record",
            "harness/tasks/example.task.json",
            "schema_version must equal integer 3",
        ),
    )


def test_method__execute_control_state__does_not_contaminate_python_conformance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: SV-HRV-CS-001

    Requirement: Control-only disagreement, including a finding without a path, does
    not become Python conformance.

    Method: Verify the maintained conforming source corpus while replacing only the
    control verifier result with one pathless source-input failure.

    Oracle: PythonConformanceValidator owns conformance; the private projection
    verifier owns drift.

    Acceptance: Conformance passes, control fails with its exact finding, and the
    aggregate fails.

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
    result = SUT().execute(HarnessValidationRequest(repository))
    assert result.status == "FAIL"
    assert result.checks[0] == HarnessValidationCheck("python_conformance", "PASS", ())
    assert result.checks[-1].status == "FAIL"
    assert result.checks[-1].findings == (
        (
            "control.source_input_failure",
            None,
            "controlled control-only disagreement",
        ),
    )
