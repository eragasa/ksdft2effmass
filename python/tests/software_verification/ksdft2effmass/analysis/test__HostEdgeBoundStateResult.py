r"""Software verification of ``HostEdgeBoundStateResult``.

Evidence profile: routine

Bounded artifact scope: immutable below-edge indices, binding energies, and selected
window completeness.

Facet and represented meaning

The ResultObject prevents a truncated all-bound selected window from claiming a
complete below-edge count or no-bound-state outcome.

Intrinsic and cross-object scope

A two-of-three synthetic selected window and contradictory complete-status edit are
included.

VVUQ and scientific exclusions

The spectrum is synthetic test data. This is not eigensolver or material validation,
UQ, campaign execution, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.finite_domain_spectra import (
    BoundStateSelectionStatus,
    HostEdgeBoundStateAnalyzer,
    HostEdgeBoundStateResult,
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
SUT = HostEdgeBoundStateResult


class TestHostEdgeBoundStateResult:
    """Own software evidence for bound-state result completeness."""

    def test_constructor__selection_status__must_match_spectral_coverage(self) -> None:
        """Evidence ID: SV-ANALYSIS-BOUND-STATE-002

        Requirement: Completeness is derived from retained spectral coverage.

        Acceptance: Two retained bound states from a three-state operator are
        incomplete; replacing the status by complete raises ``ValueError``.
        """
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), Unitless()
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            ComplexSparseHermiticityAnalyzer().execute(
                operator, absolute_tolerance=0.0
            ),
            VectorQuantity(np.array([-2.0, -1.0]), Unitless()),
            ComplexMatrixQuantity(np.eye(3, 2, dtype=np.complex128), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        residuals = ComplexHermitianEigenpairResidualAnalyzer().execute(
            eigenpairs, absolute_tolerance=0.0
        )
        result = HostEdgeBoundStateAnalyzer().execute(
            residuals,
            HostEdgeReference("edge", ScalarQuantity(0.0, Unitless())),
            ScalarQuantity(0.0, Unitless()),
        )

        assert not result.count_is_complete
        assert not result.no_bound_state
        with pytest.raises(ValueError, match="spectral coverage"):
            replace(
                result,
                selection_status=BoundStateSelectionStatus.COMPLETE_BELOW_EDGE,
            )
