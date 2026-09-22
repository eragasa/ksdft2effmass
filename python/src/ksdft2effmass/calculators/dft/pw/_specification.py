"""Backend-neutral plane-wave DFT specification and binding records.

These immutable records describe one deliberately small portable specification and
its exact binding to an explicitly selected backend. They do not render native input,
invoke an executable, interpret a scientific quantity, select convergence settings,
or assert that nominally similar backend settings are equivalent.

The numerical vocabulary contains a positive finite wavefunction energy cutoff and
an exact three-axis reciprocal-space mesh with explicit half-step shift flags. Other
discretization, physical-model, solver, and observation fields remain outside this
public contract until their shared meaning is demonstrated.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.units import UnitIdentity, UnitScalar


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
    """Represent a positive finite canonical plane-wave energy cutoff.

    Parameters
    ----------
    quantity
        Exact :class:`ksdft2effmass.units.UnitScalar` in electron volts. Native
        Hartree or Rydberg values require an explicit provenance-retaining conversion
        before construction; they are never relabelled or converted implicitly.
    """

    quantity: UnitScalar

    def __post_init__(self) -> None:
        if type(self.quantity) is not UnitScalar:
            raise TypeError("quantity must be UnitScalar")
        if self.quantity.unit is not UnitIdentity.ELECTRON_VOLT:
            raise ValueError("plane-wave cutoff quantity must use electron_volt")
        if self.quantity.value <= 0.0:
            raise ValueError("cutoff value must be positive")

    @property
    def value(self) -> float:
        """Return the finite canonical electron-volt value."""
        return self.quantity.value

    @property
    def unit(self) -> UnitIdentity:
        """Return the canonical electron-volt unit identity."""
        return self.quantity.unit


@dataclass(frozen=True, slots=True)
class PlaneWaveReciprocalMesh:
    """Represent one backend-neutral regular reciprocal-space sampling mesh.

    Parameters
    ----------
    axis_counts
        Exactly three positive built-in integers giving the number of regular
        sampling points along each reciprocal-lattice axis. Booleans, numeric
        strings, zero, negative values, and values above signed 64-bit range are
        rejected. No multiplication is performed, so construction cannot overflow.
    half_step_shifts
        Exactly three built-in Booleans. ``True`` means that the regular grid is
        shifted by one half of its grid spacing along the corresponding reciprocal
        axis; ``False`` means no shift along that axis.

    Notes
    -----
    This record defines grid cardinality and half-step displacement only. Reciprocal
    basis vectors, coordinate convention, symmetry reduction, weights, integration
    method, native syntax, and backend defaults remain outside this compact contract.
    Equal mesh records do not establish backend equivalence.
    """

    axis_counts: tuple[int, int, int]
    half_step_shifts: tuple[bool, bool, bool]

    def __post_init__(self) -> None:
        """Validate exact tuple shape, scalar types, positivity, and i64 bounds."""
        if type(self.axis_counts) is not tuple:
            raise TypeError("axis_counts must be a built-in tuple")
        if len(self.axis_counts) != 3:
            raise ValueError("axis_counts must contain exactly three values")
        if any(type(value) is not int for value in self.axis_counts):
            raise TypeError("axis_counts must contain built-in integers excluding bool")
        if any(value <= 0 for value in self.axis_counts):
            raise ValueError("axis_counts must be positive")
        if any(value > 2**63 - 1 for value in self.axis_counts):
            raise ValueError("axis_counts must fit signed 64-bit integers")
        if type(self.half_step_shifts) is not tuple:
            raise TypeError("half_step_shifts must be a built-in tuple")
        if len(self.half_step_shifts) != 3:
            raise ValueError("half_step_shifts must contain exactly three values")
        if any(type(value) is not bool for value in self.half_step_shifts):
            raise TypeError("half_step_shifts must contain built-in Booleans")


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
    reciprocal_mesh
        Exact regular reciprocal-space grid cardinalities and half-step shift flags.
        Native coordinate syntax, symmetry reduction, and quadrature weights remain
        integration-owned.
    observation_requirement_identities
        Nonempty tuple of unique calculator-independent requirements. Tuple order is
        retained and must be supplied deliberately by the composing application.

    Notes
    -----
    This compact record does not contain a complete physical system, density cutoff,
    reciprocal basis, symmetry-reduced point list, quadrature weights, solver policy,
    or native defaults. Those omissions are not implied defaults.
    """

    identity: PlaneWaveSimulationSpecificationIdentity
    physical_model_identity: PlaneWavePhysicalModelIdentity
    wavefunction_cutoff: PlaneWaveEnergyCutoff
    reciprocal_mesh: PlaneWaveReciprocalMesh
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
        if type(self.reciprocal_mesh) is not PlaneWaveReciprocalMesh:
            raise TypeError("reciprocal_mesh must be PlaneWaveReciprocalMesh")
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
