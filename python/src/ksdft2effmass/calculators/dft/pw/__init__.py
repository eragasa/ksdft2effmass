"""Public backend-neutral plane-wave DFT calculator contracts.

``pw`` denotes the plane-wave numerical method; it does not denote Quantum
ESPRESSO's ``pw.x`` executable. Concrete native records and effects remain owned by
packages such as :mod:`ksdft2effmass.integration.quantum_espresso`.
"""

from ._calculator import PlaneWaveCalculator
from ._specification import (
    PlaneWaveBackendBinding,
    PlaneWaveBackendBindingIdentity,
    PlaneWaveBackendCompilationCompiled,
    PlaneWaveBackendCompilationFailure,
    PlaneWaveBackendCompilationFailureCode,
    PlaneWaveBackendCompilationOutcome,
    PlaneWaveBackendCompilationResult,
    PlaneWaveBackendIdentity,
    PlaneWaveBackendSupplement,
    PlaneWaveBackendSupplementIdentity,
    PlaneWaveEnergyCutoff,
    PlaneWaveNativeConfigurationIdentity,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
    PlaneWaveReciprocalMesh,
    PlaneWaveSimulationSpecification,
    PlaneWaveSimulationSpecificationIdentity,
)

__all__ = [
    "PlaneWaveBackendBinding",
    "PlaneWaveBackendBindingIdentity",
    "PlaneWaveBackendCompilationCompiled",
    "PlaneWaveBackendCompilationFailure",
    "PlaneWaveBackendCompilationFailureCode",
    "PlaneWaveBackendCompilationOutcome",
    "PlaneWaveBackendCompilationResult",
    "PlaneWaveBackendIdentity",
    "PlaneWaveBackendSupplement",
    "PlaneWaveBackendSupplementIdentity",
    "PlaneWaveCalculator",
    "PlaneWaveEnergyCutoff",
    "PlaneWaveNativeConfigurationIdentity",
    "PlaneWaveObservationRequirementIdentity",
    "PlaneWavePhysicalModelIdentity",
    "PlaneWaveReciprocalMesh",
    "PlaneWaveSimulationSpecification",
    "PlaneWaveSimulationSpecificationIdentity",
]
