from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    HermiticityAnalyzer,
    HermiticityResult,
    OperatorRecord,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def make_record(matrix: Any) -> OperatorRecord:
    return OperatorRecord(
        "synthetic-two-level",
        "finite_test_hamiltonian",
        matrix,
        StateSpace("H_test", "finite synthetic", 2),
        Basis("canonical", "test basis", ("a", "b"), True),
        Geometry(
            "synthetic",
            VALID_CELL,
            "finite synthetic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        EnergyReference("explicit zero", "eV"),
        {"source": "unit test"},
    )


def test_public_import_constructs_analyzer_with_default_tolerance() -> None:
    analyzer = HermiticityAnalyzer()

    assert analyzer.tolerance == 1.0e-12


@pytest.mark.parametrize("tolerance", [-1.0, np.nan, np.inf, -np.inf])
def test_tolerance_must_be_finite_and_nonnegative(tolerance: float) -> None:
    message = "finite" if not np.isfinite(tolerance) else "non-negative"
    with pytest.raises(ValueError, match=message):
        HermiticityAnalyzer(tolerance=tolerance)


@pytest.mark.parametrize("tolerance", [True, False, "1e-12", 0.0 + 0.0j])
def test_tolerance_must_be_real_not_boolean_string_or_complex(tolerance: Any) -> None:
    with pytest.raises(TypeError, match="real number"):
        HermiticityAnalyzer(tolerance=tolerance)


def test_execute_returns_hermiticity_result_for_entrywise_max_residual() -> None:
    record = make_record(np.array([[1.0, 2.0 + 1.0j], [3.0 + 4.0j, 4.0]]))
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12)

    result = analyzer.execute(record)

    assert isinstance(result, HermiticityResult)
    assert result.residual == pytest.approx(np.sqrt(26.0))
    assert result.tolerance == analyzer.tolerance
    assert not result.is_hermitian


def test_require_returns_result_when_record_satisfies_tolerance() -> None:
    record = make_record(np.array([[1.0, 1.0j], [-1.0j, 2.0]]))
    analyzer = HermiticityAnalyzer(tolerance=0.0)

    result = analyzer.require(record)

    assert result == analyzer.execute(record)
    assert result.is_hermitian


def test_require_raises_when_record_exceeds_tolerance() -> None:
    record = make_record(np.array([[1.0, 2.0], [3.0, 4.0]]))
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12)

    with pytest.raises(ValueError, match=r"residual=1.*tolerance=1e-12"):
        analyzer.require(record)


def test_different_analyzers_can_apply_different_tolerances() -> None:
    record = make_record(np.array([[1.0, 0.0], [1.0e-8, 2.0]]))

    assert not HermiticityAnalyzer(tolerance=1.0e-12).execute(record).is_hermitian
    assert HermiticityAnalyzer(tolerance=1.0e-6).execute(record).is_hermitian
