r"""Software verification of Quantum ESPRESSO local execution boundaries.

Evidence profile: routine

Bounded artifact scope: root-confined local QE preparation, input staging,
workspace snapshots, bounded local process entry, exact stream capture, native-output
collection, and private terminal publication over deterministic synthetic resources.

Facet and represented meaning

The current cases verify exact preparation, no-replace staging, deterministic bounded
workspace snapshots, explicit native-output candidate collection, and atomic
no-replace terminal publication and one-attempt deterministic process effects.

Intrinsic and cross-object scope

Tests cover file and predecessor-tree sources, supported binding correlation,
existing workspace, symlink and identity failures, free-space failure, deterministic
dry-run output, staged identity rechecks, snapshots, collection, serialization, and
publication, normal/nonzero/signal/timeout process lifecycle, and separate stream
capture. Diagnostic outcome resolution and Workflow adaptation remain separate
pending phases.

VVUQ and scientific exclusions

All maintained resources are synthetic test data. The tests invoke no Quantum
ESPRESSO executable and establish no calculator compatibility, numerical verification,
scientific validation, uncertainty quantification, production readiness, or physical
claim.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

import pytest
from projectkoios.simulations.calculator import CalculatorIntegrationId
from projectkoios.simulations.calculator.input import (
    CalculatorExternalInputRequirement,
    CalculatorInputArtifact,
    CalculatorInputRecord,
    CalculatorInputSourceReference,
)
from projectkoios.simulations.execution import (
    CalculatorExecutablePreparationFailure,
    CalculatorExecutablePreparationFailureCode,
    CalculatorExecutablePreparer,
    CalculatorExitDisposition,
)

from ksdft2effmass.integration.quantum_espresso import (
    LocalQeArtifactSource,
    LocalQeAttemptWorkspaceName,
    LocalQeCapturedProcess,
    LocalQeExecutionLimits,
    LocalQeExecutionPreparationRequest,
    LocalQeExecutionPreparer,
    LocalQeFileSourceObservation,
    LocalQePeakResidentBytesUnlimited,
    LocalQePreparationFailure,
    LocalQePreparationFailureCode,
    LocalQePreparationImplementationIdentity,
    LocalQePreparedExecution,
    LocalQeProcessFailure,
    LocalQeProcessFailureCode,
    LocalQeProcessFailureDisposition,
    LocalQeProcessRunner,
    LocalQeStreamArtifactBindings,
    LocalQeSupportedExecutableBinding,
    LocalQeTreeSourceObservation,
    QeArtifactDestination,
    QeCalculatorInputAdmission,
    QeCalculatorInputAdmissionFailure,
    QeCalculatorInputAdmissionPolicyIdentity,
    QeCalculatorInputBinding,
    QeDiagnosticCatalog,
    QeDiagnosticReportIdentity,
    QeExecutableConfiguration,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeExecutionInput,
    QeExecutionInputIdentity,
    QeExternalInputResourceBinding,
    QeFileArtifactContent,
    QeInputStager,
    QeNativeInputArtifact,
    QeNativeOutputCandidateSpecification,
    QeNativeOutputCollector,
    QeNativeOutputExtractionSpecification,
    QeNativeOutputManifest,
    QeNativeOutputRole,
    QeNormalProcessExit,
    QePredecessorNativeStateArtifact,
    QeProcessObservationIdentity,
    QeProcessSignalTermination,
    QeProcessTimeout,
    QeProgram,
    QePseudopotentialArtifact,
    QePublishedTerminalRecord,
    QeStagedExecution,
    QeStagingFailure,
    QeStagingFailureCode,
    QeTerminalPublicationFailure,
    QeTerminalPublicationFailureCode,
    QeTerminalRecord,
    QeTerminalRecordArtifact,
    QeTerminalRecordIdentity,
    QeTerminalRecordPublisher,
    QeTerminalRecordSerializer,
    QeTerminalStatus,
    QeTreeArtifactContent,
    QeWorkspaceEntryType,
    QeWorkspaceSnapshot,
    QeWorkspaceSnapshotFailure,
    QeWorkspaceSnapshotFailureCode,
    QeWorkspaceSnapshotPhase,
    QeWorkspaceSnapshotter,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    ScientificExecutorIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

_MAX_U64 = 18_446_744_073_709_551_615
_TREE_MANIFEST_IDENTITY_VALUE: str = (
    "qe-tree-manifest-v1:"
    "74a027967739800f98d6891eaad3f3458ba7e4abf09c6905a0c3c16caf6360fb"
)
_TREE_ENTRY_IDENTITY_VALUE: str = (
    "qe-tree-entry-v1:c10e7c611f6bb78479dacc2184784f56295d7376cac9956aff7a17a42594dc3b"
)


class TestLocalQeExecutionPreparer:
    """Own read-only local preparation software verification."""

    @staticmethod
    def resource(relative: str) -> Path:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return (
            Path(__file__).parent / "resources" / "local_execution" / relative
        ).resolve()

    @staticmethod
    def content_identity(path: Path) -> ArtifactContentIdentity:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        content = path.read_bytes()
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )

    @classmethod
    def calculator_input_binding(
        cls,
        request: LocalQeExecutionPreparationRequest,
        *,
        native_bytes: bytes | None = None,
    ) -> QeCalculatorInputBinding:
        """Return an admitted provider record for one fixture preparation request."""
        admitted_native_bytes: bytes = (
            cls.resource("input/pw.in").read_bytes()
            if native_bytes is None
            else native_bytes
        )
        pseudo_bytes: bytes = cls.resource("pseudo/Si.fixture.UPF").read_bytes()
        record: CalculatorInputRecord = CalculatorInputRecord(
            input_id=f"{cls.__name__}.PreparedInput",
            schema_version=1,
            source=CalculatorInputSourceReference(
                simulation_id="fixture.QE.SCF",
                representation="projectkoios.fixture+json",
                schema_version=1,
                byte_size=1,
                sha256="1" * 64,
            ),
            integration_id=CalculatorIntegrationId("quantum-espresso"),
            calculator_name="Quantum ESPRESSO pw.x fixture",
            calculator_version_constraint="fixture-pw-v1",
            representation="quantum-espresso-pw-input",
            artifacts=(
                CalculatorInputArtifact(
                    role="primary-input",
                    filename="pw.in",
                    media_type="text/plain; charset=us-ascii",
                    content=admitted_native_bytes,
                    byte_size=len(admitted_native_bytes),
                    sha256=hashlib.sha256(admitted_native_bytes).hexdigest(),
                ),
            ),
            external_requirements=(
                CalculatorExternalInputRequirement(
                    role="pseudopotential",
                    stable_id="Si.fixture",
                    filename="Si.fixture.UPF",
                    format="synthetic-fixture",
                    byte_size=len(pseudo_bytes),
                    sha256=hashlib.sha256(pseudo_bytes).hexdigest(),
                    provenance="synthetic software-verification fixture",
                    element_symbol="Si",
                ),
            ),
            mappings=(),
            preparation_operation="projectkoios.qe.pw.fixture.prepare",
            preparation_version="1",
        )
        result: QeCalculatorInputBinding | QeCalculatorInputAdmissionFailure = (
            QeCalculatorInputAdmission(
                QeCalculatorInputAdmissionPolicyIdentity(
                    "ksd.qe.calculator-input-admission:1"
                )
            ).execute(record, request.execution_input)
        )
        assert type(result) is QeCalculatorInputBinding
        return result

    @classmethod
    def stage(
        cls, prepared: LocalQePreparedExecution
    ) -> QeStagedExecution | QeStagingFailure:
        """Stage one prepared fixture with its directly admitted provider input."""
        return QeInputStager("qe-input-stager:1").execute(
            prepared, prepared.calculator_input_binding
        )

    @classmethod
    def prepare(
        cls,
        request: LocalQeExecutionPreparationRequest,
        *,
        preparer: LocalQeExecutionPreparer | None = None,
        native_bytes: bytes | None = None,
    ) -> LocalQePreparedExecution | LocalQePreparationFailure:
        """Prepare one request with its exact admitted provider-input binding."""
        selected_preparer: LocalQeExecutionPreparer = (
            cls.preparer() if preparer is None else preparer
        )
        binding: QeCalculatorInputBinding = cls.calculator_input_binding(
            request, native_bytes=native_bytes
        )
        return selected_preparer.execute(request, binding)

    @classmethod
    def preparer(
        cls,
        *,
        supported_version: str = "fixture-pw-v1",
        executable_content_identity: ArtifactContentIdentity | None = None,
    ) -> LocalQeExecutionPreparer:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        catalog = QeDiagnosticCatalog.fixture_pw_v1()
        return LocalQeExecutionPreparer(
            implementation_identity=(
                LocalQePreparationImplementationIdentity(
                    "qe-local-execution-preparer:1"
                )
            ),
            supported_bindings=(
                LocalQeSupportedExecutableBinding(
                    executable_configuration_identity=(
                        QeExecutableConfigurationIdentity("fixture.configuration")
                    ),
                    executable_content_identity=(
                        cls.content_identity(cls.resource("executable/fixture_pw.py"))
                        if executable_content_identity is None
                        else executable_content_identity
                    ),
                    program=QeProgram.PW,
                    executable_kind=(QeExecutableKind.DETERMINISTIC_FIXTURE),
                    program_version=supported_version,
                    classifier_identity=catalog.classifier_identity,
                ),
            ),
        )

    @classmethod
    def request(
        cls,
        run_root: Path,
        *,
        native_content: bytes | None = None,
        pseudopotential_source: Path | None = None,
        executable_source: Path | None = None,
        executable_content_identity: ArtifactContentIdentity | None = None,
        workspace_name: str = "attempt-001",
        minimum_free_bytes: int = 0,
        include_predecessor: bool = False,
        argument_suffix: tuple[str, ...] = ("--fixture-mode",),
        wall_time_milliseconds: int = 2_000,
        termination_grace_milliseconds: int = 100,
        maximum_created_entry_count: int = 100,
        maximum_created_total_bytes: int = 1_000_000,
    ) -> LocalQeExecutionPreparationRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        executable = (
            cls.resource("executable/fixture_pw.py")
            if executable_source is None
            else executable_source
        )
        default_native_content: bytes = cls.resource("input/pw.in").read_bytes()
        selected_native_content: bytes = (
            default_native_content if native_content is None else native_content
        )
        pseudo_identity_source: Path = cls.resource("pseudo/Si.fixture.UPF")
        pseudo_source: Path = (
            pseudo_identity_source
            if pseudopotential_source is None
            else pseudopotential_source
        )
        predecessor = cls.resource("predecessor/Si.save")
        executable_identity = (
            cls.content_identity(executable)
            if executable_content_identity is None
            else executable_content_identity
        )
        native_artifact = QeNativeInputArtifact(
            identity=ArtifactIdentity("artifact.input"),
            content=QeFileArtifactContent(
                ArtifactContentIdentity(
                    "sha256",
                    hashlib.sha256(selected_native_content).hexdigest(),
                    len(selected_native_content),
                )
            ),
            destination=QeArtifactDestination("input/pw.in"),
        )
        pseudo_artifact = QePseudopotentialArtifact(
            identity=ArtifactIdentity("artifact.pseudo"),
            content=QeFileArtifactContent(cls.content_identity(pseudo_identity_source)),
            destination=QeArtifactDestination("pseudo/Si.fixture.UPF"),
        )
        predecessor_artifacts: tuple[QePredecessorNativeStateArtifact, ...] = ()
        if include_predecessor:
            predecessor_artifacts = (
                QePredecessorNativeStateArtifact(
                    identity=ArtifactIdentity("artifact.state"),
                    content=QeTreeArtifactContent(
                        manifest_identity=ArtifactManifestIdentity(
                            _TREE_MANIFEST_IDENTITY_VALUE
                        ),
                        manifest_entry_identities=(
                            ArtifactManifestEntryIdentity(_TREE_ENTRY_IDENTITY_VALUE),
                        ),
                    ),
                    destination=QeArtifactDestination("work/Si.save"),
                    predecessor_result_identity=ResultObjectIdentity(
                        "result.predecessor"
                    ),
                    predecessor_manifest_entry_identity=(
                        ArtifactManifestEntryIdentity(_TREE_ENTRY_IDENTITY_VALUE)
                    ),
                ),
            )
        execution_input = QeExecutionInput(
            identity=QeExecutionInputIdentity("qe.input.001"),
            program=QeProgram.PW,
            native_input=native_artifact,
            pseudopotentials=(pseudo_artifact,),
            predecessor_native_state=predecessor_artifacts,
            task_definition_identity=TaskDefinitionIdentity("task.definition"),
            task_instance_identity=TaskInstanceIdentity("task.instance"),
            activation_identity=TaskActivationIdentity("task.activation"),
            operation_identity=OperationIdentity("operation.001"),
            attempt_identity=AttemptIdentity("attempt.001"),
            contract_version="qe-execution-input:1",
        )
        configuration = QeExecutableConfiguration(
            identity=QeExecutableConfigurationIdentity("fixture.configuration"),
            program=QeProgram.PW,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=executable_identity,
            program_version="fixture-pw-v1",
            argument_suffix=argument_suffix,
            environment_additions=(("OMP_NUM_THREADS", "1"),),
            classifier_identity=(
                QeDiagnosticCatalog.fixture_pw_v1().classifier_identity
            ),
            contract_version="qe-executable-configuration:1",
        )
        sources: list[LocalQeArtifactSource] = [
            LocalQeArtifactSource(pseudo_artifact.identity, pseudo_source),
        ]
        if include_predecessor:
            sources.append(
                LocalQeArtifactSource(
                    predecessor_artifacts[0].identity,
                    predecessor,
                )
            )
        return LocalQeExecutionPreparationRequest(
            execution_input=execution_input,
            executable_configuration=configuration,
            executable_path=executable,
            executable_content_identity=executable_identity,
            executable_destination=QeArtifactDestination("integration/executable"),
            authorized_run_root=run_root,
            attempt_workspace_name=LocalQeAttemptWorkspaceName(workspace_name),
            external_artifact_sources=tuple(
                sorted(sources, key=lambda value: value.artifact_identity.value)
            ),
            limits=LocalQeExecutionLimits(
                wall_time_milliseconds=wall_time_milliseconds,
                termination_grace_milliseconds=termination_grace_milliseconds,
                minimum_free_bytes=minimum_free_bytes,
                maximum_created_entry_count=maximum_created_entry_count,
                maximum_created_total_bytes=maximum_created_total_bytes,
                peak_resident_bytes=(LocalQePeakResidentBytesUnlimited()),
            ),
            stdout_destination=QeArtifactDestination("streams/stdout"),
            stderr_destination=QeArtifactDestination("streams/stderr"),
            before_snapshot_destination=QeArtifactDestination(
                "records/before.snapshot"
            ),
            after_snapshot_destination=QeArtifactDestination("records/after.snapshot"),
            execution_record_destination=QeArtifactDestination(
                "records/execution.json"
            ),
            terminal_record_destination=QeArtifactDestination("records/terminal.json"),
            work_destination=QeArtifactDestination("work"),
            result_destination=QeArtifactDestination("results"),
            simulation_execution_request_identity=SimulationExecutionRequestIdentity(
                "dispatch.request"
            ),
            scientific_executor_identity=ScientificExecutorIdentity("executor.fixture"),
            dispatch_destination_identity=DispatchDestinationIdentity(
                "destination.local"
            ),
            dispatch_resource_scope_identity=DispatchResourceScopeIdentity(
                "resources.fixture"
            ),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.fixture")
            ),
        )

    @classmethod
    def run_process(
        cls,
        run_root: Path,
        *,
        argument_suffix: tuple[str, ...],
        wall_time_milliseconds: int = 2_000,
        termination_grace_milliseconds: int = 100,
        maximum_created_entry_count: int = 100,
        maximum_created_total_bytes: int = 1_000_000,
    ) -> tuple[
        LocalQePreparedExecution,
        QeStagedExecution,
        LocalQeCapturedProcess | LocalQeProcessFailure,
    ]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        prepared = cls.prepare(
            cls.request(
                run_root,
                argument_suffix=argument_suffix,
                wall_time_milliseconds=wall_time_milliseconds,
                termination_grace_milliseconds=termination_grace_milliseconds,
                maximum_created_entry_count=maximum_created_entry_count,
                maximum_created_total_bytes=maximum_created_total_bytes,
            )
        )
        assert type(prepared) is LocalQePreparedExecution
        staged = cls.stage(prepared)
        assert type(staged) is QeStagedExecution
        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QeWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )
        return prepared, staged, result

    def test_method__execute__valid_request_is_read_only_and_dry_run_ready(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-001

        Requirement: Valid preparation observes exact inputs and resolves destinations
        without creating the absent workspace or invoking the fixture executable.

        Acceptance: The result is prepared, root-confined, dry-run output states that
        no effect occurred, and the run root remains byte-for-byte unmodified.
        """
        run_root = tmp_path.resolve()
        before = tuple(run_root.iterdir())
        request = self.request(run_root)

        result = self.prepare(request)

        assert type(result) is LocalQePreparedExecution
        assert tuple(run_root.iterdir()) == before
        assert not result.workspace.exists()
        assert result.argv == (
            str(run_root / "attempt-001/integration/executable"),
            "--fixture-mode",
        )
        assert all(
            destination.absolute_path.is_relative_to(result.workspace)
            for destination in result.resolved_destinations
        )
        assert all(
            type(observation) is LocalQeFileSourceObservation
            for observation in result.source_observations
        )
        dry_run = self.preparer().render_dry_run(result)
        assert "effect=not_performed\n" in dry_run
        assert "environment_key[0]=OMP_NUM_THREADS\n" in dry_run
        assert "destination[stdout:stdout]=streams/stdout\n" in dry_run
        assert tuple(run_root.iterdir()) == before

    def test_method__execute__predecessor_tree_verifies_exact_local_manifest(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-002

        Requirement: Read-only preparation verifies predecessor native state with the
        integration-local deterministic tree-manifest convention.

        Acceptance: The prepared result contains the exact declared manifest and the
        source resource is unchanged.
        """
        run_root = tmp_path.resolve()
        predecessor_file = self.resource("predecessor/Si.save/data-file-schema.xml")
        before = self.content_identity(predecessor_file)

        result = self.prepare(self.request(run_root, include_predecessor=True))

        assert type(result) is LocalQePreparedExecution
        tree_observations = tuple(
            observation
            for observation in result.source_observations
            if type(observation) is LocalQeTreeSourceObservation
        )
        assert len(tree_observations) == 1
        assert tree_observations[0].manifest_identity == ArtifactManifestIdentity(
            _TREE_MANIFEST_IDENTITY_VALUE
        )
        assert tree_observations[0].regular_file_total_bytes == 73
        assert self.content_identity(predecessor_file) == before
        assert tuple(run_root.iterdir()) == ()

    def test_method__execute__missing_source_returns_failure_without_workspace(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-003

        Requirement: A missing input source fails closed before mutation.

        Acceptance: The result has ``missing_source`` and the workspace is absent.
        """
        run_root = tmp_path.resolve()
        result = self.prepare(
            self.request(
                run_root,
                pseudopotential_source=run_root / "missing.UPF",
            )
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is LocalQePreparationFailureCode.MISSING_SOURCE
        assert not (run_root / "attempt-001").exists()

    def test_method__execute__executable_identity_mismatch_returns_failure(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-004

        Requirement: Executable bytes must equal the exact declared SHA-256 and byte
        count before a workspace may be created.

        Acceptance: Mismatch is represented as ``executable_identity_mismatch``.
        """
        wrong = ArtifactContentIdentity("sha256", "0" * 64, 1)
        request: LocalQeExecutionPreparationRequest = self.request(
            tmp_path.resolve(), executable_content_identity=wrong
        )
        result = self.prepare(
            request,
            preparer=self.preparer(executable_content_identity=wrong),
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is (
            LocalQePreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH
        )
        assert tuple(tmp_path.iterdir()) == ()

    @pytest.mark.parametrize(
        ("executable_kind", "expected_code"),
        [
            pytest.param(
                "missing",
                LocalQePreparationFailureCode.MISSING_SOURCE,
                id="missing",
            ),
            pytest.param(
                "directory",
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                id="not-regular",
            ),
            pytest.param(
                "symlink",
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                id="symbolic-link",
            ),
            pytest.param(
                "non-runnable",
                LocalQePreparationFailureCode.EXECUTABLE_NOT_RUNNABLE,
                id="not-executable",
            ),
        ],
    )
    def test_method__execute__provider_executable_path_failures_map_exactly(
        self,
        tmp_path: Path,
        executable_kind: str,
        expected_code: LocalQePreparationFailureCode,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-004A

        Requirement: Provider path/type/mode failures map to the exact KSD preparation
        vocabulary without process invocation or workspace mutation.

        Acceptance: Missing, non-regular, symbolic-link, and non-runnable executable
        deployments return their declared KSD failure codes and leave the root empty.
        """
        fixture = self.resource("executable/fixture_pw.py")
        expected_identity = self.content_identity(fixture)
        executable = tmp_path / "candidate"
        if executable_kind == "directory":
            executable.mkdir()
        elif executable_kind == "symlink":
            executable.symlink_to(fixture)
        elif executable_kind == "non-runnable":
            executable.write_bytes(fixture.read_bytes())
            executable.chmod(0o600)
        elif executable_kind != "missing":
            raise AssertionError(f"unsupported test executable kind: {executable_kind}")

        result = self.prepare(
            self.request(
                tmp_path.resolve(),
                executable_source=executable,
                executable_content_identity=expected_identity,
            )
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is expected_code
        assert not (tmp_path / "attempt-001").exists()
        assert not (tmp_path / "fixture-was-invoked").exists()

    def test_method__execute__provider_digest_mismatch_maps_exactly(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-004B

        Requirement: Equal-size executable bytes with a wrong SHA-256 fail through the
        provider and map to KSD executable identity mismatch.

        Acceptance: Preparation returns the exact code and performs no mutation or
        process invocation.
        """
        fixture = self.resource("executable/fixture_pw.py")
        wrong = ArtifactContentIdentity(
            "sha256", "0" * 64, self.content_identity(fixture).byte_count
        )
        request: LocalQeExecutionPreparationRequest = self.request(
            tmp_path.resolve(), executable_content_identity=wrong
        )

        result = self.prepare(
            request,
            preparer=self.preparer(executable_content_identity=wrong),
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is (
            LocalQePreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH
        )
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__provider_observation_failure_maps_exactly(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-004C

        Requirement: A provider observation failure remains distinguishable from byte
        identity, path-type, and runnable-mode failures.

        Acceptance: KSD returns ``executable_observation_failed`` without mutation or
        process invocation.
        """

        def fail_observation(
            preparer: CalculatorExecutablePreparer,
        ) -> CalculatorExecutablePreparationFailure:
            return CalculatorExecutablePreparationFailure(
                binding=preparer.binding,
                code=CalculatorExecutablePreparationFailureCode.OBSERVATION_FAILED,
                observed_condition="synthetic executable observation failure",
            )

        monkeypatch.setattr(CalculatorExecutablePreparer, "prepare", fail_observation)

        result = self.prepare(self.request(tmp_path.resolve()))

        assert type(result) is LocalQePreparationFailure
        assert result.code is (
            LocalQePreparationFailureCode.EXECUTABLE_OBSERVATION_FAILED
        )
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__existing_workspace_returns_failure_without_changes(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-005

        Requirement: Preparation never reuses or mutates an existing attempt
        workspace.

        Acceptance: Existing workspace is reported and its sentinel remains exact.
        """
        workspace = tmp_path / "attempt-001"
        workspace.mkdir()
        sentinel = workspace / "sentinel"
        sentinel.write_bytes(b"preserve")

        result = self.prepare(self.request(tmp_path.resolve()))

        assert type(result) is LocalQePreparationFailure
        assert result.code is (LocalQePreparationFailureCode.EXISTING_WORKSPACE)
        assert sentinel.read_bytes() == b"preserve"

    def test_method__execute__symlink_source_returns_failure_without_following(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-006

        Requirement: Input source paths containing symlinks are rejected before
        content staging or process entry.

        Acceptance: The result reports unsupported symlink/type and no workspace.
        """
        source_link = tmp_path / "Si-link.UPF"
        source_link.symlink_to(self.resource("pseudo/Si.fixture.UPF"))

        result = self.prepare(
            self.request(
                tmp_path.resolve(),
                pseudopotential_source=source_link,
            )
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is (LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE)
        assert not (tmp_path / "attempt-001").exists()

    def test_method__execute__unsupported_binding_fails_before_filesystem_observation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-007

        Requirement: Configuration, executable-content, program, version, and
        classifier support is an explicit composed allowlist rather than permissive
        backend discovery.

        Acceptance: A nonmatching version or executable identity returns
        ``unsupported_binding`` without creating a workspace.
        """
        result = self.prepare(
            self.request(tmp_path.resolve()),
            preparer=self.preparer(supported_version="fixture-pw-v2"),
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is (LocalQePreparationFailureCode.UNSUPPORTED_BINDING)
        request = self.request(tmp_path.resolve())
        mismatched_configuration = replace(
            request.executable_configuration,
            executable_content_identity=ArtifactContentIdentity("sha256", "f" * 64, 1),
        )
        content_mismatch_request: LocalQeExecutionPreparationRequest = replace(
            request,
            executable_configuration=mismatched_configuration,
            executable_content_identity=(
                mismatched_configuration.executable_content_identity
            ),
        )
        content_mismatch = self.prepare(content_mismatch_request)
        assert type(content_mismatch) is LocalQePreparationFailure
        assert content_mismatch.code is (
            LocalQePreparationFailureCode.UNSUPPORTED_BINDING
        )
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__insufficient_free_space_returns_sanitized_failure(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-008

        Requirement: The exact minimum-free-byte ceiling is checked read-only before
        workspace creation.

        Acceptance: An unattainable u64 requirement returns a typed failure without
        embedding source paths in its sanitized conditions.
        """
        result = self.prepare(
            self.request(tmp_path.resolve(), minimum_free_bytes=_MAX_U64)
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is (LocalQePreparationFailureCode.INSUFFICIENT_FREE_SPACE)
        assert "/" not in result.expected_condition
        assert "/" not in result.observed_condition
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__staging_and_snapshot_exact_inputs_produce_closed_manifest(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-009

        Requirement: Staging creates one absent workspace with exact declared inputs,
        and a bounded snapshot closes every directory and regular-file identity.

        Acceptance: Copied bytes agree, the predecessor tree is present, repeated
        before-snapshots are identical, and source resources remain unchanged.
        """
        prepared = self.prepare(
            self.request(tmp_path.resolve(), include_predecessor=True)
        )
        assert type(prepared) is LocalQePreparedExecution
        source_identity = self.content_identity(self.resource("input/pw.in"))

        staged = self.stage(prepared)

        assert type(staged) is QeStagedExecution
        assert (prepared.workspace / "input/pw.in").read_bytes() == self.resource(
            "input/pw.in"
        ).read_bytes()
        assert (prepared.workspace / "work/Si.save/data-file-schema.xml").is_file()
        assert prepared.workspace.stat().st_mode & 0o222 == 0
        assert (prepared.workspace / "integration").stat().st_mode & 0o222 == 0
        assert (prepared.workspace / "input").stat().st_mode & 0o222 == 0
        assert (prepared.workspace / "pseudo").stat().st_mode & 0o222 == 0
        snapshotter = QeWorkspaceSnapshotter("qe-snapshotter:1")
        first = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.BEFORE)
        second = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.BEFORE)
        assert type(first) is QeWorkspaceSnapshot
        assert type(second) is QeWorkspaceSnapshot
        assert first == second
        assert first.entry_count == len(first.entries)
        assert all(not entry.symlink_observed for entry in first.entries)
        assert self.content_identity(self.resource("input/pw.in")) == source_identity

    def test_method__execute__native_input_requires_no_local_source_path(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-010

        Requirement: Preparation and staging represent native input only through the
        execution-input identity and the exact admitted provider artifact bytes.

        Acceptance: No native-input source binding exists, and staging writes the
        exact custom provider bytes without reading an owner-local native-input path.
        """
        provider_bytes: bytes = b"synthetic provider-owned native input\n"
        request: LocalQeExecutionPreparationRequest = self.request(
            tmp_path.resolve(),
            native_content=provider_bytes,
        )
        prepared: LocalQePreparedExecution | LocalQePreparationFailure = self.prepare(
            request,
            native_bytes=provider_bytes,
        )
        assert type(prepared) is LocalQePreparedExecution
        assert all(
            source.artifact_identity
            != prepared.request.execution_input.native_input.identity
            for source in prepared.request.external_artifact_sources
        )
        binding: QeCalculatorInputBinding = prepared.calculator_input_binding

        result: QeStagedExecution | QeStagingFailure = QeInputStager(
            "qe-input-stager:1"
        ).execute(prepared, binding)

        assert type(result) is QeStagedExecution
        assert (prepared.workspace / "input/pw.in").read_bytes() == provider_bytes

    def test_method__execute__native_content_identity_changes_preparation_identity(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-031

        Requirement: Removing the local native-input source path must not remove the
        declared native content identity from preparation-result correlation.

        Acceptance: Two otherwise identical read-only requests with different native
        byte identities produce distinct preparation identities.
        """
        first_bytes: bytes = b"first provider input\n"
        second_bytes: bytes = b"second provider input\n"
        first: LocalQePreparedExecution | LocalQePreparationFailure = self.prepare(
            self.request(
                tmp_path.resolve(),
                native_content=first_bytes,
            ),
            native_bytes=first_bytes,
        )
        second: LocalQePreparedExecution | LocalQePreparationFailure = self.prepare(
            self.request(
                tmp_path.resolve(),
                native_content=second_bytes,
            ),
            native_bytes=second_bytes,
        )

        assert type(first) is LocalQePreparedExecution
        assert type(second) is LocalQePreparedExecution
        assert first.identity != second.identity
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__pseudopotential_source_change_rejects_before_mutation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-032

        Requirement: The exact provider external requirement governs pseudopotential
        identity while the KSD local source path remains a rechecked deployment input.

        Acceptance: Replacing source bytes after read-only preparation returns
        ``source_changed`` before the attempt workspace is created.
        """
        copied_source: Path = tmp_path / "Si.fixture.UPF"
        copied_source.write_bytes(self.resource("pseudo/Si.fixture.UPF").read_bytes())
        prepared: LocalQePreparedExecution | LocalQePreparationFailure = self.prepare(
            self.request(
                tmp_path.resolve(),
                pseudopotential_source=copied_source,
            )
        )
        assert type(prepared) is LocalQePreparedExecution
        external_resource: QeExternalInputResourceBinding = (
            prepared.calculator_input_binding.external_input_resources[0]
        )
        assert external_resource.external_requirement.sha256 == (
            self.content_identity(copied_source).digest
        )
        copied_source.write_bytes(b"changed after preparation\n")

        result: QeStagedExecution | QeStagingFailure = QeInputStager(
            "qe-input-stager:1"
        ).execute(prepared, prepared.calculator_input_binding)

        assert type(result) is QeStagingFailure
        assert result.code is QeStagingFailureCode.SOURCE_CHANGED
        assert not prepared.workspace.exists()

    def test_method__execute__input_binding_mismatch_rejects_before_observation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-033

        Requirement: Read-only preparation consumes the exact admitted provider/KSD
        binding rather than rediscovering or inferring external requirements.

        Acceptance: A binding for another execution-input instance fails before
        workspace mutation or local source observation.
        """
        request: LocalQeExecutionPreparationRequest = self.request(
            tmp_path.resolve(),
            pseudopotential_source=tmp_path / "missing.UPF",
        )
        other_execution_input: QeExecutionInput = replace(
            request.execution_input,
            identity=QeExecutionInputIdentity("qe.input.other"),
        )
        other_request: LocalQeExecutionPreparationRequest = replace(
            request,
            execution_input=other_execution_input,
        )
        other_binding: QeCalculatorInputBinding = self.calculator_input_binding(
            other_request
        )

        result: LocalQePreparedExecution | LocalQePreparationFailure = (
            self.preparer().execute(request, other_binding)
        )

        assert type(result) is LocalQePreparationFailure
        assert result.code is LocalQePreparationFailureCode.INPUT_BINDING_MISMATCH
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__binding_policy_mismatch_rejects_before_mutation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-030

        Requirement: Staging independently reapplies the binding's explicit admission
        policy before creating the workspace.

        Acceptance: A binding containing an unsupported provider representation is
        rejected without workspace mutation.
        """
        prepared: LocalQePreparedExecution | LocalQePreparationFailure = self.prepare(
            self.request(tmp_path.resolve())
        )
        assert type(prepared) is LocalQePreparedExecution
        binding: QeCalculatorInputBinding = prepared.calculator_input_binding
        mismatched_binding: QeCalculatorInputBinding = replace(
            binding,
            calculator_input=replace(
                binding.calculator_input,
                representation="unsupported-representation",
            ),
        )

        result: QeStagedExecution | QeStagingFailure = QeInputStager(
            "qe-input-stager:1"
        ).execute(prepared, mismatched_binding)

        assert type(result) is QeStagingFailure
        assert result.code is QeStagingFailureCode.INPUT_BINDING_MISMATCH
        assert not prepared.workspace.exists()

    def test_method__execute__replaced_run_root_rejects_before_mutation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-013

        Requirement: Staging rechecks destination-root confinement immediately before
        creating the attempt workspace.

        Acceptance: A post-preparation root symlink yields a typed failure and no
        workspace is created through the substituted path.
        """
        run_root: Path = tmp_path / "run"
        run_root.mkdir()
        prepared: LocalQePreparedExecution | LocalQePreparationFailure = self.prepare(
            self.request(run_root.resolve())
        )
        assert type(prepared) is LocalQePreparedExecution
        binding: QeCalculatorInputBinding = prepared.calculator_input_binding
        moved_root: Path = tmp_path / "moved-run"
        run_root.rename(moved_root)
        run_root.symlink_to(moved_root, target_is_directory=True)

        result: QeStagedExecution | QeStagingFailure = QeInputStager(
            "qe-input-stager:1"
        ).execute(prepared, binding)

        assert type(result) is QeStagingFailure
        assert result.code is QeStagingFailureCode.SYMLINK_OR_TYPE
        assert not (moved_root / "attempt-001").exists()

    def test_method__execute__explicit_candidates_preserve_empty_stream(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-011

        Requirement: Native collection uses only explicit operation/version candidate
        paths from a closed after-snapshot and retains zero-byte stream evidence.

        Acceptance: Both streams and one native result are represented with exact
        content identities; an unsupported symlink makes snapshot closure fail.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        (prepared.workspace / "streams/stdout").write_bytes(b"JOB DONE.\n")
        (prepared.workspace / "streams/stderr").write_bytes(b"")
        (prepared.workspace / "results/native.dat").write_bytes(b"synthetic\n")
        snapshotter = QeWorkspaceSnapshotter("qe-snapshotter:1")
        after = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.AFTER)
        assert type(after) is QeWorkspaceSnapshot
        candidates = (
            QeNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.native-result"),
                role=QeNativeOutputRole.NATIVE_RESULT,
                relative_path=QeArtifactDestination("results/native.dat"),
                entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
            QeNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.stderr"),
                role=QeNativeOutputRole.STDERR,
                relative_path=QeArtifactDestination("streams/stderr"),
                entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
            QeNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                role=QeNativeOutputRole.STDOUT,
                relative_path=QeArtifactDestination("streams/stdout"),
                entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
        )
        specification = QeNativeOutputExtractionSpecification(
            identity="fixture-pw-output-specification:1",
            executable_configuration_identity=(
                prepared.request.executable_configuration.identity
            ),
            program=QeProgram.PW,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            program_version="fixture-pw-v1",
            candidates=candidates,
        )

        manifest = QeNativeOutputCollector("qe-native-output-collector:1").execute(
            after, specification
        )

        assert type(manifest) is QeNativeOutputManifest
        assert len(manifest.entries) == 3
        stderr = next(
            entry
            for entry in manifest.entries
            if entry.role is QeNativeOutputRole.STDERR
        )
        assert type(stderr.content) is QeFileArtifactContent
        assert stderr.content.content_identity.byte_count == 0
        (prepared.workspace / "results/unsafe-link").symlink_to(
            prepared.workspace / "results/native.dat"
        )
        failed = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.AFTER)
        assert type(failed) is QeWorkspaceSnapshotFailure
        assert failed.code is (QeWorkspaceSnapshotFailureCode.SYMLINK_OR_TYPE)

    def test_method__execute__terminal_publication_is_atomic_no_replace(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-012

        Requirement: Private v2 terminal bytes are deterministic and publication is
        same-directory, atomic, durable, and no-replace.

        Acceptance: Publication exceeding the declared transient ceiling fails before
        mutation; the exact admitted bytes appear once and a second publication
        preserves them.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        stdout_identity = ArtifactContentIdentity("sha256", "1" * 64, 10)
        stderr_identity = ArtifactContentIdentity("sha256", "2" * 64, 0)
        record = QeTerminalRecord(
            identity=QeTerminalRecordIdentity("terminal.record.001"),
            status=QeTerminalStatus.COMPLETED,
            simulation_execution_request_identity=(
                prepared.request.simulation_execution_request_identity
            ),
            execution_input_identity=prepared.request.execution_input.identity,
            preparation_identity=prepared.identity,
            process_observation_identity=QeProcessObservationIdentity(
                "process.observation.001"
            ),
            stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
            stdout_content_identity=stdout_identity,
            stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            stderr_content_identity=stderr_identity,
            before_snapshot_identity=ArtifactManifestIdentity("snapshot.before"),
            after_snapshot_identity=ArtifactManifestIdentity("snapshot.after"),
            execution_record_manifest_entry_identity=ArtifactManifestEntryIdentity(
                "execution.record.entry.001"
            ),
            execution_record_content_identity=ArtifactContentIdentity(
                "sha256", "3" * 64, 100
            ),
            execution_record_publication_snapshot_identity=ArtifactManifestIdentity(
                "snapshot.execution-record"
            ),
            diagnostic_report_identity=QeDiagnosticReportIdentity(
                "diagnostic.report.001"
            ),
            native_output_manifest_identity=ArtifactManifestIdentity(
                "native.manifest.001"
            ),
        )
        record_artifact = QeTerminalRecordSerializer().execute(record)
        assert type(record_artifact) is QeTerminalRecordArtifact
        serialized = record_artifact.content
        snapshotter = QeWorkspaceSnapshotter("qe-snapshotter:1")
        publisher = QeTerminalRecordPublisher("qe-publisher:1", snapshotter)
        current = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.AFTER)
        assert type(current) is QeWorkspaceSnapshot
        constrained = replace(
            prepared,
            request=replace(
                prepared.request,
                limits=replace(
                    prepared.request.limits,
                    maximum_created_entry_count=current.entry_count + 2,
                    maximum_created_total_bytes=(
                        current.regular_file_total_bytes + 2 * len(serialized) - 1
                    ),
                ),
            ),
        )
        limited = publisher.execute(constrained, record_artifact)
        assert type(limited) is QeTerminalPublicationFailure
        assert limited.code is (QeTerminalPublicationFailureCode.LIMIT_EXCEEDED)
        assert not (
            prepared.workspace / prepared.request.terminal_record_destination.value
        ).exists()

        published = publisher.execute(prepared, record_artifact)

        assert type(published) is QePublishedTerminalRecord
        assert published.destination.read_bytes() == serialized
        second = publisher.execute(prepared, record_artifact)
        assert type(second) is QeTerminalPublicationFailure
        assert second.code is (QeTerminalPublicationFailureCode.DESTINATION_EXISTS)
        assert published.destination.read_bytes() == serialized

    def test_method__execute__process_runner_success_captures_streams_and_normal_exit(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-014

        Requirement: One fixture process uses exact argv, working directory, stdin,
        and distinct no-replace stream files.

        Acceptance: Exit zero, both exact streams, and before/after snapshots are
        retained in one immutable mechanical observation.
        """
        prepared, _, result = self.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-mode",)
        )

        assert type(result) is LocalQeCapturedProcess
        assert type(result.observation.termination) is QeNormalProcessExit
        assert (
            result.observation.termination.disposition
            is CalculatorExitDisposition.succeeded
        )
        assert result.stdout_bytes == b"JOB DONE.\n"
        assert result.stderr_bytes == (
            b"DIAGNOSTIC: NONBLOCKING synthetic floating-point notice\n"
        )
        assert result.observation.stdout.artifact_identity == ArtifactIdentity(
            "artifact.stdout"
        )
        assert result.observation.stderr.artifact_identity == ArtifactIdentity(
            "artifact.stderr"
        )
        assert result.before_snapshot.phase is (QeWorkspaceSnapshotPhase.BEFORE)
        assert result.after_snapshot.phase is QeWorkspaceSnapshotPhase.AFTER
        assert (
            prepared.workspace / "streams/stdout"
        ).read_bytes() == result.stdout_bytes
        assert (
            prepared.workspace / "streams/stderr"
        ).read_bytes() == result.stderr_bytes
        before_record = prepared.workspace / "records/before.snapshot"
        after_record = prepared.workspace / "records/after.snapshot"
        assert (
            result.before_snapshot.identity.value.encode() in before_record.read_bytes()
        )
        assert (
            result.after_snapshot.identity.value.encode() in after_record.read_bytes()
        )

    def test_method__execute__stdin_recheck_preserves_descriptor_position(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-028

        Requirement: Exact native-input descriptor verification must not consume the
        process stdin stream before entry.

        Acceptance: The deterministic fixture reads and echoes every exact staged
        native-input byte after the runner's descriptor identity recheck.
        """
        _prepared, _staged, result = self.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-echo-stdin",)
        )

        assert type(result) is LocalQeCapturedProcess
        assert result.stdout_bytes == self.resource("input/pw.in").read_bytes()
        assert result.stderr_bytes == b""

    def test_method__execute__process_runner_empty_stderr_retains_zero_byte_artifact(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-015

        Requirement: Empty stderr remains a distinct exact captured artifact.

        Acceptance: The stderr bytes and content byte count are both exactly zero.
        """
        _, _, result = self.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-empty-stderr",)
        )

        assert type(result) is LocalQeCapturedProcess
        assert result.stderr_bytes == b""
        assert result.observation.stderr.content_identity.byte_count == 0
        assert result.observation.stdout.content_identity.byte_count > 0

    def test_method__execute__process_runner_nonzero_exit_is_determinate_observation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-016

        Requirement: A closed nonzero process exit is mechanical result evidence, not
        an integration exception or implied calculator classification.

        Acceptance: Exit code three and both exact streams are retained.
        """
        _, _, result = self.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-fail",)
        )

        assert type(result) is LocalQeCapturedProcess
        assert type(result.observation.termination) is QeNormalProcessExit
        assert (
            result.observation.termination.disposition
            is CalculatorExitDisposition.failed
        )
        assert result.stdout_bytes == b"FIXTURE PROCESS FAILURE\n"
        assert result.stderr_bytes == b"FIXTURE STDERR\n"

    def test_method__execute__process_runner_signal_exit_records_positive_signal(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-017

        Requirement: Determinate signal termination is distinct from normal exit.

        Acceptance: The observation records a positive SIGTERM number.
        """
        _, _, result = self.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-signal",)
        )

        assert type(result) is LocalQeCapturedProcess
        assert type(result.observation.termination) is (QeProcessSignalTermination)
        assert result.observation.termination.signal_number > 0

    def test_method__execute__timeout_terminates_group_and_closes_capture(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-018

        Requirement: Wall-time expiry performs bounded process-group cleanup and
        returns timeout only after both stream captures close.

        Acceptance: Timeout retains the exact limit, records termination delivery,
        and preserves the fixture's flushed pre-timeout stdout.
        """
        _, _, result = self.run_process(
            tmp_path.resolve(),
            argument_suffix=("--fixture-timeout",),
            wall_time_milliseconds=2_000,
            termination_grace_milliseconds=100,
        )

        assert type(result) is LocalQeCapturedProcess
        assert type(result.observation.termination) is QeProcessTimeout
        assert result.observation.termination.timeout_milliseconds == 2_000
        assert result.observation.termination.termination_sent
        assert result.stdout_bytes == b"FIXTURE ENTERED\n"

    def test_method__execute__pre_spawn_time_counts_toward_timeout(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-029

        Requirement: The wall-time deadline uses the monotonic origin captured before
        process creation and checks expiry before accepting a polled exit.

        Acceptance: A synthetic clock already beyond the deadline immediately after
        spawn produces a timeout rather than a normal exit.
        """
        monkeypatch.setattr(
            "ksdft2effmass.integration.quantum_espresso.process.time.monotonic_ns",
            Mock(side_effect=(1_000_000, 21_000_000, 22_000_000)),
        )

        _prepared, _staged, result = self.run_process(
            tmp_path.resolve(),
            argument_suffix=("--fixture-empty-stderr",),
            wall_time_milliseconds=10,
        )

        assert type(result) is LocalQeCapturedProcess
        assert type(result.observation.termination) is QeProcessTimeout
        assert result.observation.wall_duration_nanoseconds == 21_000_000

    def test_method__execute__process_runner_stream_race_rejects_without_process_entry(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-019

        Requirement: Stream capture destinations are opened with no-replace semantics.

        Acceptance: A post-staging destination race is rejected before process entry
        and preserves the preexisting bytes.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        stdout_path = prepared.workspace / "streams/stdout"
        stdout_path.write_bytes(b"preserve")

        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QeWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is (LocalQeProcessFailureCode.STREAM_DESTINATION_EXISTS)
        assert result.disposition is (LocalQeProcessFailureDisposition.REJECTED)
        assert not result.process_entered
        assert stdout_path.read_bytes() == b"preserve"

    def test_method__execute__process_runner_staged_input_changed_rejects_before_entry(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-020

        Requirement: The process boundary rechecks every staged input identity after
        its before-snapshot and before opening process streams.

        Acceptance: Mutated native input is rejected without process entry or stream
        artifacts.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        staged_input = prepared.workspace / "input/pw.in"
        staged_input.chmod(0o600)
        staged_input.write_bytes(b"changed\n")

        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QeWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is (LocalQeProcessFailureCode.INPUT_IDENTITY_CHANGED)
        assert not result.process_entered
        assert not (prepared.workspace / "streams/stdout").exists()
        assert not (prepared.workspace / "streams/stderr").exists()

    def test_method__execute__process_runner_spawn_failure_rejects_before_process_entry(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-021

        Requirement: A deterministic operating-system process-creation failure is a
        pre-entry rejection rather than calculator evidence.

        Acceptance: The runner returns ``spawn_failed`` with ``process_entered``
        false and no process observation.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        monkeypatch.setattr(
            "ksdft2effmass.integration.quantum_espresso.process.subprocess.Popen",
            Mock(side_effect=OSError("synthetic spawn failure")),
        )

        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QeWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is LocalQeProcessFailureCode.SPAWN_FAILED
        assert not result.process_entered

    def test_method__execute__before_snapshot_failure_rejects_before_entry(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-022

        Requirement: An unsupported workspace entry before process entry prevents
        dispatch from entering the executable effect.

        Acceptance: A symlink yields ``before_snapshot_failed`` and a rejected
        pre-entry process result.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        (prepared.workspace / "work/unsupported-link").symlink_to("missing")

        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QeWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is (LocalQeProcessFailureCode.BEFORE_SNAPSHOT_FAILED)
        assert not result.process_entered

    def test_method__execute__snapshot_publication_limit_rejects_before_entry(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-027

        Requirement: Private snapshot publication remains inside the declared
        transient workspace entry ceiling.

        Acceptance: A ceiling with room for only one publication entry fails before
        the temporary file and hard-link pair or process can be entered.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        snapshotter = QeWorkspaceSnapshotter("qe-snapshotter:1")
        current = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.BEFORE)
        assert type(current) is QeWorkspaceSnapshot
        constrained = replace(
            prepared,
            request=replace(
                prepared.request,
                limits=replace(
                    prepared.request.limits,
                    maximum_created_entry_count=current.entry_count + 1,
                ),
            ),
        )

        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=snapshotter,
        ).execute(
            constrained,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is (LocalQeProcessFailureCode.BEFORE_SNAPSHOT_FAILED)
        assert not result.process_entered
        assert not (
            prepared.workspace / prepared.request.before_snapshot_destination.value
        ).exists()

    def test_method__execute__process_runner_after_snapshot_failure_is_indeterminate(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-023

        Requirement: Unsupported workspace state produced after process entry cannot
        become a determinate calculator result.

        Acceptance: A deterministic second-snapshot observation failure yields
        ``after_snapshot_failed`` with an indeterminate post-entry process result.
        """
        prepared = self.prepare(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        snapshotter = QeWorkspaceSnapshotter("qe-snapshotter:1")
        before = snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.BEFORE)
        assert type(before) is QeWorkspaceSnapshot
        after_failure = QeWorkspaceSnapshotFailure(
            code=QeWorkspaceSnapshotFailureCode.OBSERVATION_FAILED,
            phase=QeWorkspaceSnapshotPhase.AFTER,
            preparation_identity=prepared.identity,
            observed_condition="synthetic after-snapshot observation failure",
        )
        monkeypatch.setattr(
            QeWorkspaceSnapshotter,
            "execute",
            Mock(side_effect=(before, after_failure)),
        )

        result = LocalQeProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=snapshotter,
        ).execute(
            prepared,
            staged,
            LocalQeStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is (LocalQeProcessFailureCode.AFTER_SNAPSHOT_FAILED)
        assert result.process_entered
        assert result.disposition is (LocalQeProcessFailureDisposition.INDETERMINATE)

    def test_method__execute__output_byte_limit_terminates_and_fails_closed(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-024

        Requirement: Process execution actively observes the aggregate workspace-byte
        ceiling and never loads an over-limit stream into memory.

        Acceptance: A synthetic 64-KiB stream against a 20-KiB ceiling terminates and
        returns ``output_limit_exceeded`` as post-entry uncertainty.
        """
        _, _, result = self.run_process(
            tmp_path.resolve(),
            argument_suffix=("--fixture-output-limit",),
            maximum_created_total_bytes=20_000,
        )

        assert type(result) is LocalQeProcessFailure
        assert result.code is (LocalQeProcessFailureCode.OUTPUT_LIMIT_EXCEEDED)
        assert result.process_entered

    def test_method__execute__entry_limit_returns_typed_failure(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-025

        Requirement: Workspace snapshots fail closed when the aggregate entry count
        exceeds the declared ceiling.

        Acceptance: Added zero-byte synthetic files produce ``entry_limit_exceeded``.
        """
        prepared = self.prepare(
            self.request(tmp_path.resolve(), maximum_created_entry_count=20)
        )
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        result_root = prepared.workspace / "results"
        (result_root / "entry-00").write_bytes(b"")
        (result_root / "entry-01").write_bytes(b"")
        (result_root / "entry-02").write_bytes(b"")
        (result_root / "entry-03").write_bytes(b"")
        (result_root / "entry-04").write_bytes(b"")
        (result_root / "entry-05").write_bytes(b"")
        (result_root / "entry-06").write_bytes(b"")
        (result_root / "entry-07").write_bytes(b"")
        (result_root / "entry-08").write_bytes(b"")
        (result_root / "entry-09").write_bytes(b"")
        (result_root / "entry-10").write_bytes(b"")
        (result_root / "entry-11").write_bytes(b"")
        (result_root / "entry-12").write_bytes(b"")
        (result_root / "entry-13").write_bytes(b"")
        (result_root / "entry-14").write_bytes(b"")
        (result_root / "entry-15").write_bytes(b"")
        (result_root / "entry-16").write_bytes(b"")
        (result_root / "entry-17").write_bytes(b"")
        (result_root / "entry-18").write_bytes(b"")
        (result_root / "entry-19").write_bytes(b"")

        result = QeWorkspaceSnapshotter("qe-snapshotter:1").execute(
            prepared, QeWorkspaceSnapshotPhase.AFTER
        )

        assert type(result) is QeWorkspaceSnapshotFailure
        assert result.code is (QeWorkspaceSnapshotFailureCode.ENTRY_LIMIT_EXCEEDED)

    def test_method__execute__snapshotter_byte_limit_fails_before_hashing_large_file(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-026

        Requirement: Snapshot byte admission checks file metadata against the
        remaining aggregate ceiling before reading file content.

        Acceptance: An over-limit synthetic file produces ``byte_limit_exceeded``.
        """
        prepared = self.prepare(
            self.request(tmp_path.resolve(), maximum_created_total_bytes=20_000)
        )
        assert type(prepared) is LocalQePreparedExecution
        staged = self.stage(prepared)
        assert type(staged) is QeStagedExecution
        (prepared.workspace / "results/large.dat").write_bytes(b"x" * 65_536)

        result = QeWorkspaceSnapshotter("qe-snapshotter:1").execute(
            prepared, QeWorkspaceSnapshotPhase.AFTER
        )

        assert type(result) is QeWorkspaceSnapshotFailure
        assert result.code is (QeWorkspaceSnapshotFailureCode.BYTE_LIMIT_EXCEEDED)
