r"""Software verification of ``ScalarHoppingModel``.

Evidence profile: routine

Bounded artifact scope: deterministic scalar hopping inventories.

Facet and represented meaning

The DataObject retains explicit dimension, units, references, and canonical terms.

Intrinsic and cross-object scope

Complex scalar values and duplicate-displacement rejection are included.

VVUQ and scientific exclusions

This verifies represented terms, not Hermiticity or a finite Hamiltonian.
"""

import pytest

from ksdft2effmass.operators import Unitless
from ksdft2effmass.solid_state import (
    LatticeDimension,
    LatticeDisplacement,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarHoppingModel


class TestScalarHoppingModel:
    """Own software evidence for ``ScalarHoppingModel``."""

    def test_constructor__terms__retains_order_and_rejects_duplicates(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-005

        Requirement: Canonical hopping terms retain exact complex values and unique
        displacements.

        Acceptance: A two-term 2D model constructs and a duplicate displacement fails.
        """
        negative = ScalarHoppingTerm(
            LatticeDisplacement(LatticeDimension.TWO, (-1, 0)), -1.0, 0.0
        )
        positive = ScalarHoppingTerm(
            LatticeDisplacement(LatticeDimension.TWO, (1, 0)), -1.0, 0.0
        )
        model = ScalarHoppingModel(
            "parent",
            LatticeDimension.TWO,
            (negative, positive),
            Unitless(),
            "parent_zero",
            "scalar_cell_basis",
        )

        assert tuple(term.value for term in model.terms) == (-1.0 + 0.0j,) * 2
        with pytest.raises(ValueError, match="sorted and unique"):
            ScalarHoppingModel(
                "duplicate",
                LatticeDimension.TWO,
                (negative, negative),
                Unitless(),
                "parent_zero",
                "scalar_cell_basis",
            )
