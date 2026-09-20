r"""Software verification of ``ReciprocalOperatorFourierTransformer1D``.

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
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = ReciprocalOperatorFourierTransformer1D


class TestReciprocalOperatorFourierTransformer1D:
    """Verify the complete centered finite Fourier pair."""

    def test_method__execute__recovers_known_scalar_nearest_neighbor_hoppings(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-020

        Requirement: The public contract enforces recovers known scalar nearest
        neighbor hoppings.

        Acceptance: The asserted values and failures match the declared contract.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 4)
        values = 2.0 + np.cos(2.0 * np.pi * mesh.coordinates.magnitude)
        source = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            mesh.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(np.asarray([[value]]), Unitless())
                for value in values
            ),
        )

        result = ReciprocalOperatorFourierTransformer1D().execute(
            source, mesh, 0.0, 1.0e-14
        )

        assert result.hopping_model.representatives == (-2, -1, 0, 1)
        np.testing.assert_allclose(
            [block.magnitude[0, 0] for block in result.hopping_model.hopping_blocks],
            [0.0, 0.5, 2.0, 0.5],
            atol=1.0e-15,
        )
        assert result.reconstruction_passes
        assert result.reconstruction_maximum_frobenius_error <= 1.0e-14

    def test_method__execute__matches_centered_matrix_fourier_definition(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-029

        Requirement: The FFT implementation preserves the centered reciprocal origin,
        normalization, representative order, and negative Nyquist convention.

        Method: Construct dense two-by-two samples from independently authored hopping
        blocks using the inverse finite Fourier sum, then apply the public transform.

        Oracle: The explicit centered finite Fourier-pair definition.

        Acceptance: Every recovered complex block agrees within binary64 roundoff.

        Interpretation: A pass verifies FFT agreement with the represented transform.

        Limitations: Runtime scaling and scientific model validity are not assessed.

        Provenance: Authored deterministic software-verification matrices.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(2.0, Unitless()), 8)
        representatives = mesh.centered_cell_representatives
        cells = np.asarray(representatives, dtype=np.float64)
        expected = np.empty((8, 2, 2), dtype=np.complex128)
        expected[:, 0, 0] = cells + 5.0
        expected[:, 0, 1] = 0.25 * cells + 0.5j
        expected[:, 1, 0] = -0.125 * cells + 0.25j
        expected[:, 1, 1] = 2.0 * cells - 1.0
        normalized = mesh.coordinates.magnitude / mesh.reciprocal_period.magnitude
        inverse_transform = np.exp(2j * np.pi * np.outer(normalized, cells))
        samples = np.einsum("kr,rij->kij", inverse_transform, expected, optimize=True)
        source = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            mesh.reciprocal_period,
            tuple(map(self.matrix_quantity, samples)),
        )

        result = SUT().execute(source, mesh, 0.0, 1.0e-12)

        assert result.hopping_model.representatives == representatives
        recovered = np.asarray(
            tuple(map(self.matrix_magnitude, result.hopping_model.hopping_blocks))
        )
        np.testing.assert_allclose(recovered, expected, rtol=0.0, atol=5.0e-15)

    @staticmethod
    def matrix_quantity(
        matrix: npt.NDArray[np.complex128],
    ) -> ComplexMatrixQuantity:
        """Wrap one authored complex matrix in the explicit unit convention."""
        return ComplexMatrixQuantity(matrix, Unitless())

    @staticmethod
    def matrix_magnitude(
        matrix: ComplexMatrixQuantity,
    ) -> npt.NDArray[np.complex128]:
        """Return one represented complex matrix for a single stacked assertion."""
        return matrix.magnitude
