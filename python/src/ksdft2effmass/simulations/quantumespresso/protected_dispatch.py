"""Protected typed entry point for one fully assembled local QE dispatch.

The Workflow accepts only explicit persisted-state, activation, authority, repository,
serializer, authorizer, and diagnostic-catalog dependencies. It performs no discovery,
grant issuance, retry, or fallback. Calling ``execute`` can enter the external effect
only after the generic durable control lifecycle succeeds.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import final

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoExecutor,
    QuantumEspressoDiagnosticCatalog,
)
from ksdft2effmass.workflows import (
    SimulationDispatchAdapterResult,
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationResult,
    SimulationExecutionAuthorizer,
    WorkflowRunRepository,
    WorkflowRunSerializer,
)
from ksdft2effmass.workflows.control.lifecycle import (
    SimulationDispatchControlFailure,
)

from .dispatch_assembly import (
    QuantumEspressoDispatchAssembler,
    QuantumEspressoDispatchAssemblyOutcomeKind,
    QuantumEspressoDispatchAssemblyRequest,
    QuantumEspressoDispatchAssemblyResult,
)
from .execution import QuantumEspressoAuthorizedDispatchWorkflow
from .executor_assembly import (
    QuantumEspressoLocalExecutorAssembler,
    QuantumEspressoLocalExecutorAssemblyRequest,
)


class QuantumEspressoProtectedDispatchPreflightKind(StrEnum):
    """Closed outcomes of effect-free operator preflight."""

    READY = "ready"
    ASSEMBLY_FAILED = "assembly_failed"
    AUTHORITY_FAILED = "authority_failed"
    EXECUTOR_FAILED = "executor_failed"


type QuantumEspressoProtectedDispatchResult = (
    QuantumEspressoDispatchAssemblyResult
    | SimulationDispatchAdapterResult
    | SimulationDispatchControlFailure
)
"""Closed assembly or generic persisted-control result."""


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoProtectedDispatchRequest:
    """Supply the complete explicit inputs for one protected QE dispatch.

    Attributes
    ----------
    assembly_request
        Exact predecessor read, replay bundle, Task activation, independently supplied
        preparation/claim authority views, and lifecycle commit identities.
    diagnostic_catalog
        Explicit version-bound classifier catalog matching the manifest-derived local
        executor plan.
    """

    assembly_request: QuantumEspressoDispatchAssemblyRequest
    diagnostic_catalog: QuantumEspressoDiagnosticCatalog

    def __post_init__(self) -> None:
        if type(self.assembly_request) is not QuantumEspressoDispatchAssemblyRequest:
            raise TypeError(
                "assembly_request must be QuantumEspressoDispatchAssemblyRequest"
            )
        if type(self.diagnostic_catalog) is not QuantumEspressoDiagnosticCatalog:
            raise TypeError(
                "diagnostic_catalog must be QuantumEspressoDiagnosticCatalog"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoProtectedDispatchPreflightResult:
    """Report effect-free readiness without granting or promising execution."""

    kind: QuantumEspressoProtectedDispatchPreflightKind
    assembly_result: QuantumEspressoDispatchAssemblyResult
    preparation_authorization: SimulationExecutionAuthorizationResult | None
    claim_authorization: SimulationExecutionAuthorizationResult | None
    executor: LocalQuantumEspressoExecutor | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.kind) is not QuantumEspressoProtectedDispatchPreflightKind:
            raise TypeError(
                "kind must be QuantumEspressoProtectedDispatchPreflightKind"
            )
        if type(self.assembly_result) is not QuantumEspressoDispatchAssemblyResult:
            raise TypeError(
                "assembly_result must be QuantumEspressoDispatchAssemblyResult"
            )
        for value, name in (
            (self.preparation_authorization, "preparation_authorization"),
            (self.claim_authorization, "claim_authorization"),
        ):
            if value is not None and type(value) is not (
                SimulationExecutionAuthorizationResult
            ):
                raise TypeError(
                    f"{name} must be SimulationExecutionAuthorizationResult or None"
                )
        if self.executor is not None and type(self.executor) is not (
            LocalQuantumEspressoExecutor
        ):
            raise TypeError("executor must be LocalQuantumEspressoExecutor or None")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must contain built-in str values")
        if any(not value for value in self.diagnostics):
            raise ValueError("diagnostics must not contain empty strings")
        if self.kind is QuantumEspressoProtectedDispatchPreflightKind.READY:
            authorizations = (
                self.preparation_authorization,
                self.claim_authorization,
            )
            if (
                self.assembly_result.kind
                is not QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED
                or any(
                    value is None
                    or value.kind
                    is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
                    for value in authorizations
                )
                or self.executor is None
                or self.diagnostics
            ):
                raise ValueError("ready preflight requires complete authorized inputs")
        elif self.executor is not None or not self.diagnostics:
            raise ValueError(
                "failed preflight prohibits executor and requires diagnostics"
            )
        elif self.kind is (
            QuantumEspressoProtectedDispatchPreflightKind.ASSEMBLY_FAILED
        ) and (
            self.assembly_result.kind
            is QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED
            or self.preparation_authorization is not None
            or self.claim_authorization is not None
        ):
            raise ValueError("assembly failure prohibits authorization results")
        elif self.kind is (
            QuantumEspressoProtectedDispatchPreflightKind.AUTHORITY_FAILED
        ):
            authorizations = (
                self.preparation_authorization,
                self.claim_authorization,
            )
            if (
                self.assembly_result.kind
                is not QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED
                or any(value is None for value in authorizations)
                or all(
                    value is not None
                    and value.kind
                    is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
                    for value in authorizations
                )
            ):
                raise ValueError(
                    "authority failure requires assembled and nonauthorized inputs"
                )
        elif self.kind is (
            QuantumEspressoProtectedDispatchPreflightKind.EXECUTOR_FAILED
        ):
            authorizations = (
                self.preparation_authorization,
                self.claim_authorization,
            )
            if (
                self.assembly_result.kind
                is not QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED
                or any(
                    value is None
                    or value.kind
                    is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
                    for value in authorizations
                )
            ):
                raise ValueError(
                    "executor failure requires assembled and authorized inputs"
                )


@dataclass(frozen=True, slots=True)
@final
class QuantumEspressoProtectedDispatchWorkflow:
    """Connect exact typed assembly to the durable at-most-once control lifecycle."""

    repository: WorkflowRunRepository
    serializer: WorkflowRunSerializer
    authorizer: SimulationExecutionAuthorizer

    def __post_init__(self) -> None:
        if not isinstance(self.repository, WorkflowRunRepository):
            raise TypeError("repository must implement WorkflowRunRepository")
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")
        if type(self.authorizer) is not SimulationExecutionAuthorizer:
            raise TypeError("authorizer must be SimulationExecutionAuthorizer")

    def preflight(
        self, request: QuantumEspressoProtectedDispatchRequest
    ) -> QuantumEspressoProtectedDispatchPreflightResult:
        """Check replay, authority, and executor composition without mutation."""
        if type(request) is not QuantumEspressoProtectedDispatchRequest:
            raise TypeError("request must be QuantumEspressoProtectedDispatchRequest")
        assembly = QuantumEspressoDispatchAssembler(self.repository).execute(
            request.assembly_request
        )
        if assembly.kind is not QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED:
            return QuantumEspressoProtectedDispatchPreflightResult(
                kind=(QuantumEspressoProtectedDispatchPreflightKind.ASSEMBLY_FAILED),
                assembly_result=assembly,
                preparation_authorization=None,
                claim_authorization=None,
                executor=None,
                diagnostics=("persisted dispatch assembly is not ready",),
            )
        preparation = self.authorizer.execute(
            request.assembly_request.preparation_authorization_request
        )
        claim = self.authorizer.execute(
            request.assembly_request.claim_authorization_request
        )
        if (
            preparation.kind
            is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
            or claim.kind is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
        ):
            return QuantumEspressoProtectedDispatchPreflightResult(
                kind=QuantumEspressoProtectedDispatchPreflightKind.AUTHORITY_FAILED,
                assembly_result=assembly,
                preparation_authorization=preparation,
                claim_authorization=claim,
                executor=None,
                diagnostics=(
                    "preflight authority is not authorized for both lifecycle phases",
                ),
            )
        try:
            executor = QuantumEspressoLocalExecutorAssembler().execute(
                QuantumEspressoLocalExecutorAssemblyRequest(
                    execution=request.assembly_request.execution,
                    diagnostic_catalog=request.diagnostic_catalog,
                )
            )
        except ValueError:
            return QuantumEspressoProtectedDispatchPreflightResult(
                kind=QuantumEspressoProtectedDispatchPreflightKind.EXECUTOR_FAILED,
                assembly_result=assembly,
                preparation_authorization=preparation,
                claim_authorization=claim,
                executor=None,
                diagnostics=("local QE executor composition was rejected",),
            )
        return QuantumEspressoProtectedDispatchPreflightResult(
            kind=QuantumEspressoProtectedDispatchPreflightKind.READY,
            assembly_result=assembly,
            preparation_authorization=preparation,
            claim_authorization=claim,
            executor=executor,
            diagnostics=(),
        )

    def execute(
        self, request: QuantumEspressoProtectedDispatchRequest
    ) -> QuantumEspressoProtectedDispatchResult:
        """Assemble exact dependencies and delegate one no-retry control attempt."""
        if type(request) is not QuantumEspressoProtectedDispatchRequest:
            raise TypeError("request must be QuantumEspressoProtectedDispatchRequest")
        assembly = QuantumEspressoDispatchAssembler(self.repository).execute(
            request.assembly_request
        )
        if assembly.kind is not QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED:
            return assembly
        control_request = assembly.control_request
        assert control_request is not None
        executor = QuantumEspressoLocalExecutorAssembler().execute(
            QuantumEspressoLocalExecutorAssemblyRequest(
                execution=request.assembly_request.execution,
                diagnostic_catalog=request.diagnostic_catalog,
            )
        )
        return QuantumEspressoAuthorizedDispatchWorkflow(
            repository=self.repository,
            serializer=self.serializer,
            runtime_bundle=request.assembly_request.runtime_bundle,
            authorizer=self.authorizer,
            executor=executor,
        ).execute(control_request)
