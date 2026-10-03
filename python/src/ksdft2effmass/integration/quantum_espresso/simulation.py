"""Immutable application composition for one Quantum ESPRESSO simulation.

``QuantumEspressoSimulation`` binds one accepted operation-specific Task, its exact
QE execution input, one separately selected backend-neutral calculator capability,
and one Workflow dispatch-effect executor. The definition-only Task invokes neither
boundary. The composition keeps calculator capability and authority-bearing Workflow
dispatch distinct; it performs neither operation.

The value stores no output or mutable execution state.  Concrete execution remains
owned by the injected ports, and ``LocalQuantumEspressoExecutor`` is the implemented
QE ``AbstractSimulationDispatchEffect``. Construction establishes software
correlation only, not execution authority, numerical convergence, or scientific
acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.calculators.dft.pw import AbstractPlaneWaveCalculator
from ksdft2effmass.workflows import AbstractSimulationDispatchEffect

from .contracts import (
    QuantumEspressoBandsResult,
    QuantumEspressoExecutionInput,
    QuantumEspressoPwResult,
)
from .tasks import (
    QuantumEspressoBandPathTask,
    QuantumEspressoBandsExtractionTask,
    QuantumEspressoNscfTask,
    QuantumEspressoScfTask,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoSimulation:
    """Bind one exact QE Task to its calculator and Workflow effect executor.

    Parameters
    ----------
    task
        One exact accepted operation-specific QE Task: SCF, NSCF, band path, or
        bands extraction.
    execution_input
        Exact immutable QE execution input.  It must equal the input retained by
        ``task``.
    calculator
        Exact backend-neutral ``AbstractPlaneWaveCalculator`` capability selected by
        application composition. The definition-only Task does not retain or invoke
        this object.
    executor
        Workflow
        :class:`~ksdft2effmass.workflows.AbstractSimulationDispatchEffect`
        selected for the same application composition. The implemented local QE
        binding is
        :class:`~ksdft2effmass.integration.quantum_espresso.LocalQuantumEspressoExecutor`.

    Notes
    -----
    The calculator port returns the Task's immutable QE AbstractResultObject type.  The
    executor separately returns a Workflow ``SimulationDispatchOutcome`` after its
    authority and dispatch-entry checks.  This value deliberately does not adapt one
    call signature into the other, invoke either dependency, retain an output, or
    create Workflow authority.
    """

    task: (
        QuantumEspressoScfTask
        | QuantumEspressoNscfTask
        | QuantumEspressoBandPathTask
        | QuantumEspressoBandsExtractionTask
    )
    execution_input: QuantumEspressoExecutionInput
    calculator: (
        AbstractPlaneWaveCalculator[
            QuantumEspressoExecutionInput, QuantumEspressoPwResult
        ]
        | AbstractPlaneWaveCalculator[
            QuantumEspressoExecutionInput, QuantumEspressoBandsResult
        ]
    )
    executor: AbstractSimulationDispatchEffect

    def __post_init__(self) -> None:
        """Validate the exact immutable application-composition bindings."""
        if type(self.task) not in (
            QuantumEspressoScfTask,
            QuantumEspressoNscfTask,
            QuantumEspressoBandPathTask,
            QuantumEspressoBandsExtractionTask,
        ):
            raise TypeError("task must be an operation-specific Quantum ESPRESSO Task")
        if type(self.execution_input) is not QuantumEspressoExecutionInput:
            raise TypeError("execution_input must be QuantumEspressoExecutionInput")
        if not isinstance(self.calculator, AbstractPlaneWaveCalculator):
            raise TypeError("calculator must implement AbstractPlaneWaveCalculator")
        if not isinstance(self.executor, AbstractSimulationDispatchEffect):
            raise TypeError("executor must implement AbstractSimulationDispatchEffect")
        if self.task.simulation_input != self.execution_input:
            raise ValueError("task and Simulation must retain the same execution input")

    @property
    def result_type(
        self,
    ) -> type[QuantumEspressoPwResult] | type[QuantumEspressoBandsResult]:
        """Return the immutable QE result class selected by the operation Task."""
        if type(self.task) is QuantumEspressoBandsExtractionTask:
            return QuantumEspressoBandsResult
        return QuantumEspressoPwResult
