"""Definition-only Quantum ESPRESSO simulation Task adapters.

Each Task owns one immutable QE execution input and its operation-specific intrinsic
correlations. Tasks perform no calculator invocation or external effect. Authorized
execution remains behind the Workflow simulation-dispatch control plane and
``AbstractSimulationDispatchEffect``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from ksdft2effmass.workflows import AbstractSimulationTask, TaskDefinitionIdentity

from .contracts import QuantumEspressoExecutionInput, QuantumEspressoProgram


@dataclass(frozen=True, slots=True)
class QuantumEspressoScfTask(AbstractSimulationTask):
    """Define one QE self-consistent-field simulation operation."""

    simulation_input: QuantumEspressoExecutionInput

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.scf.v1"
    )

    def __post_init__(self) -> None:
        """Validate the exact SCF input definition and predecessor shape."""
        _validate_input(self.simulation_input, self.identity)
        if self.simulation_input.program is not QuantumEspressoProgram.PW:
            raise ValueError("SCF input must use the pw program role")
        if self.simulation_input.predecessor_native_state:
            raise ValueError("SCF input must not contain predecessor native state")

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable SCF Task-definition identity."""
        return self._IDENTITY


@dataclass(frozen=True, slots=True)
class QuantumEspressoNscfTask(AbstractSimulationTask):
    """Define one QE non-self-consistent-field simulation operation."""

    simulation_input: QuantumEspressoExecutionInput

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.nscf.v1"
    )

    def __post_init__(self) -> None:
        """Validate the exact NSCF input definition and predecessor shape."""
        _validate_input(self.simulation_input, self.identity)
        if self.simulation_input.program is not QuantumEspressoProgram.PW:
            raise ValueError("NSCF input must use the pw program role")
        if len(self.simulation_input.predecessor_native_state) != 1:
            raise ValueError("NSCF input requires exactly one predecessor native state")

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable NSCF Task-definition identity."""
        return self._IDENTITY


@dataclass(frozen=True, slots=True)
class QuantumEspressoBandPathTask(AbstractSimulationTask):
    """Define one QE band-path ``pw`` simulation operation."""

    simulation_input: QuantumEspressoExecutionInput

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.band-path.v1"
    )

    def __post_init__(self) -> None:
        """Validate the exact band-path input and predecessor shape."""
        _validate_input(self.simulation_input, self.identity)
        if self.simulation_input.program is not QuantumEspressoProgram.PW:
            raise ValueError("band-path input must use the pw program role")
        if len(self.simulation_input.predecessor_native_state) != 1:
            raise ValueError(
                "band-path input requires exactly one predecessor native state"
            )

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable band-path Task-definition identity."""
        return self._IDENTITY


@dataclass(frozen=True, slots=True)
class QuantumEspressoBandsExtractionTask(AbstractSimulationTask):
    """Define one QE ``bands`` extraction simulation operation."""

    simulation_input: QuantumEspressoExecutionInput

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.bands-extraction.v1"
    )

    def __post_init__(self) -> None:
        """Validate the exact extraction input and predecessor shape."""
        _validate_input(self.simulation_input, self.identity)
        if self.simulation_input.program is not QuantumEspressoProgram.BANDS:
            raise ValueError("bands-extraction input must use the bands program role")
        if len(self.simulation_input.predecessor_native_state) != 1:
            raise ValueError(
                "bands-extraction input requires exactly one predecessor native state"
            )

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable extraction Task-definition identity."""
        return self._IDENTITY


def _validate_input(
    simulation_input: QuantumEspressoExecutionInput,
    identity: TaskDefinitionIdentity,
) -> None:
    """Validate shared exact input and Task-definition correlation."""
    if type(simulation_input) is not QuantumEspressoExecutionInput:
        raise TypeError("simulation_input must be QuantumEspressoExecutionInput")
    if simulation_input.task_definition_identity != identity:
        raise ValueError("simulation input must identify the exact Task definition")
