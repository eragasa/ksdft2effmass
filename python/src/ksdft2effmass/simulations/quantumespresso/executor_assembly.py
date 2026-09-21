"""Effect-free application composition of one complete local QE executor.

The assembler consumes an inert manifest-derived execution plan and an explicitly
supplied version-bound diagnostic catalog. It constructs native integration
ActionObjects but performs no preparation, staging, process entry, or publication.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoExecutionPreparer,
    LocalQuantumEspressoExecutor,
    LocalQuantumEspressoPreparationImplementationIdentity,
    LocalQuantumEspressoProcessRunner,
    LocalQuantumEspressoSupportedExecutableBinding,
    QuantumEspressoCalculatorOutcomeResolver,
    QuantumEspressoDiagnosticCatalog,
    QuantumEspressoDiagnosticClassifier,
    QuantumEspressoInputStager,
    QuantumEspressoNativeOutputCollector,
    QuantumEspressoTerminalRecordPublisher,
    QuantumEspressoTerminalRecordSerializer,
    QuantumEspressoWorkspaceSnapshotter,
)

from .planning import QuantumEspressoExecution


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoLocalExecutorAssemblyRequest:
    """Supply one inert QE execution composition and an exact classifier catalog.

    Attributes
    ----------
    execution
        Manifest-derived execution and complete local execution plan.
    diagnostic_catalog
        Explicit immutable catalog matching the executable kind, program, version,
        and classifier identity retained by the execution plan.
    """

    execution: QuantumEspressoExecution
    diagnostic_catalog: QuantumEspressoDiagnosticCatalog

    def __post_init__(self) -> None:
        if type(self.execution) is not QuantumEspressoExecution:
            raise TypeError("execution must be QuantumEspressoExecution")
        if type(self.diagnostic_catalog) is not QuantumEspressoDiagnosticCatalog:
            raise TypeError(
                "diagnostic_catalog must be QuantumEspressoDiagnosticCatalog"
            )


@dataclass(frozen=True, slots=True)
@final
class QuantumEspressoLocalExecutorAssembler:
    """Construct native local-QE integration owners without invoking an effect."""

    def execute(
        self, request: QuantumEspressoLocalExecutorAssemblyRequest
    ) -> LocalQuantumEspressoExecutor:
        """Return a complete executor or reject catalog/configuration mismatch."""
        if type(request) is not QuantumEspressoLocalExecutorAssemblyRequest:
            raise TypeError(
                "request must be QuantumEspressoLocalExecutorAssemblyRequest"
            )
        plan = request.execution.local_execution_plan
        configuration = plan.preparation_request.executable_configuration
        catalog = request.diagnostic_catalog
        if (
            catalog.classifier_identity != configuration.classifier_identity
            or catalog.executable_kind is not configuration.executable_kind
            or catalog.program is not configuration.program
            or catalog.program_version != configuration.program_version
        ):
            raise ValueError(
                "diagnostic catalog does not match the executable configuration"
            )
        binding = LocalQuantumEspressoSupportedExecutableBinding(
            executable_configuration_identity=configuration.identity,
            executable_content_identity=configuration.executable_content_identity,
            program=configuration.program,
            executable_kind=configuration.executable_kind,
            program_version=configuration.program_version,
            classifier_identity=configuration.classifier_identity,
        )
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-workspace-snapshotter:1")
        return LocalQuantumEspressoExecutor(
            plan=plan,
            preparer=LocalQuantumEspressoExecutionPreparer(
                implementation_identity=(
                    LocalQuantumEspressoPreparationImplementationIdentity(
                        "qe-local-preparer:1"
                    )
                ),
                supported_bindings=(binding,),
            ),
            stager=QuantumEspressoInputStager("qe-input-stager:1"),
            process_runner=LocalQuantumEspressoProcessRunner(
                observer_version="qe-local-process-observer:1",
                snapshotter=snapshotter,
            ),
            classifier=QuantumEspressoDiagnosticClassifier(catalog),
            collector=QuantumEspressoNativeOutputCollector(
                "qe-native-output-collector:1"
            ),
            outcome_resolver=QuantumEspressoCalculatorOutcomeResolver(
                "qe-calculator-outcome-resolver:1"
            ),
            terminal_serializer=QuantumEspressoTerminalRecordSerializer(),
            terminal_publisher=QuantumEspressoTerminalRecordPublisher(
                implementation_version="qe-terminal-record-publisher:1",
                snapshotter=snapshotter,
            ),
        )
