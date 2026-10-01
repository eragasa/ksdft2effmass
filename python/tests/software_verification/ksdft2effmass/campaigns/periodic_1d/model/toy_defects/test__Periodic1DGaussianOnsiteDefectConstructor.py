r"""Software verification of ``Periodic1DGaussianOnsiteDefectConstructor``.

Evidence profile: claim_bearing

The tests establish minimum-image profile and block placement behavior for a synthetic
onsite perturbation, not a material defect potential.
"""

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic_1d.model.toy_defects import (
    Periodic1DGaussianOnsiteDefectConstructor,
    Periodic1DGaussianOnsiteDefectModel,
    Periodic1DGaussianOnsiteDefectRequest,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DGaussianOnsiteDefectConstructor


class TestPeriodic1DGaussianOnsiteDefectConstructor:
    """Own Gaussian onsite toy-defect construction evidence."""

    def test_method__execute__uses_minimum_image_coordinates(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-TOY-003.

        Requirement: The Gaussian profile uses integer minimum-image coordinates and
        places only onsite orbital blocks.

        Method: Construct a five-cell two-orbital perturbation with an identity block.

        Oracle: Authored coordinates, direct Gaussian values, zero offsite blocks, and
        exact block-diagonal placement.

        Acceptance: Coordinates agree exactly and matrix entries agree to roundoff.

        Interpretation: A pass establishes reusable onsite toy-defect mechanics.

        Limitations: This synthetic profile is not identified with a dopant potential.
        """
        block = np.eye(2, dtype=np.complex128)
        model = Periodic1DGaussianOnsiteDefectModel(1.0, -2.0, block)

        result = SUT().execute(Periodic1DGaussianOnsiteDefectRequest(model, 5))

        np.testing.assert_array_equal(result.coordinates_cells, (0, 1, 2, -2, -1))
        expected_profile = -2.0 * np.exp(
            -np.square(np.asarray((0, 1, 2, -2, -1), dtype=np.float64)) / 2.0
        )
        np.testing.assert_allclose(
            result.profile, expected_profile, rtol=0.0, atol=1.0e-15
        )
        np.testing.assert_allclose(
            result.matrix,
            np.kron(np.diag(expected_profile), block),
            rtol=0.0,
            atol=1.0e-15,
        )
        assert not result.matrix.flags.writeable

    def test_method__model__rejects_nonhermitian_orbital_block(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-TOY-004.

        Requirement: An onsite perturbation model must be Hermitian.

        Method: Supply a finite nonsymmetric real block.

        Oracle: Exact invariant ``ValueError``.

        Acceptance: Model construction stops before representation.

        Interpretation: A pass prevents a general directed bond block from being
        mislabeled as an onsite Hermitian perturbation.

        Limitations: General finite-extent operator perturbations have a different
        owner.
        """
        with pytest.raises(ValueError, match="orbital_block must be Hermitian"):
            Periodic1DGaussianOnsiteDefectModel(
                1.0,
                -2.0,
                np.asarray(((0.0, 1.0), (0.0, 0.0))),
            )
