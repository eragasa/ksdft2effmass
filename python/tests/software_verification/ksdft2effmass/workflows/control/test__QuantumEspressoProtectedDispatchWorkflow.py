r"""Software verification of ``QuantumEspressoProtectedDispatchWorkflow``.

Evidence profile: routine

Bounded artifact scope: typed connection from persisted QE assembly through the
generic reservation and claim lifecycle with a complete real-QE executor composition.

Facet and represented meaning

The application Workflow receives all authority and persistence dependencies
explicitly and delegates one no-retry attempt to the generic control owner.

Intrinsic and cross-object scope

The test covers a stale claim-phase authority boundary after successful preparation
reservation. Process entry and result reconciliation remain unexercised.

VVUQ and scientific exclusions

All authority values are synthetic test data. No executable is invoked, and this test
establishes no production authority, numerical verification, scientific validation,
uncertainty quantification, or human acceptance.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoDiagnosticCatalog,
)
from ksdft2effmass.simulations.quantumespresso.protected_dispatch import (
    QuantumEspressoProtectedDispatchPreflightKind,
    QuantumEspressoProtectedDispatchRequest,
    QuantumEspressoProtectedDispatchWorkflow,
)
from ksdft2effmass.workflows import SimulationExecutionAuthorizer
from ksdft2effmass.workflows.control.lifecycle import (
    SimulationDispatchControlFailure,
    SimulationDispatchControlFailureStage,
)

from .resources.scenarios import ControlScenarioFactory
from .test__QuantumEspressoDispatchAssembler import (
    TestQuantumEspressoDispatchAssembler as AssemblyEvidenceFactory,
)
from .test__SimulationDispatchControlWorkflow import (
    TestSimulationDispatchControlWorkflow as ControlWorkflowEvidenceFactory,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoProtectedDispatchWorkflow


class TestQuantumEspressoProtectedDispatchWorkflow:
    """Own software evidence for the protected typed QE application entry."""

    def test_method__preflight__reports_ready_without_commit_or_effect(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-PROTECTED-DISPATCH-002

        Requirement: The operator boundary must inspect exact persisted replay,
        supplied authority views, and executor composition without committing control
        state, creating a workspace, or entering a process.

        Acceptance: Exact synthetic inputs report ready with a complete executor while
        the manifest-derived external run root remains absent.
        """
        assembly_request, repository = AssemblyEvidenceFactory.request(tmp_path)
        workflow = SUT(
            repository=repository,
            serializer=ControlWorkflowEvidenceFactory.serializer(),
            authorizer=SimulationExecutionAuthorizer(),
        )

        result = workflow.preflight(
            QuantumEspressoProtectedDispatchRequest(
                assembly_request=assembly_request,
                diagnostic_catalog=QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1(),
            )
        )

        assert result.kind is QuantumEspressoProtectedDispatchPreflightKind.READY
        assert result.executor is not None
        assert not assembly_request.execution.plan.external_runs_root.exists()

    def test_method__execute__stale_claim_stops_before_local_executor_effect(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-PROTECTED-DISPATCH-001

        Requirement: The complete application composition must preserve immediate
        claim-phase reauthorization after a successfully persisted reservation.

        Acceptance: Stale claim authority returns a claim-stage failure and creates no
        external run workspace or QE process effect.
        """
        assembly_request, repository = AssemblyEvidenceFactory.request(tmp_path)
        stale_request = replace(
            assembly_request,
            claim_authorization_request=replace(
                assembly_request.claim_authorization_request,
                evaluated_at=ControlScenarioFactory.instant(11),
            ),
        )
        execution = stale_request.execution

        workflow = SUT(
            repository=repository,
            serializer=ControlWorkflowEvidenceFactory.serializer(),
            authorizer=SimulationExecutionAuthorizer(),
        )
        protected_request = QuantumEspressoProtectedDispatchRequest(
            assembly_request=stale_request,
            diagnostic_catalog=QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1(),
        )

        preflight = workflow.preflight(protected_request)
        result = workflow.execute(protected_request)

        assert preflight.kind is (
            QuantumEspressoProtectedDispatchPreflightKind.AUTHORITY_FAILED
        )
        assert preflight.executor is None
        assert type(result) is SimulationDispatchControlFailure
        assert result.stage is SimulationDispatchControlFailureStage.CLAIM
        assert not execution.plan.external_runs_root.exists()
