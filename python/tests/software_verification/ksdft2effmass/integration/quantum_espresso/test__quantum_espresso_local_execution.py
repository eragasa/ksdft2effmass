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

import ksdft2effmass.integration.quantum_espresso.process as quantum_espresso_process
from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoArtifactSource,
    LocalQuantumEspressoAttemptWorkspaceName,
    LocalQuantumEspressoCapturedProcess,
    LocalQuantumEspressoExecutionLimits,
    LocalQuantumEspressoExecutionPreparationRequest,
    LocalQuantumEspressoExecutionPreparer,
    LocalQuantumEspressoFileSourceObservation,
    LocalQuantumEspressoPeakResidentBytesUnlimited,
    LocalQuantumEspressoPreparationFailure,
    LocalQuantumEspressoPreparationFailureCode,
    LocalQuantumEspressoPreparationImplementationIdentity,
    LocalQuantumEspressoPreparedExecution,
    LocalQuantumEspressoProcessFailure,
    LocalQuantumEspressoProcessFailureCode,
    LocalQuantumEspressoProcessFailureDisposition,
    LocalQuantumEspressoProcessRunner,
    LocalQuantumEspressoStreamArtifactBindings,
    LocalQuantumEspressoSupportedExecutableBinding,
    LocalQuantumEspressoTreeSourceObservation,
    QuantumEspressoArtifactDestination,
    QuantumEspressoDiagnosticCatalog,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInput,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoInputStager,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoNativeOutputCandidateSpecification,
    QuantumEspressoNativeOutputCollector,
    QuantumEspressoNativeOutputExtractionSpecification,
    QuantumEspressoNativeOutputManifest,
    QuantumEspressoNativeOutputRole,
    QuantumEspressoNormalProcessExit,
    QuantumEspressoPredecessorNativeStateArtifact,
    QuantumEspressoProcessObservationIdentity,
    QuantumEspressoProcessSignalTermination,
    QuantumEspressoProcessTimeout,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
    QuantumEspressoPublishedTerminalRecord,
    QuantumEspressoStagedExecution,
    QuantumEspressoStagingFailure,
    QuantumEspressoStagingFailureCode,
    QuantumEspressoTerminalPublicationFailure,
    QuantumEspressoTerminalPublicationFailureCode,
    QuantumEspressoTerminalRecord,
    QuantumEspressoTerminalRecordIdentity,
    QuantumEspressoTerminalRecordPublisher,
    QuantumEspressoTerminalRecordSerializer,
    QuantumEspressoTerminalStatus,
    QuantumEspressoTreeArtifactContent,
    QuantumEspressoWorkspaceEntryType,
    QuantumEspressoWorkspaceSnapshot,
    QuantumEspressoWorkspaceSnapshotFailure,
    QuantumEspressoWorkspaceSnapshotFailureCode,
    QuantumEspressoWorkspaceSnapshotPhase,
    QuantumEspressoWorkspaceSnapshotter,
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

pytestmark = pytest.mark.software_verification

_MAX_U64 = 18_446_744_073_709_551_615
_TREE_MANIFEST_IDENTITY = (
    "qe-tree-manifest-v1:"
    "74a027967739800f98d6891eaad3f3458ba7e4abf09c6905a0c3c16caf6360fb"
)
_TREE_ENTRY_IDENTITY = (
    "qe-tree-entry-v1:c10e7c611f6bb78479dacc2184784f56295d7376cac9956aff7a17a42594dc3b"
)


