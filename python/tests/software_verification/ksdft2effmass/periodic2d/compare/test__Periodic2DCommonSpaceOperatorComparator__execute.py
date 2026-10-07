"""Software verification of common-space comparison range failure.

A synthetic finite Hermitian matrix near the binary64 maximum establishes that the
Action fails closed when dense transport cannot remain finite. The values are a range
stress fixture, not a physical operator, retained calculation, or scientific result.
Passing this test establishes only the documented software exception boundary.
"""

import numpy as np
import pytest

from ksdft2effmass.periodic2d.compare.common_space import (
    Periodic2DCommonSpaceComparisonRequest,
    Periodic2DCommonSpaceOperatorComparator,
)
from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DFiniteDifferenceHamiltonianResult,
    Periodic2DPlaneWaveHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCommonSpaceOperatorComparatorExecute:
    """Own fail-closed complex128 range evidence for comparator execution."""

    def test_execute__transport_overflow__raises_overflow_error(self) -> None:
        """Finite source entries must not become accepted nonfinite transport output."""
        model = Periodic2DCosinePotentialToyModel(0.0, 0.0, 0.0)
        plane_request = Periodic2DPlaneWaveHamiltonianRequest(model, 0.0, 0.0, 1)
        finite_request = Periodic2DFiniteDifferenceHamiltonianRequest(
            model, 0.0, 0.0, 5
        )
        plane = Periodic2DPlaneWaveHamiltonianResult(
            matrix=np.zeros((9, 9), dtype=np.complex128),
            request=plane_request,
            maximum_duality_residual=0.0,
        )
        maximum = np.finfo(np.float64).max
        finite = Periodic2DFiniteDifferenceHamiltonianResult(
            matrix=np.full((25, 25), maximum, dtype=np.complex128),
            request=finite_request,
        )
        request = Periodic2DCommonSpaceComparisonRequest(
            plane,
            finite,
            "complex128-overflow-stress",
        )

        with pytest.raises(OverflowError, match="transport is outside"):
            Periodic2DCommonSpaceOperatorComparator().execute(request)
