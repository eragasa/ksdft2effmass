r"""Software verification of ``Wannier90InputData``.

Evidence profile: claim_bearing

Bounded artifact scope: immutable representation of the demonstrated Appendix G
Wannier90 ``.win`` subset.

Facet and represented meaning

The DataObject retains explicit settings and an x-directed one-dimensional reciprocal
mesh embedded in three coordinates.

Intrinsic and cross-object scope

Closed scalar, sequence, and one-dimensional mesh invariants are included; scientific
setting selection and Wannier90 execution are excluded.

VVUQ and scientific exclusions

Constructor checks are software verification, not localization validation,
uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.integration.wannier90 import Wannier90InputData

pytestmark = pytest.mark.software_verification
SUT = Wannier90InputData


class TestWannier90InputData:
    """Own demonstrated ``.win`` input-record invariant evidence."""

    @staticmethod
    def create(
        mp_grid: tuple[int, int, int],
        kpoints: tuple[tuple[float, float, float], ...],
    ) -> Wannier90InputData:
        """Construct a minimal record with selected mesh data.

        Evidence ID: Helper owns no identifier.
        """

        return SUT(
            num_bands=2,
            num_wann=2,
            num_iter=5000,
            convergence_tolerance=1.0e-12,
            convergence_window=5,
            precondition=True,
            search_shells=130,
            write_hr=True,
            write_u_matrices=True,
            translate_home_cell=True,
            unit_cell_cart_angstrom=(
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            atoms_fractional=(("H", 0.0, 0.0, 0.0),),
            projections=("random",),
            mp_grid=mp_grid,
            kpoints_fractional=kpoints,
        )

    def test_constructor__mp_grid__rejects_nondemonstrated_dimensions(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-022

        Requirement: The extracted record must not imply an unextracted 2D/3D writer.

        Method: Supply a two-point y-directed mesh count.

        Oracle: The demonstrated Appendix G subset permits only ``(n, 1, 1)``.

        Acceptance: Construction raises ``ValueError`` naming the 1D restriction.

        Interpretation: A pass verifies the bounded dimensional contract.

        Limitations: This does not reject future separately specified 2D records.
        """

        with pytest.raises(ValueError, match="requires a 1D mp_grid"):
            self.create(
                (1, 2, 1),
                ((0.0, 0.0, 0.0), (0.0, 0.5, 0.0)),
            )

    def test_constructor__kpoints_fractional__rejects_off_axis_point(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-023

        Requirement: Reciprocal points in the demonstrated subset lie on the x axis.

        Method: Supply one nonzero fractional y coordinate with a 1D mesh count.

        Oracle: The record contract requires exact zero y and z coordinates.

        Acceptance: Construction raises ``ValueError`` naming x-directed points.

        Interpretation: A pass verifies fail-closed coordinate dimensionality.

        Limitations: This is a representation boundary, not a physical mesh test.
        """

        with pytest.raises(ValueError, match="requires x-directed kpoints"):
            self.create((1, 1, 1), ((0.0, 0.5, 0.0),))
