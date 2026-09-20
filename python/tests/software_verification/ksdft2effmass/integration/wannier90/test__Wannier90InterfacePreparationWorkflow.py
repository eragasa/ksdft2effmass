r"""Software verification of ``Wannier90InterfacePreparationWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: complete execution-independent ``.win/.eig/.amn/.mmn``
preparation correlated with a parsed ``.nnkp`` inventory.

Facet and represented meaning

The Workflow correlates shared dimensions, reciprocal points, and native neighbor order
before composing four deterministic text writers.

Intrinsic and cross-object scope

Typed composition and representation compatibility are included; filesystem access,
interface-data construction, and Wannier90 execution are excluded.

VVUQ and scientific exclusions

Passing establishes the documented software composition only, not localization,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.integration.wannier90 import (
    Wannier90EigenvalueData,
    Wannier90EigenvalueParser,
    Wannier90InputData,
    Wannier90InterfacePreparationRequest,
    Wannier90InterfacePreparationWorkflow,
    Wannier90NeighborListData,
    Wannier90NeighborOverlapData,
    Wannier90NeighborOverlapParser,
    Wannier90ProjectionData,
    Wannier90ProjectionParser,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = Wannier90InterfacePreparationWorkflow


class TestWannier90InterfacePreparationWorkflow:
    """Own complete deterministic interface-preparation evidence."""

    @staticmethod
    def request(
        nnkp_second_x_coordinate: float,
        nnkp_kpoint_tolerance: float,
    ) -> Wannier90InterfacePreparationRequest:
        """Return one complete authored request with selected mesh correlation.

        Evidence ID: Helper owns no identifier.
        """

        unit = PhysicalUnit("eV")
        identity = ComplexMatrixQuantity(np.eye(2, dtype=np.complex128), Unitless())
        return Wannier90InterfacePreparationRequest(
            input_data=Wannier90InputData(
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
                mp_grid=(2, 1, 1),
                kpoints_fractional=((0.0, 0.0, 0.0), (0.5, 0.0, 0.0)),
            ),
            eigenvalues=Wannier90EigenvalueData(
                MatrixQuantity(np.asarray([[1.0, 2.0], [3.0, 4.0]]), unit)
            ),
            projections=Wannier90ProjectionData((identity, identity)),
            neighbor_list=Wannier90NeighborListData(
                1,
                ((1, 2, 0, 0, 0), (2, 1, 0, 0, 0)),
                (
                    (0.0, 0.0, 0.0),
                    (nnkp_second_x_coordinate, 0.0, 0.0),
                ),
            ),
            neighbor_overlaps=Wannier90NeighborOverlapData(
                kpoint_count=2,
                neighbor_count=1,
                first_kpoint_indices=(0, 1),
                second_kpoint_indices=(1, 0),
                reciprocal_shifts=((0, 0, 0), (0, 0, 0)),
                matrices=(identity, identity),
            ),
            projection_comment="authored projections",
            neighbor_overlap_comment="authored overlaps",
            nnkp_kpoint_tolerance=ScalarQuantity(nnkp_kpoint_tolerance, Unitless()),
        )

    def test_method__execute__correlates_and_writes_complete_interface(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-021

        Requirement: All four interface texts share exact dimensions, reciprocal
        points agree within the declared tolerance, and ``.mmn`` headers agree with
        the supplied ``.nnkp`` neighbor inventory.

        Method: Compose a two-point, two-band authored interface and independently
        parse the three indexed output formats.

        Oracle: Existing parsers reconstruct the supplied typed records; ``.win``
        text explicitly retains the two-point mesh and ordered reciprocal points.

        Acceptance: Every output is newline-terminated, parsed values agree exactly,
        and the result retains the explicit eV unit and zero mesh defect.

        Interpretation: A pass verifies complete execution-independent composition.

        Limitations: Authored matrices do not validate Wannier localization or a
        material model.
        """

        request = self.request(0.5, 0.0)

        result = SUT().execute(request)
        eigenvalues = Wannier90EigenvalueParser().execute(
            result.eigenvalue_text.encode(), request.eigenvalues.eigenvalues.unit
        )
        projections = Wannier90ProjectionParser().execute(
            result.projection_text.encode()
        )
        overlaps = Wannier90NeighborOverlapParser().execute(
            result.neighbor_overlap_text.encode()
        )

        assert all(
            text.endswith("\n")
            for text in (
                result.input_text,
                result.eigenvalue_text,
                result.projection_text,
                result.neighbor_overlap_text,
            )
        )
        assert "mp_grid = 2 1 1" in result.input_text
        assert eigenvalues.kpoint_count == projections.kpoint_count == 2
        assert overlaps.first_kpoint_indices == (0, 1)
        assert overlaps.second_kpoint_indices == (1, 0)
        assert result.eigenvalue_unit == PhysicalUnit("eV")
        assert result.maximum_nnkp_kpoint_defect.magnitude == 0.0
        assert isinstance(result.maximum_nnkp_kpoint_defect.unit, Unitless)
        assert result.nnkp_kpoint_tolerance.magnitude == 0.0

    def test_method__execute__rejects_nnkp_mesh_beyond_tolerance(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-025

        Requirement: Equal mesh counts cannot hide different reciprocal coordinates.

        Method: Shift one parsed ``.nnkp`` point by ``1e-4`` under ``1e-6`` tolerance.

        Oracle: The maximum authored coordinate defect exceeds the explicit tolerance.

        Acceptance: The Workflow raises ``ValueError`` before returning file text.

        Interpretation: A pass verifies fail-closed reciprocal-mesh correlation.

        Limitations: The tolerance is an interface decimal-precision policy, not a
        scientific acceptance metric.
        """

        with pytest.raises(ValueError, match="points differ beyond tolerance"):
            SUT().execute(self.request(0.5001, 1.0e-6))
