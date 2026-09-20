r"""Software verification of ``ParticleInBoxAnalytical``.

Evidence profile: routine

Bounded artifact scope: public analytical one-dimensional Dirichlet-box spectrum.

Facet and represented meaning

The model owns continuum mode ordering and energy scaling for one declared box.

Intrinsic and cross-object scope

Mode indexing, represented values, and energy units are included.

VVUQ and scientific exclusions

This is software verification of the declared formula, not material validation,
uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxAnalytical,
    ParticleInBoxParameters,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxAnalytical


class TestParticleInBoxAnalytical:
    """Own software evidence for ``ParticleInBoxAnalytical``."""

    def test_method__energy_levels__returns_ordered_continuum_spectrum(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PIB-002

        Requirement: Unitless ``L=m=hbar=1`` energies are ``pi**2*n**2/2`` for
        one-based ascending mode indices.

        Acceptance: The first three values equal the independently stated expression.
        """
        model = ParticleInBoxAnalytical(
            ParticleInBoxParameters(
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
            )
        )

        np.testing.assert_array_equal(
            model.energy_levels(3).magnitude,
            np.pi * np.pi * np.array([1.0, 4.0, 9.0]) / 2.0,
        )
        assert isinstance(model.energy_levels(3).unit, Unitless)
