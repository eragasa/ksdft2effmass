r"""Software verification of ``PlaneWaveBackendBinding``.

Evidence profile: routine

Bounded artifact scope: exact portable plane-wave and native-supplement binding.

Facet and represented meaning

The module verifies that calculator-neutral specification state and backend-native
supplement state remain distinct immutable records.

Intrinsic and cross-object scope

``PlaneWaveBackendBinding`` is the sole system under test. Native rendering,
calculator execution, QoI evaluation, and backend equivalence are excluded.

VVUQ and scientific exclusions

This is software verification with synthetic identities. It establishes no physical
correctness, scientific validation, uncertainty quantification, or accepted setting.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.calculators._plane_wave_study import (
    PlaneWaveBackendBinding,
    PlaneWaveBackendBindingIdentity,
    PlaneWaveBackendIdentity,
    PlaneWaveBackendSupplement,
    PlaneWaveBackendSupplementIdentity,
    PlaneWaveEnergyCutoff,
    PlaneWaveEnergyUnit,
    PlaneWaveNativeConfigurationIdentity,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
    PlaneWaveSimulationSpecification,
    PlaneWaveSimulationSpecificationIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveBackendBinding


class TestPlaneWaveBackendBinding:
    """Own software evidence for exact portable-to-native binding."""

    def test_constructor__portable_and_native_state__remain_distinct(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-007

        Requirement: A portable plane-wave specification and typed backend supplement
        remain distinct immutable records joined only by an explicit binding.

        Acceptance: The binding preserves both exact records, exposes no mutation,
        and infers no backend default.
        """
        specification = PlaneWaveSimulationSpecification(
            PlaneWaveSimulationSpecificationIdentity("spec.cutoff.30"),
            PlaneWavePhysicalModelIdentity("pw-model.scalar.non-soc"),
            PlaneWaveEnergyCutoff(30.0, PlaneWaveEnergyUnit.RYDBERG),
            (PlaneWaveObservationRequirementIdentity("calculator.total-energy"),),
        )
        supplement = PlaneWaveBackendSupplement(
            PlaneWaveBackendSupplementIdentity("supplement.cutoff.30"),
            PlaneWaveBackendIdentity("quantum-espresso.7.5"),
            PlaneWaveNativeConfigurationIdentity("native-config:cutoff.30"),
        )
        binding = SUT(
            PlaneWaveBackendBindingIdentity("binding.cutoff.30"),
            specification,
            supplement,
        )
        assert binding.specification.wavefunction_cutoff.value == 30.0
        assert binding.supplement.backend_identity.value == "quantum-espresso.7.5"
        assert binding.supplement.native_configuration_identity.value == (
            "native-config:cutoff.30"
        )
        with pytest.raises(FrozenInstanceError):
            binding.identity = PlaneWaveBackendBindingIdentity("replacement")  # type: ignore[misc]
