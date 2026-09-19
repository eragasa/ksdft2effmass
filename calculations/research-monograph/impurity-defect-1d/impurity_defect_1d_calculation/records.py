"""Defect-1D records ownership."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np

from .model import (
    AlignmentControl,
    ComplexMatrix,
    ComplexMatrixTuple,
    DefectExerciseInput,
    ExtractionControl,
    FiniteSizeControl,
    FoldingControl,
    JsonValue,
    MetricContrastControl,
    ParentData,
    ParentSourceReference,
    RealMatrixTuple,
    SmoothnessControl,
)


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


class DefectResultSerializer:
    """Serialize one canonical retained result."""

    __slots__ = ()

    def execute(self, payload: dict[str, JsonValue]) -> bytes:
        serialized = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False)
        return (serialized + "\n").encode("utf-8")
