r"""Software verification of ``HostEdgeBoundStateAnalyzer``.

Evidence profile: routine

Bounded artifact scope: thresholded below-edge classification of retained lowest complex
Hermitian eigenvalues.

Facet and represented meaning

The ActionObject distinguishes a complete below-edge count from a selected window whose
highest retained state remains below the thresholded edge.

Intrinsic and cross-object scope

Complete three-state and incomplete two-state selections share one synthetic spectrum.

VVUQ and scientific exclusions

The spectrum is synthetic test data. This does not validate an eigensolver, material
model, uncertainty estimate, campaign execution, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.finite_domain_spectra import (
    BoundStateSelectionStatus,
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
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = HostEdgeBoundStateAnalyzer


class TestHostEdgeBoundStateAnalyzer:
    """Own software evidence for thresholded host-edge classification."""

    def test_method__execute__distinguishes_complete_and_incomplete_counts(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-BOUND-STATE-001

        Requirement: A below-edge count is complete only when the retained window
        includes an unbound state or the complete represented spectrum.

        Acceptance: Full values -2, -1, 1 produce two complete bound states; retaining
        only -2 and -1 reports the same lower bound with incomplete coverage.
        """
        unit = PhysicalUnit("electron_volt")
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), unit
        )
        hermiticity = ComplexSparseHermiticityAnalyzer().execute(
            operator, absolute_tolerance=0.0
        )
        full = ComplexHermitianEigenpairResult(
            operator,
            hermiticity,
            VectorQuantity(np.array([-2.0, -1.0, 1.0]), unit),
            ComplexMatrixQuantity(np.eye(3, dtype=np.complex128), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        partial = ComplexHermitianEigenpairResult(
            operator,
            hermiticity,
            VectorQuantity(np.array([-2.0, -1.0]), unit),
            ComplexMatrixQuantity(np.eye(3, 2, dtype=np.complex128), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        edge = HostEdgeReference("host_edge", ScalarQuantity(0.0, unit))
        threshold = ScalarQuantity(0.1, unit)
        analyzer = HostEdgeBoundStateAnalyzer()

        residual_analyzer = ComplexHermitianEigenpairResidualAnalyzer()
        complete = analyzer.execute(
            residual_analyzer.execute(full, absolute_tolerance=0.0), edge, threshold
        )
        incomplete = analyzer.execute(
            residual_analyzer.execute(partial, absolute_tolerance=0.0), edge, threshold
        )

        assert complete.below_edge_state_count == 2
        assert complete.count_is_complete
        np.testing.assert_array_equal(complete.binding_energies.magnitude, [2.0, 1.0])
        assert incomplete.below_edge_state_count == 2
        assert (
            incomplete.selection_status
            is BoundStateSelectionStatus.INCOMPLETE_SELECTED_WINDOW
        )
        assert not incomplete.count_is_complete
