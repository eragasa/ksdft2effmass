r"""Software verification of ``BoundStateProjectorResult``.

Evidence profile: routine

Bounded artifact scope: immutable complete-selection projector or explicit
no-bound-state outcome.

Facet and represented meaning

The ResultObject validates projector shape, Hermiticity, idempotency, and trace rank.

Intrinsic and cross-object scope

A rank-two synthetic projector and rank-three trace attack are included.

VVUQ and scientific exclusions

Spectra are synthetic test data. This is not eigensolver or material validation, UQ,
campaign execution, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.bound_subspaces import (
    BoundStateProjectorConstructor,
    BoundStateProjectorResult,
)
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
SUT = BoundStateProjectorResult


class TestBoundStateProjectorResult:
    """Own software evidence for bound-projector consistency."""

    def test_constructor__projector_trace__must_equal_bound_rank(self) -> None:
        """Evidence ID: SV-ANALYSIS-BOUND-PROJECTOR-002

        Requirement: Projector algebra and complete below-edge rank remain correlated.

        Acceptance: Replacing a valid rank-two projector with the rank-three identity
        raises ``ValueError``.
        """
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), Unitless()
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            ComplexSparseHermiticityAnalyzer().execute(
                operator, absolute_tolerance=0.0
            ),
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
        result = BoundStateProjectorConstructor().execute(bound)

        with pytest.raises(ValueError, match="trace"):
            replace(
                result,
                projector=ComplexMatrixQuantity(
                    np.eye(3, dtype=np.complex128), Unitless()
                ),
            )
