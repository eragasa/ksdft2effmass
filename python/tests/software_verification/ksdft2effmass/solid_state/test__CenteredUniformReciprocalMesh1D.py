r"""Software verification of ``CenteredUniformReciprocalMesh1D``.

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

from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity
from ksdft2effmass.solid_state import CenteredUniformReciprocalMesh1D

pytestmark = pytest.mark.software_verification
SUT = CenteredUniformReciprocalMesh1D


class TestCenteredUniformReciprocalMesh1D:
    """Verify the centered half-open reciprocal-mesh contract."""

    def test_constructor__geometry__enumerates_appendix_g_mesh_and_representatives(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-007

        Requirement: The public contract enforces enumerates appendix g mesh and
        representatives.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, PhysicalUnit("1 / nanometer")), 4
        )

        np.testing.assert_array_equal(
            mesh.coordinates.magnitude,
            np.asarray([-0.5, -0.25, 0.0, 0.25], dtype=np.float64),
        )
        assert mesh.spacing.magnitude == 0.25
        assert mesh.spacing.unit == mesh.reciprocal_period.unit
        assert mesh.centered_cell_representatives == (-2, -1, 0, 1)
        assert mesh.coordinates.magnitude.flags.writeable is False

    @pytest.mark.parametrize(
        "point_count",
        [
            pytest.param(0, id="zero"),
            pytest.param(1, id="one"),
            pytest.param(3, id="violates_even_cardinality"),
        ],
    )
    def test_constructor__geometry__rejects_nonpositive_trivial_or_odd_counts(
        self, point_count: int
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-008

        Requirement: The public contract enforces rejects nonpositive trivial or
        odd counts.

        Acceptance: The asserted values and failures match the declared contract.
        """
        with pytest.raises(ValueError, match="nontrivial, and even"):
            CenteredUniformReciprocalMesh1D(
                ScalarQuantity(1.0, PhysicalUnit("1 / meter")), point_count
            )

    def test_constructor__geometry__rejects_nonpositive_reciprocal_period(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-009

        Requirement: The public contract enforces rejects nonpositive reciprocal
        period.

        Acceptance: The asserted values and failures match the declared contract.
        """
        with pytest.raises(ValueError, match="must be positive"):
            CenteredUniformReciprocalMesh1D(
                ScalarQuantity(0.0, PhysicalUnit("1 / meter")), 4
            )
