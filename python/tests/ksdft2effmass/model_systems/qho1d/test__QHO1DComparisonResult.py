r"""Software verification of ``QHO1DComparisonResult``.

Evidence profile: routine

Bounded artifact scope: immutable array fields of QHO1DComparisonResult.

Facet and represented meaning

The class under test records one finite-grid injection, common-coordinate operators,
signed difference, and numerical diagnostics for a harmonic-oscillator comparison.

Intrinsic and cross-object scope

The exact public import, binary64 canonicalization, contract-derived array shapes, and
operational array immutability are included. The comparator is used only to construct
a coherent result; numerical correctness of its values is excluded.

VVUQ and scientific exclusions

This is software verification of immutable represented state. It establishes no
numerical verification, convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest
from ksdft2effmass import model_systems
from ksdft2effmass.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.model_systems.qho1d import (
    QHO1DAnalytical,
    QHO1DComparator,
    QHO1DComparisonRequest,
    QHO1DComparisonResult,
    QHO1DFiniteDifference,
    QHO1DLadderOperators,
    QHO1DNondimensionalizer,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = QHO1DComparisonResult


class TestQHO1DComparisonResult:
    """Own software evidence for ``QHO1DComparisonResult``."""

    @staticmethod
    def result() -> QHO1DComparisonResult:
        """Return one coherent comparator-produced result fixture."""
        analytical = QHO1DAnalytical(
            QHO1DNondimensionalizer().execute(hbar=1.0, mass=1.0, omega=1.0)
        )
        request = QHO1DComparisonRequest(
            analytical=analytical,
            finite_difference=QHO1DFiniteDifference(
                analytical,
                DirichletInterval(
                    UniformCartesianGrid1D(
                        ScalarQuantity(-1.0, Unitless()),
                        ScalarQuantity(1.0, Unitless()),
                        ScalarQuantity(0.5, Unitless()),
                    ),
                    DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
                ),
            ),
            ladder_operators=QHO1DLadderOperators(analytical, LadderOperator1D(1)),
        )
        return QHO1DComparator().execute(request)

    def test_public_api__package__exports_supported_result_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-005

        Requirement: QHO1DComparisonResult is available through the
        supported public model-systems import surface.

        Acceptance: The package binding is the same class object as the documented
        harmonic-oscillator import.
        """
        assert model_systems.QHO1DComparisonResult is (QHO1DComparisonResult)

    def test_field__arrays__own_immutable_binary64_storage(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-006

        Requirement: QHO1DComparisonResult canonicalizes every numerical
        array to finite immutable binary64 storage with contract-derived shapes.

        Acceptance: A coherent result has float64 arrays with expected shapes, no
        array permits assignment, and a mutation attempt raises ValueError.
        """
        result = self.result()

        assert result.grid_coordinates.magnitude.dtype == np.dtype("float64")
        assert result.grid_coordinates.magnitude.shape == (3,)
        assert result.injection.magnitude.shape == (3, 1)
        assert result.gram_matrix.magnitude.shape == (1, 1)
        assert result.gram_inverse_square_root.magnitude.shape == (1, 1)
        assert result.pulled_back_hamiltonian.magnitude.shape == (1, 1)
        assert result.reference_hamiltonian.magnitude.shape == (1, 1)
        assert result.difference.magnitude.shape == (1, 1)
        assert not result.grid_coordinates.magnitude.flags.writeable
        assert not result.injection.magnitude.flags.writeable
        assert not result.difference.magnitude.flags.writeable
        with pytest.raises(ValueError, match="read-only"):
            result.injection.magnitude[0, 0] = 0.0
