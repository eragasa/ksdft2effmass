r"""Software verification of ``BoundSubspaceLocalizationResult``.

Evidence profile: routine

Bounded artifact scope: immutable gauge-invariant bound-subspace localization outcomes.

Facet and represented meaning

The ResultObject correlates normalized site probabilities with the declared core and
retained IPR while preserving explicit metric unavailability for no bound state.

Intrinsic and cross-object scope

A two-site synthetic subspace and contradictory core-probability edit are included.

VVUQ and scientific exclusions

Spectra are synthetic test data. This is not physical localization or material
validation, UQ, campaign execution, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.bound_subspaces import (
    BoundStateProjectorConstructor,
    BoundSubspaceLocalizationAnalyzer,
    BoundSubspaceLocalizationResult,
)
from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartitioner,
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
from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = BoundSubspaceLocalizationResult


class TestBoundSubspaceLocalizationResult:
    """Own software evidence for localization result consistency."""

    def test_constructor__core_probability__must_match_site_distribution(self) -> None:
        """Evidence ID: SV-ANALYSIS-BOUND-LOCALIZATION-002

        Requirement: Core probability is derived from probabilities on exact core
        indices rather than independently editable summary data.

        Acceptance: Replacing the valid one-half core probability by one raises
        ``ValueError``.
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
        projector = BoundStateProjectorConstructor().execute(bound)
        partition = MinimumImageChebyshevPartitioner().execute(
            FiniteLatticeShape(LatticeDimension.ONE, (3,)),
            LatticeCoordinate(LatticeDimension.ONE, (0,)),
            core_radius=0,
        )
        result = BoundSubspaceLocalizationAnalyzer().execute(projector, partition)

        with pytest.raises(ValueError, match="locality partition"):
            replace(result, core_probability=1.0)
