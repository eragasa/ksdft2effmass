r"""Software verification of ``PlaneWaveEnergyCutoff``.

Evidence profile: routine

Bounded artifact scope: canonical quantity and positivity invariants of a cutoff.

Facet and represented meaning

The module verifies one positive finite electron-volt cutoff after explicit conversion.

Intrinsic and cross-object scope

``PlaneWaveEnergyCutoff`` is the sole system under test. Unit conversion, simulation
specification, backend binding, execution, and convergence interpretation are excluded.

VVUQ and scientific exclusions

This is software verification using illustrative scalar values. It establishes no
production cutoff, physical convergence, validation, or uncertainty result.
"""

import pytest

from ksdft2effmass.calculators.dft.pw import PlaneWaveEnergyCutoff
from ksdft2effmass.units import UnitIdentity, UnitScalar

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveEnergyCutoff


class TestPlaneWaveEnergyCutoff:
    """Own software evidence for canonical cutoff quantity invariants."""

    def test_constructor__electron_volt_quantity__retains_canonical_value(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-CUTOFF-001

        Requirement: A portable cutoff is an explicit positive canonical eV scalar.

        Acceptance: Construction retains the exact typed quantity and exposes its
        finite value and electron-volt identity.
        """
        quantity = UnitScalar(408.0, UnitIdentity.ELECTRON_VOLT)

        cutoff = SUT(quantity)

        assert cutoff.quantity is quantity
        assert cutoff.value == 408.0
        assert cutoff.unit is UnitIdentity.ELECTRON_VOLT

    def test_constructor__native_unit_without_conversion__rejects_relabelling(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-CUTOFF-002

        Requirement: Hartree or Rydberg values require an explicit conversion result
        before entering the canonical portable specification.

        Acceptance: A finite Rydberg scalar raises ``ValueError`` naming eV.
        """
        with pytest.raises(ValueError, match="electron_volt"):
            SUT(UnitScalar(30.0, UnitIdentity.RYDBERG))

    @pytest.mark.parametrize("invalid_value", [0.0, -1.0], ids=["zero", "negative"])
    def test_constructor__nonpositive_value__rejects_invalid_cutoff(
        self, invalid_value: float
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-CUTOFF-003

        Requirement: A plane-wave cutoff is positive.

        Acceptance: Zero and negative canonical quantities raise ``ValueError``.
        """
        with pytest.raises(ValueError, match="positive"):
            SUT(UnitScalar(invalid_value, UnitIdentity.ELECTRON_VOLT))
