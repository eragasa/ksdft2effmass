r"""Software verification of ``BlockHoppingModel1D``.

Evidence profile: routine

Bounded artifact scope: extracted Appendix G periodic-1D public contract.

Facet and represented meaning

The public class retains or transforms the explicitly represented periodic-1D values.

Intrinsic and cross-object scope

Construction invariants and the demonstrated public operation are included.

VVUQ and scientific exclusions

This is software verification, not a rerun or scientific validation of Appendix G.
"""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.periodic.lattice.hopping import DenseBlockHoppingModel
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.solidstate import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingModel1D


class TestBlockHoppingModel1D:
    """Verify ordered matrix-valued cell-hopping models."""

    def test_constructor__hoppings__retains_block_dimension_and_maximum_range(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-003

        Requirement: The public contract enforces retains block dimension and
        maximum range.

        Acceptance: The asserted values and failures match the declared contract.
        """
        block = ComplexMatrixQuantity(np.eye(2, dtype=np.complex128), Unitless())

        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (-2, 0, 3), (block, block, block)
        )

        assert model.matrix_dimension == 2
        assert model.maximum_range == 3

    def test_method__to_physkit_ordinary_representation__preserves_arbitrary_rank(
        self,
    ) -> None:
        """Map ordinary integer support without narrowing the represented block rank.

        Notes
        -----
        The three-state fixture establishes that representation conversion remains
        independent of the separately approved rank-two scientific-model hierarchy.
        The reciprocal period stays on the source because this operation does not infer
        a physical direct lattice from a coordinate-period convention.

        """
        unit = Unitless()
        reciprocal_period = ScalarQuantity(1.0, unit)
        blocks = tuple(
            ComplexMatrixQuantity(
                np.eye(3, dtype=np.complex128) * float(index + 1),
                unit,
            )
            for index in range(3)
        )
        source = BlockHoppingModel1D(
            reciprocal_period=reciprocal_period,
            representatives=(-1, 0, 1),
            hopping_blocks=blocks,
        )

        representation = source.to_physkit_ordinary_representation(
            identifier="legacy-rank3-ordinary-v1",
            energy_reference="dimensionless-zero-v1",
            basis_identifier="ordered-rank3-basis-v1",
        )

        assert type(representation) is DenseBlockHoppingModel
        assert representation.dimension is LatticeDimension.ONE
        assert representation.basis_size == 3
        assert representation.energy_unit is unit
        assert representation.energy_reference == "dimensionless-zero-v1"
        assert representation.basis_identifier == "ordered-rank3-basis-v1"
        assert tuple(term.displacement.components for term in representation.terms) == (
            (-1,),
            (0,),
            (1,),
        )
        assert all(
            term.coefficient is block
            for term, block in zip(
                representation.terms,
                blocks,
                strict=True,
            )
        )
        assert source.reciprocal_period is reciprocal_period

    def test_method__to_physkit_ordinary_representation__requires_identities(
        self,
    ) -> None:
        """Reject missing scientific identities rather than deriving them from data."""
        unit = Unitless()
        block = ComplexMatrixQuantity(np.eye(1, dtype=np.complex128), unit)
        source = BlockHoppingModel1D(
            ScalarQuantity(1.0, unit),
            (0,),
            (block,),
        )

        with pytest.raises(ValueError, match="energy_reference must be nonempty"):
            source.to_physkit_ordinary_representation(
                identifier="ordinary-rank1-v1",
                energy_reference="",
                basis_identifier="ordered-rank1-basis-v1",
            )

    def test_constructor__hoppings__rejects_unsorted_or_duplicate_representatives(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-004

        Requirement: The public contract enforces rejects unsorted or duplicate
        representatives.

        Acceptance: The asserted values and failures match the declared contract.
        """
        block = ComplexMatrixQuantity(np.eye(1, dtype=np.complex128), Unitless())

        with pytest.raises(ValueError, match="strictly increasing"):
            BlockHoppingModel1D(
                ScalarQuantity(1.0, Unitless()), (0, -1, 0), (block, block, block)
            )