class TestLocalQuantumEspressoExecutionPreparer:
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
    def preparer(
        cls,
        *,
        supported_version: str = "fixture-pw-v1",
        executable_content_identity: ArtifactContentIdentity | None = None,
    ) -> LocalQuantumEspressoExecutionPreparer:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        catalog = QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        return LocalQuantumEspressoExecutionPreparer(
            implementation_identity=(
                LocalQuantumEspressoPreparationImplementationIdentity(
                    "qe-local-execution-preparer:1"
                )
            ),
            supported_bindings=(
                LocalQuantumEspressoSupportedExecutableBinding(
                    executable_configuration_identity=(
                        QuantumEspressoExecutableConfigurationIdentity(
                            "fixture.configuration"
                        )
                    ),
                    executable_content_identity=(
                        cls.content_identity(cls.resource("executable/fixture_pw.py"))
                        if executable_content_identity is None
                        else executable_content_identity
                    ),
                    program=QuantumEspressoProgram.PW,
                    executable_kind=(
                        QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE
                    ),
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
        native_source: Path | None = None,
        executable_content_identity: ArtifactContentIdentity | None = None,
        workspace_name: str = "attempt-001",
        minimum_free_bytes: int = 0,
        include_predecessor: bool = False,
        argument_suffix: tuple[str, ...] = ("--fixture-mode",),
        wall_time_milliseconds: int = 2_000,
        termination_grace_milliseconds: int = 100,
        maximum_created_entry_count: int = 100,
        maximum_created_total_bytes: int = 1_000_000,
    ) -> LocalQuantumEspressoExecutionPreparationRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        executable = cls.resource("executable/fixture_pw.py")
        native = cls.resource("input/pw.in")
        pseudo = cls.resource("pseudo/Si.fixture.UPF")
        predecessor = cls.resource("predecessor/Si.save")
        executable_identity = (
            cls.content_identity(executable)
            if executable_content_identity is None
            else executable_content_identity
        )
        native_artifact = QuantumEspressoNativeInputArtifact(
            identity=ArtifactIdentity("artifact.input"),
            content=QuantumEspressoFileArtifactContent(cls.content_identity(native)),
            destination=QuantumEspressoArtifactDestination("input/pw.in"),
        )
        pseudo_artifact = QuantumEspressoPseudopotentialArtifact(
            identity=ArtifactIdentity("artifact.pseudo"),
            content=QuantumEspressoFileArtifactContent(cls.content_identity(pseudo)),
            destination=QuantumEspressoArtifactDestination("pseudo/Si.fixture.UPF"),
        )
        predecessor_artifacts: tuple[
            QuantumEspressoPredecessorNativeStateArtifact, ...
        ] = ()
        if include_predecessor:
            predecessor_artifacts = (
                QuantumEspressoPredecessorNativeStateArtifact(
                    identity=ArtifactIdentity("artifact.state"),
                    content=QuantumEspressoTreeArtifactContent(
                        manifest_identity=ArtifactManifestIdentity(
                            _TREE_MANIFEST_IDENTITY
                        ),
                        manifest_entry_identities=(
                            ArtifactManifestEntryIdentity(_TREE_ENTRY_IDENTITY),
                        ),
                    ),
                    destination=QuantumEspressoArtifactDestination("work/Si.save"),
                    predecessor_result_identity=ResultObjectIdentity(
                        "result.predecessor"
                    ),
                    predecessor_manifest_entry_identity=(
                        ArtifactManifestEntryIdentity("manifest.entry.predecessor")
                    ),
                ),
            )
        execution_input = QuantumEspressoExecutionInput(
            identity=QuantumEspressoExecutionInputIdentity("qe.input.001"),
            program=QuantumEspressoProgram.PW,
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
        configuration = QuantumEspressoExecutableConfiguration(
            identity=QuantumEspressoExecutableConfigurationIdentity(
                "fixture.configuration"
            ),
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=executable_identity,
            program_version="fixture-pw-v1",
            argument_suffix=argument_suffix,
            environment_additions=(("OMP_NUM_THREADS", "1"),),
            classifier_identity=(
                QuantumEspressoDiagnosticCatalog.fixture_pw_v1().classifier_identity
            ),
            contract_version="qe-executable-configuration:1",
        )
        sources = [
            LocalQuantumEspressoArtifactSource(
                native_artifact,
                native if native_source is None else native_source,
            ),
            LocalQuantumEspressoArtifactSource(pseudo_artifact, pseudo),
        ]
        if include_predecessor:
            sources.append(
                LocalQuantumEspressoArtifactSource(
                    predecessor_artifacts[0], predecessor
                )
            )
        return LocalQuantumEspressoExecutionPreparationRequest(
            execution_input=execution_input,
            executable_configuration=configuration,
            executable_path=executable,
            executable_content_identity=executable_identity,
            executable_destination=QuantumEspressoArtifactDestination(
                "integration/executable"
            ),
            authorized_run_root=run_root,
            attempt_workspace_name=LocalQuantumEspressoAttemptWorkspaceName(
                workspace_name
            ),
            artifact_sources=tuple(
                sorted(sources, key=lambda value: value.artifact.identity.value)
            ),
            limits=LocalQuantumEspressoExecutionLimits(
                wall_time_milliseconds=wall_time_milliseconds,
                termination_grace_milliseconds=termination_grace_milliseconds,
                minimum_free_bytes=minimum_free_bytes,
                maximum_created_entry_count=maximum_created_entry_count,
                maximum_created_total_bytes=maximum_created_total_bytes,
                peak_resident_bytes=(LocalQuantumEspressoPeakResidentBytesUnlimited()),
            ),
            stdout_destination=QuantumEspressoArtifactDestination("streams/stdout"),
            stderr_destination=QuantumEspressoArtifactDestination("streams/stderr"),
            before_snapshot_destination=QuantumEspressoArtifactDestination(
                "records/before.snapshot"
            ),
            after_snapshot_destination=QuantumEspressoArtifactDestination(
                "records/after.snapshot"
            ),
            terminal_record_destination=QuantumEspressoArtifactDestination(
                "records/terminal.json"
            ),
            work_destination=QuantumEspressoArtifactDestination("work"),
            result_destination=QuantumEspressoArtifactDestination("results"),
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
        LocalQuantumEspressoPreparedExecution,
        QuantumEspressoStagedExecution,
        LocalQuantumEspressoCapturedProcess | LocalQuantumEspressoProcessFailure,
    ]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        prepared = cls.preparer().execute(
            cls.request(
                run_root,
                argument_suffix=argument_suffix,
                wall_time_milliseconds=wall_time_milliseconds,
                termination_grace_milliseconds=termination_grace_milliseconds,
                maximum_created_entry_count=maximum_created_entry_count,
                maximum_created_total_bytes=maximum_created_total_bytes,
            )
        )
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
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

        result = self.preparer().execute(request)

        assert type(result) is LocalQuantumEspressoPreparedExecution
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
            type(observation) is LocalQuantumEspressoFileSourceObservation
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

        result = self.preparer().execute(
            self.request(run_root, include_predecessor=True)
        )

        assert type(result) is LocalQuantumEspressoPreparedExecution
        tree_observations = tuple(
            observation
            for observation in result.source_observations
            if type(observation) is LocalQuantumEspressoTreeSourceObservation
        )
        assert len(tree_observations) == 1
        assert tree_observations[0].manifest_identity == ArtifactManifestIdentity(
            _TREE_MANIFEST_IDENTITY
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
        result = self.preparer().execute(
            self.request(run_root, native_source=run_root / "missing.in")
        )

        assert type(result) is LocalQuantumEspressoPreparationFailure
        assert result.code is LocalQuantumEspressoPreparationFailureCode.MISSING_SOURCE
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
        result = self.preparer(executable_content_identity=wrong).execute(
            self.request(tmp_path.resolve(), executable_content_identity=wrong)
        )

        assert type(result) is LocalQuantumEspressoPreparationFailure
        assert result.code is (
            LocalQuantumEspressoPreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH
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

        result = self.preparer().execute(self.request(tmp_path.resolve()))

        assert type(result) is LocalQuantumEspressoPreparationFailure
        assert result.code is (
            LocalQuantumEspressoPreparationFailureCode.EXISTING_WORKSPACE
        )
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
        source_link = tmp_path / "pw-link.in"
        source_link.symlink_to(self.resource("input/pw.in"))

        result = self.preparer().execute(
            self.request(tmp_path.resolve(), native_source=source_link)
        )

        assert type(result) is LocalQuantumEspressoPreparationFailure
        assert result.code is (
            LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE
        )
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
        result = self.preparer(supported_version="fixture-pw-v2").execute(
            self.request(tmp_path.resolve())
        )

        assert type(result) is LocalQuantumEspressoPreparationFailure
        assert result.code is (
            LocalQuantumEspressoPreparationFailureCode.UNSUPPORTED_BINDING
        )
        request = self.request(tmp_path.resolve())
        mismatched_configuration = replace(
            request.executable_configuration,
            executable_content_identity=ArtifactContentIdentity("sha256", "f" * 64, 1),
        )
        content_mismatch = self.preparer().execute(
            replace(
                request,
                executable_configuration=mismatched_configuration,
                executable_content_identity=(
                    mismatched_configuration.executable_content_identity
                ),
            )
        )
        assert type(content_mismatch) is LocalQuantumEspressoPreparationFailure
        assert content_mismatch.code is (
            LocalQuantumEspressoPreparationFailureCode.UNSUPPORTED_BINDING
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
        result = self.preparer().execute(
            self.request(tmp_path.resolve(), minimum_free_bytes=_MAX_U64)
        )

        assert type(result) is LocalQuantumEspressoPreparationFailure
        assert result.code is (
            LocalQuantumEspressoPreparationFailureCode.INSUFFICIENT_FREE_SPACE
        )
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
        prepared = self.preparer().execute(
            self.request(tmp_path.resolve(), include_predecessor=True)
        )
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        source_identity = self.content_identity(self.resource("input/pw.in"))

        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)

        assert type(staged) is QuantumEspressoStagedExecution
        assert (prepared.workspace / "input/pw.in").read_bytes() == self.resource(
            "input/pw.in"
        ).read_bytes()
        assert (prepared.workspace / "work/Si.save/data-file-schema.xml").is_file()
        assert prepared.workspace.stat().st_mode & 0o222 == 0
        assert (prepared.workspace / "integration").stat().st_mode & 0o222 == 0
        assert (prepared.workspace / "input").stat().st_mode & 0o222 == 0
        assert (prepared.workspace / "pseudo").stat().st_mode & 0o222 == 0
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        first = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        )
        second = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        )
        assert type(first) is QuantumEspressoWorkspaceSnapshot
        assert type(second) is QuantumEspressoWorkspaceSnapshot
        assert first == second
        assert first.entry_count == len(first.entries)
        assert all(not entry.symlink_observed for entry in first.entries)
        assert self.content_identity(self.resource("input/pw.in")) == source_identity

    def test_method__execute__changed_staging_source_rejects_before_mutation(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-010

        Requirement: Staging reobserves prepared source identities before mutation.

        Acceptance: Changed bytes yield ``source_changed`` and no workspace exists.
        """
        copied_source = tmp_path / "prepared-input.in"
        copied_source.write_bytes(self.resource("input/pw.in").read_bytes())
        prepared = self.preparer().execute(
            self.request(tmp_path.resolve(), native_source=copied_source)
        )
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        copied_source.write_bytes(b"changed after preparation\n")

        result = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)

        assert type(result) is QuantumEspressoStagingFailure
        assert result.code is QuantumEspressoStagingFailureCode.SOURCE_CHANGED
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
        run_root = tmp_path / "run"
        run_root.mkdir()
        prepared = self.preparer().execute(self.request(run_root.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        moved_root = tmp_path / "moved-run"
        run_root.rename(moved_root)
        run_root.symlink_to(moved_root, target_is_directory=True)

        result = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)

        assert type(result) is QuantumEspressoStagingFailure
        assert result.code is QuantumEspressoStagingFailureCode.SYMLINK_OR_TYPE
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        (prepared.workspace / "streams/stdout").write_bytes(b"JOB DONE.\n")
        (prepared.workspace / "streams/stderr").write_bytes(b"")
        (prepared.workspace / "results/native.dat").write_bytes(b"synthetic\n")
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        after = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )
        assert type(after) is QuantumEspressoWorkspaceSnapshot
        candidates = (
            QuantumEspressoNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.native-result"),
                role=QuantumEspressoNativeOutputRole.NATIVE_RESULT,
                relative_path=QuantumEspressoArtifactDestination("results/native.dat"),
                entry_type=QuantumEspressoWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
            QuantumEspressoNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.stderr"),
                role=QuantumEspressoNativeOutputRole.STDERR,
                relative_path=QuantumEspressoArtifactDestination("streams/stderr"),
                entry_type=QuantumEspressoWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
            QuantumEspressoNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                role=QuantumEspressoNativeOutputRole.STDOUT,
                relative_path=QuantumEspressoArtifactDestination("streams/stdout"),
                entry_type=QuantumEspressoWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
        )
        specification = QuantumEspressoNativeOutputExtractionSpecification(
            identity="fixture-pw-output-specification:1",
            executable_configuration_identity=(
                prepared.request.executable_configuration.identity
            ),
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            program_version="fixture-pw-v1",
            candidates=candidates,
        )

        manifest = QuantumEspressoNativeOutputCollector(
            "qe-native-output-collector:1"
        ).execute(after, specification)

        assert type(manifest) is QuantumEspressoNativeOutputManifest
        assert len(manifest.entries) == 3
        stderr = next(
            entry
            for entry in manifest.entries
            if entry.role is QuantumEspressoNativeOutputRole.STDERR
        )
        assert type(stderr.content) is QuantumEspressoFileArtifactContent
        assert stderr.content.content_identity.byte_count == 0
        (prepared.workspace / "results/unsafe-link").symlink_to(
            prepared.workspace / "results/native.dat"
        )
        failed = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )
        assert type(failed) is QuantumEspressoWorkspaceSnapshotFailure
        assert failed.code is (
            QuantumEspressoWorkspaceSnapshotFailureCode.SYMLINK_OR_TYPE
        )

    def test_method__execute__terminal_publication_is_atomic_no_replace(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-012

        Requirement: Private v1 terminal bytes are deterministic and publication is
        same-directory, atomic, durable, and no-replace.

        Acceptance: Publication exceeding the declared transient ceiling fails before
        mutation; the exact admitted bytes appear once and a second publication
        preserves them.
        """
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        stdout_identity = ArtifactContentIdentity("sha256", "1" * 64, 10)
        stderr_identity = ArtifactContentIdentity("sha256", "2" * 64, 0)
        record = QuantumEspressoTerminalRecord(
            identity=QuantumEspressoTerminalRecordIdentity("terminal.record.001"),
            status=QuantumEspressoTerminalStatus.COMPLETED,
            simulation_execution_request_identity=(
                prepared.request.simulation_execution_request_identity
            ),
            execution_input_identity=prepared.request.execution_input.identity,
            preparation_identity=prepared.identity,
            process_observation_identity=QuantumEspressoProcessObservationIdentity(
                "process.observation.001"
            ),
            stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
            stdout_content_identity=stdout_identity,
            stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            stderr_content_identity=stderr_identity,
            before_snapshot_identity=ArtifactManifestIdentity("snapshot.before"),
            after_snapshot_identity=ArtifactManifestIdentity("snapshot.after"),
            diagnostic_report_identity=QuantumEspressoDiagnosticReportIdentity(
                "diagnostic.report.001"
            ),
            native_output_manifest_identity=ArtifactManifestIdentity(
                "native.manifest.001"
            ),
        )
        serialized = QuantumEspressoTerminalRecordSerializer().execute(record)
        content_identity = ArtifactContentIdentity(
            "sha256", hashlib.sha256(serialized).hexdigest(), len(serialized)
        )
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        publisher = QuantumEspressoTerminalRecordPublisher(
            "qe-publisher:1", snapshotter
        )
        current = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )
        assert type(current) is QuantumEspressoWorkspaceSnapshot
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
        limited = publisher.execute(
            constrained, record.identity, serialized, content_identity
        )
        assert type(limited) is QuantumEspressoTerminalPublicationFailure
        assert limited.code is (
            QuantumEspressoTerminalPublicationFailureCode.LIMIT_EXCEEDED
        )
        assert not (
            prepared.workspace / prepared.request.terminal_record_destination.value
        ).exists()

        published = publisher.execute(
            prepared, record.identity, serialized, content_identity
        )

        assert type(published) is QuantumEspressoPublishedTerminalRecord
        assert published.destination.read_bytes() == serialized
        second = publisher.execute(
            prepared, record.identity, serialized, content_identity
        )
        assert type(second) is QuantumEspressoTerminalPublicationFailure
        assert second.code is (
            QuantumEspressoTerminalPublicationFailureCode.DESTINATION_EXISTS
        )
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

        assert type(result) is LocalQuantumEspressoCapturedProcess
        assert type(result.observation.termination) is QuantumEspressoNormalProcessExit
        assert result.observation.termination.exit_code == 0
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
        assert result.before_snapshot.phase is (
            QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        )
        assert (
            result.after_snapshot.phase is QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )
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

        assert type(result) is LocalQuantumEspressoCapturedProcess
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

        assert type(result) is LocalQuantumEspressoCapturedProcess
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

        assert type(result) is LocalQuantumEspressoCapturedProcess
        assert type(result.observation.termination) is QuantumEspressoNormalProcessExit
        assert result.observation.termination.exit_code == 3
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

        assert type(result) is LocalQuantumEspressoCapturedProcess
        assert type(result.observation.termination) is (
            QuantumEspressoProcessSignalTermination
        )
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

        assert type(result) is LocalQuantumEspressoCapturedProcess
        assert type(result.observation.termination) is QuantumEspressoProcessTimeout
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
            quantum_espresso_process.time,
            "monotonic_ns",
            Mock(side_effect=(1_000_000, 21_000_000, 22_000_000)),
        )

        _prepared, _staged, result = self.run_process(
            tmp_path.resolve(),
            argument_suffix=("--fixture-empty-stderr",),
            wall_time_milliseconds=10,
        )

        assert type(result) is LocalQuantumEspressoCapturedProcess
        assert type(result.observation.termination) is QuantumEspressoProcessTimeout
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        stdout_path = prepared.workspace / "streams/stdout"
        stdout_path.write_bytes(b"preserve")

        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is (
            LocalQuantumEspressoProcessFailureCode.STREAM_DESTINATION_EXISTS
        )
        assert result.disposition is (
            LocalQuantumEspressoProcessFailureDisposition.REJECTED
        )
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        staged_input = prepared.workspace / "input/pw.in"
        staged_input.chmod(0o600)
        staged_input.write_bytes(b"changed\n")

        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is (
            LocalQuantumEspressoProcessFailureCode.INPUT_IDENTITY_CHANGED
        )
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        monkeypatch.setattr(
            quantum_espresso_process.subprocess,
            "Popen",
            Mock(side_effect=OSError("synthetic spawn failure")),
        )

        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is LocalQuantumEspressoProcessFailureCode.SPAWN_FAILED
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        (prepared.workspace / "work/unsupported-link").symlink_to("missing")

        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1"),
        ).execute(
            prepared,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is (
            LocalQuantumEspressoProcessFailureCode.BEFORE_SNAPSHOT_FAILED
        )
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        current = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        )
        assert type(current) is QuantumEspressoWorkspaceSnapshot
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

        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=snapshotter,
        ).execute(
            constrained,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is (
            LocalQuantumEspressoProcessFailureCode.BEFORE_SNAPSHOT_FAILED
        )
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
        prepared = self.preparer().execute(self.request(tmp_path.resolve()))
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        before = snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        )
        assert type(before) is QuantumEspressoWorkspaceSnapshot
        after_failure = QuantumEspressoWorkspaceSnapshotFailure(
            code=QuantumEspressoWorkspaceSnapshotFailureCode.OBSERVATION_FAILED,
            phase=QuantumEspressoWorkspaceSnapshotPhase.AFTER,
            preparation_identity=prepared.identity,
            observed_condition="synthetic after-snapshot observation failure",
        )
        monkeypatch.setattr(
            QuantumEspressoWorkspaceSnapshotter,
            "execute",
            Mock(side_effect=(before, after_failure)),
        )

        result = LocalQuantumEspressoProcessRunner(
            observer_version="qe-process-observer:1",
            snapshotter=snapshotter,
        ).execute(
            prepared,
            staged,
            LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
        )

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is (
            LocalQuantumEspressoProcessFailureCode.AFTER_SNAPSHOT_FAILED
        )
        assert result.process_entered
        assert result.disposition is (
            LocalQuantumEspressoProcessFailureDisposition.INDETERMINATE
        )

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

        assert type(result) is LocalQuantumEspressoProcessFailure
        assert result.code is (
            LocalQuantumEspressoProcessFailureCode.OUTPUT_LIMIT_EXCEEDED
        )
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
        prepared = self.preparer().execute(
            self.request(tmp_path.resolve(), maximum_created_entry_count=20)
        )
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
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

        result = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1").execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )

        assert type(result) is QuantumEspressoWorkspaceSnapshotFailure
        assert result.code is (
            QuantumEspressoWorkspaceSnapshotFailureCode.ENTRY_LIMIT_EXCEEDED
        )

    def test_method__execute__snapshotter_byte_limit_fails_before_hashing_large_file(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-QE-LOCAL-EXEC-026

        Requirement: Snapshot byte admission checks file metadata against the
        remaining aggregate ceiling before reading file content.

        Acceptance: An over-limit synthetic file produces ``byte_limit_exceeded``.
        """
        prepared = self.preparer().execute(
            self.request(tmp_path.resolve(), maximum_created_total_bytes=20_000)
        )
        assert type(prepared) is LocalQuantumEspressoPreparedExecution
        staged = QuantumEspressoInputStager("qe-input-stager:1").execute(prepared)
        assert type(staged) is QuantumEspressoStagedExecution
        (prepared.workspace / "results/large.dat").write_bytes(b"x" * 65_536)

        result = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1").execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )

        assert type(result) is QuantumEspressoWorkspaceSnapshotFailure
        assert result.code is (
            QuantumEspressoWorkspaceSnapshotFailureCode.BYTE_LIMIT_EXCEEDED
        )
