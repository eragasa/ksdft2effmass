"""Software verification of Wigner--Seitz binary64 representability.

Synthetic diagonal lattices isolate determinant-range behavior independently of
conditioning, while integer representatives straddling ``2**53`` expose binary64
identity collapse. These tests establish fail-closed finite-representation behavior;
they do not establish lattice provenance, interpolation convergence, physical
adequacy, scientific validation, uncertainty quantification, or acceptance.
"""

import warnings

import numpy as np
import pytest

from ksdft2effmass.operators import MatrixQuantity, PhysicalUnit
from ksdft2effmass.solid_state.wignerseitz.interpolation import (
    WignerSeitzInterpolationInventory3D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestWignerSeitzInterpolationInventory3DBinary64Representability:
    """Own determinant-range and representative-identity failure evidence."""

    @staticmethod
    def inventory(
        scale: float,
        representatives: tuple[tuple[int, int, int], ...] = ((0, 0, 0),),
    ) -> WignerSeitzInterpolationInventory3D:
        """Return a synthetic one-residue inventory at the requested lattice scale."""
        multiplicity = len(representatives)
        return WignerSeitzInterpolationInventory3D(
            identifier="test.inventory",
            source_binding_identifier="test.source",
            mesh_shape=(1, 1, 1),
            direct_lattice=MatrixQuantity(
                np.eye(3, dtype=np.float64) * scale,
                PhysicalUnit("meter"),
            ),
            representatives=representatives,
            degeneracies=(multiplicity,) * multiplicity,
        )

    @pytest.mark.parametrize("scale", (1.0e200, 1.0e-200))
    def test_construction_accepts_nonsingular_lattice_without_range_warning(
        self, scale: float
    ) -> None:
        """A finite nonsingular diagonal lattice is not classified by raw det range."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            inventory = self.inventory(scale)

        assert inventory.direct_lattice.magnitude[0, 0] == scale

    def test_construction_rejects_binary64_representative_identity_collapse(
        self,
    ) -> None:
        """Distinct integer translations cannot share one interpolation coordinate."""
        exactly_representable = 2**53
        collapsed_successor = exactly_representable + 1

        with pytest.raises(
            OverflowError,
            match="distinct lattice translations would collapse",
        ):
            self.inventory(
                1.0,
                (
                    (0, 0, 0),
                    (exactly_representable, 0, 0),
                    (collapsed_successor, 0, 0),
                ),
            )
