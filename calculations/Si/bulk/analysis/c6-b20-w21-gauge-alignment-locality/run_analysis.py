from __future__ import annotations

import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric

from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.field_geometry import (
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.policy import (
    Periodic3DRankNBandEquivalenceHoppingLocalityPolicy,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    Periodic3DRankNFittedAlignmentEvidence,
    Periodic3DRankNPrescribedAlignmentEvidence,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.wannier_fields import (
    Periodic3DRankNWannierFieldProducer,
    Periodic3DRankNWannierFieldSource,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.attack import (
    Periodic3DRankNGaugeNormalizationEnum,
    Periodic3DRankNGivensGaugeAttack,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)

RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
REPOSITORY = ROOT.parents[4]
REQUEST = ROOT / "request.json"
OUTPUT = ROOT / "result.json"
HARTREE_TO_EV = 27.211386245988
ASSURANCE_LABEL = "producer-checked-development-analysis-not-independently-verified"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path) -> JsonObject:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def mapping(value: JsonValue, name: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a mapping")
    return value


def values(value: JsonValue, name: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    return value


def numeric(value: JsonValue, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    return float(value)


def string(value: JsonValue, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{name} must be a nonempty string")
    return value


def source_path(declaration: JsonObject, name: str) -> Path:
    path = Path(string(declaration["path"], f"{name} path"))
    return path if path.is_absolute() else REPOSITORY / path


def authenticate_request_sources(request: JsonObject) -> JsonObject:
    authenticated: JsonObject = {}
    for label, declaration_value in mapping(request["sources"], "sources").items():
        declaration = mapping(declaration_value, f"source {label}")
        path = source_path(declaration, f"source {label}")
        expected_size = int(numeric(declaration["byte_size"], f"source {label} size"))
        expected_digest = string(declaration["sha256"], f"source {label} digest")
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"source is absent or is a symlink: {path}")
        observed = identity(path)
        if observed["byte_size"] != expected_size or observed["sha256"] != expected_digest:
            raise RuntimeError(f"source identity mismatch: {path}")
        authenticated[label] = observed
    return authenticated


@dataclass(frozen=True, slots=True)
class SiliconLattice:
    direct: DirectLattice3D
    lattice_parameter_angstrom: float


def load_lattice(path: Path) -> SiliconLattice:
    record_value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    record = mapping(record_value, "structure")
    lattice_record = mapping(record["lattice"], "structure lattice")
    parameter = numeric(
        mapping(lattice_record["lattice_parameter"], "lattice parameter")["magnitude"],
        "lattice parameter magnitude",
    )
    normalized = mapping(lattice_record["A"], "normalized lattice")
    columns = []
    for label in ("a1", "a2", "a3"):
        columns.append(
            np.asarray(
                [numeric(item, f"{label} component") for item in values(normalized[label], label)],
                dtype=np.float64,
            )
            * parameter
        )
    return SiliconLattice(
        direct=DirectLattice3D(a1=columns[0], a2=columns[1], a3=columns[2]),
        lattice_parameter_angstrom=parameter,
    )


@dataclass(frozen=True, slots=True)
class NativeHamiltonian:
    representatives: tuple[tuple[int, int, int], ...]
    degeneracies: tuple[int, ...]
    blocks_ev: ComplexArray
    wannier_count: int


def parse_hr(path: Path) -> NativeHamiltonian:
    lines = path.read_text(encoding="utf-8").splitlines()
    wannier_count = int(lines[1].strip())
    representative_count = int(lines[2].strip())
    degeneracy_line_count = (representative_count + 14) // 15
    degeneracies = tuple(
        int(value)
        for line in lines[3 : 3 + degeneracy_line_count]
        for value in line.split()
    )
    if len(degeneracies) != representative_count or any(value <= 0 for value in degeneracies):
        raise RuntimeError("invalid HR degeneracy inventory")
    data = lines[3 + degeneracy_line_count :]
    expected_count = representative_count * wannier_count * wannier_count
    if len(data) != expected_count:
        raise RuntimeError("unexpected HR matrix-element count")
    representatives: list[tuple[int, int, int]] = []
    blocks = np.empty(
        (representative_count, wannier_count, wannier_count), dtype=np.complex128
    )
    index = 0
    for representative_index in range(representative_count):
        current: tuple[int, int, int] | None = None
        for _ in range(wannier_count * wannier_count):
            fields = data[index].split()
            index += 1
            representative = (int(fields[0]), int(fields[1]), int(fields[2]))
            if current is None:
                current = representative
            elif representative != current:
                raise RuntimeError("HR representative changed within one block")
            row = int(fields[3]) - 1
            column = int(fields[4]) - 1
            blocks[representative_index, row, column] = complex(
                float(fields[5]), float(fields[6])
            )
        if current is None:
            raise RuntimeError("empty HR block")
        representatives.append(current)
    return NativeHamiltonian(
        representatives=tuple(representatives),
        degeneracies=degeneracies,
        blocks_ev=blocks,
        wannier_count=wannier_count,
    )


def parse_ws_vectors(
    path: Path,
    representatives: tuple[tuple[int, int, int], ...],
    wannier_count: int,
) -> tuple[tuple[tuple[tuple[tuple[int, int, int], ...], ...], ...], ...]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or "use_ws_distance=.true." not in lines[0]:
        raise RuntimeError("WS-vector header is invalid")
    records = tuple(line for line in lines[1:] if line.strip())
    line_index = 0
    all_representatives = []
    for representative in representatives:
        rows = []
        for row in range(wannier_count):
            columns = []
            for column in range(wannier_count):
                header = tuple(int(value) for value in records[line_index].split())
                line_index += 1
                if header != (*representative, row + 1, column + 1):
                    raise RuntimeError("WS-vector ordering disagrees with HR")
                shift_count = int(records[line_index].strip())
                line_index += 1
                shifts = []
                for _ in range(shift_count):
                    shift = tuple(int(value) for value in records[line_index].split())
                    line_index += 1
                    if len(shift) != 3:
                        raise RuntimeError("WS-vector shift must have three components")
                    shifts.append((shift[0], shift[1], shift[2]))
                columns.append(tuple(shifts))
            rows.append(tuple(columns))
        all_representatives.append(tuple(rows))
    if line_index != len(records):
        raise RuntimeError("WS-vector payload contains trailing records")
    return tuple(all_representatives)


@dataclass(frozen=True, slots=True)
class FiniteWannierOperator:
    representatives: NDArray[np.int64]
    blocks_ev: ComplexArray
    native_representative_count: int

    @classmethod
    def from_native(cls, native: NativeHamiltonian, ws_path: Path) -> FiniteWannierOperator:
        shifts = parse_ws_vectors(ws_path, native.representatives, native.wannier_count)
        effective: dict[tuple[int, int, int], ComplexArray] = {}
        for representative_index, representative in enumerate(native.representatives):
            block_degeneracy = native.degeneracies[representative_index]
            for row in range(native.wannier_count):
                for column in range(native.wannier_count):
                    element_shifts = shifts[representative_index][row][column]
                    for shift in element_shifts:
                        actual = (
                            representative[0] + shift[0],
                            representative[1] + shift[1],
                            representative[2] + shift[2],
                        )
                        if actual not in effective:
                            effective[actual] = np.zeros(
                                (native.wannier_count, native.wannier_count),
                                dtype=np.complex128,
                            )
                        effective[actual][row, column] += (
                            native.blocks_ev[representative_index, row, column]
                            / (block_degeneracy * len(element_shifts))
                        )
        ordered = tuple(sorted(effective))
        return cls(
            representatives=np.asarray(ordered, dtype=np.int64),
            blocks_ev=np.asarray([effective[item] for item in ordered], dtype=np.complex128),
            native_representative_count=len(native.representatives),
        )

    def matrices(self, kpoints: RealArray) -> ComplexArray:
        phase = np.exp(2.0j * np.pi * (kpoints @ self.representatives.T))
        matrices = np.einsum("kr,rij->kij", phase, self.blocks_ev, optimize=True)
        return np.asarray(
            0.5 * (matrices + matrices.conj().transpose(0, 2, 1)),
            dtype=np.complex128,
        )


def centered_coordinates(size: int) -> RealArray:
    axis = -0.5 + np.arange(size, dtype=np.float64) / float(size)
    return np.asarray(
        np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1),
        dtype=np.float64,
    )


def load_parent_field(qexsd_path: Path, manifest_path: Path) -> tuple[RealArray, RealArray]:
    manifest_value: JsonValue = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest = mapping(manifest_value, "point manifest")
    points = values(manifest["points"], "point manifest points")
    fractional = np.asarray(
        [
            [
                numeric(component, "fractional coordinate")
                for component in values(
                    mapping(point, "point")["fractional_reciprocal_coordinates"],
                    "fractional coordinates",
                )
            ]
            for point in points
        ],
        dtype=np.float64,
    )
    if fractional.shape != (408, 3):
        raise RuntimeError("revealed evaluation inventory must have shape (408, 3)")
    payload = qexsd_path.read_bytes()
    document = QuantumEspressoXsdDocumentParser().execute(
        QexsdSource(
            canonical_path=str(qexsd_path),
            sha256=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
            content=payload,
        )
    )
    reciprocal = np.asarray(document.reciprocal_lattice_coefficients, dtype=np.float64)
    expected_native = fractional @ reciprocal
    observed_native = np.asarray(document.k_points, dtype=np.float64)
    if float(np.max(np.abs(expected_native - observed_native))) > 5.0e-12:
        raise RuntimeError("parent QEXSD order disagrees with the revealed manifest")
    spectrum = np.asarray(document.eigenvalues, dtype=np.float64) * HARTREE_TO_EV
    if spectrum.shape != (408, 12) or not np.all(np.isfinite(spectrum)):
        raise RuntimeError("revealed parent spectrum is invalid")
    return fractional, spectrum


def matched_parent_spectrum(
    represented: RealArray, parent: RealArray
) -> tuple[RealArray, NDArray[np.int64]]:
    combinations = tuple(itertools.combinations(range(12), 10))
    selected_values: list[RealArray] = []
    selected_indices: list[tuple[int, ...]] = []
    for represented_row, parent_row in zip(represented, parent, strict=True):
        selected = min(
            combinations,
            key=lambda indices: float(
                np.sum(np.square(represented_row - parent_row[list(indices)]))
            ),
        )
        selected_values.append(parent_row[list(selected)])
        selected_indices.append(selected)
    return (
        np.asarray(selected_values, dtype=np.float64),
        np.asarray(selected_indices, dtype=np.int64),
    )


def error_record(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
    rank: int,
    energy_scale_ev: float,
) -> JsonObject:
    root_rank = float(np.sqrt(rank))
    return {
        "maximum_matrix_frobenius_normalized": value.maximum_matrix_frobenius,
        "root_mean_square_matrix_frobenius_normalized": (
            value.root_mean_square_matrix_frobenius
        ),
        "maximum_ordered_spectrum_normalized": value.maximum_ordered_spectrum,
        "root_mean_square_ordered_spectrum_normalized": (
            value.root_mean_square_ordered_spectrum
        ),
        "maximum_matrix_frobenius_ev": (
            value.maximum_matrix_frobenius * root_rank * energy_scale_ev
        ),
        "root_mean_square_matrix_frobenius_ev": (
            value.root_mean_square_matrix_frobenius * root_rank * energy_scale_ev
        ),
        "maximum_ordered_spectrum_ev": (
            value.maximum_ordered_spectrum * energy_scale_ev
        ),
        "root_mean_square_ordered_spectrum_ev": (
            value.root_mean_square_ordered_spectrum * root_rank * energy_scale_ev
        ),
    }


def evidence_record(
    evidence: Periodic3DRankNFittedAlignmentEvidence
    | Periodic3DRankNPrescribedAlignmentEvidence,
) -> JsonObject:
    if type(evidence) is Periodic3DRankNPrescribedAlignmentEvidence:
        return {"kind": "prescribed", "identifier": evidence.identifier}
    if type(evidence) is not Periodic3DRankNFittedAlignmentEvidence:
        raise TypeError("unknown alignment evidence type")
    return {
        "kind": "fitted",
        "sample_count": evidence.sample_count,
        "minimum_numerical_rank": evidence.minimum_numerical_rank,
        "minimum_cross_singular_value": evidence.minimum_cross_singular_value,
        "maximum_optimal_residual_frobenius_norm": (
            evidence.maximum_optimal_residual_frobenius_norm
        ),
        "maximum_applied_rank_cutoff": evidence.maximum_applied_rank_cutoff,
    }


def qualified_alignment_record(
    analysis: Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    rank: int,
    energy_scale_ev: float,
    shell_metric_scale: float,
) -> JsonObject:
    shells: list[JsonValue] = []
    for shell in analysis.shells:
        shells.append(
            {
                "ordinal_shell_index": shell.ordinal_shell_index,
                "metric_shell_value": shell.metric_shell_value,
                "physical_radius_angstrom": float(
                    np.sqrt(shell.metric_shell_value / shell_metric_scale)
                ),
                "retained_block_count": shell.retained_block_count,
                "reference_shell_power_per_state_ev2": shell.reference_shell_power,
                "comparison_shell_power_per_state_ev2": shell.comparison_shell_power,
                "reference_omitted_power_per_state_ev2": shell.reference_omitted_power,
                "comparison_omitted_power_per_state_ev2": shell.comparison_omitted_power,
                "reference_total_errors": error_record(
                    shell.reference_total_errors, rank, energy_scale_ev
                ),
                "comparison_total_errors": error_record(
                    shell.comparison_total_errors, rank, energy_scale_ev
                ),
                "reference_truncation_errors": error_record(
                    shell.reference_truncation_errors, rank, energy_scale_ev
                ),
                "comparison_truncation_errors": error_record(
                    shell.comparison_truncation_errors, rank, energy_scale_ev
                ),
            }
        )
    return {
        "alignment": analysis.alignment.to_wire(),
        "applicable": True,
        "alignment_evidence": evidence_record(analysis.alignment_evidence),
        "maximum_aligned_frame_defect": analysis.maximum_aligned_frame_defect,
        "minimum_transport_singular_value": analysis.minimum_transport_singular_value,
        "maximum_transport_procrustes_residual": (
            analysis.maximum_transport_procrustes_residual
        ),
        "maximum_transport_unitarity_defect": (
            analysis.maximum_transport_unitarity_defect
        ),
        "maximum_transport_rank_cutoff": analysis.maximum_transport_rank_cutoff,
        "maximum_absolute_closure_phases": list(
            analysis.maximum_absolute_closure_phases
        ),
        "maximum_plaquette_phase": analysis.maximum_plaquette_phase,
        "maximum_direct_matrix_difference_ev": analysis.maximum_direct_matrix_difference,
        "maximum_direct_ordered_spectrum_difference_ev": (
            analysis.maximum_direct_ordered_spectrum_difference
        ),
        "reference_reconstruction_errors": error_record(
            analysis.reference_reconstruction_errors, rank, energy_scale_ev
        ),
        "comparison_reconstruction_errors": error_record(
            analysis.comparison_reconstruction_errors, rank, energy_scale_ev
        ),
        "reference_interpolation_errors": error_record(
            analysis.reference_interpolation_errors, rank, energy_scale_ev
        ),
        "comparison_interpolation_errors": error_record(
            analysis.comparison_interpolation_errors, rank, energy_scale_ev
        ),
        "reference_locality": {
            "total_power_per_state_ev2": analysis.reference_locality.total_power,
            "onsite_power_per_state_ev2": analysis.reference_locality.onsite_power,
            "nononsite_power_per_state_ev2": analysis.reference_locality.nononsite_power,
        },
        "comparison_locality": {
            "total_power_per_state_ev2": analysis.comparison_locality.total_power,
            "onsite_power_per_state_ev2": analysis.comparison_locality.onsite_power,
            "nononsite_power_per_state_ev2": analysis.comparison_locality.nononsite_power,
        },
        "shells": shells,
        "tolerance_decisions": [],
    }


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"refusing to overwrite retained result: {OUTPUT}")
    start = time.perf_counter()
    request_value: JsonValue = json.loads(REQUEST.read_text(encoding="utf-8"))
    request = mapping(request_value, "request")
    authenticated_sources = authenticate_request_sources(request)
    sources = mapping(request["sources"], "sources")

    native = parse_hr(
        source_path(mapping(sources["hamiltonian"], "hamiltonian"), "HR")
    )
    if native.wannier_count != 10:
        raise RuntimeError("authenticated HR artifact must have rank 10")
    operator = FiniteWannierOperator.from_native(
        native,
        source_path(mapping(sources["ws_vectors"], "ws vectors"), "WS"),
    )
    lattice = load_lattice(
        source_path(mapping(sources["structure"], "structure"), "structure")
    )

    construction_coordinates = centered_coordinates(6)
    construction_operators = np.asarray(
        operator.matrices(construction_coordinates.reshape(-1, 3)).reshape(
            6, 6, 6, 10, 10
        ),
        dtype=np.complex128,
    )
    qexsd_path = source_path(
        mapping(sources["revealed_parent_qexsd"], "parent QEXSD"),
        "parent QEXSD",
    )
    manifest_path = source_path(
        mapping(sources["revealed_point_manifest"], "point manifest"),
        "point manifest",
    )
    evaluation_coordinates, parent_spectrum = load_parent_field(qexsd_path, manifest_path)
    evaluation_operators = np.asarray(
        operator.matrices(evaluation_coordinates), dtype=np.complex128
    )
    identity_frame = np.eye(10, dtype=np.complex128)
    construction_frames = np.broadcast_to(
        identity_frame, (6, 6, 6, 10, 10)
    ).copy()
    evaluation_frames = np.broadcast_to(identity_frame, (408, 10, 10)).copy()

    attack = Periodic3DRankNGivensGaugeAttack(
        retained_rank=10,
        circuit_depth=2,
        harmonic_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
        coefficient=float.fromhex("0x1.921fb54442d18p-2"),
    )
    source = Periodic3DRankNWannierFieldSource(
        retained_rank=10,
        operator_identifier="C6-B20-W21-aiida-precise-eligible-full-untruncated-rank10-H",
        energy_reference="native Wannier90/QE eigenvalue reference; no fitted energy shift",
        energy_unit="eV",
        basis_identifier="authenticated C6-B20-W21 rank-10 Wannier basis",
        construction_coordinates=construction_coordinates,
        evaluation_coordinates=evaluation_coordinates,
        construction_frames=construction_frames,
        evaluation_frames=evaluation_frames,
        construction_operators=construction_operators,
        evaluation_operators=evaluation_operators,
    )
    fields = Periodic3DRankNWannierFieldProducer(
        source=source,
        attack=attack,
        frame_isometry_absolute_tolerance=1.0e-12,
        operator_hermiticity_absolute_tolerance=1.0e-12,
    ).execute()
    shell_metric_scale = 4.0 / lattice.lattice_parameter_angstrom**2
    policy = Periodic3DRankNBandEquivalenceHoppingLocalityPolicy(
        construction_size=6,
        construction_offsets=(0.0, 0.0, 0.0),
        norm_energy_scale=1.0,
        band_tolerances=(),
        gauge_alignments=(
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        ),
        shell_cap=48,
        procrustes_tolerance=ComplexUnitaryProcrustesTolerance(
            rank_absolute=1.0e-12,
            rank_relative=1.0e-10,
            validation_absolute=1.0e-12,
            validation_relative=1.0e-10,
        ),
        transport_rank_absolute=1.0e-12,
        transport_rank_relative=1.0e-10,
    )
    geometry = Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry(
        identifier="Si primitive FCC direct-lattice block metric",
        direct_metric=DirectLatticeMetric(lattice.direct),
        shell_metric_scale=shell_metric_scale,
    )
    analyzer = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
        policy=policy,
        geometry=geometry,
        fields=fields,
    )
    analysis = analyzer.execute()
    alignments: list[JsonValue] = []
    for alignment in analysis.alignments:
        if type(alignment) is not Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis:
            raise RuntimeError(f"alignment route is inapplicable: {alignment.alignment}")
        alignments.append(
            qualified_alignment_record(alignment, 10, 1.0, shell_metric_scale)
        )

    reference_data = analyzer._reference_fourier(
        fields=fields,
        geometry=geometry,
        construction_values=fields.reference_construction_operators,
    )
    comparison_series = analyzer._ordinary_series(
        6,
        analyzer._transform(
            reference_data.source_mesh,
            fields.comparison_construction_operators,
        ),
    )
    reference_series = reference_data.ordinary_series
    if not np.array_equal(reference_series.integer_modes, comparison_series.integer_modes):
        raise RuntimeError("reference and attacked displacement inventories differ")
    modes = np.asarray(reference_series.integer_modes, dtype=np.int64)
    q_values = 2 * (
        modes[:, 0] ** 2
        + modes[:, 1] ** 2
        + modes[:, 2] ** 2
        + modes[:, 0] * modes[:, 1]
        + modes[:, 0] * modes[:, 2]
        + modes[:, 1] * modes[:, 2]
    )
    reference_block_power = np.sum(
        np.abs(reference_series.matrix_coefficients) ** 2, axis=(1, 2)
    ) / 10.0
    comparison_block_power = np.sum(
        np.abs(comparison_series.matrix_coefficients) ** 2, axis=(1, 2)
    ) / 10.0

    reference_spectrum = np.linalg.eigvalsh(evaluation_operators)
    attacked_spectrum = np.linalg.eigvalsh(fields.comparison_evaluation_operators)
    pointwise_invariance = np.max(
        np.abs(reference_spectrum - attacked_spectrum), axis=1
    )
    selected_parent, selected_indices = matched_parent_spectrum(
        reference_spectrum, parent_spectrum
    )
    parent_residual = reference_spectrum - selected_parent

    result: JsonObject = {
        "schema_version": 1,
        "status": ASSURANCE_LABEL,
        "calculator_invocations": 0,
        "independent_reconstruction_performed": False,
        "request": identity(REQUEST),
        "producer": identity(Path(__file__)),
        "reusable_source_revision": {
            "hamiltonian_adapter": "calculation-local authenticated HR/WS parser",
        },
        "authenticated_sources": authenticated_sources,
        "operator": {
            "identifier": analysis.operator_identifier,
            "retained_rank": analysis.retained_rank,
            "energy_reference": analysis.energy_reference,
            "energy_unit": analysis.energy_unit,
            "basis_identifier": analysis.basis_identifier,
            "construction_shape": [6, 6, 6],
            "evaluation_point_count": 408,
            "native_hr_representative_count": operator.native_representative_count,
            "effective_ws_representative_count": len(operator.representatives),
        },
        "attack": {
            "identity": attack.attack_identity,
            "angle_upper_bound": attack.angle_upper_bound,
        },
        "geometry": {
            "identifier": analysis.geometry_identifier,
            "lattice_parameter_angstrom": lattice.lattice_parameter_angstrom,
            "shell_metric_scale_inverse_angstrom_squared": shell_metric_scale,
            "shell_cap": 48,
        },
        "producer_checks": {
            "maximum_reference_construction_hermiticity_defect_ev": float(
                np.max(
                    np.linalg.norm(
                        construction_operators
                        - construction_operators.conj().swapaxes(-1, -2),
                        axis=(-2, -1),
                    )
                )
            ),
            "maximum_reference_evaluation_hermiticity_defect_ev": float(
                np.max(
                    np.linalg.norm(
                        evaluation_operators
                        - evaluation_operators.conj().swapaxes(-1, -2),
                        axis=(-2, -1),
                    )
                )
            ),
            "maximum_pointwise_complete_spectrum_attack_difference_ev": float(
                np.max(pointwise_invariance)
            ),
            "ordinary_displacement_count": len(modes),
            "maximum_metric_shell_value": int(np.max(q_values)),
        },
        "alignments": alignments,
        "displacement_power": {
            "integer_modes": modes.tolist(),
            "metric_shell_values": q_values.tolist(),
            "physical_radii_angstrom": np.sqrt(q_values / shell_metric_scale).tolist(),
            "reference_power_per_state_ev2": reference_block_power.tolist(),
            "attacked_identity_power_per_state_ev2": comparison_block_power.tolist(),
        },
        "evaluation_spectra": {
            "ordered_point_indices_zero_based": list(range(408)),
            "fractional_reciprocal_coordinates": evaluation_coordinates.tolist(),
            "reference_rank10_ev": reference_spectrum.tolist(),
            "attacked_rank10_ev": attacked_spectrum.tolist(),
            "maximum_pointwise_attack_difference_ev": pointwise_invariance.tolist(),
            "matched_parent_rank10_ev": selected_parent.tolist(),
            "matched_parent_band_indices_one_based": (selected_indices + 1).tolist(),
            "represented_minus_matched_parent_ev": parent_residual.tolist(),
            "parent_matching": (
                "pointwise injective ordered-spectrum matching of rank 10 into the "
                "12 revealed parent bands without fitted energy alignment"
            ),
        },
        "execution": {
            "elapsed_seconds": float(time.perf_counter() - start),
            "output_path": str(OUTPUT),
        },
        "limitations": [
            "Producer-checked development analysis; no independent reconstruction was performed.",
            "No Quantum ESPRESSO or Wannier90 process was invoked.",
            "The revealed 408-point inventory is development evidence only.",
            "The frozen 402-point confirmation values remain excluded.",
            "Supports are complete rank-10 lattice-block supports, not orbital-center-resolved distances.",
            "Native HR/Wigner-Seitz and centered finite-cyclic Fourier routes remain distinct.",
            "The direct-parent overlay preserves the previously reported parent-fidelity failure.",
        ],
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
