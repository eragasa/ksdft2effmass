r"""Software verification of ``ParticleInBoxGridEvaluator``.

Evidence profile: routine

Bounded artifact scope: one finite particle-in-a-box grid evaluation.

Facet and represented meaning

The ActionObject composes the public box, interval, sparse Hamiltonian, and complete
tridiagonal eigensolver contracts.

Intrinsic and cross-object scope

Dimension, sparse storage, and closed-form eigenvalue agreement are included.

VVUQ and scientific exclusions

This is software verification of the finite representation, not continuum convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxGridEvaluator,
    ParticleInBoxParameters,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import SparseMatrixQuantity

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxGridEvaluator


class TestParticleInBoxGridEvaluator:
    """Own software evidence for ``ParticleInBoxGridEvaluator``."""

    def test_method__execute__retains_sparse_complete_eigensystem(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PIB-004

        Requirement: One grid evaluation diagonalizes the sparse represented
        Hamiltonian without changing its finite closed-form spectrum.

        Acceptance: Eight points retain 22 CSR nonzeros and eigenvalues agree with the
        independently exposed discrete formula to binary64 tolerance.
        """
        parameters = ParticleInBoxParameters(
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
        )
        result = ParticleInBoxGridEvaluator().execute(parameters, 8)

        assert isinstance(result.eigenpairs.operator, SparseMatrixQuantity)
        assert result.eigenpairs.operator.nonzero_count == 22
        np.testing.assert_allclose(
            result.eigenpairs.eigenvalues.magnitude,
            result.finite_difference.discrete_energy_levels().magnitude,
            rtol=64.0 * np.finfo(np.float64).eps,
        )
