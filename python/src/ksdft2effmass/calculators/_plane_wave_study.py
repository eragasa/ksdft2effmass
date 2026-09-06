"""Private backend-neutral plane-wave parameter-study contract probe.

This module represents only exact study inputs and backend bindings. It renders no
native input, invokes no executable, interprets no QoI, and exports no stable API.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class PlaneWaveSimulationSpecificationIdentity:
    """Nominal identity of one portable plane-wave simulation specification."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("simulation-specification identity must be a string")
        if not self.value:
            raise ValueError("simulation-specification identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWavePhysicalModelIdentity:
    """Nominal identity of one complete physical/model branch."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("physical-model identity must be a string")
        if not self.value:
            raise ValueError("physical-model identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveObservationRequirementIdentity:
    """Nominal identity of one calculator-independent observation requirement."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("observation-requirement identity must be a string")
        if not self.value:
            raise ValueError("observation-requirement identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendIdentity:
    """Nominal identity and version of one selected plane-wave backend."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("backend identity must be a string")
        if not self.value:
            raise ValueError("backend identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendSupplementIdentity:
    """Nominal identity of one typed backend-specific supplement."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("backend-supplement identity must be a string")
        if not self.value:
            raise ValueError("backend-supplement identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendBindingIdentity:
    """Nominal identity of one exact portable-to-backend binding."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("backend-binding identity must be a string")
        if not self.value:
            raise ValueError("backend-binding identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveNativeConfigurationIdentity:
    """Nominal identity of one exact backend-native configuration artifact."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("native-configuration identity must be a string")
        if not self.value:
            raise ValueError("native-configuration identity must not be empty")


class PlaneWaveEnergyUnit(StrEnum):
    """Closed energy units admitted by the first private cutoff probe."""

    HARTREE = "hartree"
    RYDBERG = "rydberg"
    ELECTRON_VOLT = "electron_volt"


class PlaneWaveBackendCompilationOutcome(StrEnum):
    """Closed outcome of portable-to-backend compilation."""

    COMPILED = "compiled"
    UNSUPPORTED = "unsupported"
    INCOMPATIBLE = "incompatible"
    INVALID = "invalid"
    ERROR = "error"


class PlaneWaveBackendCompilationFailureCode(StrEnum):
    """Stable failure vocabulary for a future concrete backend binder."""

    UNSUPPORTED_REQUIREMENT = "unsupported_requirement"
    INCOMPATIBLE_MODEL_AND_SUPPLEMENT = "incompatible_model_and_supplement"
    INVALID_SPECIFICATION = "invalid_specification"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True, slots=True)
class PlaneWaveEnergyCutoff:
    """Positive finite plane-wave cutoff with an explicit energy unit."""

    value: float
    unit: PlaneWaveEnergyUnit

    def __post_init__(self) -> None:
        """Validate the exact numeric representation and unit."""
        if type(self.value) is not float:
            raise TypeError("cutoff value must be a float excluding bool and int")
        if not math.isfinite(self.value):
            raise ValueError("cutoff value must be finite")
        if self.value <= 0.0:
            raise ValueError("cutoff value must be positive")
        if type(self.unit) is not PlaneWaveEnergyUnit:
            raise TypeError("cutoff unit must be PlaneWaveEnergyUnit")


@dataclass(frozen=True, slots=True)
class PlaneWaveSimulationSpecification:
    """Portable meaning of one plane-wave candidate used by the private probe."""

    identity: PlaneWaveSimulationSpecificationIdentity
    physical_model_identity: PlaneWavePhysicalModelIdentity
    wavefunction_cutoff: PlaneWaveEnergyCutoff
    observation_requirement_identities: tuple[
        PlaneWaveObservationRequirementIdentity, ...
    ]

    def __post_init__(self) -> None:
        """Validate intrinsic specification closure."""
        if type(self.identity) is not PlaneWaveSimulationSpecificationIdentity:
            raise TypeError("identity must be PlaneWaveSimulationSpecificationIdentity")
        if type(self.physical_model_identity) is not PlaneWavePhysicalModelIdentity:
            raise TypeError(
                "physical_model_identity must be PlaneWavePhysicalModelIdentity"
            )
        if type(self.wavefunction_cutoff) is not PlaneWaveEnergyCutoff:
            raise TypeError("wavefunction_cutoff must be PlaneWaveEnergyCutoff")
        values = self.observation_requirement_identities
        if type(values) is not tuple or any(
            type(item) is not PlaneWaveObservationRequirementIdentity for item in values
        ):
            raise TypeError(
                "observation_requirement_identities must be a tuple of "
                "PlaneWaveObservationRequirementIdentity"
            )
        if not values:
            raise ValueError("observation_requirement_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("observation requirement identities must be unique")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendSupplement:
    """Exact typed supplement identity for one explicitly selected backend."""

    identity: PlaneWaveBackendSupplementIdentity
    backend_identity: PlaneWaveBackendIdentity
    native_configuration_identity: PlaneWaveNativeConfigurationIdentity

    def __post_init__(self) -> None:
        """Validate exact supplement fields without interpreting native content."""
        if type(self.identity) is not PlaneWaveBackendSupplementIdentity:
            raise TypeError("identity must be PlaneWaveBackendSupplementIdentity")
        if type(self.backend_identity) is not PlaneWaveBackendIdentity:
            raise TypeError("backend_identity must be PlaneWaveBackendIdentity")
        if (
            type(self.native_configuration_identity)
            is not PlaneWaveNativeConfigurationIdentity
        ):
            raise TypeError(
                "native_configuration_identity must be "
                "PlaneWaveNativeConfigurationIdentity"
            )


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendBinding:
    """Exact backend binding of one portable plane-wave specification."""

    identity: PlaneWaveBackendBindingIdentity
    specification: PlaneWaveSimulationSpecification
    supplement: PlaneWaveBackendSupplement

    def __post_init__(self) -> None:
        """Validate exact binding fields."""
        if type(self.identity) is not PlaneWaveBackendBindingIdentity:
            raise TypeError("identity must be PlaneWaveBackendBindingIdentity")
        if type(self.specification) is not PlaneWaveSimulationSpecification:
            raise TypeError("specification must be PlaneWaveSimulationSpecification")
        if type(self.supplement) is not PlaneWaveBackendSupplement:
            raise TypeError("supplement must be PlaneWaveBackendSupplement")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendCompilationCompiled:
    """Represent a complete exact backend binding ready for Workflow compilation."""

    outcome: PlaneWaveBackendCompilationOutcome
    binding: PlaneWaveBackendBinding

    def __post_init__(self) -> None:
        """Validate the closed successful result."""
        if self.outcome is not PlaneWaveBackendCompilationOutcome.COMPILED:
            raise ValueError("outcome must be COMPILED")
        if type(self.binding) is not PlaneWaveBackendBinding:
            raise TypeError("binding must be PlaneWaveBackendBinding")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendCompilationFailure:
    """Represent one fail-closed backend compilation outcome."""

    outcome: PlaneWaveBackendCompilationOutcome
    code: PlaneWaveBackendCompilationFailureCode

    def __post_init__(self) -> None:
        """Validate the closed failure result."""
        if self.outcome not in {
            PlaneWaveBackendCompilationOutcome.UNSUPPORTED,
            PlaneWaveBackendCompilationOutcome.INCOMPATIBLE,
            PlaneWaveBackendCompilationOutcome.INVALID,
            PlaneWaveBackendCompilationOutcome.ERROR,
        }:
            raise ValueError("outcome must be a backend failure outcome")
        if type(self.code) is not PlaneWaveBackendCompilationFailureCode:
            raise TypeError("code must be PlaneWaveBackendCompilationFailureCode")


type PlaneWaveBackendCompilationResult = (
    PlaneWaveBackendCompilationCompiled | PlaneWaveBackendCompilationFailure
)
"""Closed private result of binding one portable specification to a backend."""
