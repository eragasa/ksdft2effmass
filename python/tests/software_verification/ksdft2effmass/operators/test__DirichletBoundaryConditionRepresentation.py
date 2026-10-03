r"""Software verification of ``AbstractDirichletBoundaryConditionRepresentation``.

Evidence profile: routine

Bounded artifact scope: public nominal homogeneous-Dirichlet input contract.

Facet and represented meaning

The nominal ABC identifies boundary kind and homogeneity required by the represented
finite-difference Laplacian without transferring boundary ownership to operators.

Intrinsic and cross-object scope

Nominal recognition and structural-lookalike rejection are included.

VVUQ and scientific exclusions

This verifies software conformance only, not boundary-model adequacy, convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import AbstractDirichletBoundaryConditionRepresentation

pytestmark = pytest.mark.software_verification
SUT = AbstractDirichletBoundaryConditionRepresentation


class TestDirichletBoundaryConditionRepresentation:
    """Own software evidence for the operator boundary-input ABC."""

    def test_abc__rejects_non_inheriting_boundary_lookalike(self) -> None:
        """Require nominal membership even when all boundary properties match."""

        class BoundaryLookalike:
            condition_kind = "dirichlet"
            is_homogeneous = True

        assert not isinstance(BoundaryLookalike(), SUT)

    def test_abc__nominal_membership__accepts_public_dirichlet_condition(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-006

        Requirement: Laplacian construction depends on a nominal Dirichlet ABC while
        the concrete boundary DataObject remains analysis-owned.

        Acceptance: The public homogeneous Dirichlet condition satisfies the nominal
        ABC and reports exact kind ``dirichlet`` and homogeneous state.
        """
        condition = DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless()))

        assert isinstance(condition, AbstractDirichletBoundaryConditionRepresentation)
        assert condition.condition_kind == "dirichlet"
        assert condition.is_homogeneous
