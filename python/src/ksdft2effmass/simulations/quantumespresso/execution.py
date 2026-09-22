"""Project-owned QE plan correlation and persisted Workflow dispatch composition.

Direct plan execution remains blocked. The authorized composition consumes an exact
persisted claim, repeats generic claim-phase authorization, wins durable dispatch
entry, and only then exposes the integration-owned local QE effect port.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Never

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoExecutionPreparationRequest,
    LocalQuantumEspressoExecutor,
    LocalQuantumEspressoStreamArtifactBindings,
    QuantumEspressoExecutableKind,
    QuantumEspressoProgram,
)
from ksdft2effmass.workflows import (
    ScientificExecutionAuthorityReference,
    SimulationDispatchAdapterResult,
    SimulationExecutionAuthorizer,
    WorkflowRunRepository,
    WorkflowRunSerializer,
    WorkflowRuntimeBundle,
)
from ksdft2effmass.workflows.control.lifecycle import (
    SimulationDispatchControlFailure,
    SimulationDispatchControlRequest,
    SimulationDispatchControlWorkflow,
)

from .run_identity import QuantumEspressoBundledExampleRunIdentity


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoBundledExampleExecutionPlan:
    """Bind one project run identity to an integration-owned preparation request.

    Parameters
    ----------
    manifest_schema_identity
        Exact dated schema-v2 identity of the manifest decoded into this plan.
    run_identity
        Exact Task-, QE-release-, and UTC-derived bundled-example run identity.
    development_decision_id
        Exact canonical development-decision identity cited as decision evidence.
        The identifier is not itself an execution grant.
    authority_reference
        Generic Workflow record identifying the externally issued grant revision,
        verified authority snapshot, and represented grant state.
    external_runs_root
        Absolute nonsymlink parent beneath which the run identity maps its workspace.
        The directory must already exist; creation remains integration-owned staging.
    preparation_request
        Exact QE-native integration request containing executable, input-artifact,
        resource, destination, and authorization-correlation identities.
    stream_artifacts
        Exact distinct stdout and stderr artifact identities used by native capture.

    Notes
    -----
    This plan represents composition only. Its authorization identity must refer to
    authority established outside this object. Construction neither verifies that
    authority nor performs filesystem mutation or process execution.
    """

    manifest_schema_identity: str
    run_identity: QuantumEspressoBundledExampleRunIdentity
    development_decision_id: str
    authority_reference: ScientificExecutionAuthorityReference
    external_runs_root: Path
    preparation_request: LocalQuantumEspressoExecutionPreparationRequest
    stream_artifacts: LocalQuantumEspressoStreamArtifactBindings

    def __post_init__(self) -> None:
        if type(self.manifest_schema_identity) is not str:
            raise TypeError("manifest_schema_identity must be a built-in string")
        if not self.manifest_schema_identity:
            raise ValueError("manifest_schema_identity must not be empty")
        if type(self.run_identity) is not QuantumEspressoBundledExampleRunIdentity:
            raise TypeError(
                "run_identity must be QuantumEspressoBundledExampleRunIdentity"
            )
        if type(self.development_decision_id) is not str:
            raise TypeError("development_decision_id must be a built-in string")
        if not self.development_decision_id:
            raise ValueError("development_decision_id must not be empty")
        if type(self.authority_reference) is not ScientificExecutionAuthorityReference:
            raise TypeError(
                "authority_reference must be ScientificExecutionAuthorityReference"
            )
        if not isinstance(self.external_runs_root, Path):
            raise TypeError("external_runs_root must be pathlib.Path")
        if not self.external_runs_root.is_absolute():
            raise ValueError("external_runs_root must be absolute")
        if type(self.preparation_request) is not (
            LocalQuantumEspressoExecutionPreparationRequest
        ):
            raise TypeError(
                "preparation_request must be "
                "LocalQuantumEspressoExecutionPreparationRequest"
            )
        if type(self.stream_artifacts) is not (
            LocalQuantumEspressoStreamArtifactBindings
        ):
            raise TypeError(
                "stream_artifacts must be LocalQuantumEspressoStreamArtifactBindings"
            )
        request = self.preparation_request
        expected_parent = self.external_runs_root.joinpath(
            *self.run_identity.relative_parent_path.parts
        )
        if request.authorized_run_root != expected_parent:
            raise ValueError(
                "preparation run root must equal the run-identity parent path"
            )
        if request.attempt_workspace_name != self.run_identity.attempt_workspace_name:
            raise ValueError(
                "preparation workspace name must equal the run-identity timestamp"
            )
        if (
            request.execution_input.task_definition_identity.value
            != self.run_identity.task_id
        ):
            raise ValueError(
                "execution input Task identity must equal the bundled-example Task"
            )
        configuration = request.executable_configuration
        if configuration.program is not QuantumEspressoProgram.PW:
            raise ValueError("bundled PW execution requires the pw program role")
        if configuration.executable_kind is not (
            QuantumEspressoExecutableKind.QUANTUM_ESPRESSO
        ):
            raise ValueError("bundled execution requires an actual QE executable")
        if configuration.program_version != self.run_identity.release:
            raise ValueError(
                "executable version must equal the run-identity QE release"
            )

    @property
    def workspace(self) -> Path:
        """Return the exact external workspace that integration staging may create."""
        return self.external_runs_root.joinpath(
            *self.run_identity.relative_workspace_path.parts
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoAuthorizedDispatchWorkflow:
    """Bind the complete persisted dispatch lifecycle to the QE local effect port.

    Parameters
    ----------
    repository
        Exact repository that commits reservation and claim state, reconciles the
        resulting claim, and atomically wins dispatch entry before effect invocation.
    serializer, runtime_bundle
        Exact persistence serialization and replay dependencies used by the durable
        dispatch-entry committer.
    authorizer
        Generic claim-phase authorizer evaluated immediately before dispatch entry.
    executor
        Integration-owned local QE effect port bound to one exact execution plan.

    Notes
    -----
    This application composition issues no grant, performs no retry, and does not
    infer authority from a manifest. It delegates reservation, claim, and dispatch
    sequencing to the calculator-independent Workflow owner while requiring the exact
    integration-owned local QE executor as its effect port.
    """

    repository: WorkflowRunRepository
    serializer: WorkflowRunSerializer
    runtime_bundle: WorkflowRuntimeBundle
    authorizer: SimulationExecutionAuthorizer
    executor: LocalQuantumEspressoExecutor

    def __post_init__(self) -> None:
        if not isinstance(self.repository, WorkflowRunRepository):
            raise TypeError("repository must implement WorkflowRunRepository")
        expected = (
            (self.serializer, WorkflowRunSerializer, "serializer"),
            (self.runtime_bundle, WorkflowRuntimeBundle, "runtime_bundle"),
            (self.authorizer, SimulationExecutionAuthorizer, "authorizer"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if not isinstance(self.executor, LocalQuantumEspressoExecutor):
            raise TypeError("executor must be LocalQuantumEspressoExecutor")

    def execute(
        self, request: SimulationDispatchControlRequest
    ) -> SimulationDispatchAdapterResult | SimulationDispatchControlFailure:
        """Persist reservation and claim, then enter the QE effect at most once."""
        if type(request) is not SimulationDispatchControlRequest:
            raise TypeError("request must be SimulationDispatchControlRequest")
        return SimulationDispatchControlWorkflow(
            repository=self.repository,
            serializer=self.serializer,
            runtime_bundle=self.runtime_bundle,
            authorizer=self.authorizer,
            effect=self.executor,
        ).execute(request)


@dataclass(frozen=True, slots=True)
class QuantumEspressoBundledExampleExecutionWorkflow:
    """Fail closed until the generic Workflow dispatch path owns effect entry."""

    def execute(self, plan: QuantumEspressoBundledExampleExecutionPlan) -> Never:
        """Reject direct execution before preparation, staging, or process entry."""
        if type(plan) is not QuantumEspressoBundledExampleExecutionPlan:
            raise TypeError("plan must be QuantumEspressoBundledExampleExecutionPlan")
        raise RuntimeError(
            "direct QE execution is disabled; use authorized Workflow dispatch"
        )
