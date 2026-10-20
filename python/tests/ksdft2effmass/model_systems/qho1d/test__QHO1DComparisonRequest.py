r"""Software verification of ``QHO1DComparisonRequest``.

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
from ksdft2effmass import model_systems
from ksdft2effmass.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.model_systems.qho1d import (
    QHO1DAnalytical,
    QHO1DComparisonRequest,
    QHO1DFiniteDifference,
    QHO1DLadderOperators,
    QHO1DNondimensionalizer,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = QHO1DComparisonRequest


class TestQHO1DComparisonRequest:
    """Own software evidence for ``QHO1DComparisonRequest``."""

    @staticmethod
    def analytical(*, omega: float = 1.0) -> QHO1DAnalytical:
        """Return valid dimensionless analytical oscillator parameters."""
        return QHO1DAnalytical(
            QHO1DNondimensionalizer().execute(hbar=1.0, mass=1.0, omega=omega)
        )

    @staticmethod
    def finite_difference(
        analytical: QHO1DAnalytical,
    ) -> QHO1DFiniteDifference:
        """Return one oscillator on a symmetric homogeneous Dirichlet interval."""
        return QHO1DFiniteDifference(
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

        Requirement: QHO1DComparisonRequest is available through the
        supported public model-systems import surface.

        Acceptance: The package binding is the same class object as the documented
        harmonic-oscillator import.
        """
        assert model_systems.QHO1DComparisonRequest is (QHO1DComparisonRequest)

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
        ladder = QHO1DLadderOperators(analytical, LadderOperator1D(1))

        with pytest.raises(TypeError, match="analytical must be"):
            QHO1DComparisonRequest(True, finite_difference, ladder)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must share"):
            QHO1DComparisonRequest(
                analytical,
                self.finite_difference(self.analytical(omega=2.0)),
                ladder,
            )
        with pytest.raises(ValueError, match="exceeds the spatial dimension"):
            QHO1DComparisonRequest(
                analytical,
                finite_difference,
                QHO1DLadderOperators(analytical, LadderOperator1D(4)),
            )
