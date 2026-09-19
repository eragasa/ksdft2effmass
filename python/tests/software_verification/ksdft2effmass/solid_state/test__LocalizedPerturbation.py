r"""Software verification of ``LocalizedPerturbation``.

Evidence profile: routine

Bounded artifact scope: localized scalar onsite and bond perturbation inventories.

Facet and represented meaning

The DataObject retains deterministic mixed-term ordering and represented values.

Intrinsic and cross-object scope

One onsite term followed by one bond term is included.

VVUQ and scientific exclusions

This verifies data retention, not impurity-model adequacy or scientific validation.
"""

import pytest

from ksdft2effmass.operators import Unitless
from ksdft2effmass.solid_state import (
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
)

pytestmark = pytest.mark.software_verification
SUT = LocalizedPerturbation


class TestLocalizedPerturbation:
    """Own software evidence for ``LocalizedPerturbation``."""

    def test_constructor__terms__retains_onsite_then_bond_order(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-015

        Requirement: Canonical localized terms retain their complex scalar values.

        Acceptance: Onsite value ``0.2`` precedes bond value ``0.05``.
        """
        onsite = LocalizedOnsiteTerm(
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)), 0.2, 0.0
        )
        bond = LocalizedBondTerm(
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            LatticeDisplacement(LatticeDimension.TWO, (1, 1)),
            0.05,
            0.0,
        )
        perturbation = LocalizedPerturbation(
            "defect",
            LatticeDimension.TWO,
            (onsite, bond),
            Unitless(),
            "parent_zero",
            "scalar_cell_basis",
        )

        assert tuple(term.value for term in perturbation.terms) == (
            0.2 + 0.0j,
            0.05 + 0.0j,
        )
