r"""Software verification of ``Wannier90NeighborOverlapFileWriter``.

Evidence profile: claim_bearing

Bounded artifact scope: deterministic ``.mmn`` writing correlated with ordered
``.nnkp`` neighbor records.

Facet and represented meaning

The ActionObject writes column-major complex overlap matrices only after exact header
agreement with the caller-supplied parsed neighbor list.

Intrinsic and cross-object scope

Header correlation and text writing are included; overlap construction and Wannier90
execution are excluded.

VVUQ and scientific exclusions

Round-trip and fail-closed checks are software verification, not localization
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.integration.wannier90 import (
    Wannier90NeighborListData,
    Wannier90NeighborOverlapData,
    Wannier90NeighborOverlapFileWriter,
    Wannier90NeighborOverlapParser,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Wannier90NeighborOverlapFileWriter


class TestWannier90NeighborOverlapFileWriter:
    """Own deterministic and correlated ``.mmn`` writer evidence."""

    @staticmethod
    def overlap_data() -> Wannier90NeighborOverlapData:
        """Return one authored two-band overlap record.

        Evidence ID: Helper owns no identifier.
        """

        matrix = np.asarray([[1.0, 2.0], [3.0j, 4.0 - 0.5j]])
        return Wannier90NeighborOverlapData(
            kpoint_count=1,
            neighbor_count=1,
            first_kpoint_indices=(0,),
            second_kpoint_indices=(0,),
            reciprocal_shifts=((1, 0, 0),),
            matrices=(ComplexMatrixQuantity(matrix, Unitless()),),
        )

    def test_method__execute__round_trips_nnkp_correlated_matrix(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-019

        Requirement: ``.mmn`` headers agree exactly with ordered ``.nnkp`` records.

        Method: Write one correlated neighbor block and parse the resulting bytes.

        Oracle: The parsed neighbor record and matrix are compared with authored data.

        Acceptance: Header, shift, and column-major complex matrix round trip exactly.

        Interpretation: A pass verifies deterministic correlated ``.mmn`` writing.

        Limitations: The authored matrix is not a calculated physical overlap.
        """

        data = self.overlap_data()
        neighbor_list = Wannier90NeighborListData(1, ((1, 1, 1, 0, 0),))

        text = SUT().execute(data, neighbor_list, "authored overlap fixture")
        reconstructed = Wannier90NeighborOverlapParser().execute(text.encode())

        assert reconstructed.reciprocal_shifts == ((1, 0, 0),)
        np.testing.assert_array_equal(
            reconstructed.matrices[0].magnitude, data.matrices[0].magnitude
        )

    def test_method__execute__rejects_ordered_nnkp_header_mismatch(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-020

        Requirement: A dimensionally compatible but different neighbor header fails.

        Method: Change only the ``.nnkp`` reciprocal shift before writing.

        Oracle: Exact ordered header equality is required by the interface contract.

        Acceptance: The writer raises ``ValueError`` before returning text.

        Interpretation: A pass verifies fail-closed neighbor correlation.

        Limitations: The check establishes representation compatibility only.
        """

        neighbor_list = Wannier90NeighborListData(1, ((1, 1, 0, 0, 0),))

        with pytest.raises(ValueError, match="differs from ordered nnkp"):
            SUT().execute(
                self.overlap_data(), neighbor_list, "authored overlap fixture"
            )
