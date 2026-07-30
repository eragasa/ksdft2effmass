"""Object tests for the unit-bearing ``HermiticityAnalyzer`` ActionObject.

The tests exercise explicit units, exact unit matching, structured errors, and
fixed-representation residual behavior.  They are software-verification tests,
not scientific validation of an electronic-structure model.
"""

from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    HermiticityAnalyzer,
    HermiticityNumericalError,
    HermiticityRequirementError,
    HermiticityResult,
    HermiticityUnitMismatchError,
    OperatorRecord,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def make_record(matrix: Any, unit: str = "eV") -> OperatorRecord:
    """Return a valid operator record for analyzer tests."""

    dimension = int(np.asarray(matrix).shape[0])
    ordering = tuple(f"b{i}" for i in range(dimension))
    return OperatorRecord(
        "synthetic-two-level",
        "finite_test_hamiltonian",
        matrix,
        StateSpace("H_test", "finite synthetic", dimension),
        Basis("canonical", "test basis", ordering, True),
        Geometry(
            "synthetic",
            VALID_CELL,
            "finite synthetic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        EnergyReference("explicit zero", unit),
        {"source": "unit test"},
    )


def test_public_import_constructs_analyzer_with_explicit_unit() -> None:
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")

    assert analyzer.tolerance == 1.0e-12
    assert analyzer.energy_unit == "eV"


@pytest.mark.parametrize("tolerance", [-1.0, np.nan, np.inf, -np.inf])
def test_tolerance_must_be_finite_and_nonnegative(tolerance: float) -> None:
    message = "finite" if not np.isfinite(tolerance) else "non-negative"
    with pytest.raises(ValueError, match=message):
        HermiticityAnalyzer(tolerance=tolerance, energy_unit="eV")


@pytest.mark.parametrize("tolerance", [True, False, "1e-12", 0.0 + 0.0j])
def test_tolerance_must_be_real_not_boolean_string_or_complex(tolerance: Any) -> None:
    with pytest.raises(TypeError, match="real number"):
        HermiticityAnalyzer(tolerance=tolerance, energy_unit="eV")


def test_analyzer_requires_energy_unit_argument() -> None:
    with pytest.raises(TypeError, match="energy_unit"):
        HermiticityAnalyzer(tolerance=1.0e-12)  # type: ignore[call-arg]


@pytest.mark.parametrize("unit", [1, b"eV", object()])
def test_energy_unit_must_be_string(unit: Any) -> None:
    with pytest.raises(TypeError, match="string"):
        HermiticityAnalyzer(tolerance=0.0, energy_unit=unit)


def test_execute_returns_hermiticity_result_for_entrywise_max_residual() -> None:
    record = make_record(np.array([[1.0, 2.0 + 1.0j], [3.0 + 4.0j, 4.0]]))
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")

    result = analyzer.execute(record)

    assert isinstance(result, HermiticityResult)
    assert result.residual == pytest.approx(np.sqrt(26.0))
    assert result.tolerance == analyzer.tolerance
    assert result.energy_unit == "eV"
    assert not result.is_hermitian


def test_execute_requires_exact_unit_match() -> None:
    record = make_record(np.eye(2), unit="hartree")
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with pytest.raises(HermiticityUnitMismatchError) as exc_info:
        analyzer.execute(record)

    assert exc_info.value.analyzer_energy_unit == "eV"
    assert exc_info.value.record_energy_unit == "hartree"


def test_execute_requires_operator_record_input() -> None:
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with pytest.raises(TypeError, match="OperatorRecord"):
        analyzer.execute(object())  # type: ignore[arg-type]


def test_require_returns_result_when_record_satisfies_tolerance() -> None:
    record = make_record(np.array([[1.0, 1.0j], [-1.0j, 2.0]]))
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    result = analyzer.require(record)

    assert result == analyzer.execute(record)
    assert result.is_hermitian


def test_require_raises_structured_error_when_record_exceeds_tolerance() -> None:
    record = make_record(np.array([[1.0, 2.0], [3.0, 4.0]]))
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")

    with pytest.raises(HermiticityRequirementError) as exc_info:
        analyzer.require(record)

    assert exc_info.value.result.residual == pytest.approx(1.0)
    assert exc_info.value.result.tolerance == 1.0e-12
    assert exc_info.value.result.energy_unit == "eV"


def test_different_analyzers_can_apply_different_tolerances_with_same_unit() -> None:
    record = make_record(np.array([[1.0, 0.0], [1.0e-8, 2.0]]))

    assert (
        not HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")
        .execute(record)
        .is_hermitian
    )
    assert (
        HermiticityAnalyzer(tolerance=1.0e-6, energy_unit="eV")
        .execute(record)
        .is_hermitian
    )


def test_nonzero_entrywise_residual_can_change_under_unitary_basis_change() -> None:
    matrix = np.zeros((3, 3), dtype=np.complex128)
    matrix[0, 1] = 1.0
    phase = np.exp(2.0j * np.pi / 3.0)
    unitary = np.array(
        [[1.0, 1.0, 1.0], [1.0, phase, phase**2], [1.0, phase**2, phase]],
        dtype=np.complex128,
    ) / np.sqrt(3.0)
    record = make_record(matrix)
    rotated = make_record(unitary.conj().T @ matrix @ unitary)
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    assert analyzer.execute(record).residual == pytest.approx(1.0)
    assert analyzer.execute(rotated).residual == pytest.approx(1.0 / np.sqrt(3.0))


def test_exact_hermiticity_is_preserved_for_rotated_fixture() -> None:
    record = make_record(np.array([[1.0, 1.0j], [-1.0j, 2.0]]))
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    assert analyzer.execute(record).is_hermitian


def test_execute_raises_structured_numerical_error_for_subtraction_overflow() -> None:
    record = make_record(np.array([[0.0, 1.0e308], [-1.0e308, 0.0]]))
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with pytest.raises(HermiticityNumericalError) as exc_info:
        analyzer.execute(record)

    assert exc_info.value.reason == "nonfinite_residual"
