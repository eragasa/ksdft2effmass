r"""Software verification of ``Qho1dComparisonRequest``.

Evidence profile: routine

Bounded artifact scope: public three-model binding invariants.

Facet and represented meaning

The class under test binds analytical, Dirichlet-interval, and ladder-operator models
for one aligned comparison.

Intrinsic and cross-object scope

The exact public import, exact model types, shared analytical definition, and compatible
finite dimensions are included. Numerical comparison is excluded.

VVUQ and scientific exclusions

This is software verification using dimensionless values. It establishes no numerical
verification, convergence, scientific validation, uncertainty quantification, or
human acceptance.
"""

import pytest
from projectkoios.physkit.units import (
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass import model_systems
from ksdft2effmass.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalytical,
    Qho1dComparisonRequest,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
    Qho1dNondimensionalizationRequest,
    Qho1dNondimensionalizer,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = Qho1dComparisonRequest


class TestQho1dComparisonRequest:
    """Own software evidence for ``Qho1dComparisonRequest``."""

    @staticmethod
    def analytical(*, omega: float = 1.0) -> Qho1dAnalytical:
        """Return valid dimensionless analytical oscillator parameters."""
        return Qho1dAnalytical(
            Qho1dNondimensionalizer(
                Qho1dNondimensionalizationRequest(1.0, 1.0, omega)
            ).execute()
        )

    @staticmethod
    def finite_difference(
        analytical: Qho1dAnalytical,
    ) -> Qho1dFiniteDifference:
        """Return one oscillator on a symmetric homogeneous Dirichlet interval."""
        return Qho1dFiniteDifference(
            analytical,
            DirichletInterval(
                UniformCartesianGrid1D(
                    ScalarQuantity(-1.0, Unitless()),
                    ScalarQuantity(1.0, Unitless()),
                    ScalarQuantity(0.5, Unitless()),
                ),
                DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
            ),
        )

    def test_public_api__package__exports_supported_request_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-003

        Requirement: Qho1dComparisonRequest is available through the
        supported public model-systems import surface.

        Acceptance: The package binding is the same class object as the documented
        harmonic-oscillator import.
        """
        assert model_systems.Qho1dComparisonRequest is (Qho1dComparisonRequest)

    def test_constructor__model_binding__rejects_incompatible_models(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-004

        Requirement: one request binds all three exact model types to a shared
        analytical definition and requires the retained dimension not to exceed the
        spatial dimension.

        Acceptance: A wrong model type, a different analytical definition, and an
        oversized retained ladder space raise the documented exception categories.
        """
        analytical = self.analytical()
        finite_difference = self.finite_difference(analytical)
        ladder = Qho1dLadderOperators(analytical, LadderOperator1D(1))

        with pytest.raises(TypeError, match="analytical must be"):
            Qho1dComparisonRequest(True, finite_difference, ladder)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must share"):
            Qho1dComparisonRequest(
                analytical,
                self.finite_difference(self.analytical(omega=2.0)),
                ladder,
            )
        with pytest.raises(ValueError, match="exceeds the spatial dimension"):
            Qho1dComparisonRequest(
                analytical,
                finite_difference,
                Qho1dLadderOperators(analytical, LadderOperator1D(4)),
            )
