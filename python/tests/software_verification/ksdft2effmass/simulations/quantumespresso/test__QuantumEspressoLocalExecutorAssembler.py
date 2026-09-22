r"""Software verification of ``QuantumEspressoLocalExecutorAssembler``.

Evidence profile: routine

Bounded artifact scope: effect-free composition of native local-QE integration owners
from the dated-v2 synthetic manifest plan and explicit QE ``pw`` 7.2 catalog.

Facet and represented meaning

The assembler constructs the complete ``LocalQuantumEspressoExecutor`` dependency
closure while retaining the plan's exact classifier binding.

Intrinsic and cross-object scope

Tests cover exact successful composition and fail-closed catalog mismatch. Dispatch,
workspace mutation, process entry, result ingress, and retry remain separate.

VVUQ and scientific exclusions

No executable is invoked. The tests establish software construction behavior only,
not numerical verification, scientific validation, uncertainty quantification,
production authority, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoExecutor,
    QuantumEspressoDiagnosticCatalog,
)
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoExecutionRequest,
    QuantumEspressoPlanner,
)
from ksdft2effmass.simulations.quantumespresso.executor_assembly import (
    QuantumEspressoLocalExecutorAssembler,
    QuantumEspressoLocalExecutorAssemblyRequest,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoLocalExecutorAssembler


class TestQuantumEspressoLocalExecutorAssembler:
    """Own software evidence for effect-free native executor composition."""

    @staticmethod
    def execution_request() -> QuantumEspressoExecutionRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Name the maintained dated-v2 synthetic execution manifest.

        Acceptance: The returned manifest path is absolute.
        """
        return QuantumEspressoExecutionRequest(
            manifest_path=(
                Path(__file__).parent / "resources" / "execution-manifest-v2.json"
            ).resolve()
        )

    def test_method__execute__constructs_complete_qe72_executor_without_effect(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-ASSEMBLY-001

        Requirement: An exact QE ``pw`` 7.2 catalog and matching inert plan must
        construct the complete local executor without entering any effect boundary.

        Acceptance: The executor retains the exact plan and catalog while the external
        run root remains absent.
        """
        execution = QuantumEspressoPlanner().execute(self.execution_request())
        catalog = QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1()

        executor = SUT().execute(
            QuantumEspressoLocalExecutorAssemblyRequest(
                execution=execution,
                diagnostic_catalog=catalog,
            )
        )

        assert type(executor) is LocalQuantumEspressoExecutor
        assert executor.plan is execution.local_execution_plan
        assert executor.classifier.catalog is catalog
        assert not execution.plan.external_runs_root.exists()

    def test_method__execute__rejects_mismatched_fixture_catalog(self) -> None:
        """Evidence ID: SV-QE-EXECUTOR-ASSEMBLY-002

        Requirement: Executor composition must not substitute a classifier from
        another executable-kind and program-version namespace.

        Acceptance: A fixture catalog raises before an executor or workspace exists.
        """
        execution = QuantumEspressoPlanner().execute(self.execution_request())

        with pytest.raises(ValueError):
            SUT().execute(
                QuantumEspressoLocalExecutorAssemblyRequest(
                    execution=execution,
                    diagnostic_catalog=(
                        QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
                    ),
                )
            )

        assert not execution.plan.external_runs_root.exists()
