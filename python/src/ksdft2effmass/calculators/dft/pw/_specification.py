"""Backend-neutral plane-wave DFT specification and binding records.

These immutable records describe one deliberately small portable specification and
its exact binding to an explicitly selected backend. They do not render native input,
invoke an executable, interpret a scientific quantity, select convergence settings,
or assert that nominally similar backend settings are equivalent.

The initial numerical vocabulary contains only a positive finite wavefunction energy
cutoff. Other discretization, physical-model, solver, and observation fields remain
outside this public contract until their shared meaning is demonstrated.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class PlaneWaveSimulationSpecificationIdentity:
    """Identify one exact portable plane-wave simulation specification.

    Attributes
    ----------
    value
        Nonempty built-in string in the identity namespace selected by the composing
        application. Equal text in another nominal identity class is not equivalent.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("simulation-specification identity must be a built-in str")
        if not self.value:
            raise ValueError("simulation-specification identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWavePhysicalModelIdentity:
    """Identify one complete fixed physical/model branch.

    Attributes
    ----------
    value
        Nonempty built-in string identifying the complete branch, including exact
        model choices and scientific assets outside this compact record.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("physical-model identity must be a built-in str")
        if not self.value:
            raise ValueError("physical-model identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveObservationRequirementIdentity:
    """Identify one calculator-independent observation requirement.

    Attributes
    ----------
    value
        Nonempty built-in string naming the exact observation requirement. The
        identity does not itself contain a value, unit, tolerance, or acceptance rule.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("observation-requirement identity must be a built-in str")
        if not self.value:
            raise ValueError("observation-requirement identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendIdentity:
    """Identify one explicitly selected plane-wave backend and version.

    Attributes
    ----------
    value
        Nonempty built-in string. Application composition owns the exact identity
        convention; no ambient backend discovery occurs.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("backend identity must be a built-in str")
        if not self.value:
            raise ValueError("backend identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendSupplementIdentity:
    """Identify one exact backend-specific supplement.

    Attributes
    ----------
    value
        Nonempty built-in string identifying an integration-owned supplement. The
        supplement content is intentionally not erased into a generic dictionary.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("backend-supplement identity must be a built-in str")
        if not self.value:
            raise ValueError("backend-supplement identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendBindingIdentity:
    """Identify one exact portable-to-backend binding.

    Attributes
    ----------
    value
        Nonempty built-in string identifying the complete binding rather than a
        backend label or nominally matching setting.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("backend-binding identity must be a built-in str")
        if not self.value:
            raise ValueError("backend-binding identity must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveNativeConfigurationIdentity:
    """Identify one exact backend-native configuration artifact.

    Attributes
    ----------
    value
        Nonempty built-in string identifying native configuration content retained by
        the concrete integration. Matching text does not establish content equality.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("native-configuration identity must be a built-in str")
        if not self.value:
            raise ValueError("native-configuration identity must not be empty")


class PlaneWaveEnergyUnit(StrEnum):
    """Energy units admitted for plane-wave cutoff values.

    Attributes
    ----------
    HARTREE
        Hartree atomic energy.
    RYDBERG
        Rydberg energy; one Rydberg is one half Hartree.
    ELECTRON_VOLT
        Electron volt.
    """

    HARTREE = "hartree"
    RYDBERG = "rydberg"
    ELECTRON_VOLT = "electron_volt"


class PlaneWaveBackendCompilationOutcome(StrEnum):
    """Closed outcome kinds for portable-to-backend compilation.

    Attributes
    ----------
    COMPILED
        A complete exact backend binding was produced.
    UNSUPPORTED
        The selected backend does not implement a required capability.
    INCOMPATIBLE
        Individually valid inputs cannot be combined.
    INVALID
        The request violates the portable specification contract.
    ERROR
        The binder failed internally without producing a partial binding.
    """

    COMPILED = "compiled"
    UNSUPPORTED = "unsupported"
    INCOMPATIBLE = "incompatible"
    INVALID = "invalid"
    ERROR = "error"


class PlaneWaveBackendCompilationFailureCode(StrEnum):
    """Closed backend-compilation failure codes.

    Attributes
    ----------
    UNSUPPORTED_REQUIREMENT
        A required portable capability has no supported native binding.
    INCOMPATIBLE_MODEL_AND_SUPPLEMENT
        The selected physical branch and backend supplement cannot be combined.
    INVALID_SPECIFICATION
        The portable specification is intrinsically invalid.
    INTERNAL_ERROR
        Binder implementation failed without a valid domain result.
    """

    UNSUPPORTED_REQUIREMENT = "unsupported_requirement"
    INCOMPATIBLE_MODEL_AND_SUPPLEMENT = "incompatible_model_and_supplement"
    INVALID_SPECIFICATION = "invalid_specification"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True, slots=True)
class PlaneWaveEnergyCutoff:
    """Represent a positive finite plane-wave energy cutoff.

    Attributes
    ----------
    value
        Positive finite built-in ``float``. Integers, booleans, strings, infinities,
        and NaNs are rejected; no unit conversion or overflow coercion is performed.
    unit
        Explicit energy unit for ``value``.
    """

    value: float
    unit: PlaneWaveEnergyUnit

    def __post_init__(self) -> None:
        if type(self.value) is not float:
            raise TypeError("cutoff value must be a built-in float excluding bool")
        if not math.isfinite(self.value):
            raise ValueError("cutoff value must be finite")
        if self.value <= 0.0:
            raise ValueError("cutoff value must be positive")
        if type(self.unit) is not PlaneWaveEnergyUnit:
            raise TypeError("cutoff unit must be PlaneWaveEnergyUnit")


@dataclass(frozen=True, slots=True)
class PlaneWaveSimulationSpecification:
    """Represent one portable plane-wave DFT simulation candidate.

    Attributes
    ----------
    identity
        Identity of this complete specification.
    physical_model_identity
        Identity of the fixed physical/model branch. Equality is required when a
        numerical study claims only discretization convergence.
    wavefunction_cutoff
        Plane-wave wavefunction-basis energy cutoff with explicit units.
    observation_requirement_identities
        Nonempty tuple of unique calculator-independent requirements. Tuple order is
        retained and must be supplied deliberately by the composing application.

    Notes
    -----
    This compact record does not contain a complete physical system, density cutoff,
    reciprocal-space mesh, solver policy, or native defaults. Those omissions are not
    implied defaults.
    """

    identity: PlaneWaveSimulationSpecificationIdentity
    physical_model_identity: PlaneWavePhysicalModelIdentity
    wavefunction_cutoff: PlaneWaveEnergyCutoff
    observation_requirement_identities: tuple[
        PlaneWaveObservationRequirementIdentity, ...
    ]

    def __post_init__(self) -> None:
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
    """Reference one exact typed supplement for an explicitly selected backend.

    Attributes
    ----------
    identity
        Identity of the complete supplement.
    backend_identity
        Exact backend and version for which the supplement is meaningful.
    native_configuration_identity
        Identity of the integration-owned native configuration artifact.
    """

    identity: PlaneWaveBackendSupplementIdentity
    backend_identity: PlaneWaveBackendIdentity
    native_configuration_identity: PlaneWaveNativeConfigurationIdentity

    def __post_init__(self) -> None:
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
    """Bind one portable specification to one exact backend supplement.

    Attributes
    ----------
    identity
        Identity of the complete portable-to-native binding.
    specification
        Complete portable plane-wave specification.
    supplement
        Exact selected backend and native-configuration reference.

    Notes
    -----
    Construction proves only nominal field validity. A concrete backend binder must
    separately establish support, compatibility, and complete parameter binding.
    """

    identity: PlaneWaveBackendBindingIdentity
    specification: PlaneWaveSimulationSpecification
    supplement: PlaneWaveBackendSupplement

    def __post_init__(self) -> None:
        if type(self.identity) is not PlaneWaveBackendBindingIdentity:
            raise TypeError("identity must be PlaneWaveBackendBindingIdentity")
        if type(self.specification) is not PlaneWaveSimulationSpecification:
            raise TypeError("specification must be PlaneWaveSimulationSpecification")
        if type(self.supplement) is not PlaneWaveBackendSupplement:
            raise TypeError("supplement must be PlaneWaveBackendSupplement")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendCompilationCompiled:
    """Represent successful complete backend compilation.

    Attributes
    ----------
    outcome
        Must be :attr:`PlaneWaveBackendCompilationOutcome.COMPILED`.
    binding
        Complete exact backend binding. No partial binding is represented.
    """

    outcome: PlaneWaveBackendCompilationOutcome
    binding: PlaneWaveBackendBinding

    def __post_init__(self) -> None:
        if type(self.outcome) is not PlaneWaveBackendCompilationOutcome:
            raise TypeError("outcome must be PlaneWaveBackendCompilationOutcome")
        if self.outcome is not PlaneWaveBackendCompilationOutcome.COMPILED:
            raise ValueError("outcome must be COMPILED")
        if type(self.binding) is not PlaneWaveBackendBinding:
            raise TypeError("binding must be PlaneWaveBackendBinding")


@dataclass(frozen=True, slots=True)
class PlaneWaveBackendCompilationFailure:
    """Represent one fail-closed backend-compilation result.

    Attributes
    ----------
    outcome
        One of ``unsupported``, ``incompatible``, ``invalid``, or ``error``.
    code
        Closed reason associated with the failed compilation. The pairing is exact:
        ``unsupported_requirement`` requires ``unsupported``,
        ``incompatible_model_and_supplement`` requires ``incompatible``,
        ``invalid_specification`` requires ``invalid``, and ``internal_error``
        requires ``error``. Contradictory pairs are rejected.
    """

    outcome: PlaneWaveBackendCompilationOutcome
    code: PlaneWaveBackendCompilationFailureCode

    def __post_init__(self) -> None:
        if type(self.outcome) is not PlaneWaveBackendCompilationOutcome:
            raise TypeError("outcome must be PlaneWaveBackendCompilationOutcome")
        if self.outcome is PlaneWaveBackendCompilationOutcome.COMPILED:
            raise ValueError("outcome must be a backend failure outcome")
        if type(self.code) is not PlaneWaveBackendCompilationFailureCode:
            raise TypeError("code must be PlaneWaveBackendCompilationFailureCode")
        expected_outcome = {
            PlaneWaveBackendCompilationFailureCode.UNSUPPORTED_REQUIREMENT: (
                PlaneWaveBackendCompilationOutcome.UNSUPPORTED
            ),
            PlaneWaveBackendCompilationFailureCode.INCOMPATIBLE_MODEL_AND_SUPPLEMENT: (
                PlaneWaveBackendCompilationOutcome.INCOMPATIBLE
            ),
            PlaneWaveBackendCompilationFailureCode.INVALID_SPECIFICATION: (
                PlaneWaveBackendCompilationOutcome.INVALID
            ),
            PlaneWaveBackendCompilationFailureCode.INTERNAL_ERROR: (
                PlaneWaveBackendCompilationOutcome.ERROR
            ),
        }[self.code]
        if self.outcome is not expected_outcome:
            raise ValueError("failure outcome must agree with failure code")


type PlaneWaveBackendCompilationResult = (
    PlaneWaveBackendCompilationCompiled | PlaneWaveBackendCompilationFailure
)
"""Closed result of binding one portable specification to a backend."""
