r"""Software verification of ``BoundStateProjectorConstructor``.

Evidence profile: routine

Bounded artifact scope: gauge-invariant projector construction from a complete retained
below-edge selection.

Facet and represented meaning

The ActionObject forms ``V V^dagger`` for the complete bound subspace and retains
``None`` for a complete no-bound-state outcome.

Intrinsic and cross-object scope

A two-state diagonal subspace and full-spectrum no-bound-state case are included.

VVUQ and scientific exclusions

Spectra are synthetic test data. This does not validate an eigensolver or material
model, establish UQ, execute a campaign, or provide human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.bound_subspaces import BoundStateProjectorConstructor
from ksdft2effmass.analysis.finite_domain_spectra import (
    HostEdgeBoundStateAnalyzer,
    HostEdgeReference,
)
from ksdft2effmass.operators import (
    ComplexHermitianEigenpairResidualAnalyzer,
    ComplexHermitianEigenpairResult,
    ComplexMatrixQuantity,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    HermitianEigenpairSelection,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = BoundStateProjectorConstructor


class TestBoundStateProjectorConstructor:
    """Own software evidence for bound-projector construction."""

    def test_method__execute__constructs_projector_and_retains_empty_outcome(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-BOUND-PROJECTOR-001

        Requirement: Complete nonempty and empty below-edge selections remain distinct.

        Acceptance: Two basis states yield diagonal projector ``(1,1,0)``; a positive
        two-state spectrum yields an unavailable projector rather than a zero matrix.
        """
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), Unitless()
        )
        hermiticity = ComplexSparseHermiticityAnalyzer().execute(
            operator, absolute_tolerance=0.0
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            hermiticity,
            VectorQuantity(np.array([-2.0, -1.0, 1.0]), Unitless()),
            ComplexMatrixQuantity(np.eye(3, dtype=np.complex128), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        bound = HostEdgeBoundStateAnalyzer().execute(
            ComplexHermitianEigenpairResidualAnalyzer().execute(
                eigenpairs, absolute_tolerance=0.0
            ),
            HostEdgeReference("edge", ScalarQuantity(0.0, Unitless())),
            ScalarQuantity(0.0, Unitless()),
        )

        projected = BoundStateProjectorConstructor().execute(bound)

        np.testing.assert_array_equal(
            projected.projector.magnitude if projected.projector is not None else None,
            np.diag([1.0, 1.0, 0.0]),
        )
        assert projected.rank == 2
        positive_operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([1.0, 2.0], format="csr"), Unitless()
        )
        positive_eigenpairs = ComplexHermitianEigenpairResult(
            positive_operator,
            ComplexSparseHermiticityAnalyzer().execute(
                positive_operator, absolute_tolerance=0.0
            ),
            VectorQuantity(np.array([1.0, 2.0]), Unitless()),
            ComplexMatrixQuantity(np.eye(2, dtype=np.complex128), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        no_bound = HostEdgeBoundStateAnalyzer().execute(
            ComplexHermitianEigenpairResidualAnalyzer().execute(
                positive_eigenpairs, absolute_tolerance=0.0
            ),
            HostEdgeReference("edge", ScalarQuantity(0.0, Unitless())),
            ScalarQuantity(0.0, Unitless()),
        )
        empty = BoundStateProjectorConstructor().execute(no_bound)
        assert not empty.available
        assert empty.projector is None
