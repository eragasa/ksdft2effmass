r"""Software verification of ``ParticleInBoxParameters``.

Evidence profile: routine

Bounded artifact scope: public unit-aware one-dimensional box parameter contract.

Facet and represented meaning

The DataObject owns positive length, mass, and action quantities in one unit mode.

Intrinsic and cross-object scope

Type, positivity, dimensional compatibility, and canonical length are included.

VVUQ and scientific exclusions

This verifies software invariants only, not physical-model adequacy, validation,
uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxParameters,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxParameters


class TestParticleInBoxParameters:
    """Own software evidence for ``ParticleInBoxParameters``."""

    def test_constructor__unit_mode__accepts_coherent_physical_and_unitless_values(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PIB-001

        Requirement: Parameters are positive and either wholly Unitless or dimensionally
        physical.

        Acceptance: Unitless values construct exactly, centimeters canonicalize to
        meters, and mixed unit modes are rejected.
        """
        normalized = ParticleInBoxParameters(
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
        )
        physical = ParticleInBoxParameters(
            ScalarQuantity(100.0, PhysicalUnit("centimeter")),
            ScalarQuantity(1.0, PhysicalUnit("kilogram")),
            ScalarQuantity(1.0, PhysicalUnit("joule * second")),
        )

        assert normalized.is_nondimensional
        assert physical.canonical_length == ScalarQuantity(1.0, PhysicalUnit("meter"))
        with pytest.raises(ValueError, match="one unit mode"):
            ParticleInBoxParameters(
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(1.0, PhysicalUnit("kilogram")),
                ScalarQuantity(1.0, Unitless()),
            )
