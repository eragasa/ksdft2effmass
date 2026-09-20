r"""Comparison of three quantum harmonic-oscillator models.

For one request, the comparator samples the exact analytical number states on the
interior Dirichlet grid, applies symmetric Gram orthonormalization, and forms an
injection :math:`J` from retained ladder coordinates into grid coordinates. It
compares :math:`J^T H_h J` with the retained ladder-operator Hamiltonian.

The algorithm uses ``numpy.float64`` and symmetric eigendecomposition of the sampled
Gram matrix. It rejects a non-positive-definite Gram matrix rather than selecting a
regularization policy.
"""

from __future__ import annotations

import numpy as np

from ksdft2effmass.operators.quantities import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from .model import (
    HarmonicOscillatorComparisonRequest,
    HarmonicOscillatorComparisonResult,
)


class HarmonicOscillatorComparator:
    """Compare analytical, Dirichlet-interval, and ladder-operator models.

    The ActionObject has no hidden mutable state. It performs one deterministic
    binary64 comparison for each explicit request.
    """

    __slots__ = ()

    def execute(
        self,
        request: HarmonicOscillatorComparisonRequest,
    ) -> HarmonicOscillatorComparisonResult:
        """Execute one aligned three-model comparison.

        Parameters
        ----------
        request
            Bound analytical, Dirichlet-interval, and ladder-operator models.

        Returns
        -------
        HarmonicOscillatorComparisonResult
            Immutable injection, common-coordinate operators, signed difference, and
            numerical diagnostics.

        Raises
        ------
        TypeError
            If ``request`` is not ``HarmonicOscillatorComparisonRequest``.
        ValueError
            If the sampled-state Gram matrix is not positive definite or the exact
            analytical energies and retained ladder Hamiltonian disagree.
        """
        if not isinstance(request, HarmonicOscillatorComparisonRequest):
            raise TypeError("request must be HarmonicOscillatorComparisonRequest")

        analytical = request.analytical
        finite_difference = request.finite_difference
        ladder = request.ladder_operators
        spacing = finite_difference.grid_spacing
        coordinates = finite_difference.grid_coordinates()
        oscillator_length = request.parameters.oscillator_length
        dimensionless_coordinates = VectorQuantity(
            coordinates.magnitude / oscillator_length.magnitude,
            Unitless(),
        )
        sampled_states = np.sqrt(spacing.magnitude) * (
            analytical.number_state_wavefunctions(
                dimensionless_coordinates,
                request.retained_dimension,
            ).magnitude
        )
        gram = sampled_states.T @ sampled_states
        gram_eigenvalues, gram_eigenvectors = np.linalg.eigh(gram)
        if gram_eigenvalues[0] <= 0.0:
            raise ValueError("sampled-state Gram matrix is not positive definite")
        gram_inverse_square_root = (
            gram_eigenvectors
            @ np.diag(np.power(gram_eigenvalues, -0.5))
            @ gram_eigenvectors.T
        )
        injection = sampled_states @ gram_inverse_square_root
        finite_difference_hamiltonian = finite_difference.hamiltonian()
        finite_difference_dense = finite_difference_hamiltonian.to_dense().magnitude
        pulled_back = injection.T @ finite_difference_dense @ injection
        ladder_hamiltonian = ladder.hamiltonian()
        reference = np.diag(ladder_hamiltonian.to_csr().diagonal())
        analytical_reference = np.diag(
            analytical.number_state_energies(request.retained_dimension).magnitude
        )
        if not np.array_equal(reference, analytical_reference):
            raise ValueError(
                "analytical energies and ladder Hamiltonian must agree exactly"
            )

        difference = pulled_back - reference
        diagonal = np.diag(np.diag(difference))
        off_diagonal = difference - diagonal
        absolute = float(np.linalg.norm(difference, ord="fro"))
        reference_scale = float(np.linalg.norm(reference, ord="fro"))
        return HarmonicOscillatorComparisonResult(
            request=request,
            grid_spacing=spacing,
            interior_points=finite_difference.interior_points,
            grid_coordinates=coordinates,
            injection=MatrixQuantity(injection, Unitless()),
            gram_matrix=MatrixQuantity(gram, Unitless()),
            gram_inverse_square_root=MatrixQuantity(
                gram_inverse_square_root, Unitless()
            ),
            pulled_back_hamiltonian=MatrixQuantity(
                pulled_back, finite_difference_hamiltonian.unit
            ),
            reference_hamiltonian=MatrixQuantity(reference, ladder_hamiltonian.unit),
            difference=MatrixQuantity(difference, ladder_hamiltonian.unit),
            gram_deviation=ScalarQuantity(
                float(np.linalg.norm(gram - np.eye(request.retained_dimension))),
                Unitless(),
            ),
            gram_condition_number=ScalarQuantity(
                float(gram_eigenvalues[-1] / gram_eigenvalues[0]), Unitless()
            ),
            injection_isometry_error=ScalarQuantity(
                float(
                    np.linalg.norm(
                        injection.T @ injection - np.eye(request.retained_dimension)
                    )
                ),
                Unitless(),
            ),
            absolute_discrepancy=ScalarQuantity(absolute, ladder_hamiltonian.unit),
            relative_discrepancy=ScalarQuantity(absolute / reference_scale, Unitless()),
            diagonal_discrepancy=ScalarQuantity(
                float(np.linalg.norm(diagonal, ord="fro")), ladder_hamiltonian.unit
            ),
            off_diagonal_discrepancy=ScalarQuantity(
                float(np.linalg.norm(off_diagonal, ord="fro")),
                ladder_hamiltonian.unit,
            ),
        )
