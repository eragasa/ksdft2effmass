r"""Software verification of ``PlaneWaveEnergyCutoff``.

Evidence profile: routine

Bounded artifact scope: exact numeric and unit invariants of a plane-wave cutoff.

Facet and represented meaning

The module verifies the closed representation of one positive finite energy cutoff.

Intrinsic and cross-object scope

``PlaneWaveEnergyCutoff`` is the sole system under test. Simulation specification,
backend binding, calculator execution, and convergence interpretation are excluded.

VVUQ and scientific exclusions

This is software verification using illustrative scalar values. It establishes no
production cutoff, physical convergence, scientific validation, or uncertainty result.
"""

import pytest

from ksdft2effmass.calculators._plane_wave_study import (
    PlaneWaveEnergyCutoff,
    PlaneWaveEnergyUnit,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveEnergyCutoff


class TestPlaneWaveEnergyCutoff:
    """Own software evidence for cutoff value and unit invariants."""

    def test_constructor__value_type__rejects_numeric_string(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-CUTOFF-001

        Requirement: A cutoff value is an exact built-in finite positive ``float``;
        numeric strings are not accepted as implicit conversions.

        Acceptance: Constructing a cutoff with ``"30"`` raises ``TypeError`` naming
        the required float representation.
        """
        with pytest.raises(TypeError, match="float"):
            SUT(
                "30",  # type: ignore[arg-type]
                PlaneWaveEnergyUnit.RYDBERG,
            )
