r"""Software verification of ``QuantumEspressoBundledExampleExecutionWorkflow``.

Evidence profile: routine

Bounded artifact scope: project-owned run-path correlation and fail-closed direct
execution before generic Workflow dispatch.

Facet and represented meaning

The Workflow binds one Task-derived bundled-example run to one integration request and
rejects direct preparation, staging, and process entry.

Intrinsic and cross-object scope

Tests cover run-path correlation and the direct-effect blockade pending generic
Workflow authorization, reservation, claim, and dispatch composition.

VVUQ and scientific exclusions

All process inputs are synthetic test data. The tests invoke no Quantum ESPRESSO
executable and establish no calculator compatibility, numerical verification,
scientific validation, production readiness, execution authority, or human acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoArtifactSource,
    LocalQuantumEspressoExecutionLimits,
    LocalQuantumEspressoExecutionPreparationRequest,
    LocalQuantumEspressoPeakResidentBytesUnlimited,
    LocalQuantumEspressoStreamArtifactBindings,
    QuantumEspressoArtifactDestination,
    QuantumEspressoDiagnosticClassifierIdentity,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInput,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
)
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoBundledExampleRunIdentity,
)
from ksdft2effmass.simulations.quantumespresso.execution import (
    QuantumEspressoBundledExampleExecutionPlan,
    QuantumEspressoBundledExampleExecutionWorkflow,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    AttemptIdentity,
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    OperationIdentity,
    ScientificExecutionAuthorityReference,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutorIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoBundledExampleExecutionWorkflow


class TestQuantumEspressoBundledExampleExecutionWorkflow:
    """Own maintained evidence for project-to-integration execution composition."""

    @staticmethod
    def resource(name: str) -> Path:
        """Return one maintained synthetic execution resource."""
        return (Path(__file__).parent / "resources" / "execution" / name).resolve()

    @staticmethod
    def content_identity(path: Path) -> ArtifactContentIdentity:
        """Return the exact SHA-256 and size of one synthetic resource."""
        content = path.read_bytes()
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )

    @classmethod
    def plan(
        cls, external_runs_root: Path
    ) -> QuantumEspressoBundledExampleExecutionPlan:
        """Construct one synthetic plan using production integration owners."""
        run_identity = QuantumEspressoBundledExampleRunIdentity(
            task_id="quantumespresso.simulations.qe_examples.pw.example01",
            release="7.2",
            workspace_created_at=datetime(2026, 9, 21, 12, 3, 25, tzinfo=UTC),
        )
        executable = cls.resource("fixture_pw.py")
        native_input = cls.resource("pw.in")
        pseudopotential = cls.resource("Si.fixture.UPF")
        executable_content = cls.content_identity(executable)
        native_artifact = QuantumEspressoNativeInputArtifact(
            identity=ArtifactIdentity("artifact.example01.input"),
            content=QuantumEspressoFileArtifactContent(
                cls.content_identity(native_input)
            ),
            destination=QuantumEspressoArtifactDestination("input/pw.in"),
        )
        pseudopotential_artifact = QuantumEspressoPseudopotentialArtifact(
            identity=ArtifactIdentity("artifact.example01.pseudopotential"),
            content=QuantumEspressoFileArtifactContent(
                cls.content_identity(pseudopotential)
            ),
            destination=QuantumEspressoArtifactDestination("pseudo/Si.fixture.UPF"),
        )
        execution_input = QuantumEspressoExecutionInput(
            identity=QuantumEspressoExecutionInputIdentity("qe.example01.input"),
            program=QuantumEspressoProgram.PW,
            native_input=native_artifact,
            pseudopotentials=(pseudopotential_artifact,),
            predecessor_native_state=(),
            task_definition_identity=TaskDefinitionIdentity(run_identity.task_id),
            task_instance_identity=TaskInstanceIdentity("task.example01.instance"),
            activation_identity=TaskActivationIdentity("activation.example01"),
            operation_identity=OperationIdentity("operation.example01.scf"),
            attempt_identity=AttemptIdentity("attempt.example01.001"),
            contract_version="qe-execution-input:1",
        )
        configuration_identity = QuantumEspressoExecutableConfigurationIdentity(
            "qe-7.2.synthetic-composition-test"
        )
        classifier_identity = QuantumEspressoDiagnosticClassifierIdentity(
            "qe-diagnostic-classifier.pw-7.2:1"
        )
        configuration = QuantumEspressoExecutableConfiguration(
            identity=configuration_identity,
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.QUANTUM_ESPRESSO,
            executable_content_identity=executable_content,
            program_version="7.2",
            argument_suffix=(),
            environment_additions=(("OMP_NUM_THREADS", "1"),),
            classifier_identity=classifier_identity,
            contract_version="qe-executable-configuration:1",
        )
        parent = external_runs_root.joinpath(*run_identity.relative_parent_path.parts)
        request = LocalQuantumEspressoExecutionPreparationRequest(
            execution_input=execution_input,
            executable_configuration=configuration,
            executable_path=executable,
            executable_content_identity=executable_content,
            executable_destination=QuantumEspressoArtifactDestination(
                "integration/pw.x"
            ),
            authorized_run_root=parent,
            attempt_workspace_name=run_identity.attempt_workspace_name,
            artifact_sources=(
                LocalQuantumEspressoArtifactSource(native_artifact, native_input),
                LocalQuantumEspressoArtifactSource(
                    pseudopotential_artifact, pseudopotential
                ),
            ),
            limits=LocalQuantumEspressoExecutionLimits(
                wall_time_milliseconds=2_000,
                termination_grace_milliseconds=100,
                minimum_free_bytes=0,
                maximum_created_entry_count=100,
                maximum_created_total_bytes=1_000_000,
                peak_resident_bytes=LocalQuantumEspressoPeakResidentBytesUnlimited(),
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
                "request.example01"
            ),
            scientific_executor_identity=ScientificExecutorIdentity(
                "executor.qe.local"
            ),
            dispatch_destination_identity=DispatchDestinationIdentity(
                "destination.local"
            ),
            dispatch_resource_scope_identity=DispatchResourceScopeIdentity(
                "resources.example01"
            ),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity(
                    "authorization.example01"
                )
            ),
        )
        plan = QuantumEspressoBundledExampleExecutionPlan(
            manifest_schema_identity=(
                "quantum-espresso-execution-manifest:v2.20260921T155105Z"
            ),
            run_identity=run_identity,
            development_decision_id="QE-7-2-EXAMPLE01-SI-SCF-HC01",
            authority_reference=ScientificExecutionAuthorityReference(
                grant_identity=ExecutionGrantIdentity("grant.example01.001"),
                grant_revision_identity=ExecutionGrantRevisionIdentity(
                    "grant.example01.001.revision.001"
                ),
                snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                    "authority.snapshot.example01.001"
                ),
                state_identity=ScientificExecutionAuthorityStateIdentity(
                    "authority.state.example01.unused"
                ),
            ),
            external_runs_root=external_runs_root,
            preparation_request=request,
            stream_artifacts=LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.example01.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.example01.stderr"),
            ),
        )
        return plan

    def test_constructor__path_correlation__rejects_mismatched_run_root(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-SIM-EXEC-001

        Requirement: Project composition must correlate its external workspace with
        the Task-derived run identity before integration mutation is possible.

        Method: Replace the integration request's accepted run root while retaining
        the original Task-derived run identity.

        Oracle: The run identity's deterministic relative parent path.

        Acceptance: Replacing the integration run root with another absolute path is
        rejected during plan construction.

        Interpretation: Project composition cannot redirect the integration workspace.

        Limitations: Filesystem race resistance remains integration-owned.
        """
        root = tmp_path.resolve()
        plan = self.plan(root)

        with pytest.raises(ValueError, match="run root"):
            replace(
                plan,
                preparation_request=replace(
                    plan.preparation_request,
                    authorized_run_root=root / "wrong-parent",
                ),
            )

    def test_method__execute__blocks_direct_effect_before_workspace_creation(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-SIM-EXEC-002

        Requirement: Simulation composition must not enter preparation, staging, or a
        process directly from manifest correlations.

        Method: Submit one synthetic plan without a generic Workflow dispatch.

        Oracle: Protected execution requires authorization, reservation, claim, and
        dispatch rather than a manifest authority reference alone.

        Acceptance: Execution raises the direct-dispatch diagnostic and the external
        run root remains byte-for-byte unchanged.

        Interpretation: A manifest reference cannot bypass Workflow effect control.

        Limitations: The test does not construct or authenticate an execution grant.
        """
        root = tmp_path.resolve()
        plan = self.plan(root)
        before = tuple(root.iterdir())

        with pytest.raises(RuntimeError, match="authorized Workflow dispatch"):
            SUT().execute(plan)

        assert tuple(root.iterdir()) == before
        assert not plan.workspace.exists()
