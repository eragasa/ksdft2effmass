#!/usr/bin/env python3
"""Run the matched one-dimensional pristine-defect extraction exercise."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type RealMatrixTuple = tuple[tuple[float, ...], ...]
type ComplexMatrixTuple = tuple[tuple[complex, ...], ...]
type ComparisonStatus = Literal["compatible", "stopped"]


@dataclass(frozen=True, slots=True)
class ParentSourceReference:
    """Identify the accepted periodic-parent records used by the exercise."""

    isolated_path: str
    isolated_sha256: str
    composite_path: str
    composite_sha256: str
    composite_group_id: str
    hopping_range: int

    def __post_init__(self) -> None:
        values = (
            self.isolated_path,
            self.isolated_sha256,
            self.composite_path,
            self.composite_sha256,
            self.composite_group_id,
        )
        if not all(values):
            raise ValueError("parent source identities must be nonempty")
        if self.hopping_range < 1:
            raise ValueError("parent hopping range must be positive")


@dataclass(frozen=True, slots=True)
class FoldingControl:
    """Represent the exact primitive-to-supercell folding cases."""

    supercell_size: int
    reduced_momentum_times_supercell: tuple[float, ...]

    def __post_init__(self) -> None:
        if self.supercell_size < 3:
            raise ValueError("folding supercell must contain at least three cells")
        if not self.reduced_momentum_times_supercell:
            raise ValueError("folding momenta must be nonempty")
        if any(
            not np.isfinite(value) or not -0.5 <= value < 0.5
            for value in self.reduced_momentum_times_supercell
        ):
            raise ValueError("folding momenta must lie in the reduced half-open zone")


@dataclass(frozen=True, slots=True)
class ExtractionControl:
    """Represent authored planted-defect blocks for exact recovery."""

    supercell_size: int
    reduced_momentum_times_supercell: float
    scalar_onsite_strength: float
    orbital_onsite: RealMatrixTuple
    nearest_neighbor: RealMatrixTuple
    range_two: RealMatrixTuple
    collinear_independent: RealMatrixTuple
    collinear_splitting: RealMatrixTuple
    spin_x: RealMatrixTuple
    spin_y: RealMatrixTuple
    spin_z: RealMatrixTuple

    def __post_init__(self) -> None:
        if self.supercell_size < 7:
            raise ValueError("extraction supercell must separate range-two defects")
        if not np.isfinite(self.reduced_momentum_times_supercell):
            raise ValueError("extraction momentum must be finite")
        if not -0.5 <= self.reduced_momentum_times_supercell < 0.5:
            raise ValueError("extraction momentum must lie in the reduced zone")
        if not np.isfinite(self.scalar_onsite_strength):
            raise ValueError("scalar onsite strength must be finite")
        matrices = (
            self.orbital_onsite,
            self.nearest_neighbor,
            self.range_two,
            self.collinear_independent,
            self.collinear_splitting,
            self.spin_x,
            self.spin_y,
            self.spin_z,
        )
        if any(
            len(matrix) != 2 or any(len(row) != 2 for row in matrix)
            for matrix in matrices
        ):
            raise ValueError("every authored orbital block must be two by two")


@dataclass(frozen=True, slots=True)
class AlignmentControl:
    """Represent the declared coordinate and energy-reference scrambling."""

    translation_cells: int
    orbital_permutation: tuple[int, int]
    orbital_rotation_angle: float
    orbital_phases: tuple[float, float]
    site_phase_step: float
    spin_axis: tuple[float, float, float]
    spin_rotation_angle: float
    energy_shift: float

    def __post_init__(self) -> None:
        values = np.asarray(
            (
                self.orbital_rotation_angle,
                *self.orbital_phases,
                self.site_phase_step,
                *self.spin_axis,
                self.spin_rotation_angle,
                self.energy_shift,
            ),
            dtype=np.float64,
        )
        if not np.all(np.isfinite(values)):
            raise ValueError("alignment values must be finite")
        if tuple(sorted(self.orbital_permutation)) != (0, 1):
            raise ValueError("orbital permutation must contain zero and one")
        if np.linalg.norm(np.asarray(self.spin_axis, dtype=np.float64)) == 0.0:
            raise ValueError("spin rotation axis must be nonzero")


@dataclass(frozen=True, slots=True)
class FiniteSizeControl:
    """Represent the periodic-image sequence for one localized defect."""

    supercell_sizes: tuple[int, ...]
    momentum_mesh_size: int
    gaussian_width: float
    gaussian_strength: float
    orbital_block: RealMatrixTuple
    core_radius: int

    def __post_init__(self) -> None:
        if tuple(sorted(set(self.supercell_sizes))) != self.supercell_sizes:
            raise ValueError("supercell sizes must be strictly increasing")
        if not self.supercell_sizes or self.supercell_sizes[0] <= 2 * self.core_radius:
            raise ValueError("every supercell must contain the declared core")
        if self.momentum_mesh_size < 3 or self.momentum_mesh_size % 2 == 0:
            raise ValueError("momentum mesh size must be odd and at least three")
        if (
            not np.isfinite(self.gaussian_width)
            or self.gaussian_width <= 0.0
            or not np.isfinite(self.gaussian_strength)
        ):
            raise ValueError("Gaussian controls must be finite with positive width")
        if len(self.orbital_block) != 2 or any(
            len(row) != 2 for row in self.orbital_block
        ):
            raise ValueError("finite-size orbital block must be two by two")
        if self.core_radius < 0:
            raise ValueError("core radius must be nonnegative")


@dataclass(frozen=True, slots=True)
class SmoothnessControl:
    """Represent the fixed-peak and fixed-integrated Gaussian scans."""

    supercell_size: int
    widths: tuple[float, ...]
    fixed_peak_strength: float
    fixed_integrated_strength: float

    def __post_init__(self) -> None:
        if self.supercell_size < 16 or self.supercell_size % 2 != 0:
            raise ValueError("smoothness supercell must be even and at least sixteen")
        if tuple(sorted(set(self.widths))) != self.widths or any(
            not np.isfinite(value) or value <= 0.0 for value in self.widths
        ):
            raise ValueError("smoothness widths must be positive and increasing")
        if not np.isfinite(self.fixed_peak_strength) or not np.isfinite(
            self.fixed_integrated_strength
        ):
            raise ValueError("smoothness strengths must be finite")


@dataclass(frozen=True, slots=True)
class MetricContrastControl:
    """Represent two controlled operator-versus-observable counterexamples."""

    profile_family: str
    width: float
    excited_residual_strength: float
    coupling_to_gap_ratio: float

    def __post_init__(self) -> None:
        if self.profile_family != "fixed-integrated":
            raise ValueError("metric contrast must use the fixed-integrated family")
        values = (
            self.width,
            self.excited_residual_strength,
            self.coupling_to_gap_ratio,
        )
        if any(not np.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("metric contrast controls must be positive and finite")


@dataclass(frozen=True, slots=True)
class DefectExerciseInput:
    """Represent the complete frozen synthetic exercise input."""

    experiment_id: str
    parent: ParentSourceReference
    folding: FoldingControl
    extraction: ExtractionControl
    alignment: AlignmentControl
    finite_size: FiniteSizeControl
    smoothness: SmoothnessControl
    metric_contrast: MetricContrastControl
    algebraic_tolerance: float
    bound_threshold_tolerance: float

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        tolerances = (self.algebraic_tolerance, self.bound_threshold_tolerance)
        if any(not np.isfinite(value) or value <= 0.0 for value in tolerances):
            raise ValueError("tolerances must be positive and finite")


@dataclass(frozen=True, slots=True)
class SupercellBasis:
    """Identify comparison-critical metadata for one supercell representation."""

    state_space_id: str
    cell_count: int
    orbital_count: int
    spin_count: int
    reduced_momentum: float
    site_ordering: str
    orbital_ordering: str
    spin_ordering: str
    coordinate_frame: str
    energy_unit: str
    energy_reference: str
    geometry_id: str
    subspace_id: str

    def __post_init__(self) -> None:
        text = (
            self.state_space_id,
            self.site_ordering,
            self.orbital_ordering,
            self.spin_ordering,
            self.coordinate_frame,
            self.energy_unit,
            self.energy_reference,
            self.geometry_id,
            self.subspace_id,
        )
        if not all(text):
            raise ValueError("basis metadata must be nonempty")
        if self.cell_count < 1 or self.orbital_count < 1 or self.spin_count < 1:
            raise ValueError("basis dimensions must be positive")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced momentum must be finite")

    @property
    def dimension(self) -> int:
        """Return the matrix dimension implied by the represented factors."""
        return self.cell_count * self.orbital_count * self.spin_count


@dataclass(frozen=True, slots=True)
class RepresentedOperator:
    """Store one operationally immutable represented finite operator."""

    identifier: str
    basis: SupercellBasis
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("operator identifier must be nonempty")
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.shape != (self.basis.dimension, self.basis.dimension):
            raise ValueError("operator matrix shape must agree with basis metadata")
        if not np.all(np.isfinite(value)):
            raise ValueError("operator matrix must be finite")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    """Record direct comparison compatibility or structured stop codes."""

    status: ComparisonStatus
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if (self.status == "compatible") == bool(self.issue_codes):
            raise ValueError("compatibility status must agree with issue codes")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("compatibility issues must be sorted and unique")


@dataclass(frozen=True, slots=True)
class ParentData:
    """Retain accepted scalar and two-orbital hopping records in immutable form."""

    period: float
    scalar_hoppings: tuple[tuple[int, complex], ...]
    composite_hoppings: tuple[tuple[int, ComplexMatrixTuple], ...]
    source_identities: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not np.isfinite(self.period) or self.period <= 0.0:
            raise ValueError("period must be positive and finite")
        scalar_representatives = tuple(value[0] for value in self.scalar_hoppings)
        composite_representatives = tuple(value[0] for value in self.composite_hoppings)
        if scalar_representatives != tuple(sorted(set(scalar_representatives))):
            raise ValueError("scalar hopping representatives must be sorted and unique")
        if composite_representatives != tuple(sorted(set(composite_representatives))):
            raise ValueError("composite representatives must be sorted and unique")
        if not self.source_identities:
            raise ValueError("source identities must be retained")


class DefectExerciseInputDeserializer:
    """Deserialize the closed version-1 input record."""

    __slots__ = ()

    def execute(self, payload: bytes) -> DefectExerciseInput:
        root = self._mapping(
            cast(JsonValue, json.loads(payload.decode("utf-8"))), "input"
        )
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported input schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence_status must identify synthetic test data")
        parent = self._mapping(root["parent_sources"], "parent_sources")
        folding = self._mapping(root["folding_control"], "folding_control")
        extraction = self._mapping(root["extraction_control"], "extraction_control")
        alignment = self._mapping(root["alignment_control"], "alignment_control")
        finite_size = self._mapping(root["finite_size_control"], "finite_size_control")
        smoothness = self._mapping(root["smoothness_control"], "smoothness_control")
        contrast = self._mapping(
            root["metric_contrast_control"], "metric_contrast_control"
        )
        orbital_permutation = self._integers(
            alignment["orbital_permutation"], "orbital_permutation"
        )
        orbital_phases = self._reals(
            alignment["orbital_phases_radians"], "orbital_phases_radians"
        )
        spin_axis = self._reals(alignment["spin_rotation_axis"], "spin_rotation_axis")
        if (
            len(orbital_permutation) != 2
            or len(orbital_phases) != 2
            or len(spin_axis) != 3
        ):
            raise ValueError(
                "alignment permutation, phase, and axis dimensions are fixed"
            )
        return DefectExerciseInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            parent=ParentSourceReference(
                isolated_path=self._string(
                    parent["isolated_band_result_path"], "isolated path"
                ),
                isolated_sha256=self._string(
                    parent["isolated_band_result_sha256"], "isolated sha256"
                ),
                composite_path=self._string(
                    parent["composite_result_path"], "composite path"
                ),
                composite_sha256=self._string(
                    parent["composite_result_sha256"], "composite sha256"
                ),
                composite_group_id=self._string(
                    parent["composite_group_id"], "composite group"
                ),
                hopping_range=self._integer(
                    parent["parent_hopping_range_cells"], "hopping range"
                ),
            ),
            folding=FoldingControl(
                supercell_size=self._integer(
                    folding["supercell_size"], "folding supercell_size"
                ),
                reduced_momentum_times_supercell=self._reals(
                    folding["reduced_momentum_times_supercell"],
                    "folding momenta",
                ),
            ),
            extraction=ExtractionControl(
                supercell_size=self._integer(
                    extraction["supercell_size"], "extraction supercell_size"
                ),
                reduced_momentum_times_supercell=self._real(
                    extraction["reduced_momentum_times_supercell"],
                    "extraction momentum",
                ),
                scalar_onsite_strength=self._real(
                    extraction["scalar_onsite_strength"], "scalar onsite"
                ),
                orbital_onsite=self._matrix(
                    extraction["orbital_onsite_block"], "orbital onsite"
                ),
                nearest_neighbor=self._matrix(
                    extraction["nearest_neighbor_block"], "nearest neighbor"
                ),
                range_two=self._matrix(extraction["range_two_block"], "range two"),
                collinear_independent=self._matrix(
                    extraction["collinear_spin_independent_block"],
                    "collinear independent",
                ),
                collinear_splitting=self._matrix(
                    extraction["collinear_splitting_block"],
                    "collinear splitting",
                ),
                spin_x=self._matrix(extraction["spin_mixing_x_block"], "spin x"),
                spin_y=self._matrix(extraction["spin_mixing_y_block"], "spin y"),
                spin_z=self._matrix(extraction["spin_mixing_z_block"], "spin z"),
            ),
            alignment=AlignmentControl(
                translation_cells=self._integer(
                    alignment["translation_cells"], "translation_cells"
                ),
                orbital_permutation=(
                    orbital_permutation[0],
                    orbital_permutation[1],
                ),
                orbital_rotation_angle=self._real(
                    alignment["orbital_rotation_angle_radians"],
                    "orbital rotation",
                ),
                orbital_phases=(orbital_phases[0], orbital_phases[1]),
                site_phase_step=self._real(
                    alignment["site_phase_step_radians"], "site phase step"
                ),
                spin_axis=(spin_axis[0], spin_axis[1], spin_axis[2]),
                spin_rotation_angle=self._real(
                    alignment["spin_rotation_angle_radians"], "spin rotation"
                ),
                energy_shift=self._real(
                    alignment["energy_reference_shift"], "energy shift"
                ),
            ),
            finite_size=FiniteSizeControl(
                supercell_sizes=self._integers(
                    finite_size["supercell_sizes"], "supercell_sizes"
                ),
                momentum_mesh_size=self._integer(
                    finite_size["reduced_momentum_mesh_size"], "momentum mesh"
                ),
                gaussian_width=self._real(
                    finite_size["gaussian_width_cells"], "Gaussian width"
                ),
                gaussian_strength=self._real(
                    finite_size["gaussian_strength"], "Gaussian strength"
                ),
                orbital_block=self._matrix(
                    finite_size["orbital_block"], "finite-size orbital block"
                ),
                core_radius=self._integer(
                    finite_size["core_radius_cells"], "core radius"
                ),
            ),
            smoothness=SmoothnessControl(
                supercell_size=self._integer(
                    smoothness["supercell_size"], "smoothness supercell"
                ),
                widths=self._reals(smoothness["widths_cells"], "widths"),
                fixed_peak_strength=self._real(
                    smoothness["fixed_peak_strength"], "fixed peak"
                ),
                fixed_integrated_strength=self._real(
                    smoothness["fixed_integrated_strength"], "fixed integrated"
                ),
            ),
            metric_contrast=MetricContrastControl(
                profile_family=self._string(
                    contrast["profile_family"], "profile family"
                ),
                width=self._real(contrast["width_cells"], "contrast width"),
                excited_residual_strength=self._real(
                    contrast["excited_state_residual_strength"],
                    "excited residual",
                ),
                coupling_to_gap_ratio=self._real(
                    contrast["bound_continuum_coupling_to_gap_ratio"],
                    "coupling ratio",
                ),
            ),
            algebraic_tolerance=self._real(
                root["algebraic_tolerance"], "algebraic_tolerance"
            ),
            bound_threshold_tolerance=self._real(
                root["bound_state_threshold_tolerance"],
                "bound_state_threshold_tolerance",
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)

    def _matrix(self, value: JsonValue, name: str) -> RealMatrixTuple:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[tuple[float, ...]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be JSON arrays")
            rows.append(tuple(self._real(item, name) for item in row))
        return tuple(rows)


class ParentDataLoader:
    """Load and validate exact accepted parent artifacts selected by the input."""

    __slots__ = ()

    def execute(
        self, reference: ParentSourceReference, repository_root: Path
    ) -> ParentData:
        isolated_path = repository_root / reference.isolated_path
        composite_path = repository_root / reference.composite_path
        if self._sha256(isolated_path) != reference.isolated_sha256:
            raise ValueError("isolated-band parent identity mismatch")
        if self._sha256(composite_path) != reference.composite_sha256:
            raise ValueError("composite-band parent identity mismatch")
        isolated = self._mapping(
            cast(JsonValue, json.loads(isolated_path.read_text(encoding="utf-8"))),
            "isolated result",
        )
        convention = self._mapping(
            isolated["dimensionless_convention"], "dimensionless convention"
        )
        reduction = self._mapping(
            isolated["isolated_band_reduction"], "isolated reduction"
        )
        representatives = self._integers(
            reduction["hopping_representatives_cells"], "scalar representatives"
        )
        coefficients = self._complexes(
            reduction["hopping_coefficients"], "scalar hoppings"
        )
        if len(representatives) != len(coefficients):
            raise ValueError("scalar hopping arrays must agree")
        scalar = tuple(sorted(zip(representatives, coefficients, strict=True)))
        composite = self._mapping(
            cast(JsonValue, json.loads(composite_path.read_text(encoding="utf-8"))),
            "composite result",
        )
        groups = self._records(composite["groups"], "groups")
        matches = [
            group for group in groups if group["id"] == reference.composite_group_id
        ]
        if len(matches) != 1:
            raise ValueError("selected composite group must occur exactly once")
        hopping_records = self._records(
            matches[0]["smooth_hopping_blocks"], "smooth hopping blocks"
        )
        selected: list[tuple[int, ComplexMatrixTuple]] = []
        for record in hopping_records:
            representative = self._integer(
                record["representative_cells"], "representative_cells"
            )
            if abs(representative) <= reference.hopping_range:
                matrix = self._complex_matrix(record["matrix"], "hopping matrix")
                immutable = tuple(
                    tuple(complex(value) for value in row) for row in matrix
                )
                selected.append((representative, immutable))
        selected.sort(key=lambda item: item[0])
        expected_representatives = tuple(
            range(-reference.hopping_range, reference.hopping_range + 1)
        )
        if tuple(item[0] for item in selected) != expected_representatives:
            raise ValueError("composite hopping range is incomplete")
        composite_hoppings = tuple(selected)
        self._verify_hopping_hermiticity(composite_hoppings)
        return ParentData(
            period=self._real(convention["lattice_period"], "lattice period"),
            scalar_hoppings=scalar,
            composite_hoppings=composite_hoppings,
            source_identities=(
                (reference.isolated_path, reference.isolated_sha256),
                (reference.composite_path, reference.composite_sha256),
            ),
        )

    @staticmethod
    def _verify_hopping_hermiticity(
        hoppings: tuple[tuple[int, ComplexMatrixTuple], ...],
    ) -> None:
        values = {
            representative: np.asarray(matrix, dtype=np.complex128)
            for representative, matrix in hoppings
        }
        for representative, matrix in values.items():
            opposite = values[-representative]
            if not np.allclose(matrix, opposite.conj().T, rtol=0.0, atol=1.0e-12):
                raise ValueError("composite hopping blocks violate Hermiticity")

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _complexes(self, value: JsonValue, name: str) -> tuple[complex, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        result: list[complex] = []
        for pair in value:
            if not isinstance(pair, list) or len(pair) != 2:
                raise TypeError(f"{name} entries must be complex pairs")
            result.append(complex(self._real(pair[0], name), self._real(pair[1], name)))
        return tuple(result)

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be arrays")
            rows.append(list(self._complexes(row, name)))
        return np.asarray(rows, dtype=np.complex128)

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class OperatorCompatibilityAnalyzer:
    """Check every represented convention needed before direct subtraction."""

    __slots__ = ()

    def execute(
        self, reference: RepresentedOperator, candidate: RepresentedOperator
    ) -> CompatibilityResult:
        left = reference.basis
        right = candidate.basis
        fields = (
            ("STATE_SPACE", left.state_space_id, right.state_space_id),
            ("DIMENSION", left.dimension, right.dimension),
            ("CELL_COUNT", left.cell_count, right.cell_count),
            ("ORBITAL_COUNT", left.orbital_count, right.orbital_count),
            ("SPIN_COUNT", left.spin_count, right.spin_count),
            ("MOMENTUM", left.reduced_momentum, right.reduced_momentum),
            ("SITE_ORDER", left.site_ordering, right.site_ordering),
            ("ORBITAL_ORDER", left.orbital_ordering, right.orbital_ordering),
            ("SPIN_ORDER", left.spin_ordering, right.spin_ordering),
            ("COORDINATE_FRAME", left.coordinate_frame, right.coordinate_frame),
            ("ENERGY_UNIT", left.energy_unit, right.energy_unit),
            ("ENERGY_REFERENCE", left.energy_reference, right.energy_reference),
            ("GEOMETRY", left.geometry_id, right.geometry_id),
            ("SUBSPACE", left.subspace_id, right.subspace_id),
        )
        issues = tuple(
            sorted(
                f"DEFECT.COMPATIBILITY.{code}"
                for code, first, second in fields
                if first != second
            )
        )
        return CompatibilityResult("stopped" if issues else "compatible", issues)


class DefectResultSerializer:
    """Serialize one canonical retained result."""

    __slots__ = ()

    def execute(self, payload: dict[str, JsonValue]) -> bytes:
        serialized = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False)
        return (serialized + "\n").encode("utf-8")


class MatchedDefectExtractionExperiment:
    """Execute folding, extraction, finite-size, model, and observable controls."""

    __slots__ = ("_compatibility", "_serializer")

    def __init__(self) -> None:
        self._compatibility = OperatorCompatibilityAnalyzer()
        self._serializer = DefectResultSerializer()

    def execute(
        self,
        specification: DefectExerciseInput,
        parent: ParentData,
        input_path: Path,
        script_path: Path,
    ) -> bytes:
        folding = self._folding_control(specification, parent)
        extraction, model_hierarchy, stopping = self._extraction_controls(
            specification, parent
        )
        finite_size = self._finite_size_control(specification, parent)
        smoothness, smoothness_state = self._smoothness_control(specification, parent)
        metric_contrast = self._metric_contrast_control(specification, smoothness_state)
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
            "parent": {
                "period": parent.period,
                "composite_orbital_count": 2,
                "composite_hopping_range_cells": specification.parent.hopping_range,
                "source_identities": [
                    {"path": path, "sha256": digest}
                    for path, digest in parent.source_identities
                ],
                "role": (
                    "accepted periodic-1D represented parents reused as fixed "
                    "synthetic inputs"
                ),
            },
            "folding_control": folding,
            "extraction_controls": extraction,
            "model_class_hierarchy": model_hierarchy,
            "stopping_controls": stopping,
            "finite_size_control": finite_size,
            "smoothness_control": smoothness,
            "metric_contrast_control": metric_contrast,
            "error_accounting": {
                "parent_representation_and_reduction": (
                    "Inherited from the accepted periodic-1D records; this exercise "
                    "adds no parent-solver or parent-reduction validation."
                ),
                "folding_and_alignment": (
                    "Reported by map unitarity, folded block residuals, null "
                    "extraction, and planted-operator recovery defects."
                ),
                "finite_size": (
                    "Reported through defect-band width, center, bound-state count, "
                    "core restriction, exterior norm, and localization metrics."
                ),
                "model_optimization": (
                    "The frozen finite classes use closed-form orthogonal projections; "
                    "there is no iterative optimizer error."
                ),
                "model_class": (
                    "Reported by frozen classwise operator residuals and never "
                    "combined with extraction or optimization error."
                ),
                "observable": (
                    "Operator residual, binding-energy difference, bound-state count, "
                    "and state fidelity remain separate."
                ),
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "limitations": [
                "Every defect and comparison map is synthetic and known by "
                "construction.",
                "The periodic parents are accepted represented reductions, not "
                "material Hamiltonians.",
                "The parabolic comparator is band-limited on one fixed grid and "
                "does not establish a continuum crossover.",
                "No silicon, dopant, DFT, production Wannier, scientific-validation, "
                "or UQ claim is made.",
            ],
            "provenance": {
                "input_path": input_path.resolve()
                .relative_to(repository_root)
                .as_posix(),
                "input_sha256": self._sha256(input_path),
                "script_path": script_path.resolve()
                .relative_to(repository_root)
                .as_posix(),
                "script_sha256": self._sha256(script_path),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
        }
        return self._serializer.execute(payload)

    def _folding_control(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> list[JsonValue]:
        hoppings = self._composite_hoppings(parent)
        size = specification.folding.supercell_size
        records: list[JsonValue] = []
        for scaled_momentum in specification.folding.reduced_momentum_times_supercell:
            momentum = scaled_momentum / size
            supercell = self._supercell_hamiltonian(hoppings, size, momentum)
            folded_momenta = tuple(
                self._reduce_momentum(momentum + branch / size)
                for branch in range(size)
            )
            folding_map = self._folding_map(size, folded_momenta)
            target = np.zeros_like(supercell)
            for branch, primitive_momentum in enumerate(folded_momenta):
                target[
                    2 * branch : 2 * branch + 2,
                    2 * branch : 2 * branch + 2,
                ] = self._primitive_hamiltonian(hoppings, primitive_momentum)
            represented = folding_map.conj().T @ supercell @ folding_map
            block_mask = np.zeros_like(represented, dtype=bool)
            for branch in range(size):
                block_mask[
                    2 * branch : 2 * branch + 2,
                    2 * branch : 2 * branch + 2,
                ] = True
            records.append(
                {
                    "reduced_momentum": momentum,
                    "reduced_momentum_times_supercell": scaled_momentum,
                    "folded_primitive_momenta": list(folded_momenta),
                    "folding_map_sha256": self._matrix_sha256(folding_map),
                    "folding_map_unitarity_frobenius_defect": self._norm(
                        folding_map.conj().T @ folding_map - np.eye(2 * size)
                    ),
                    "folded_operator_frobenius_defect": self._norm(
                        represented - target
                    ),
                    "folded_off_block_frobenius_norm": self._norm(
                        np.where(block_mask, 0.0, represented)
                    ),
                    "eigenvalue_maximum_absolute_defect": self._eigenvalue_defect(
                        supercell, target
                    ),
                    "supercell_operator_sha256": self._matrix_sha256(supercell),
                    "folded_target_sha256": self._matrix_sha256(target),
                }
            )
        return records

    def _extraction_controls(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> tuple[list[JsonValue], list[JsonValue], list[JsonValue]]:
        control = specification.extraction
        size = control.supercell_size
        momentum = control.reduced_momentum_times_supercell / size
        hoppings = self._composite_hoppings(parent)
        pristine = self._supercell_hamiltonian(hoppings, size, momentum)
        spinless_basis = self._basis(size, 1, momentum, "canonical", "shared_zero")
        spin_basis = self._basis(size, 2, momentum, "canonical", "shared_zero")
        pristine_spin: ComplexMatrix = np.asarray(
            np.kron(pristine, np.eye(2, dtype=np.complex128)), dtype=np.complex128
        )
        defects = self._planted_defects(control, size)
        records: list[JsonValue] = []
        model_records: list[JsonValue] = []
        null = np.zeros_like(pristine)
        null_record = self._extraction_record(
            "null",
            pristine,
            null,
            spinless_basis,
            specification,
        )
        records.append(null_record)
        for identifier in (
            "scalar-onsite",
            "orbital-onsite",
            "nearest-neighbor",
            "range-two-nonlocal",
        ):
            defect = defects[identifier]
            record = self._extraction_record(
                identifier,
                pristine,
                defect,
                spinless_basis,
                specification,
            )
            records.append(record)
            model_records.append(
                self._spinless_model_hierarchy(identifier, defect, size, specification)
            )
        for identifier in ("collinear-spin", "spin-mixing"):
            defect = defects[identifier]
            record = self._extraction_record(
                identifier,
                pristine_spin,
                defect,
                spin_basis,
                specification,
            )
            records.append(record)
            model_records.append(
                self._spin_model_hierarchy(identifier, defect, size, specification)
            )
        stopping = self._stopping_controls(pristine, spinless_basis)
        return records, model_records, stopping

    def _extraction_record(
        self,
        identifier: str,
        pristine: ComplexMatrix,
        defect: ComplexMatrix,
        canonical_basis: SupercellBasis,
        specification: DefectExerciseInput,
    ) -> dict[str, JsonValue]:
        spin_count = canonical_basis.spin_count
        coordinate_map = self._alignment_map(
            canonical_basis.cell_count,
            canonical_basis.reduced_momentum,
            spin_count,
            specification.alignment,
        )
        shift = specification.alignment.energy_shift
        raw = coordinate_map @ (
            pristine + defect
        ) @ coordinate_map.conj().T + shift * np.eye(pristine.shape[0])
        aligned_hamiltonian = (
            coordinate_map.conj().T
            @ (raw - shift * np.eye(raw.shape[0]))
            @ coordinate_map
        )
        extracted = aligned_hamiltonian - pristine
        uncorrected = coordinate_map.conj().T @ raw @ coordinate_map - pristine
        raw_basis = SupercellBasis(
            state_space_id=canonical_basis.state_space_id,
            cell_count=canonical_basis.cell_count,
            orbital_count=canonical_basis.orbital_count,
            spin_count=canonical_basis.spin_count,
            reduced_momentum=canonical_basis.reduced_momentum,
            site_ordering="translated-cyclic",
            orbital_ordering="rotated-and-phased",
            spin_ordering=(
                "rotated-spin-frame" if spin_count == 2 else "not-applicable"
            ),
            coordinate_frame="scrambled-known-map",
            energy_unit=canonical_basis.energy_unit,
            energy_reference="shifted_raw_zero",
            geometry_id=canonical_basis.geometry_id,
            subspace_id=canonical_basis.subspace_id,
        )
        pristine_record = RepresentedOperator("pristine", canonical_basis, pristine)
        raw_record = RepresentedOperator("raw-defect", raw_basis, raw)
        compatibility = self._compatibility.execute(pristine_record, raw_record)
        core_projector = self._site_projector(
            canonical_basis.cell_count,
            canonical_basis.orbital_count * spin_count,
            (0,),
        )
        exterior = np.eye(pristine.shape[0]) - core_projector
        false_offset = uncorrected - defect
        return {
            "id": identifier,
            "spin_count": spin_count,
            "dimension": pristine.shape[0],
            "planted_operator_sha256": self._matrix_sha256(defect),
            "raw_operator_sha256": self._matrix_sha256(raw),
            "alignment_map_sha256": self._matrix_sha256(coordinate_map),
            "extracted_operator_sha256": self._matrix_sha256(extracted),
            "alignment_map_unitarity_frobenius_defect": self._norm(
                coordinate_map.conj().T @ coordinate_map - np.eye(pristine.shape[0])
            ),
            "direct_comparison_status": compatibility.status,
            "direct_comparison_issue_codes": list(compatibility.issue_codes),
            "raw_coordinate_difference_frobenius_not_interpreted": self._norm(
                raw - pristine
            ),
            "aligned_extraction_frobenius_defect": self._norm(extracted - defect),
            "aligned_extraction_maximum_absolute_defect": self._maximum(
                extracted - defect
            ),
            "extracted_hermiticity_maximum_absolute_residual": self._maximum(
                extracted - extracted.conj().T
            ),
            "declared_energy_reference_shift": shift,
            "uncorrected_false_offset_frobenius_norm": self._norm(false_offset),
            "uncorrected_false_offset_exterior_frobenius_norm": self._norm(
                exterior @ false_offset @ exterior
            ),
            "corrected_exterior_frobenius_norm": self._norm(
                exterior @ extracted @ exterior
            ),
            "corrected_cross_coupling_frobenius_norm": float(
                np.sqrt(
                    self._norm(core_projector @ extracted @ exterior) ** 2
                    + self._norm(exterior @ extracted @ core_projector) ** 2
                )
            ),
            "compact_planted_blocks": self._compact_blocks(
                defect,
                canonical_basis.cell_count,
                canonical_basis.orbital_count * spin_count,
            ),
            "alignment_parameters": {
                "translation_cells": specification.alignment.translation_cells,
                "orbital_permutation": list(
                    specification.alignment.orbital_permutation
                ),
                "orbital_rotation_angle_radians": (
                    specification.alignment.orbital_rotation_angle
                ),
                "orbital_phases_radians": list(specification.alignment.orbital_phases),
                "site_phase_step_radians": specification.alignment.site_phase_step,
                "spin_rotation_axis": list(specification.alignment.spin_axis),
                "spin_rotation_angle_radians": (
                    specification.alignment.spin_rotation_angle
                ),
            },
        }

    def _planted_defects(
        self, control: ExtractionControl, size: int
    ) -> dict[str, ComplexMatrix]:
        dimension = 2 * size
        scalar = np.zeros((dimension, dimension), dtype=np.complex128)
        scalar[:2, :2] = control.scalar_onsite_strength * np.eye(2)
        orbital = np.zeros_like(scalar)
        orbital[:2, :2] = np.asarray(control.orbital_onsite, dtype=np.complex128)
        nearest = np.zeros_like(scalar)
        nearest_block = np.asarray(control.nearest_neighbor, dtype=np.complex128)
        nearest[:2, 2:4] = nearest_block
        nearest[2:4, :2] = nearest_block.conj().T
        range_two = np.zeros_like(scalar)
        range_two_block = np.asarray(control.range_two, dtype=np.complex128)
        range_two[:2, 4:6] = range_two_block
        range_two[4:6, :2] = range_two_block.conj().T
        identity_spin = np.eye(2, dtype=np.complex128)
        pauli_x, pauli_y, pauli_z = self._pauli()
        collinear = np.zeros((2 * dimension, 2 * dimension), dtype=np.complex128)
        collinear[:4, :4] = np.kron(
            np.asarray(control.collinear_independent, dtype=np.complex128),
            identity_spin,
        ) + np.kron(
            np.asarray(control.collinear_splitting, dtype=np.complex128),
            pauli_z,
        )
        spin_mixing = np.zeros_like(collinear)
        spin_mixing[:4, :4] = np.kron(
            np.asarray(control.collinear_independent, dtype=np.complex128),
            identity_spin,
        )
        for block, pauli in zip(
            (control.spin_x, control.spin_y, control.spin_z),
            (pauli_x, pauli_y, pauli_z),
            strict=True,
        ):
            spin_mixing[:4, :4] += np.kron(
                np.asarray(block, dtype=np.complex128), pauli
            )
        return {
            "scalar-onsite": scalar,
            "orbital-onsite": orbital,
            "nearest-neighbor": nearest,
            "range-two-nonlocal": range_two,
            "collinear-spin": collinear,
            "spin-mixing": spin_mixing,
        }

    def _spinless_model_hierarchy(
        self,
        identifier: str,
        defect: ComplexMatrix,
        size: int,
        specification: DefectExerciseInput,
    ) -> dict[str, JsonValue]:
        central = defect[:2, :2]
        scalar = np.zeros_like(defect)
        scalar[:2, :2] = 0.5 * np.trace(central) * np.eye(2)
        orbital = np.zeros_like(defect)
        orbital[:2, :2] = central
        range_one = orbital.copy()
        range_two = orbital.copy()
        for site in range(1, size):
            distance = min(site, size - site)
            block = defect[:2, 2 * site : 2 * site + 2]
            reverse = defect[2 * site : 2 * site + 2, :2]
            if distance <= 1:
                range_one[:2, 2 * site : 2 * site + 2] = block
                range_one[2 * site : 2 * site + 2, :2] = reverse
            if distance <= 2:
                range_two[:2, 2 * site : 2 * site + 2] = block
                range_two[2 * site : 2 * site + 2, :2] = reverse
        classes = (
            ("scalar-onsite", scalar),
            ("orbital-onsite", orbital),
            ("range-1-nonlocal", range_one),
            ("range-2-nonlocal", range_two),
        )
        records: list[JsonValue] = []
        first_adequate: str | None = None
        for class_id, model in classes:
            residual = self._norm(defect - model)
            if first_adequate is None and residual <= specification.algebraic_tolerance:
                first_adequate = class_id
            records.append(
                {
                    "class_id": class_id,
                    "absolute_frobenius_residual": residual,
                    "relative_frobenius_residual": self._relative_norm(
                        defect - model, defect
                    ),
                    "model_operator_sha256": self._matrix_sha256(model),
                }
            )
        return {
            "defect_id": identifier,
            "hierarchy": records,
            "first_adequate_class": first_adequate,
        }

    def _spin_model_hierarchy(
        self,
        identifier: str,
        defect: ComplexMatrix,
        size: int,
        specification: DefectExerciseInput,
    ) -> dict[str, JsonValue]:
        block = defect[:4, :4].reshape(2, 2, 2, 2)
        pauli_x, pauli_y, pauli_z = self._pauli()
        identity = np.eye(2, dtype=np.complex128)
        spin_matrices = (identity, pauli_x, pauli_y, pauli_z)
        coefficients: list[ComplexMatrix] = []
        for spin_matrix in spin_matrices:
            coefficient = np.zeros((2, 2), dtype=np.complex128)
            for first in range(2):
                for second in range(2):
                    coefficient += (
                        0.5 * spin_matrix[second, first] * block[:, first, :, second]
                    )
            coefficients.append(coefficient)
        independent_block = np.kron(coefficients[0], identity)
        collinear_block = independent_block + np.kron(coefficients[3], pauli_z)
        spinor_block = sum(
            (
                np.kron(coefficient, spin_matrix)
                for coefficient, spin_matrix in zip(
                    coefficients, spin_matrices, strict=True
                )
            ),
            start=np.zeros((4, 4), dtype=np.complex128),
        )
        classes: list[tuple[str, ComplexMatrix]] = []
        for class_id, central_block in (
            ("spin-independent-onsite", independent_block),
            ("collinear-onsite", collinear_block),
            ("spinor-onsite", spinor_block),
        ):
            model = np.zeros((4 * size, 4 * size), dtype=np.complex128)
            model[:4, :4] = central_block
            classes.append((class_id, model))
        records: list[JsonValue] = []
        first_adequate: str | None = None
        for class_id, model in classes:
            residual = self._norm(defect - model)
            if first_adequate is None and residual <= specification.algebraic_tolerance:
                first_adequate = class_id
            records.append(
                {
                    "class_id": class_id,
                    "absolute_frobenius_residual": residual,
                    "relative_frobenius_residual": self._relative_norm(
                        defect - model, defect
                    ),
                    "model_operator_sha256": self._matrix_sha256(model),
                }
            )
        return {
            "defect_id": identifier,
            "hierarchy": records,
            "first_adequate_class": first_adequate,
        }

    def _stopping_controls(
        self, pristine: ComplexMatrix, canonical_basis: SupercellBasis
    ) -> list[JsonValue]:
        reference = RepresentedOperator("reference", canonical_basis, pristine)
        variants: tuple[tuple[str, SupercellBasis, ComplexMatrix], ...] = (
            (
                "unequal-retained-rank",
                self._basis_variant(canonical_basis, orbital_count=3),
                np.zeros(
                    (
                        canonical_basis.cell_count * 3,
                        canonical_basis.cell_count * 3,
                    ),
                    dtype=np.complex128,
                ),
            ),
            (
                "mismatched-spin-space",
                self._basis_variant(canonical_basis, spin_count=2),
                np.asarray(
                    np.kron(pristine, np.eye(2, dtype=np.complex128)),
                    dtype=np.complex128,
                ),
            ),
            (
                "incorrect-supercell-shape",
                self._basis_variant(canonical_basis, geometry_id="wrong-length"),
                pristine,
            ),
            (
                "lost-site-correspondence",
                self._basis_variant(canonical_basis, site_ordering="unknown-sites"),
                pristine,
            ),
            (
                "incompatible-retained-subspace",
                self._basis_variant(canonical_basis, subspace_id="orthogonal-subspace"),
                pristine,
            ),
            (
                "different-energy-reference",
                self._basis_variant(canonical_basis, energy_reference="unknown-zero"),
                pristine,
            ),
        )
        records: list[JsonValue] = []
        for identifier, basis, matrix in variants:
            candidate = RepresentedOperator(identifier, basis, matrix)
            result = self._compatibility.execute(reference, candidate)
            records.append(
                {
                    "id": identifier,
                    "status": result.status,
                    "issue_codes": list(result.issue_codes),
                    "residual": None,
                    "retained_subspace_minimum_singular_overlap": (
                        0.0 if identifier == "incompatible-retained-subspace" else None
                    ),
                    "retained_subspace_maximum_principal_angle_radians": (
                        float(np.pi / 2.0)
                        if identifier == "incompatible-retained-subspace"
                        else None
                    ),
                }
            )
        return records

    def _finite_size_control(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> dict[str, JsonValue]:
        control = specification.finite_size
        hoppings = self._composite_hoppings(parent)
        orbital_block = np.asarray(control.orbital_block, dtype=np.complex128)
        host_edge = self._host_edge(hoppings)
        reference_size = control.supercell_sizes[-1]
        reference_defect = self._gaussian_defect(
            reference_size,
            control.gaussian_width,
            control.gaussian_strength,
            orbital_block,
        )
        reference_core = self._core_restriction(
            reference_defect, reference_size, control.core_radius, 2
        )
        records: list[JsonValue] = []
        scaled_momenta = (
            np.arange(control.momentum_mesh_size, dtype=np.float64)
            - control.momentum_mesh_size // 2
        ) / control.momentum_mesh_size
        for size in control.supercell_sizes:
            defect = self._gaussian_defect(
                size,
                control.gaussian_width,
                control.gaussian_strength,
                orbital_block,
            )
            core = self._core_restriction(defect, size, control.core_radius, 2)
            core_projector = self._site_projector(
                size,
                2,
                tuple(
                    index
                    for index, coordinate in enumerate(self._coordinates(size))
                    if abs(coordinate) <= control.core_radius
                ),
            )
            exterior = np.eye(2 * size) - core_projector
            energies: list[float] = []
            for scaled_momentum in scaled_momenta:
                momentum = float(scaled_momentum) / size
                hamiltonian = (
                    self._supercell_hamiltonian(hoppings, size, momentum) + defect
                )
                energies.append(float(np.linalg.eigvalsh(hamiltonian)[0]))
            zero_hamiltonian = self._supercell_hamiltonian(hoppings, size, 0.0) + defect
            zero_values, zero_vectors = np.linalg.eigh(zero_hamiltonian)
            bound_count = int(
                np.sum(
                    zero_values < host_edge - specification.bound_threshold_tolerance
                )
            )
            probability = np.sum(
                np.abs(zero_vectors[:, 0].reshape(size, 2)) ** 2, axis=1
            )
            coordinates = self._coordinates(size).astype(np.float64)
            records.append(
                {
                    "supercell_size": size,
                    "defect_operator_sha256": self._matrix_sha256(defect),
                    "core_restriction_frobenius_defect_from_largest": self._norm(
                        core - reference_core
                    ),
                    "exterior_frobenius_norm": self._norm(exterior @ defect @ exterior),
                    "cross_coupling_frobenius_norm": float(
                        np.sqrt(
                            self._norm(core_projector @ defect @ exterior) ** 2
                            + self._norm(exterior @ defect @ core_projector) ** 2
                        )
                    ),
                    "host_lower_band_edge": host_edge,
                    "lowest_defect_band_center": float(np.mean(energies)),
                    "lowest_defect_band_minimum": min(energies),
                    "lowest_defect_band_maximum": max(energies),
                    "lowest_defect_band_width": float(np.ptp(energies)),
                    "center_binding_relative_to_host_edge": host_edge
                    - float(np.mean(energies)),
                    "bound_state_count_at_zero_momentum": bound_count,
                    "lowest_state_inverse_participation_ratio": float(
                        np.sum(probability**2)
                    ),
                    "lowest_state_core_probability": float(
                        np.sum(probability[np.abs(coordinates) <= control.core_radius])
                    ),
                    "lowest_state_rms_radius_cells": float(
                        np.sqrt(np.sum(probability * coordinates**2))
                    ),
                }
            )
        return {
            "profile": {
                "family": "fixed-peak Gaussian onsite",
                "width_cells": control.gaussian_width,
                "strength": control.gaussian_strength,
                "orbital_block": [list(row) for row in control.orbital_block],
                "core_radius_cells": control.core_radius,
            },
            "records": records,
        }

    def _smoothness_control(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> tuple[
        dict[str, JsonValue], tuple[ComplexMatrix, ComplexMatrix, float, RealVector]
    ]:
        control = specification.smoothness
        size = control.supercell_size
        representatives = np.asarray(
            [value[0] for value in parent.scalar_hoppings], dtype=np.int64
        )
        hoppings = np.asarray(
            [value[1] for value in parent.scalar_hoppings], dtype=np.complex128
        )
        coordinates = self._coordinates(size).astype(np.float64)
        momenta = np.fft.fftfreq(size)
        fourier = np.exp(
            2j * np.pi * np.outer(np.arange(size, dtype=np.float64), momenta)
        ) / np.sqrt(size)
        lattice_energies = np.asarray(
            [
                np.sum(hoppings * np.exp(2j * np.pi * momentum * representatives)).real
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        edge = float(np.sum(hoppings).real)
        curvature = float(
            0.5 * np.sum(-np.square(2.0 * np.pi * representatives) * hoppings).real
        )
        if curvature <= 0.0:
            raise ValueError("accepted scalar parent must have positive edge curvature")
        continuum_energies = edge + curvature * np.square(momenta)
        lattice_parent = fourier @ np.diag(lattice_energies) @ fourier.conj().T
        continuum_parent = fourier @ np.diag(continuum_energies) @ fourier.conj().T
        families: list[JsonValue] = []
        contrast_profile = np.zeros(size, dtype=np.float64)
        for family in ("fixed-peak", "fixed-integrated"):
            records: list[JsonValue] = []
            for width in control.widths:
                gaussian = np.exp(-np.square(coordinates) / (2.0 * width**2))
                if family == "fixed-peak":
                    profile = control.fixed_peak_strength * gaussian
                else:
                    profile = (
                        control.fixed_integrated_strength
                        / (np.sqrt(2.0 * np.pi) * width)
                        * gaussian
                    )
                lattice_values, lattice_vectors = np.linalg.eigh(
                    lattice_parent + np.diag(profile)
                )
                continuum_values, continuum_vectors = np.linalg.eigh(
                    continuum_parent + np.diag(profile)
                )
                lattice_state = lattice_vectors[:, 0]
                continuum_state = continuum_vectors[:, 0]
                momentum_amplitudes = fourier.conj().T @ lattice_state
                records.append(
                    {
                        "width_cells": width,
                        "profile_peak_magnitude": float(np.max(np.abs(profile))),
                        "profile_discrete_integrated_magnitude": float(
                            abs(np.sum(profile))
                        ),
                        "lattice_binding_energy": edge - float(lattice_values[0]),
                        "parabolic_binding_energy": edge - float(continuum_values[0]),
                        "parabolic_minus_lattice_binding_error": float(
                            lattice_values[0] - continuum_values[0]
                        ),
                        "state_fidelity": float(
                            abs(np.vdot(lattice_state, continuum_state)) ** 2
                        ),
                        "lattice_bound_state_count": int(
                            np.sum(
                                lattice_values
                                < edge - specification.bound_threshold_tolerance
                            )
                        ),
                        "parabolic_bound_state_count": int(
                            np.sum(
                                continuum_values
                                < edge - specification.bound_threshold_tolerance
                            )
                        ),
                        "lattice_high_momentum_weight": float(
                            np.sum(
                                np.abs(momentum_amplitudes[np.abs(momenta) > 0.25]) ** 2
                            )
                        ),
                        "lattice_state_rms_radius_cells": self._state_rms_radius(
                            lattice_state, coordinates
                        ),
                        "parabolic_state_rms_radius_cells": self._state_rms_radius(
                            continuum_state, coordinates
                        ),
                    }
                )
                if (
                    family == specification.metric_contrast.profile_family
                    and width == specification.metric_contrast.width
                ):
                    contrast_profile = profile.copy()
            families.append({"family": family, "records": records})
        if not np.any(contrast_profile):
            raise ValueError("metric contrast profile was not selected by the scan")
        result: dict[str, JsonValue] = {
            "supercell_size": size,
            "parent_lower_edge": edge,
            "parabolic_curvature": curvature,
            "parabolic_mass_parameter_inverse_twice_curvature": (
                1.0 / (2.0 * curvature)
            ),
            "lattice_parent_sha256": self._matrix_sha256(lattice_parent),
            "parabolic_parent_sha256": self._matrix_sha256(continuum_parent),
            "families": families,
            "interpretation": (
                "The parabolic comparator improves with profile width in the "
                "retained scan, but one fixed band-limited grid does not establish "
                "a continuum crossover."
            ),
        }
        return result, (lattice_parent, continuum_parent, edge, contrast_profile)

    def _metric_contrast_control(
        self,
        specification: DefectExerciseInput,
        smoothness_state: tuple[ComplexMatrix, ComplexMatrix, float, RealVector],
    ) -> dict[str, JsonValue]:
        lattice_parent, _, edge, profile = smoothness_state
        reference_impurity = np.diag(profile).astype(np.complex128)
        reference_hamiltonian = lattice_parent + reference_impurity
        values, vectors = np.linalg.eigh(reference_hamiltonian)
        bound_count = int(
            np.sum(values < edge - specification.bound_threshold_tolerance)
        )
        if bound_count < 1 or bound_count >= values.size:
            raise ValueError("metric contrast requires bound and unbound states")
        bound_state = vectors[:, 0]
        reference_binding = edge - float(values[0])
        high_state = vectors[:, -1]
        large_strength = specification.metric_contrast.excited_residual_strength
        large_model = reference_impurity + large_strength * np.outer(
            high_state, high_state.conj()
        )
        large_values, large_vectors = np.linalg.eigh(lattice_parent + large_model)
        first_unbound = vectors[:, bound_count]
        spectral_gap = float(values[bound_count] - values[0])
        coupling = specification.metric_contrast.coupling_to_gap_ratio * spectral_gap
        small_model = reference_impurity + coupling * (
            np.outer(bound_state, first_unbound.conj())
            + np.outer(first_unbound, bound_state.conj())
        )
        small_values, small_vectors = np.linalg.eigh(lattice_parent + small_model)
        cases = (
            (
                "large-operator-residual-excited-sector",
                large_model,
                large_values,
                large_vectors,
            ),
            (
                "small-global-residual-bound-continuum-coupling",
                small_model,
                small_values,
                small_vectors,
            ),
        )
        records: list[JsonValue] = []
        for identifier, model, model_values, model_vectors in cases:
            residual = self._norm(model - reference_impurity)
            binding = edge - float(model_values[0])
            records.append(
                {
                    "id": identifier,
                    "operator_frobenius_residual": residual,
                    "operator_residual_relative_to_full_reference_hamiltonian": (
                        residual / self._norm(reference_hamiltonian)
                    ),
                    "binding_energy": binding,
                    "binding_energy_error": binding - reference_binding,
                    "lowest_state_fidelity": float(
                        abs(np.vdot(bound_state, model_vectors[:, 0])) ** 2
                    ),
                    "bound_state_count": int(
                        np.sum(
                            model_values
                            < edge - specification.bound_threshold_tolerance
                        )
                    ),
                    "model_operator_sha256": self._matrix_sha256(model),
                }
            )
        return {
            "reference": {
                "profile_family": specification.metric_contrast.profile_family,
                "width_cells": specification.metric_contrast.width,
                "binding_energy": reference_binding,
                "bound_state_count": bound_count,
                "impurity_operator_sha256": self._matrix_sha256(reference_impurity),
            },
            "construction": {
                "excited_state_residual_strength": large_strength,
                "bound_to_first_unbound_spectral_gap": spectral_gap,
                "bound_continuum_coupling": coupling,
                "coupling_to_gap_ratio": (
                    specification.metric_contrast.coupling_to_gap_ratio
                ),
            },
            "cases": records,
        }

    @staticmethod
    def _composite_hoppings(
        parent: ParentData,
    ) -> tuple[tuple[int, ComplexMatrix], ...]:
        return tuple(
            (representative, np.asarray(matrix, dtype=np.complex128))
            for representative, matrix in parent.composite_hoppings
        )

    @staticmethod
    def _primitive_hamiltonian(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], momentum: float
    ) -> ComplexMatrix:
        result = np.zeros((2, 2), dtype=np.complex128)
        for representative, block in hoppings:
            result += np.exp(2j * np.pi * momentum * representative) * block
        return result

    @staticmethod
    def _supercell_hamiltonian(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        size: int,
        momentum: float,
    ) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for source in range(size):
            for representative, block in hoppings:
                raw_target = source + representative
                target = raw_target % size
                crossings = (raw_target - target) // size
                phase = np.exp(2j * np.pi * momentum * size * crossings)
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += phase * block
        return result

    @staticmethod
    def _folding_map(size: int, momenta: tuple[float, ...]) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        identity = np.eye(2, dtype=np.complex128)
        for branch, momentum in enumerate(momenta):
            for site in range(size):
                result[
                    2 * site : 2 * site + 2,
                    2 * branch : 2 * branch + 2,
                ] = np.exp(2j * np.pi * momentum * site) / np.sqrt(size) * identity
        return result

    def _alignment_map(
        self,
        size: int,
        momentum: float,
        spin_count: int,
        control: AlignmentControl,
    ) -> ComplexMatrix:
        translation = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            raw_target = source + control.translation_cells
            target = raw_target % size
            crossings = (raw_target - target) // size
            translation[target, source] = np.exp(
                2j * np.pi * momentum * size * crossings
            )
        cosine = np.cos(control.orbital_rotation_angle)
        sine = np.sin(control.orbital_rotation_angle)
        orbital_rotation = np.asarray(
            [[cosine, -sine], [sine, cosine]], dtype=np.complex128
        )
        orbital_phases = np.diag(np.exp(1j * np.asarray(control.orbital_phases)))
        orbital_permutation = np.eye(2, dtype=np.complex128)[
            np.asarray(control.orbital_permutation, dtype=np.int64)
        ]
        site_orbital: ComplexMatrix = np.asarray(
            np.kron(
                translation,
                orbital_phases @ orbital_permutation @ orbital_rotation,
            ),
            dtype=np.complex128,
        )
        phases = np.empty(2 * size, dtype=np.complex128)
        for site in range(size):
            for orbital in range(2):
                phases[2 * site + orbital] = np.exp(
                    1j * control.site_phase_step * (site + 0.5 * orbital)
                )
        site_orbital = np.diag(phases) @ site_orbital
        if spin_count == 1:
            return site_orbital
        axis = np.asarray(control.spin_axis, dtype=np.float64)
        axis /= np.linalg.norm(axis)
        pauli_x, pauli_y, pauli_z = self._pauli()
        generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
        spin_rotation = (
            np.cos(control.spin_rotation_angle / 2.0) * np.eye(2)
            - 1j * np.sin(control.spin_rotation_angle / 2.0) * generator
        )
        return np.asarray(np.kron(site_orbital, spin_rotation), dtype=np.complex128)

    @staticmethod
    def _basis(
        size: int,
        spin_count: int,
        momentum: float,
        frame: str,
        energy_reference: str,
    ) -> SupercellBasis:
        return SupercellBasis(
            state_space_id=(
                "low-pair-orbital-supercell"
                if spin_count == 1
                else "low-pair-orbital-supercell-x-spin-half"
            ),
            cell_count=size,
            orbital_count=2,
            spin_count=spin_count,
            reduced_momentum=momentum,
            site_ordering="canonical-cyclic-sites",
            orbital_ordering="low-pair-smooth-frame",
            spin_ordering=("not-applicable" if spin_count == 1 else "up-down-fast"),
            coordinate_frame=frame,
            energy_unit="E_G",
            energy_reference=energy_reference,
            geometry_id=f"one-dimensional-supercell-{size}",
            subspace_id="accepted-low-pair-composite",
        )

    @staticmethod
    def _basis_variant(
        basis: SupercellBasis,
        *,
        orbital_count: int | None = None,
        spin_count: int | None = None,
        geometry_id: str | None = None,
        site_ordering: str | None = None,
        subspace_id: str | None = None,
        energy_reference: str | None = None,
    ) -> SupercellBasis:
        return SupercellBasis(
            state_space_id=basis.state_space_id,
            cell_count=basis.cell_count,
            orbital_count=(
                basis.orbital_count if orbital_count is None else orbital_count
            ),
            spin_count=basis.spin_count if spin_count is None else spin_count,
            reduced_momentum=basis.reduced_momentum,
            site_ordering=(
                basis.site_ordering if site_ordering is None else site_ordering
            ),
            orbital_ordering=basis.orbital_ordering,
            spin_ordering=basis.spin_ordering,
            coordinate_frame=basis.coordinate_frame,
            energy_unit=basis.energy_unit,
            energy_reference=(
                basis.energy_reference if energy_reference is None else energy_reference
            ),
            geometry_id=basis.geometry_id if geometry_id is None else geometry_id,
            subspace_id=basis.subspace_id if subspace_id is None else subspace_id,
        )

    @staticmethod
    def _gaussian_defect(
        size: int, width: float, strength: float, orbital_block: ComplexMatrix
    ) -> ComplexMatrix:
        coordinates = MatchedDefectExtractionExperiment._coordinates(size)
        profile = strength * np.exp(-np.square(coordinates) / (2.0 * width**2))
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for site, value in enumerate(profile):
            result[2 * site : 2 * site + 2, 2 * site : 2 * site + 2] = (
                value * orbital_block
            )
        return result

    @staticmethod
    def _coordinates(size: int) -> npt.NDArray[np.int64]:
        values = np.arange(size, dtype=np.int64)
        return np.where(values <= size // 2, values, values - size)

    @staticmethod
    def _site_projector(
        size: int, block_size: int, sites: tuple[int, ...]
    ) -> ComplexMatrix:
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for site in sites:
            begin = block_size * site
            result[begin : begin + block_size, begin : begin + block_size] = np.eye(
                block_size
            )
        return result

    @staticmethod
    def _core_restriction(
        matrix: ComplexMatrix, size: int, radius: int, block_size: int
    ) -> ComplexMatrix:
        coordinates = MatchedDefectExtractionExperiment._coordinates(size)
        ordered_sites = tuple(
            int(np.flatnonzero(coordinates == coordinate)[0])
            for coordinate in range(-radius, radius + 1)
        )
        indices = np.asarray(
            [
                block_size * site + internal
                for site in ordered_sites
                for internal in range(block_size)
            ],
            dtype=np.int64,
        )
        return matrix[np.ix_(indices, indices)]

    @staticmethod
    def _compact_blocks(
        matrix: ComplexMatrix, size: int, block_size: int
    ) -> list[JsonValue]:
        records: list[JsonValue] = []
        for first in range(size):
            for second in range(size):
                block = matrix[
                    block_size * first : block_size * (first + 1),
                    block_size * second : block_size * (second + 1),
                ]
                if np.any(block != 0.0):
                    records.append(
                        {
                            "row_site": first,
                            "column_site": second,
                            "matrix": (
                                MatchedDefectExtractionExperiment._complex_matrix_json(
                                    block
                                )
                            ),
                        }
                    )
        return records

    @staticmethod
    def _complex_matrix_json(matrix: ComplexMatrix) -> list[JsonValue]:
        return [
            [[float(value.real), float(value.imag)] for value in row] for row in matrix
        ]

    @staticmethod
    def _host_edge(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
    ) -> float:
        momenta = np.linspace(-0.5, 0.5, 4096, endpoint=False)
        return min(
            float(
                np.linalg.eigvalsh(
                    MatchedDefectExtractionExperiment._primitive_hamiltonian(
                        hoppings, momentum
                    )
                )[0]
            )
            for momentum in momenta
        )

    @staticmethod
    def _state_rms_radius(state: ComplexVector, coordinates: RealVector) -> float:
        probabilities = np.abs(state) ** 2
        return float(np.sqrt(np.sum(probabilities * np.square(coordinates))))

    @staticmethod
    def _reduce_momentum(momentum: float) -> float:
        return float((momentum + 0.5) % 1.0 - 0.5)

    @staticmethod
    def _pauli() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        return (
            np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128),
            np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128),
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
        )

    @staticmethod
    def _relative_norm(difference: ComplexMatrix, reference: ComplexMatrix) -> float:
        scale = float(np.linalg.norm(reference))
        if scale == 0.0:
            return 0.0 if np.linalg.norm(difference) == 0.0 else float("inf")
        return float(np.linalg.norm(difference) / scale)

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        return float(np.linalg.norm(matrix))

    @staticmethod
    def _maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix)))

    @staticmethod
    def _eigenvalue_defect(first: ComplexMatrix, second: ComplexMatrix) -> float:
        return float(
            np.max(np.abs(np.linalg.eigvalsh(first) - np.linalg.eigvalsh(second)))
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt command-line paths into the owned experiment action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = arguments.input.resolve()
    output_path = arguments.output.resolve()
    specification = DefectExerciseInputDeserializer().execute(input_path.read_bytes())
    repository_root = Path(__file__).resolve().parents[3]
    parent = ParentDataLoader().execute(specification.parent, repository_root)
    output_path.write_bytes(
        MatchedDefectExtractionExperiment().execute(
            specification, parent, input_path, Path(__file__).resolve()
        )
    )


if __name__ == "__main__":
    main()
