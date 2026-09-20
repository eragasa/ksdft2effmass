r"""Software verification of ``DirichletBoundaryCondition``.

Evidence profile: routine

Bounded artifact scope: public constant Dirichlet boundary-value contract.

Facet and represented meaning

The class under test owns one explicit unit-aware value prescribed on selected
boundary points.

Intrinsic and cross-object scope

Typed value retention and exact homogeneous classification are included.

VVUQ and scientific exclusions

This verifies represented boundary metadata only, not a differential-operator domain,
numerical convergence, scientific validation, uncertainty quantification, or human
acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = DirichletBoundaryCondition


class TestDirichletBoundaryCondition:
    """Own software evidence for ``DirichletBoundaryCondition``."""

    def test_property__is_homogeneous__classifies_exact_zero_value(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-BC-001

        Requirement: DirichletBoundaryCondition retains an explicit unit-aware value
        and classifies exact zero as homogeneous.

        Acceptance: The package export is exact, zero Unitless is homogeneous, and a
        nonzero Unitless value is not homogeneous.
        """
        assert model_systems.DirichletBoundaryCondition is DirichletBoundaryCondition
        assert DirichletBoundaryCondition(
            ScalarQuantity(0.0, Unitless())
        ).is_homogeneous
        assert not DirichletBoundaryCondition(
            ScalarQuantity(1.0, Unitless())
        ).is_homogeneous
