r"""Software verification of ``OrthogonalSpectralSubspaceSelector``.

Evidence profile: routine

Bounded artifact scope: ordered orthogonal spectral-subspace selection.

Facet and represented meaning

The ActionObject selects the lowest ordered eigenvectors and correlated eigenvalues.

Intrinsic and cross-object scope

Dimension, ordering, projector, and complement identities are included.

VVUQ and scientific exclusions

This verifies represented linear algebra, not continuum convergence, validation,
uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from projectkoios.physkit.linalg.eigen import SpectralDecomposition
from projectkoios.physkit.units import (
    MatrixQuantity,
    Unitless,
)

from ksdft2effmass.hamiltonian import (
    OrthogonalSpectralSubspaceSelectionRequest,
    OrthogonalSpectralSubspaceSelector,
)

pytestmark = pytest.mark.software_verification
SUT = OrthogonalSpectralSubspaceSelector


class TestOrthogonalSpectralSubspaceSelector:
    """Own software evidence for ``OrthogonalSpectralSubspaceSelector``."""

    def test_method__execute__selects_lowest_orthogonal_embedding(self) -> None:
        """Evidence ID: SV-OPERATORS-SUBSPACE-001

        Requirement: Selection correlates the lowest eigenvalues with their exact
        column embedding and complementary projectors.

        Acceptance: A three-state diagonal operator retained at dimension two yields
        idempotent rank-two and rank-one complementary projectors summing to identity.
        """
        eigensystem = SpectralDecomposition(
            MatrixQuantity(np.diag([1.0, 2.0, 3.0]), Unitless())
        ).eigensystem()
        request = OrthogonalSpectralSubspaceSelectionRequest(eigensystem, 2)
        selector = OrthogonalSpectralSubspaceSelector(request)

        subspace = selector.execute()
        projector = subspace.projector.magnitude
        complement = subspace.complement_projector.magnitude

        assert selector.request is request
        np.testing.assert_array_equal(subspace.eigenvalues.magnitude, [1.0, 2.0])
        np.testing.assert_allclose(projector @ projector, projector)
        np.testing.assert_allclose(projector + complement, np.eye(3))

    def test_request__boolean_retained_dimension__raises_type_error(self) -> None:
        """Boolean values do not satisfy the public retained-dimension contract."""
        eigensystem = SpectralDecomposition(
            MatrixQuantity(np.diag([1.0, 2.0]), Unitless())
        ).eigensystem()

        with pytest.raises(TypeError, match="built-in int"):
            OrthogonalSpectralSubspaceSelectionRequest(eigensystem, True)
