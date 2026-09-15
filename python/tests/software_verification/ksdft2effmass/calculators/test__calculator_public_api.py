r"""Software verification of public calculator package surface.

Evidence profile: routine

Bounded artifact scope: calculator package ownership, exports, and probe retirement.

Facet and represented meaning

The artifact verifies that backend-neutral plane-wave contracts are exposed only from
``ksdft2effmass.calculators.dft.pw`` while the superseded backend-specific probe
has no importable implementation or package-root compatibility aliases.

Intrinsic and cross-object scope

Tests cover the exact public-name inventory and package topology. Individual object
invariants, integration-owned native records, and Workflow behavior remain with their
class or package owners.

VVUQ and scientific exclusions

This is structural software verification. It establishes no calculator execution,
numerical verification, scientific validation, uncertainty quantification, backend
equivalence, production readiness, or human acceptance.
"""

import importlib.util

import pytest

import ksdft2effmass.calculators as calculators
import ksdft2effmass.calculators.dft as dft
import ksdft2effmass.calculators.dft.pw as plane_wave

pytestmark = pytest.mark.software_verification


class TestCalculatorPublicApi:
    """Own package-level calculator public-surface evidence."""

    def test_public_api__package__exports_exact_plane_wave_contracts(self) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-006

        Requirement: The canonical plane-wave package exports exactly the accepted
        backend-neutral specification, binding, compilation-result, and calculator
        port names.

        Acceptance: ``__all__`` equals the explicit contract inventory and every name
        resolves to an object defined beneath the calculator package.
        """
        expected = (
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
            "PlaneWaveEnergyUnit",
            "PlaneWaveNativeConfigurationIdentity",
            "PlaneWaveObservationRequirementIdentity",
            "PlaneWavePhysicalModelIdentity",
            "PlaneWaveSimulationSpecification",
            "PlaneWaveSimulationSpecificationIdentity",
        )

        assert tuple(plane_wave.__all__) == expected
        assert all(hasattr(plane_wave, name) for name in expected)
        defining_modules = tuple(
            getattr(getattr(plane_wave, name), "__module__", "") for name in expected
        )
        assert all(
            module.startswith("ksdft2effmass.calculators.dft.pw")
            for module in defining_modules
        )

    def test_public_api__package__keeps_retired_backend_specific_probe_absent(
        self,
    ) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-008

        Requirement: Calculator and DFT package roots expose no backend-specific
        native records or compatibility aliases for the retired ``calculators._dft``
        probe.

        Acceptance: Both roots declare no export inventory, representative QE and
        ABINIT names are absent, and Python cannot resolve the retired probe module.
        """
        prohibited = (
            "AbinitScfInput",
            "DftCalculator",
            "QuantumEspressoScfInput",
            "SimulationInputIdentity",
        )

        assert not hasattr(calculators, "__all__")
        assert not hasattr(dft, "__all__")
        assert all(not hasattr(calculators, name) for name in prohibited)
        assert all(not hasattr(dft, name) for name in prohibited)
        assert importlib.util.find_spec("ksdft2effmass.calculators._dft") is None
