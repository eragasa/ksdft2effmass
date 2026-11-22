"""Diamond geometric construction-index relations, not electronic symmetry actions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .diagnosis import JsonObject, JsonValue, KPointDiagnosis

type IntMatrix = tuple[tuple[int, ...], ...]

# Adopted executed-cell shape D=c*P, not a conversion of nominal geometry.
_P: IntMatrix = ((1, 1, 0), (0, 1, 1), (1, 0, 1))
_TWO_P_INVERSE: IntMatrix = ((1, -1, 1), (1, 1, -1), (-1, 1, 1))
_IDENTITY: IntMatrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ADOPTED_GEOMETRY = (
    "s30-source-geometry:sha256:"
    "3c74b8bbd684b0aac6d47d44fdc52920c6435ad1f21292b8983c4f91f64ecf51"
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondConstructionPointInventory:
    """Enumerate the adopted C6 index stars without snapping native coordinates.

    Input records are immutable KPointDiagnosis objects in declared order. All
    spectra/coordinates are dimensionless finite built-in scalars validated by
    that record. Geometric arithmetic uses exact integers/Fractions (no overflow).
    The scale c cancels in the index action, not in physical dimensional results.
    Every cubic signed permutation is checked against the FCC lattice and the
    identical-Si motif {0,(1/4,1/4,1/4)}, allowing its required fractional translation.
    Neither this motif action nor its reciprocal-index permutation supplies a
    parent/trial/Wannier representation, irrep, physical exact-k equality, or rank
    invariance. Printed/binary64 coordinate residuals are observations, not gates.
    """

    records: tuple[KPointDiagnosis, ...]
    geometry_identity: str

    def __post_init__(self) -> None:
        from .diagnosis import KPointDiagnosis

        if self.geometry_identity != ADOPTED_GEOMETRY:
            raise ValueError(
                "inventory requires the explicitly adopted source geometry"
            )
        if type(self.records) is not tuple or len(self.records) != 216:
            raise ValueError("inventory requires all 216 immutable point records")
        for index, record in enumerate(self.records):
            if type(record) is not KPointDiagnosis or record.ordered_index != index:
                raise ValueError(
                    "inventory point records must have exact declared order"
                )
            numerators = self._numerators(index)
            expected = tuple(float(f"{value / 6:.10f}") for value in numerators)
            if record.fractional_coordinates != expected:
                raise ValueError(
                    "inventory cannot snap or reorder coordinate presentations"
                )

    @staticmethod
    def _numerators(index: int) -> tuple[int, int, int]:
        return index // 36, index // 6 % 6, index % 6

    @staticmethod
    def _transpose(matrix: IntMatrix) -> IntMatrix:
        return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))

    @staticmethod
    def _product(left: IntMatrix, right: IntMatrix) -> IntMatrix:
        return tuple(
            tuple(sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3))
            for i in range(3)
        )

    @staticmethod
    def _half(matrix: IntMatrix) -> IntMatrix:
        if any(value % 2 for row in matrix for value in row):
            raise ValueError(
                "cubic operation did not preserve the FCC translation lattice"
            )
        return tuple(tuple(value // 2 for value in row) for row in matrix)

    @classmethod
    def operations(cls) -> tuple[tuple[IntMatrix, IntMatrix, IntMatrix, int], ...]:
        """Return all 48 (Cartesian R, direct M, reciprocal Q, translation/quarter).

        M=P^-1 R P and Q=P^T R P^-T=M^-T. For t=0 or t=tau,
        M{0,tau}+t must equal {0,tau} modulo Z^3 exactly. Both signs of det R
        are included; no antiunitary/time-reversal operation is inferred.
        """
        result: list[tuple[IntMatrix, IntMatrix, IntMatrix, int]] = []
        for permutation in permutations(range(3)):
            for signs in product((-1, 1), repeat=3):
                cartesian = tuple(
                    tuple(signs[i] if j == permutation[i] else 0 for j in range(3))
                    for i in range(3)
                )
                direct = cls._half(
                    cls._product(cls._product(_TWO_P_INVERSE, cartesian), _P)
                )
                reciprocal = cls._half(
                    cls._product(
                        cls._product(cls._transpose(_P), cartesian),
                        cls._transpose(_TWO_P_INVERSE),
                    )
                )
                if cls._product(cls._transpose(direct), reciprocal) != _IDENTITY:
                    raise ValueError(
                        "direct/reciprocal geometric actions are inconsistent"
                    )
                translations = tuple(
                    shift
                    for shift in (0, 1)
                    if {
                        (shift, shift, shift),
                        tuple((sum(row) + shift) % 4 for row in direct),
                    }
                    == {(0, 0, 0), (1, 1, 1)}
                )
                if len(translations) != 1:
                    raise ValueError(
                        "operation does not preserve the declared diamond motif"
                    )
                result.append((cartesian, direct, reciprocal, translations[0]))
        if len({item[1] for item in result}) != 48:
            raise ValueError("diamond geometric operation inventory is incomplete")
        return tuple(result)

    def execute(self) -> JsonObject:
        """Retain exhaustive index permutations/orbits and actual deficient-star rows."""
        operations: list[JsonValue] = []
        permutations_by_operation: list[tuple[int, ...]] = []
        for operation_index, (cartesian, direct, reciprocal, shift) in enumerate(
            self.operations()
        ):
            image: list[int] = []
            maximum_residual = Fraction(0)
            for index, record in enumerate(self.records):
                n = self._numerators(index)
                unwrapped = tuple(
                    sum(row[j] * n[j] for j in range(3)) for row in reciprocal
                )
                target_n = tuple(value % 6 for value in unwrapped)
                target_index = 36 * target_n[0] + 6 * target_n[1] + target_n[2]
                image.append(target_index)
                target = self.records[target_index]
                for axis in range(3):
                    wrap = (unwrapped[axis] - target_n[axis]) // 6
                    residual = abs(
                        sum(
                            reciprocal[axis][j]
                            * Fraction.from_float(record.fractional_coordinates[j])
                            for j in range(3)
                        )
                        - Fraction.from_float(target.fractional_coordinates[axis])
                        - wrap
                    )
                    maximum_residual = max(maximum_residual, residual)
            if set(image) != set(range(216)):
                raise ValueError(
                    "geometric operation is not a permutation of all source indices"
                )
            permutations_by_operation.append(tuple(image))
            operations.append(
                {
                    "operation_index": operation_index,
                    "cartesian_signed_permutation": [list(row) for row in cartesian],
                    "direct_fractional_rotation": [list(row) for row in direct],
                    "reciprocal_fractional_rotation": [list(row) for row in reciprocal],
                    "fractional_translation_quarter_numerators": [shift, shift, shift],
                    "point_permutation": list(image),
                    "maximum_printed_coordinate_component_residual": [
                        hex(maximum_residual.numerator),
                        hex(maximum_residual.denominator),
                    ],
                }
            )
        orbits = tuple(
            tuple(sorted({image[i] for image in permutations_by_operation}))
            for i in range(216)
        )
        distinct = tuple(sorted(set(orbits)))
        if sorted(index for orbit in distinct for index in orbit) != list(range(216)):
            raise ValueError(
                "geometric orbits do not partition the complete source domain"
            )
        stars: list[JsonValue] = []
        for seed in self.records:
            if seed.full_rank_gate_passed:
                continue
            members = orbits[seed.ordered_index]
            stars.append(
                {
                    "deficient_seed_index": seed.ordered_index,
                    "related_indices": list(members),
                    "point_diagnostics": [
                        self.records[index].to_json() for index in members
                    ],
                    "deficient_member_indices": [
                        index
                        for index in members
                        if not self.records[index].full_rank_gate_passed
                    ],
                    "geometric_stabilizer_operation_indices": [
                        i
                        for i, image in enumerate(permutations_by_operation)
                        if image[seed.ordered_index] == seed.ordered_index
                    ],
                }
            )
        return {
            "record_type": "c6-diamond-construction-index-inventory-v1",
            "geometry_identity": self.geometry_identity,
            "scope": "complete geometric construction-index relations; not electronic symmetry representations",
            "point_count": 216,
            "operation_count": 48,
            "index_rule": "j=36*i+6*l+m; (i,l,m) in {0,...,5}^3; Q*n modulo 6",
            "point_coordinates": [
                list(record.fractional_coordinates) for record in self.records
            ],
            "operations": operations,
            "orbit_partition": [list(orbit) for orbit in distinct],
            "deficient_point_stars": stars,
            "interpretation": "Native coordinate presentations remain unchanged. Nonzero coordinate residuals are not waived. No exact native physical-k equality, equal rank, Bloch/trial/Wannier action, irrep, or physical symmetry breaking follows from these index relations.",
        }
