"""Synthetic finite-matrix checks, not retained silicon verification results."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from fractions import Fraction
from pathlib import Path
from typing import ClassVar

import common_space.verification as verification
import numpy as np
import pytest
from common_space.verification import (
    CommonSpaceGramRankEncloser,
    CommonSpaceGramRankEnclosure,
    GramEigenvalueInterval,
    GramRankDisposition,
    GramRankFailure,
)
from common_space.verification.gram_rank import _ExactMatrix
from numpy.typing import NDArray

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestCommonSpaceGramRankEncloser:
    """Require exact arithmetic bounds and refuse unsupported rank decisions."""

    SIGNS: ClassVar[tuple[tuple[int, ...], ...]] = (
        (1, 1, 1, 1),
        (1, 1, -1, -1),
        (1, -1, 1, -1),
        (1, -1, -1, 1),
    )

    @classmethod
    def _rotated_overlap(
        cls, singular_values: tuple[Fraction, ...]
    ) -> tuple[tuple[complex, ...], ...]:
        """Known synthetic B = H diag(s) H^T with exact orthogonal H = signs/2."""
        assert len(singular_values) == 4
        return tuple(
            tuple(
                complex(
                    float(
                        sum(
                            (
                                Fraction(
                                    cls.SIGNS[row][index] * cls.SIGNS[column][index], 4
                                )
                                * value
                                for index, value in enumerate(singular_values)
                            ),
                            start=Fraction(0),
                        )
                    )
                )
                for column in range(4)
            )
            for row in range(4)
        )

    def test_exact_diagonal__resolves_rank_with_zero_arithmetic_error(self) -> None:
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((0j, 0j), (0j, 2 + 0j)),
            rank_threshold=Fraction(1),
        ).execute()

        assert result.disposition is GramRankDisposition.rank_resolved
        assert result.resolved_rank == 1
        assert result.rank_lower_bound == result.rank_upper_bound == 1
        assert result.failure is None
        assert result.hermiticity_defect_bound == 0
        assert result.orthonormality_defect_bound == 0
        assert result.spectral_error_bound == 0
        assert result.eigenpair_residual_bounds == (Fraction(0), Fraction(0))
        assert result.eigenvalue_intervals == (
            GramEigenvalueInterval(lower=Fraction(0), upper=Fraction(0)),
            GramEigenvalueInterval(lower=Fraction(4), upper=Fraction(4)),
        )

    def test_exact_threshold_equality__is_not_strictly_above_gate(self) -> None:
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((2 + 0j,),), rank_threshold=Fraction(2)
        ).execute()

        assert result.resolved_rank == 0
        assert result.rank_lower_bound == result.rank_upper_bound == 0

    def test_complex_gram__uses_conjugation_and_encloses_known_spectrum(self) -> None:
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j, 1j), (1j, -1 + 0j)),
            rank_threshold=Fraction(1, 1000),
        ).execute()

        assert result.resolved_rank == 1
        for interval, eigenvalue in zip(
            result.eigenvalue_intervals, (Fraction(0), Fraction(4)), strict=True
        ):
            assert interval.lower <= eigenvalue <= interval.upper
        assert result.eigenvalue_intervals[0].nonnegative_bounds[0] == 0
        assert result.hermiticity_defect_bound == 0

    def test_mixed_complex_overlap__encloses_exact_quadratic_roots(self) -> None:
        # Exact G has trace 45 and determinant 353: eigenvalues (45 +/- sqrt(613))/2.
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 1j, 2 + 3j), (-3 + 2j, 4 - 1j)),
            rank_threshold=Fraction(4),
        ).execute()

        lower, upper = result.eigenvalue_intervals
        assert result.resolved_rank == 1
        assert 2 * lower.upper < 45 < 2 * upper.lower
        assert (45 - 2 * lower.lower) ** 2 >= 613
        assert (45 - 2 * lower.upper) ** 2 <= 613
        assert (2 * upper.lower - 45) ** 2 <= 613
        assert (2 * upper.upper - 45) ** 2 >= 613

    @pytest.mark.parametrize(
        "singular_values, threshold, expected_rank",
        [
            (
                (Fraction(0), Fraction(1, 16), Fraction(1, 2), Fraction(1)),
                Fraction(1, 8),
                2,
            ),
            (
                (Fraction(1, 4), Fraction(1, 4), Fraction(1), Fraction(1)),
                Fraction(1, 8),
                4,
            ),
            ((Fraction(0), Fraction(0), Fraction(0), Fraction(0)), Fraction(0), 0),
        ],
    )
    def test_rotated_spectrum__contains_exact_analytic_eigenvalues(
        self,
        singular_values: tuple[Fraction, ...],
        threshold: Fraction,
        expected_rank: int,
    ) -> None:
        result = CommonSpaceGramRankEncloser(
            independent_overlap=self._rotated_overlap(singular_values),
            rank_threshold=threshold,
        ).execute()

        assert result.resolved_rank == expected_rank
        for interval, value in zip(
            result.eigenvalue_intervals, sorted(singular_values), strict=True
        ):
            assert interval.lower <= value**2 <= interval.upper

    def test_rank_ten_synthetic_overlap__resolves_one_deficient_direction(self) -> None:
        overlap = tuple(
            tuple(
                (1 + 0j, 1j)[column]
                if row == 0 and column < 2
                else (1j, -1 + 0j)[column]
                if row == 1 and column < 2
                else 1 + 0j
                if row == column and row >= 2
                else 0j
                for column in range(10)
            )
            for row in range(10)
        )
        result = CommonSpaceGramRankEncloser(
            independent_overlap=overlap,
            rank_threshold=Fraction.from_float(5.890206739032098e-7),
        ).execute()

        assert result.resolved_rank == 9
        assert result.disposition is GramRankDisposition.rank_resolved
        expected = (Fraction(0),) + (Fraction(1),) * 8 + (Fraction(4),)
        for interval, value in zip(result.eigenvalue_intervals, expected, strict=True):
            assert interval.lower <= value <= interval.upper

    def test_candidate_rounding__leaves_small_rank_contribution_inconclusive(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        singular_values = (
            Fraction(1),
            Fraction(1, 2),
            Fraction(1, 4),
            Fraction(1, 2**30),
        )

        def rounded_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            return np.asarray((0, 1 / 16, 1 / 4, 1), dtype=np.float64), np.asarray(
                tuple(
                    tuple(row[index] / 2 for index in (3, 2, 1, 0))
                    for row in self.SIGNS
                ),
                dtype=np.complex128,
            )

        monkeypatch.setattr(np.linalg, "eigh", rounded_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=self._rotated_overlap(singular_values),
            rank_threshold=Fraction(1, 2**31),
        ).execute()

        assert result.disposition is GramRankDisposition.numerically_inconclusive
        assert result.failure is None
        assert result.resolved_rank is None
        assert (result.rank_lower_bound, result.rank_upper_bound) == (3, 4)
        assert result.spectral_error_bound == Fraction(1, 2**60)
        assert result.eigenvalue_intervals[0].upper == Fraction(1, 2**60)

    def test_candidate_underflow__cannot_erase_exact_gram_contribution(self) -> None:
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((complex(2.0**-600),),),
            rank_threshold=Fraction(1, 2**601),
        ).execute()

        assert result.disposition is GramRankDisposition.numerically_inconclusive
        assert result.failure is None
        assert result.resolved_rank is None
        assert (result.rank_lower_bound, result.rank_upper_bound) == (0, 1)
        assert result.spectral_error_bound == Fraction(1, 2**1200)
        assert result.eigenvalue_intervals[0].upper == Fraction(1, 2**1200)

    def test_nonunitary_candidate__includes_polar_correction(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def scaled_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            return np.asarray((1 / 4, 1), dtype=np.float64), np.eye(
                2, dtype=np.complex128
            ) / 2

        monkeypatch.setattr(np.linalg, "eigh", scaled_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j, 0j), (0j, 2 + 0j)),
            rank_threshold=Fraction(3, 2),
        ).execute()

        assert result.orthonormality_defect_bound == Fraction(3, 4)
        assert result.spectral_error_bound == Fraction(33, 5)
        assert result.eigenpair_residual_bounds == (Fraction(3, 8), Fraction(3, 2))
        assert result.resolved_rank is None
        for interval, value in zip(result.eigenvalue_intervals, (1, 4), strict=True):
            assert interval.lower <= value <= interval.upper

    def test_singular_candidate_frame__does_not_pass_on_zero_residuals(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def zero_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            return np.zeros(2, dtype=np.float64), np.zeros((2, 2), dtype=np.complex128)

        monkeypatch.setattr(np.linalg, "eigh", zero_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j, 0j), (0j, 2 + 0j)),
            rank_threshold=Fraction(1),
        ).execute()

        assert result.failure is GramRankFailure.uncertified_frame
        assert result.orthonormality_defect_bound == 1
        assert result.eigenpair_residual_bounds == (Fraction(0), Fraction(0))
        assert result.disposition is GramRankDisposition.numerically_inconclusive
        assert result.resolved_rank is None
        assert (result.rank_lower_bound, result.rank_upper_bound) == (0, 2)

    def test_negative_estimate__clamps_only_an_interval_containing_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def negative_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            return np.asarray((-(2.0**-50),), dtype=np.float64), np.eye(
                1, dtype=np.complex128
            )

        monkeypatch.setattr(np.linalg, "eigh", negative_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((0j,),), rank_threshold=Fraction(0)
        ).execute()

        (interval,) = result.eigenvalue_intervals
        assert interval.lower < 0
        assert interval.upper == 0
        assert interval.nonnegative_bounds == (Fraction(0), Fraction(0))
        assert result.resolved_rank == 0

    def test_materially_negative_interval__cannot_be_clamped(self) -> None:
        interval = GramEigenvalueInterval(lower=Fraction(-2), upper=Fraction(-1))

        with pytest.raises(ValueError, match="materially negative"):
            _ = interval.nonnegative_bounds
        with pytest.raises(ValueError, match="materially negative"):
            CommonSpaceGramRankEnclosure(
                dimension=1,
                rank_threshold=Fraction(0),
                eigenvalue_intervals=(interval,),
                orthonormality_defect_bound=Fraction(0),
                spectral_error_bound=Fraction(0),
                eigenpair_residual_bounds=(Fraction(0),),
                minimum_eigenvector=((Fraction(1), Fraction(0)),),
            )

    def test_unitary_row_change__preserves_exact_gram_certificate(self) -> None:
        first = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j, 1j), (1j, -1 + 0j)),
            rank_threshold=Fraction(1, 1000),
        ).execute()
        rotated = CommonSpaceGramRankEncloser(
            independent_overlap=((1j, -1 + 0j), (-1j, 1 + 0j)),
            rank_threshold=Fraction(1, 1000),
        ).execute()

        assert first == rotated

    def test_unordered_candidate__sorts_vector_columns_with_eigenvalues(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def reversed_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            return np.asarray((4, 1), dtype=np.float64), np.asarray(
                ((0, 1), (1, 0)), dtype=np.complex128
            )

        monkeypatch.setattr(np.linalg, "eigh", reversed_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j, 0j), (0j, 2 + 0j)),
            rank_threshold=Fraction(3, 2),
        ).execute()

        assert result.resolved_rank == 1
        assert result.spectral_error_bound == 0
        assert tuple(interval.lower for interval in result.eigenvalue_intervals) == (
            Fraction(1),
            Fraction(4),
        )

    def test_overflowing_gram_candidate__returns_no_rank(self) -> None:
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1e308 + 0j,),), rank_threshold=Fraction(0)
        ).execute()

        assert result.failure is GramRankFailure.unrepresentable_gram
        assert result.resolved_rank is None
        assert result.eigenvalue_intervals == ()

    def test_eigensolver_failure__returns_no_rank(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def failed_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            raise np.linalg.LinAlgError("Synthetic solver failure")

        monkeypatch.setattr(np.linalg, "eigh", failed_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j,),), rank_threshold=Fraction(0)
        ).execute()

        assert result.failure is GramRankFailure.eigensolver_failure
        assert result.resolved_rank is None

    @pytest.mark.parametrize("bad_part", ("eigenvalues", "vectors", "shape"))
    def test_invalid_candidate__returns_no_rank(
        self, monkeypatch: pytest.MonkeyPatch, bad_part: str
    ) -> None:
        def invalid_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            values = np.ones(2, dtype=np.float64)
            vectors = np.eye(2, dtype=np.complex128)
            if bad_part == "eigenvalues":
                values[0] = np.nan
            elif bad_part == "vectors":
                vectors[0, 0] = np.inf
            else:
                values = np.ones(1, dtype=np.float64)
            return values, vectors

        monkeypatch.setattr(np.linalg, "eigh", invalid_candidate)
        result = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j, 0j), (0j, 1 + 0j)),
            rank_threshold=Fraction(0),
        ).execute()

        assert result.failure is GramRankFailure.invalid_eigensystem
        assert result.disposition is GramRankDisposition.numerically_inconclusive
        assert result.resolved_rank is None

    def test_resource_failure__is_not_converted_to_a_rank(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def exhausted_candidate(
            _matrix: NDArray[np.complex128],
        ) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
            raise MemoryError("Synthetic resource exhaustion")

        monkeypatch.setattr(np.linalg, "eigh", exhausted_candidate)
        with pytest.raises(MemoryError, match="resource exhaustion"):
            CommonSpaceGramRankEncloser(
                independent_overlap=((1 + 0j,),), rank_threshold=Fraction(0)
            ).execute()

    @pytest.mark.parametrize(
        "value",
        (True, 1, 1.0, "1", np.complex128(1), complex(np.nan, 0), complex(0, np.inf)),
    )
    def test_scalar_admission__rejects_coercion_and_nonfinite_entries(
        self, value: complex | float | str | np.complex128
    ) -> None:
        with pytest.raises(ValueError, match="finite built-in complex"):
            CommonSpaceGramRankEncloser(
                independent_overlap=((value,),),  # type: ignore[arg-type]
                rank_threshold=Fraction(0),
            )

    @pytest.mark.parametrize("value", (True, 0, 0.0, "0", Fraction(-1)))
    def test_threshold_admission__requires_nonnegative_exact_fraction(
        self, value: Fraction | float | str
    ) -> None:
        with pytest.raises(ValueError, match="nonnegative built-in Fraction"):
            CommonSpaceGramRankEncloser(
                independent_overlap=((1 + 0j,),),
                rank_threshold=value,  # type: ignore[arg-type]
            )

    def test_matrix_admission__rejects_mutable_or_nonsquare_storage(self) -> None:
        with pytest.raises(ValueError, match="nonempty tuple"):
            CommonSpaceGramRankEncloser(
                independent_overlap=[],  # type: ignore[arg-type]
                rank_threshold=Fraction(0),
            )
        with pytest.raises(ValueError, match="square tuple rows"):
            CommonSpaceGramRankEncloser(
                independent_overlap=((1 + 0j, 0j),), rank_threshold=Fraction(0)
            )
        with pytest.raises(ValueError, match="square tuple rows"):
            CommonSpaceGramRankEncloser(
                independent_overlap=([1 + 0j],),  # type: ignore[arg-type]
                rank_threshold=Fraction(0),
            )

    def test_empty_overlap__has_no_implicit_rank(self) -> None:
        with pytest.raises(ValueError, match="nonempty tuple"):
            CommonSpaceGramRankEncloser(
                independent_overlap=(), rank_threshold=Fraction(0)
            )

    def test_norm_bound__rejects_a_nonhermitian_matrix(self) -> None:
        matrix = _ExactMatrix.from_binary64(((0j, 1 + 0j), (0j, 0j)))

        with pytest.raises(ValueError, match="exact Hermitian matrix"):
            _ = matrix.hermitian_norm_bound

    def test_interval__rejects_nonrational_and_reversed_endpoints(self) -> None:
        with pytest.raises(TypeError, match="built-in Fractions"):
            GramEigenvalueInterval(lower=0.0, upper=Fraction(1))  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="reversed"):
            GramEigenvalueInterval(lower=Fraction(1), upper=Fraction(0))

    def test_records__are_operationally_immutable(self) -> None:
        action = CommonSpaceGramRankEncloser(
            independent_overlap=((1 + 0j,),), rank_threshold=Fraction(0)
        )
        result = action.execute()

        with pytest.raises(FrozenInstanceError):
            action.rank_threshold = Fraction(2)  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.failure = GramRankFailure.eigensolver_failure  # type: ignore[misc]
        with pytest.raises(TypeError):
            action.independent_overlap[0][0] = 0j  # type: ignore[index]
        with pytest.raises(ValueError, match="complete arithmetic certificate"):
            CommonSpaceGramRankEnclosure(dimension=1, rank_threshold=Fraction(0))

    def test_dispositions__use_closed_wire_vocabulary(self) -> None:
        for disposition in GramRankDisposition:
            assert GramRankDisposition.from_wire(disposition.to_wire()) is disposition
        for failure in GramRankFailure:
            assert GramRankFailure.from_wire(failure.to_wire()) is failure
        with pytest.raises(ValueError, match="unsupported"):
            GramRankDisposition.from_wire("scientifically-validated")

    def test_independence__forbids_producer_imports_and_svd(self) -> None:
        assert verification.__file__ is not None
        package = Path(verification.__file__).parent
        allowed = {
            "__future__",
            "dataclasses",
            "fractions",
            "math",
            "numpy",
            "numpy.typing",
            "ksdft2effmass.serialization.enums",
            "typing",
        }
        for source in package.glob("*.py"):
            module_allowed = allowed
            if source.name == "native_inputs.py":
                module_allowed = allowed | {
                    "hashlib",
                    "importlib",
                    "importlib.metadata",
                    "pathlib",
                    "projectkoios.integrations.wannier90",
                }
            if source.name == "native_precision.py":
                module_allowed = allowed | {
                    "sys",
                    "projectkoios.physkit.units.quantities",
                }
            if source.name in {"source_admission.py", "grid_verification.py"}:
                module_allowed = allowed | {
                    "json",
                    "projectkoios.integrations.wannier90",
                }
            if source.name == "producer_result.py":
                module_allowed = allowed | {
                    "pathlib",
                    "projectkoios.integrations.wannier90",
                }
            if source.name == "verification_io.py":
                module_allowed = allowed | {
                    "hashlib",
                    "pathlib",
                    "projectkoios.integrations.wannier90",
                }
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    assert all(alias.name in module_allowed for alias in node.names)
                if isinstance(node, ast.ImportFrom):
                    assert (
                        node.level == 1
                        and node.module
                        in {
                            "gram_rank",
                            "native_inputs",
                            "native_overlap",
                            "native_precision",
                            "controls",
                            "source_admission",
                            "grid_verification",
                            "producer_result",
                            "verification_io",
                        }
                    ) or (node.level == 0 and node.module in module_allowed)
                if isinstance(node, ast.Attribute):
                    assert node.attr != "svd"
