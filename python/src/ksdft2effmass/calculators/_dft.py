"""Private immutable contracts for the first cross-backend DFT workflow slice.

The concrete records preserve calculator and operation distinctions.  They are
not a stable public API, a runtime plugin registry, an execution-authority
model, or a claim that backend settings are scientifically equivalent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar, runtime_checkable

from ksdft2effmass.workflows import ResultObjectIdentity, TaskExecutionContext


@dataclass(frozen=True, slots=True)
class SimulationInputIdentity:
    """Nominal identity of one exact calculator-specific simulation input."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("simulation input identity value must be a string")
        if not self.value:
            raise ValueError("simulation input identity value must not be empty")


@dataclass(frozen=True, slots=True)
class CalculatorArtifactIdentity:
    """Nominal identity of one exact native calculator artifact or artifact set."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("calculator artifact identity value must be a string")
        if not self.value:
            raise ValueError("calculator artifact identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ProcessObservationIdentity:
    """Nominal identity of one retained mechanical process observation."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("process observation identity value must be a string")
        if not self.value:
            raise ValueError("process observation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoScfInput:
    """Exact QE input and pseudopotential identities for one logical SCF step."""

    identity: SimulationInputIdentity
    native_input_identity: CalculatorArtifactIdentity
    pseudopotential_identities: tuple[CalculatorArtifactIdentity, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic QE SCF-input fields."""
        if type(self.identity) is not SimulationInputIdentity:
            raise TypeError("identity must be SimulationInputIdentity")
        if type(self.native_input_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_input_identity must be CalculatorArtifactIdentity")
        values = self.pseudopotential_identities
        if type(values) is not tuple or any(
            type(item) is not CalculatorArtifactIdentity for item in values
        ):
            raise TypeError(
                "pseudopotential_identities must be a tuple of "
                "CalculatorArtifactIdentity"
            )
        if not values:
            raise ValueError("pseudopotential_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("pseudopotential_identities must be unique")


@dataclass(frozen=True, slots=True)
class AbinitScfInput:
    """Exact ABINIT input and pseudopotential identities for one logical SCF step."""

    identity: SimulationInputIdentity
    native_input_identity: CalculatorArtifactIdentity
    pseudopotential_identities: tuple[CalculatorArtifactIdentity, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic ABINIT SCF-input fields."""
        if type(self.identity) is not SimulationInputIdentity:
            raise TypeError("identity must be SimulationInputIdentity")
        if type(self.native_input_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_input_identity must be CalculatorArtifactIdentity")
        values = self.pseudopotential_identities
        if type(values) is not tuple or any(
            type(item) is not CalculatorArtifactIdentity for item in values
        ):
            raise TypeError(
                "pseudopotential_identities must be a tuple of "
                "CalculatorArtifactIdentity"
            )
        if not values:
            raise ValueError("pseudopotential_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("pseudopotential_identities must be unique")


@dataclass(frozen=True, slots=True)
class QuantumEspressoFixedDensityBandsInput:
    """Exact QE bands input bound to an already-produced QE SCF state."""

    identity: SimulationInputIdentity
    native_input_identity: CalculatorArtifactIdentity
    pseudopotential_identities: tuple[CalculatorArtifactIdentity, ...]
    scf_output_identity: ResultObjectIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE fixed-density-bands input fields."""
        if type(self.identity) is not SimulationInputIdentity:
            raise TypeError("identity must be SimulationInputIdentity")
        if type(self.native_input_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_input_identity must be CalculatorArtifactIdentity")
        values = self.pseudopotential_identities
        if type(values) is not tuple or any(
            type(item) is not CalculatorArtifactIdentity for item in values
        ):
            raise TypeError(
                "pseudopotential_identities must be a tuple of "
                "CalculatorArtifactIdentity"
            )
        if not values:
            raise ValueError("pseudopotential_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("pseudopotential_identities must be unique")
        if type(self.scf_output_identity) is not ResultObjectIdentity:
            raise TypeError("scf_output_identity must be ResultObjectIdentity")
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class AbinitFixedDensityBandsInput:
    """Exact ABINIT bands input bound to an already-produced ABINIT SCF state."""

    identity: SimulationInputIdentity
    native_input_identity: CalculatorArtifactIdentity
    pseudopotential_identities: tuple[CalculatorArtifactIdentity, ...]
    scf_output_identity: ResultObjectIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic ABINIT fixed-density-bands input fields."""
        if type(self.identity) is not SimulationInputIdentity:
            raise TypeError("identity must be SimulationInputIdentity")
        if type(self.native_input_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_input_identity must be CalculatorArtifactIdentity")
        values = self.pseudopotential_identities
        if type(values) is not tuple or any(
            type(item) is not CalculatorArtifactIdentity for item in values
        ):
            raise TypeError(
                "pseudopotential_identities must be a tuple of "
                "CalculatorArtifactIdentity"
            )
        if not values:
            raise ValueError("pseudopotential_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("pseudopotential_identities must be unique")
        if type(self.scf_output_identity) is not ResultObjectIdentity:
            raise TypeError("scf_output_identity must be ResultObjectIdentity")
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoNscfInput:
    """Exact QE NSCF input bound to one admitted QE SCF state."""

    identity: SimulationInputIdentity
    native_input_identity: CalculatorArtifactIdentity
    pseudopotential_identities: tuple[CalculatorArtifactIdentity, ...]
    scf_output_identity: ResultObjectIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE NSCF-input fields."""
        if type(self.identity) is not SimulationInputIdentity:
            raise TypeError("identity must be SimulationInputIdentity")
        if type(self.native_input_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_input_identity must be CalculatorArtifactIdentity")
        values = self.pseudopotential_identities
        if type(values) is not tuple or any(
            type(item) is not CalculatorArtifactIdentity for item in values
        ):
            raise TypeError(
                "pseudopotential_identities must be a tuple of "
                "CalculatorArtifactIdentity"
            )
        if not values:
            raise ValueError("pseudopotential_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("pseudopotential_identities must be unique")
        if type(self.scf_output_identity) is not ResultObjectIdentity:
            raise TypeError("scf_output_identity must be ResultObjectIdentity")
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoDosInput:
    """Exact QE DOS input bound to one admitted QE NSCF state."""

    identity: SimulationInputIdentity
    native_input_identity: CalculatorArtifactIdentity
    nscf_output_identity: ResultObjectIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE DOS-input fields."""
        if type(self.identity) is not SimulationInputIdentity:
            raise TypeError("identity must be SimulationInputIdentity")
        if type(self.native_input_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_input_identity must be CalculatorArtifactIdentity")
        if type(self.nscf_output_identity) is not ResultObjectIdentity:
            raise TypeError("nscf_output_identity must be ResultObjectIdentity")
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoScfOutput:
    """Imported or newly returned mechanical QE SCF result."""

    identity: ResultObjectIdentity
    input_identity: SimulationInputIdentity
    process_observation_identity: ProcessObservationIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE SCF-output fields."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.input_identity) is not SimulationInputIdentity:
            raise TypeError("input_identity must be SimulationInputIdentity")
        if type(self.process_observation_identity) is not ProcessObservationIdentity:
            raise TypeError(
                "process_observation_identity must be ProcessObservationIdentity"
            )
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class AbinitScfOutput:
    """Imported or newly returned mechanical ABINIT SCF result."""

    identity: ResultObjectIdentity
    input_identity: SimulationInputIdentity
    process_observation_identity: ProcessObservationIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic ABINIT SCF-output fields."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.input_identity) is not SimulationInputIdentity:
            raise TypeError("input_identity must be SimulationInputIdentity")
        if type(self.process_observation_identity) is not ProcessObservationIdentity:
            raise TypeError(
                "process_observation_identity must be ProcessObservationIdentity"
            )
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoFixedDensityBandsOutput:
    """Imported or newly returned mechanical QE fixed-density-bands result."""

    identity: ResultObjectIdentity
    input_identity: SimulationInputIdentity
    process_observation_identity: ProcessObservationIdentity
    native_band_result_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE bands-output fields."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.input_identity) is not SimulationInputIdentity:
            raise TypeError("input_identity must be SimulationInputIdentity")
        if type(self.process_observation_identity) is not ProcessObservationIdentity:
            raise TypeError(
                "process_observation_identity must be ProcessObservationIdentity"
            )
        if type(self.native_band_result_identity) is not CalculatorArtifactIdentity:
            raise TypeError(
                "native_band_result_identity must be CalculatorArtifactIdentity"
            )


@dataclass(frozen=True, slots=True)
class AbinitFixedDensityBandsOutput:
    """Imported or newly returned mechanical ABINIT fixed-density-bands result."""

    identity: ResultObjectIdentity
    input_identity: SimulationInputIdentity
    process_observation_identity: ProcessObservationIdentity
    native_band_result_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic ABINIT bands-output fields."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.input_identity) is not SimulationInputIdentity:
            raise TypeError("input_identity must be SimulationInputIdentity")
        if type(self.process_observation_identity) is not ProcessObservationIdentity:
            raise TypeError(
                "process_observation_identity must be ProcessObservationIdentity"
            )
        if type(self.native_band_result_identity) is not CalculatorArtifactIdentity:
            raise TypeError(
                "native_band_result_identity must be CalculatorArtifactIdentity"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoNscfOutput:
    """Imported or newly returned mechanical QE NSCF result and native state."""

    identity: ResultObjectIdentity
    input_identity: SimulationInputIdentity
    process_observation_identity: ProcessObservationIdentity
    native_state_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE NSCF-output fields."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.input_identity) is not SimulationInputIdentity:
            raise TypeError("input_identity must be SimulationInputIdentity")
        if type(self.process_observation_identity) is not ProcessObservationIdentity:
            raise TypeError(
                "process_observation_identity must be ProcessObservationIdentity"
            )
        if type(self.native_state_identity) is not CalculatorArtifactIdentity:
            raise TypeError("native_state_identity must be CalculatorArtifactIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoDosOutput:
    """Imported or newly returned mechanical QE DOS result artifact."""

    identity: ResultObjectIdentity
    input_identity: SimulationInputIdentity
    process_observation_identity: ProcessObservationIdentity
    native_dos_result_identity: CalculatorArtifactIdentity

    def __post_init__(self) -> None:
        """Validate intrinsic QE DOS-output fields."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.input_identity) is not SimulationInputIdentity:
            raise TypeError("input_identity must be SimulationInputIdentity")
        if type(self.process_observation_identity) is not ProcessObservationIdentity:
            raise TypeError(
                "process_observation_identity must be ProcessObservationIdentity"
            )
        if type(self.native_dos_result_identity) is not CalculatorArtifactIdentity:
            raise TypeError(
                "native_dos_result_identity must be CalculatorArtifactIdentity"
            )


type SimulationTypeInput = (
    QuantumEspressoScfInput
    | AbinitScfInput
    | QuantumEspressoFixedDensityBandsInput
    | AbinitFixedDensityBandsInput
    | QuantumEspressoNscfInput
    | QuantumEspressoDosInput
)
"""Closed calculator-specific input union for the internal architecture probe."""


type SimulationTypeOutput = (
    QuantumEspressoScfOutput
    | AbinitScfOutput
    | QuantumEspressoFixedDensityBandsOutput
    | AbinitFixedDensityBandsOutput
    | QuantumEspressoNscfOutput
    | QuantumEspressoDosOutput
)
"""Closed calculator-specific output union for the internal architecture probe."""


_InputT = TypeVar("_InputT", bound=SimulationTypeInput, contravariant=True)
_OutputT = TypeVar("_OutputT", bound=SimulationTypeOutput, covariant=True)


@runtime_checkable
class DftCalculator(Protocol[_InputT, _OutputT]):
    """Narrow injected consumer port for one exact DFT operation.

    Protocol conformance supplies neither execution authority nor a calculator
    registry.  A caller may invoke this port only after the separately owned
    workflow-control and executor-boundary checks have admitted the exact
    operation.
    """

    def execute(
        self,
        simulation_input: _InputT,
        context: TaskExecutionContext,
    ) -> _OutputT:
        """Return one new immutable result for the exact admitted operation."""
        ...
