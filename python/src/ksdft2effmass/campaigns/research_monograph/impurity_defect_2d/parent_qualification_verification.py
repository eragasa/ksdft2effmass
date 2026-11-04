"""Independent sparse reconstruction for periodic-2D parent qualification.

This module imports no production parent-qualification calculator and invokes no
maintained operator constructor or gauge-bridge Action. It reconstructs compact
parents with independent FFT arithmetic and constructs uniform-link and quotient-seam
matrices directly from integer quotient data.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.solidstate import (
    BoundaryTwistMeshEnumerator,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    ScalarHoppingModel,
)

from .parent_qualification import (
    ParentQualificationCriterionEvaluator,
    ParentQualificationDefinition,
    ParentQualificationResult,
    QualifiedParentMetrics,
    QualifiedPerturbationMetrics,
)

type IntPair = tuple[int, int]
type ComplexCsr = sparse.csr_array


@dataclass(frozen=True, slots=True)
class ParentQualificationVerificationResult:
    """Retain independent reconstruction and exact criterion-correlation evidence."""

    source: ParentQualificationResult
    absolute_tolerance: float
    maximum_metric_absolute_difference: float
    reconstructed_parent_route_evaluations: int
    reconstructed_defect_route_evaluations: int
    reconstruction_passed: bool
    criteria_match: bool

    def __post_init__(self) -> None:
        """Validate source correlation, tolerances, counts, and dispositions."""
        if type(self.source) is not ParentQualificationResult:
            raise TypeError("source must be ParentQualificationResult")
        for value, name in (
            (self.absolute_tolerance, "absolute_tolerance"),
            (
                self.maximum_metric_absolute_difference,
                "maximum_metric_absolute_difference",
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        for value, name in (
            (
                self.reconstructed_parent_route_evaluations,
                "reconstructed_parent_route_evaluations",
            ),
            (
                self.reconstructed_defect_route_evaluations,
                "reconstructed_defect_route_evaluations",
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if type(self.reconstruction_passed) is not bool:
            raise TypeError("reconstruction_passed must be a built-in bool")
        if type(self.criteria_match) is not bool:
            raise TypeError("criteria_match must be a built-in bool")

    @property
    def passes(self) -> bool:
        """Return whether independent arithmetic and criterion correlation pass."""
        return self.reconstruction_passed and self.criteria_match


class ParentQualificationIndependentVerifier:
    """Reconstruct parent qualification without production construction imports."""

    __slots__ = ()

    def execute(
        self,
        source: ParentQualificationResult,
        *,
        absolute_tolerance: float,
    ) -> ParentQualificationVerificationResult:
        """Return independently reconstructed aggregate qualification metrics."""
        if type(source) is not ParentQualificationResult:
            raise TypeError("source must be ParentQualificationResult")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        definition = source.definition
        anisotropic_full, anisotropic = self._anisotropic(definition)
        isotropic = self._model_values(definition.isotropic_parent)
        isotropic_full = self._model_values(definition.isotropic_pretruncation_parent)
        swapped = {(ry, rx): value for (rx, ry), value in anisotropic.items()}
        swapped_full = {(ry, rx): value for (rx, ry), value in anisotropic_full.items()}
        parent_values = (isotropic, anisotropic, swapped)
        full_values = (isotropic_full, anisotropic_full, swapped_full)
        reconstructed_parents = tuple(
            self._parent_metrics(
                definition,
                parent_identifier,
                values,
                full,
                expected_digest,
            )
            for (parent_identifier, expected_digest), values, full in zip(
                definition.expected_parent_digests,
                parent_values,
                full_values,
                strict=True,
            )
        )
        reconstructed_perturbations = tuple(
            self._perturbation_metrics(definition, index)
            for index in range(len(definition.perturbations))
        )
        separability = self._separability_metric(definition)
        differences: list[float] = [
            abs(source.maximum_plane_wave_separability_absolute - separability)
        ]
        for retained_parent, reconstructed_parent in zip(
            source.parents, reconstructed_parents, strict=True
        ):
            differences.extend(
                self._parent_differences(retained_parent, reconstructed_parent)
            )
        for retained_perturbation, reconstructed_perturbation in zip(
            source.perturbations, reconstructed_perturbations, strict=True
        ):
            differences.extend(
                self._perturbation_differences(
                    retained_perturbation, reconstructed_perturbation
                )
            )
        maximum = max(differences, default=0.0)
        parent_routes = sum(value.route_evaluations for value in reconstructed_parents)
        defect_routes = sum(
            value.route_evaluations for value in reconstructed_perturbations
        )
        exact_fields_match = all(
            retained.parent_identifier == reconstructed.parent_identifier
            and retained.hopping_count == reconstructed.hopping_count
            and retained.hopping_digest == reconstructed.hopping_digest
            and retained.route_evaluations == reconstructed.route_evaluations
            for retained, reconstructed in zip(
                source.parents, reconstructed_parents, strict=True
            )
        ) and all(
            retained.perturbation_identifier == reconstructed.perturbation_identifier
            and retained.term_count == reconstructed.term_count
            and retained.route_evaluations == reconstructed.route_evaluations
            for retained, reconstructed in zip(
                source.perturbations, reconstructed_perturbations, strict=True
            )
        )
        reconstructed_failures = ParentQualificationCriterionEvaluator().execute(
            definition,
            reconstructed_parents,
            reconstructed_perturbations,
            separability,
        )
        return ParentQualificationVerificationResult(
            source=source,
            absolute_tolerance=absolute_tolerance,
            maximum_metric_absolute_difference=maximum,
            reconstructed_parent_route_evaluations=parent_routes,
            reconstructed_defect_route_evaluations=defect_routes,
            reconstruction_passed=(
                exact_fields_match and maximum <= absolute_tolerance
            ),
            criteria_match=(source.failed_criteria == reconstructed_failures),
        )

    def _parent_metrics(
        self,
        definition: ParentQualificationDefinition,
        parent_identifier: str,
        values: dict[IntPair, complex],
        full_values: dict[IntPair, complex],
        expected_digest: str,
    ) -> QualifiedParentMetrics:
        """Independently reconstruct aggregate metrics for one parent."""
        operations = (
            self._d4_operations()
            if parent_identifier == definition.isotropic_parent.identifier
            else self._d2_operations()
        )
        hopping_hermiticity, hopping_symmetry = self._hopping_metrics(
            values, operations
        )
        represented_hermiticity = 0.0
        gauge_bridge = 0.0
        route_evaluations = 0
        twists = BoundaryTwistMeshEnumerator().execute(definition.twist_mesh)
        for shape in definition.shapes:
            nx, ny = self._pair(shape.extents)
            for representative in twists:
                phi_x, phi_y = self._float_pair(representative.turns)
                uniform = self._uniform_parent(values, nx, ny, phi_x, phi_y)
                seam = self._seam_parent(values, nx, ny, phi_x, phi_y)
                route_evaluations += 2
                represented_hermiticity = max(
                    represented_hermiticity,
                    self._hermiticity(uniform),
                    self._hermiticity(seam),
                )
                gauge_bridge = max(
                    gauge_bridge,
                    self._bridge_residual(uniform, seam, nx, ny, phi_x, phi_y),
                )
        truncation_maximum, truncation_frobenius = self._truncation_metrics(
            full_values, values
        )
        return QualifiedParentMetrics(
            parent_identifier=parent_identifier,
            hopping_count=len(values),
            hopping_digest=expected_digest,
            hopping_hermiticity_maximum_absolute=hopping_hermiticity,
            hopping_symmetry_maximum_absolute=hopping_symmetry,
            represented_hermiticity_maximum_absolute=represented_hermiticity,
            gauge_bridge_maximum_absolute=gauge_bridge,
            route_evaluations=route_evaluations,
            inherited_truncation_maximum_absolute=truncation_maximum,
            inherited_truncation_frobenius=truncation_frobenius,
        )

    def _perturbation_metrics(
        self, definition: ParentQualificationDefinition, index: int
    ) -> QualifiedPerturbationMetrics:
        """Independently reconstruct aggregate metrics for one perturbation."""
        perturbation = definition.perturbations[index]
        represented_hermiticity = 0.0
        gauge_bridge = 0.0
        route_evaluations = 0
        twists = BoundaryTwistMeshEnumerator().execute(definition.twist_mesh)
        for shape in definition.shapes:
            nx, ny = self._pair(shape.extents)
            for representative in twists:
                phi_x, phi_y = self._float_pair(representative.turns)
                uniform = self._uniform_perturbation(
                    perturbation.terms, nx, ny, phi_x, phi_y
                )
                seam = self._seam_perturbation(perturbation.terms, nx, ny, phi_x, phi_y)
                route_evaluations += 2
                represented_hermiticity = max(
                    represented_hermiticity,
                    self._hermiticity(uniform),
                    self._hermiticity(seam),
                )
                gauge_bridge = max(
                    gauge_bridge,
                    self._bridge_residual(uniform, seam, nx, ny, phi_x, phi_y),
                )
        return QualifiedPerturbationMetrics(
            perturbation_identifier=perturbation.identifier,
            term_count=len(perturbation.terms),
            represented_hermiticity_maximum_absolute=represented_hermiticity,
            gauge_bridge_maximum_absolute=gauge_bridge,
            route_evaluations=route_evaluations,
        )

    @staticmethod
    def _model_values(model: ScalarHoppingModel) -> dict[IntPair, complex]:
        """Convert one validated two-dimensional model to an independent mapping."""
        return {
            ParentQualificationIndependentVerifier._pair(
                term.displacement.components
            ): term.value
            for term in model.terms
        }

    def _anisotropic(
        self, definition: ParentQualificationDefinition
    ) -> tuple[dict[IntPair, complex], dict[IntPair, complex]]:
        """Reconstruct anisotropic coefficients through independent FFT arithmetic."""
        mesh = definition.reciprocal_mesh_size
        momenta = np.fft.fftfreq(mesh)
        x_energies = np.asarray(
            [
                self._lowest_band(
                    float(momentum),
                    definition.anisotropic_lambda_x,
                    definition.plane_wave_cutoff,
                )
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        y_energies = np.asarray(
            [
                self._lowest_band(
                    float(momentum),
                    definition.anisotropic_lambda_y,
                    definition.plane_wave_cutoff,
                )
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        coefficients = np.fft.ifft2(
            x_energies[:, np.newaxis] + y_energies[np.newaxis, :]
        )
        half = mesh // 2
        full = {
            (rx, ry): complex(coefficients[rx % mesh, ry % mesh])
            for rx in range(-half, half + 1)
            for ry in range(-half, half + 1)
        }
        compact = {
            displacement: value
            for displacement, value in full.items()
            if displacement[0] ** 2 + displacement[1] ** 2
            <= definition.hopping_maximum_squared_radius
        }
        if len(full) != 225 or len(compact) != 61:
            raise ValueError("independent anisotropic support inventory changed")
        return full, compact

    @staticmethod
    def _lowest_band(momentum: float, strength: float, cutoff: int) -> float:
        """Independently evaluate one-dimensional lowest-band energy."""
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.zeros((2 * cutoff + 1, 2 * cutoff + 1), dtype=np.float64)
        np.fill_diagonal(matrix, np.square(momentum + indices))
        coupling = strength / 2.0
        rows = np.arange(2 * cutoff, dtype=np.int64)
        matrix[rows, rows + 1] = coupling
        matrix[rows + 1, rows] = coupling
        return float(np.linalg.eigvalsh(matrix)[0])

    def _separability_metric(self, definition: ParentQualificationDefinition) -> float:
        """Independently assemble Kronecker-sum fibers at selected momenta."""
        momenta = (
            (0.0, 0.0),
            (1.0 / 15.0, -2.0 / 15.0),
            (7.0 / 15.0, 5.0 / 15.0),
            (-7.0 / 15.0, -6.0 / 15.0),
        )
        cutoff = definition.plane_wave_cutoff
        maximum = 0.0
        for kx, ky in momenta:
            x_matrix = self._one_dimensional_matrix(
                kx, definition.anisotropic_lambda_x, cutoff
            )
            y_matrix = self._one_dimensional_matrix(
                ky, definition.anisotropic_lambda_y, cutoff
            )
            identity = np.eye(2 * cutoff + 1, dtype=np.float64)
            represented = np.kron(x_matrix, identity) + np.kron(identity, y_matrix)
            observed = float(np.linalg.eigvalsh(represented)[0])
            expected = float(np.linalg.eigvalsh(x_matrix)[0]) + float(
                np.linalg.eigvalsh(y_matrix)[0]
            )
            maximum = max(maximum, abs(observed - expected))
        return maximum

    @staticmethod
    def _one_dimensional_matrix(
        momentum: float, strength: float, cutoff: int
    ) -> np.ndarray:
        """Return one independent dense one-dimensional cosine matrix."""
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        result = np.zeros((2 * cutoff + 1, 2 * cutoff + 1), dtype=np.float64)
        np.fill_diagonal(result, np.square(momentum + indices))
        coupling = strength / 2.0
        rows = np.arange(2 * cutoff, dtype=np.int64)
        result[rows, rows + 1] = coupling
        result[rows + 1, rows] = coupling
        return result

    @staticmethod
    def _uniform_parent(
        values: dict[IntPair, complex],
        nx: int,
        ny: int,
        phi_x: float,
        phi_y: float,
    ) -> ComplexCsr:
        """Construct one independent uniform-link parent matrix."""
        rows: list[int] = []
        columns: list[int] = []
        data: list[complex] = []
        for x in range(nx):
            for y in range(ny):
                row = x * ny + y
                for (dx, dy), value in values.items():
                    rows.append(row)
                    columns.append(((x + dx) % nx) * ny + ((y + dy) % ny))
                    data.append(
                        value
                        * np.exp(2.0j * np.pi * (phi_x * dx / nx + phi_y * dy / ny))
                    )
        return ParentQualificationIndependentVerifier._csr(rows, columns, data, nx * ny)

    @staticmethod
    def _seam_parent(
        values: dict[IntPair, complex],
        nx: int,
        ny: int,
        phi_x: float,
        phi_y: float,
    ) -> ComplexCsr:
        """Construct one independent quotient-seam parent matrix."""
        rows: list[int] = []
        columns: list[int] = []
        data: list[complex] = []
        for x in range(nx):
            for y in range(ny):
                row = x * ny + y
                for (dx, dy), value in values.items():
                    qx, tx = divmod(x + dx, nx)
                    qy, ty = divmod(y + dy, ny)
                    rows.append(row)
                    columns.append(tx * ny + ty)
                    data.append(
                        value * np.exp(2.0j * np.pi * (qx * phi_x + qy * phi_y))
                    )
        return ParentQualificationIndependentVerifier._csr(rows, columns, data, nx * ny)

    @staticmethod
    def _uniform_perturbation(
        terms: tuple[LocalizedOnsiteTerm | LocalizedBondTerm, ...],
        nx: int,
        ny: int,
        phi_x: float,
        phi_y: float,
    ) -> ComplexCsr:
        """Construct one independent uniform-link localized matrix."""
        rows: list[int] = []
        columns: list[int] = []
        data: list[complex] = []
        for term in terms:
            if type(term) is LocalizedOnsiteTerm:
                x, y = ParentQualificationIndependentVerifier._pair(
                    term.site.components
                )
                index = (x % nx) * ny + (y % ny)
                rows.append(index)
                columns.append(index)
                data.append(term.value)
            elif type(term) is LocalizedBondTerm:
                x, y = ParentQualificationIndependentVerifier._pair(
                    term.start.components
                )
                dx, dy = ParentQualificationIndependentVerifier._pair(
                    term.displacement.components
                )
                rows.append((x % nx) * ny + (y % ny))
                columns.append(((x + dx) % nx) * ny + ((y + dy) % ny))
                data.append(
                    term.value
                    * np.exp(2.0j * np.pi * (phi_x * dx / nx + phi_y * dy / ny))
                )
            else:
                raise AssertionError("validated localized term type was lost")
        return ParentQualificationIndependentVerifier._csr(rows, columns, data, nx * ny)

    @staticmethod
    def _seam_perturbation(
        terms: tuple[LocalizedOnsiteTerm | LocalizedBondTerm, ...],
        nx: int,
        ny: int,
        phi_x: float,
        phi_y: float,
    ) -> ComplexCsr:
        """Construct one independent quotient-seam localized matrix."""
        rows: list[int] = []
        columns: list[int] = []
        data: list[complex] = []
        for term in terms:
            if type(term) is LocalizedOnsiteTerm:
                x, y = ParentQualificationIndependentVerifier._pair(
                    term.site.components
                )
                index = (x % nx) * ny + (y % ny)
                rows.append(index)
                columns.append(index)
                data.append(term.value)
            elif type(term) is LocalizedBondTerm:
                x, y = ParentQualificationIndependentVerifier._pair(
                    term.start.components
                )
                dx, dy = ParentQualificationIndependentVerifier._pair(
                    term.displacement.components
                )
                source_qx, source_x = divmod(x, nx)
                source_qy, source_y = divmod(y, ny)
                target_qx, target_x = divmod(x + dx, nx)
                target_qy, target_y = divmod(y + dy, ny)
                rows.append(source_x * ny + source_y)
                columns.append(target_x * ny + target_y)
                data.append(
                    term.value
                    * np.exp(
                        2.0j
                        * np.pi
                        * (
                            (target_qx - source_qx) * phi_x
                            + (target_qy - source_qy) * phi_y
                        )
                    )
                )
            else:
                raise AssertionError("validated localized term type was lost")
        return ParentQualificationIndependentVerifier._csr(rows, columns, data, nx * ny)

    @staticmethod
    def _bridge_residual(
        uniform: ComplexCsr,
        seam: ComplexCsr,
        nx: int,
        ny: int,
        phi_x: float,
        phi_y: float,
    ) -> float:
        """Compare gauges through an independently constructed diagonal bridge."""
        phases = np.asarray(
            [
                np.exp(2.0j * np.pi * (x * phi_x / nx + y * phi_y / ny))
                for x in range(nx)
                for y in range(ny)
            ],
            dtype=np.complex128,
        )
        bridge = sparse.diags(phases, offsets=0, format="csr")
        residual = seam - bridge @ uniform @ bridge.conjugate().transpose()
        residual.sum_duplicates()
        residual.eliminate_zeros()
        return ParentQualificationIndependentVerifier._maximum(residual)

    def _truncation_metrics(
        self, full: dict[IntPair, complex], compact: dict[IntPair, complex]
    ) -> tuple[float, float]:
        """Reconstruct inherited finite-matrix truncation losses independently."""
        maximum = 0.0
        frobenius = 0.0
        for phi_x, phi_y in ((0.0, 0.0), (0.37, -0.23)):
            difference = self._uniform_parent(
                full, 8, 8, phi_x, phi_y
            ) - self._uniform_parent(compact, 8, 8, phi_x, phi_y)
            difference.sum_duplicates()
            difference.eliminate_zeros()
            maximum = max(maximum, self._maximum(difference))
            frobenius = max(
                frobenius,
                float(np.sqrt(np.sum(np.square(np.abs(difference.data))))),
            )
        return maximum, frobenius

    @staticmethod
    def _hopping_metrics(
        values: dict[IntPair, complex],
        operations: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    ) -> tuple[float, float]:
        """Return independent hopping Hermiticity and symmetry metrics."""
        hermiticity = 0.0
        symmetry = 0.0
        for displacement, value in values.items():
            reverse = (-displacement[0], -displacement[1])
            if reverse not in values:
                raise ValueError(f"missing independent Hermitian partner {reverse}")
            hermiticity = max(hermiticity, abs(values[reverse] - value.conjugate()))
            for operation in operations:
                transformed = (
                    operation[0][0] * displacement[0]
                    + operation[0][1] * displacement[1],
                    operation[1][0] * displacement[0]
                    + operation[1][1] * displacement[1],
                )
                if transformed not in values:
                    raise ValueError(
                        f"missing independent symmetry partner {transformed}"
                    )
                symmetry = max(symmetry, abs(values[transformed] - value))
        return float(hermiticity), float(symmetry)

    @staticmethod
    def _csr(
        rows: list[int], columns: list[int], values: list[complex], dimension: int
    ) -> ComplexCsr:
        """Return one canonical independent complex CSR matrix."""
        result = sparse.coo_array(
            (
                np.asarray(values, dtype=np.complex128),
                (
                    np.asarray(rows, dtype=np.int64),
                    np.asarray(columns, dtype=np.int64),
                ),
            ),
            shape=(dimension, dimension),
            dtype=np.complex128,
        ).tocsr()
        result.sum_duplicates()
        result.eliminate_zeros()
        return result

    @staticmethod
    def _hermiticity(matrix: ComplexCsr) -> float:
        """Return one independent sparse Hermiticity residual."""
        residual = matrix - matrix.conjugate().transpose()
        residual.sum_duplicates()
        residual.eliminate_zeros()
        return ParentQualificationIndependentVerifier._maximum(residual)

    @staticmethod
    def _maximum(matrix: ComplexCsr) -> float:
        """Return one finite sparse maximum absolute entry."""
        if matrix.data.size == 0:
            return 0.0
        magnitudes = np.abs(matrix.data)
        if not np.all(np.isfinite(magnitudes)):
            raise ValueError("independent sparse residual must remain finite")
        return float(np.max(magnitudes))

    @staticmethod
    def _pair(
        values: tuple[int] | tuple[int, int] | tuple[int, int, int],
    ) -> IntPair:
        """Close one validated two-dimensional integer tuple."""
        if len(values) != 2:
            raise AssertionError("two-dimensional integer components were lost")
        return values[0], values[1]

    @staticmethod
    def _float_pair(
        values: tuple[float] | tuple[float, float] | tuple[float, float, float],
    ) -> tuple[float, float]:
        """Close one validated two-dimensional float tuple."""
        if len(values) != 2:
            raise AssertionError("two-dimensional float components were lost")
        return values[0], values[1]

    @staticmethod
    def _parent_differences(
        retained: QualifiedParentMetrics, reconstructed: QualifiedParentMetrics
    ) -> tuple[float, ...]:
        """Return every parent floating metric difference."""
        return (
            abs(
                retained.hopping_hermiticity_maximum_absolute
                - reconstructed.hopping_hermiticity_maximum_absolute
            ),
            abs(
                retained.hopping_symmetry_maximum_absolute
                - reconstructed.hopping_symmetry_maximum_absolute
            ),
            abs(
                retained.represented_hermiticity_maximum_absolute
                - reconstructed.represented_hermiticity_maximum_absolute
            ),
            abs(
                retained.gauge_bridge_maximum_absolute
                - reconstructed.gauge_bridge_maximum_absolute
            ),
            abs(
                retained.inherited_truncation_maximum_absolute
                - reconstructed.inherited_truncation_maximum_absolute
            ),
            abs(
                retained.inherited_truncation_frobenius
                - reconstructed.inherited_truncation_frobenius
            ),
        )

    @staticmethod
    def _perturbation_differences(
        retained: QualifiedPerturbationMetrics,
        reconstructed: QualifiedPerturbationMetrics,
    ) -> tuple[float, ...]:
        """Return every perturbation floating metric difference."""
        return (
            abs(
                retained.represented_hermiticity_maximum_absolute
                - reconstructed.represented_hermiticity_maximum_absolute
            ),
            abs(
                retained.gauge_bridge_maximum_absolute
                - reconstructed.gauge_bridge_maximum_absolute
            ),
        )

    @staticmethod
    def _d4_operations() -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
        """Return the independent frozen D4 operation inventory."""
        return (
            ((1, 0), (0, 1)),
            ((0, -1), (1, 0)),
            ((-1, 0), (0, -1)),
            ((0, 1), (-1, 0)),
            ((-1, 0), (0, 1)),
            ((1, 0), (0, -1)),
            ((0, 1), (1, 0)),
            ((0, -1), (-1, 0)),
        )

    @staticmethod
    def _d2_operations() -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
        """Return the independent frozen anisotropic D2 inventory."""
        return (
            ((1, 0), (0, 1)),
            ((-1, 0), (0, -1)),
            ((-1, 0), (0, 1)),
            ((1, 0), (0, -1)),
        )
