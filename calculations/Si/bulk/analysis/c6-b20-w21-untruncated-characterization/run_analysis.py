from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray
from projectkoios.physkit import units as _physkit_units
from projectkoios.physkit.periodic.lattice import (
    DirectLattice3D,
    ReciprocalLattice3D,
)
from projectkoios.physkit.units import PhysicalUnit
from scipy import constants  # type: ignore[import-untyped]
from scipy.optimize import (  # type: ignore[import-untyped]
    linear_sum_assignment,
    minimize,
)

# The retained ProjectKoios tranche expects the historical class name, while the
# installed PhysKit surface exports the singleton under its current name.
if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER  # type: ignore[attr-defined]
    )

from projectkoios.integrations.wannier90 import (  # noqa: E402
    Wannier90DisentanglementMatrixParser,
    Wannier90EigenvalueParser,
    Wannier90HamiltonianBlockParser,
    Wannier90UnitaryMatrixParser,
)

from ksdft2effmass.serialization import TypedJsonMappingSerializer  # noqa: E402

RealArray = NDArray[np.float64]
IntegerArray = NDArray[np.int64]
ComplexArray = NDArray[np.complex128]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
EVIDENCE = BULK / "simulations" / "evidence"
STRUCTURE = (
    BULK
    / "simulations"
    / "structures"
    / "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
INTERFACE_EVIDENCE = (
    EVIDENCE / "sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-"
    "pw2wannier90-c6-b20-w21-aiida-precise/result"
)
ELIGIBLE_EXTERNAL = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1/run"
)
ENERGY_UNIT = PhysicalUnit("eV")
ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 = (
    constants.hbar**2 / constants.m_e / constants.electron_volt * 1.0e20
)


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Declare one exact artifact identity before analysis."""

    label: str
    path: Path
    byte_size: int
    sha256: str


@dataclass(frozen=True, slots=True)
class AuthenticatedArtifact:
    """Retain an observed artifact only after exact identity verification."""

    label: str
    path: Path
    byte_size: int
    sha256: str

    def to_json(self) -> JsonObject:
        try:
            displayed_path = str(self.path.relative_to(BULK))
        except ValueError:
            displayed_path = str(self.path)
        return {
            "path": displayed_path,
            "byte_size": self.byte_size,
            "sha256": self.sha256,
        }


class ArtifactAuthenticator:
    """Authenticate exact bytes without adapting scientific content."""

    __slots__ = ()

    def execute(self, identity: ArtifactIdentity) -> AuthenticatedArtifact:
        observed_size = identity.path.stat().st_size
        digest = hashlib.sha256()
        with identity.path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        observed_sha256 = digest.hexdigest()
        if observed_size != identity.byte_size:
            raise RuntimeError(f"{identity.label} artifact byte size mismatch")
        if observed_sha256 != identity.sha256:
            raise RuntimeError(f"{identity.label} artifact SHA-256 mismatch")
        return AuthenticatedArtifact(
            label=identity.label,
            path=identity.path,
            byte_size=observed_size,
            sha256=observed_sha256,
        )


@dataclass(frozen=True, slots=True)
class CandidateArtifactDeclaration:
    """Bind one localization occurrence to its authenticated native outputs."""

    label: str
    hamiltonian: ArtifactIdentity
    gauge: ArtifactIdentity
    disentanglement: ArtifactIdentity
    ws_vectors: ArtifactIdentity


@dataclass(frozen=True, slots=True)
class QualificationPolicy:
    """Declare analysis controls and structural reconstruction tolerances."""

    dense_grid_size: int = 41
    locality_grid_size: int = 21
    edge_window_ev: float = 0.5
    source_matrix_element_maximum_ev: float = 2.0e-5
    source_matrix_frobenius_maximum_ev: float = 5.0e-5
    source_spectrum_maximum_ev: float = 2.0e-5
    frozen_state_maximum_ev: float = 2.0e-5
    real_space_pair_hermiticity_maximum_ev: float = 1.0e-8
    hamiltonian_decimal_places: int = 6
    matrix_decimal_places: int = 10
    eigenvalue_decimal_places: int = 12
    curvature_steps_inverse_angstrom: tuple[float, ...] = (
        0.001,
        0.002,
        0.005,
        0.010,
    )
    primary_curvature_step_inverse_angstrom: float = 0.002
    reported_locality_cutoff_lattice_parameters: float = 2.0
    frozen_window_maximum_ev: float = 8.0
    conduction_band_index_zero_based: int = 4
    optimizer_starts_per_valley: int = 12

    def to_json(self) -> JsonObject:
        return {
            "scope": (
                "structural reconstruction verification and descriptive candidate "
                "characterization; no scientific pass/fail threshold is imposed"
            ),
            "dense_grid_size": self.dense_grid_size,
            "locality_grid_size": self.locality_grid_size,
            "edge_window_ev": self.edge_window_ev,
            "source_reconstruction_initial_fixed_tolerances": {
                "matrix_element_maximum_ev": self.source_matrix_element_maximum_ev,
                "matrix_frobenius_maximum_ev": (
                    self.source_matrix_frobenius_maximum_ev
                ),
                "spectrum_maximum_ev": self.source_spectrum_maximum_ev,
                "frozen_state_maximum_ev": self.frozen_state_maximum_ev,
                "real_space_pair_hermiticity_maximum_ev": (
                    self.real_space_pair_hermiticity_maximum_ev
                ),
            },
            "source_reconstruction_serialization_bound": {
                "hamiltonian_decimal_places": self.hamiltonian_decimal_places,
                "matrix_decimal_places": self.matrix_decimal_places,
                "eigenvalue_decimal_places": self.eigenvalue_decimal_places,
                "rule": (
                    "derive worst-case element, Frobenius, and spectral bounds from "
                    "native decimal quantization, HR degeneracy weights, dimensions, "
                    "and the authenticated energy scale"
                ),
            },
            "effective_mass_diagnostic": {
                "steps_inverse_angstrom": list(self.curvature_steps_inverse_angstrom),
                "primary_step_inverse_angstrom": (
                    self.primary_curvature_step_inverse_angstrom
                ),
            },
            "locality_diagnostic": {
                "reported_cutoff_lattice_parameters": (
                    self.reported_locality_cutoff_lattice_parameters
                )
            },
        }


@dataclass(frozen=True, slots=True)
class SiliconLattice:
    """Bind physical scales to PhysKit direct and reciprocal lattice objects."""

    direct: DirectLattice3D
    reciprocal: ReciprocalLattice3D
    lattice_parameter_angstrom: float

    @classmethod
    def from_structure(cls, path: Path) -> Self:
        record = json.loads(path.read_text(encoding="utf-8"))
        lattice_parameter = float(record["lattice"]["lattice_parameter"]["magnitude"])
        normalized = record["lattice"]["A"]
        direct_matrix = (
            np.asarray(
                [normalized["a1"], normalized["a2"], normalized["a3"]],
                dtype=np.float64,
            ).T
            * lattice_parameter
        )
        direct = DirectLattice3D(
            a1=direct_matrix[:, 0],
            a2=direct_matrix[:, 1],
            a3=direct_matrix[:, 2],
        )
        reciprocal = ReciprocalLattice3D.from_direct_lattice(direct)
        return cls(
            direct=direct,
            reciprocal=reciprocal,
            lattice_parameter_angstrom=lattice_parameter,
        )

    @property
    def conventional_reciprocal_axis_length_inverse_angstrom(self) -> float:
        return 2.0 * np.pi / self.lattice_parameter_angstrom

    def closest_gamma_cartesian(self, fractional: RealArray) -> RealArray:
        shifts = np.asarray(
            [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)],
            dtype=np.float64,
        )
        candidates = (fractional[np.newaxis, :] + shifts) @ (
            self.reciprocal.primitive_basis_matrix.T
        )
        return candidates[int(np.argmin(np.linalg.norm(candidates, axis=1)))]


@dataclass(frozen=True, slots=True)
class Wannier90WsVectorData:
    """Retain element-resolved superlattice shifts from ``_wsvec.dat``."""

    shifts: tuple[tuple[tuple[IntegerArray, ...], ...], ...]
    representative_count: int
    wannier_count: int


class Wannier90WsVectorParser:
    """Parse the native element-resolved WS shift inventory."""

    __slots__ = ()

    def execute(
        self,
        payload: bytes,
        representatives: tuple[tuple[int, int, int], ...],
        wannier_count: int,
    ) -> Wannier90WsVectorData:
        try:
            lines = payload.decode("utf-8").splitlines()
        except UnicodeDecodeError as error:
            raise ValueError("ws-vector payload must be UTF-8") from error
        if not lines or "use_ws_distance=.true." not in lines[0]:
            raise ValueError("ws-vector payload must declare use_ws_distance=.true.")
        records = tuple(line for line in lines[1:] if line.strip())
        line_index = 0
        representative_records: list[tuple[tuple[IntegerArray, ...], ...]] = []
        for representative in representatives:
            row_records: list[tuple[IntegerArray, ...]] = []
            for row in range(wannier_count):
                column_records: list[IntegerArray] = []
                for column in range(wannier_count):
                    if line_index + 1 >= len(records):
                        raise ValueError("ws-vector payload ends before all records")
                    header = tuple(int(value) for value in records[line_index].split())
                    line_index += 1
                    expected = (*representative, row + 1, column + 1)
                    if header != expected:
                        raise ValueError(
                            "ws-vector record ordering disagrees with _hr.dat"
                        )
                    degeneracy = int(records[line_index].strip())
                    line_index += 1
                    if degeneracy <= 0:
                        raise ValueError("ws-vector degeneracy must be positive")
                    shifts: list[IntegerArray] = []
                    for _ in range(degeneracy):
                        if line_index >= len(records):
                            raise ValueError(
                                "ws-vector payload ends within a shift list"
                            )
                        shift = np.asarray(
                            tuple(int(value) for value in records[line_index].split()),
                            dtype=np.int64,
                        )
                        line_index += 1
                        if shift.shape != (3,):
                            raise ValueError(
                                "ws-vector shift must have three components"
                            )
                        shift.setflags(write=False)
                        shifts.append(shift)
                    column_records.append(np.asarray(shifts, dtype=np.int64))
                row_records.append(tuple(column_records))
            representative_records.append(tuple(row_records))
        if line_index != len(records):
            raise ValueError("ws-vector payload contains trailing records")
        return Wannier90WsVectorData(
            shifts=tuple(representative_records),
            representative_count=len(representatives),
            wannier_count=wannier_count,
        )


@dataclass(frozen=True, slots=True)
class FiniteWannierOperator:
    """Represent a finite element-resolved real-space Wannier Hamiltonian."""

    representatives: IntegerArray
    blocks_ev: ComplexArray

    def __post_init__(self) -> None:
        if self.representatives.ndim != 2 or self.representatives.shape[1] != 3:
            raise ValueError("representatives must have shape (count, 3)")
        count = self.representatives.shape[0]
        if self.blocks_ev.ndim != 3 or self.blocks_ev.shape[0] != count:
            raise ValueError("one square block is required per representative")
        if self.blocks_ev.shape[1] != self.blocks_ev.shape[2]:
            raise ValueError("Hamiltonian blocks must be square")
        if not np.all(np.isfinite(self.blocks_ev)):
            raise ValueError("Hamiltonian blocks must be finite")

    @classmethod
    def from_native(
        cls,
        representatives: tuple[tuple[int, int, int], ...],
        degeneracies: tuple[int, ...],
        blocks_ev: ComplexArray,
        ws_vectors: Wannier90WsVectorData,
    ) -> Self:
        effective: dict[tuple[int, int, int], ComplexArray] = {}
        dimension = blocks_ev.shape[1]
        for representative_index, representative in enumerate(representatives):
            block_degeneracy = degeneracies[representative_index]
            for row in range(dimension):
                for column in range(dimension):
                    shifts = ws_vectors.shifts[representative_index][row][column]
                    shift_count = len(shifts)
                    for shift in shifts:
                        actual = (
                            int(representative[0] + shift[0]),
                            int(representative[1] + shift[1]),
                            int(representative[2] + shift[2]),
                        )
                        if actual not in effective:
                            effective[actual] = np.zeros(
                                (dimension, dimension), dtype=np.complex128
                            )
                        effective[actual][row, column] += blocks_ev[
                            representative_index, row, column
                        ] / (block_degeneracy * shift_count)
        ordered = tuple(sorted(effective))
        representative_array = np.asarray(ordered, dtype=np.int64)
        block_array = np.asarray(tuple(effective[item] for item in ordered))
        representative_array.setflags(write=False)
        block_array.setflags(write=False)
        return cls(representative_array, block_array)

    @property
    def dimension(self) -> int:
        return int(self.blocks_ev.shape[1])

    def real_space_hermiticity(self, tolerance_ev: float) -> JsonObject:
        """Return pair-closure and Hermiticity diagnostics without symmetrization."""
        indices = {
            tuple(int(value) for value in representative): index
            for index, representative in enumerate(self.representatives)
        }
        missing: list[JsonValue] = []
        maximum = 0.0
        for representative, index in indices.items():
            opposite = tuple(-value for value in representative)
            if opposite not in indices:
                missing.append(list(representative))
                continue
            maximum = max(
                maximum,
                float(
                    np.max(
                        np.abs(
                            self.blocks_ev[index]
                            - self.blocks_ev[indices[opposite]].conj().T
                        )
                    )
                ),
            )
        return {
            "effective_representative_count": len(self.representatives),
            "missing_negative_representative_count": len(missing),
            "missing_negative_representatives": missing,
            "maximum_pair_hermiticity_residual_ev": maximum,
            "tolerance_ev": tolerance_ev,
            "passed": len(missing) == 0 and maximum <= tolerance_ev,
        }

    def matrices(self, kpoints: RealArray) -> ComplexArray:
        phase = np.exp(2.0j * np.pi * (kpoints @ self.representatives.T))
        matrices = np.einsum("kr,rij->kij", phase, self.blocks_ev, optimize=True)
        return 0.5 * (matrices + matrices.conj().transpose(0, 2, 1))

    def eigenvalues(self, kpoints: RealArray, chunk_size: int = 2048) -> RealArray:
        chunks: list[RealArray] = []
        for start in range(0, len(kpoints), chunk_size):
            chunks.append(
                np.linalg.eigvalsh(self.matrices(kpoints[start : start + chunk_size]))
            )
        return np.concatenate(chunks, axis=0)

    def eigenvalue(self, kpoint: RealArray, band_index: int) -> float:
        values = np.linalg.eigvalsh(self.matrices(kpoint[np.newaxis, :])[0])
        return float(values[band_index])


@dataclass(frozen=True, slots=True)
class NativeGaugeOperator:
    """Retain source-point Hamiltonians transformed by U-dis and U."""

    fractional_kpoints: RealArray
    parent_eigenvalues_ev: RealArray
    matrices_ev: ComplexArray

    @classmethod
    def from_artifacts(
        cls,
        eigenvalue_payload: bytes,
        gauge_payload: bytes,
        disentanglement_payload: bytes,
    ) -> Self:
        eigenvalues = (
            Wannier90EigenvalueParser()
            .execute(eigenvalue_payload, ENERGY_UNIT)
            .eigenvalues.magnitude
        )
        gauge = Wannier90UnitaryMatrixParser().execute(gauge_payload)
        disentanglement = Wannier90DisentanglementMatrixParser().execute(
            disentanglement_payload
        )
        gauge_kpoints = np.asarray(gauge.fractional_kpoints.magnitude)
        disentanglement_kpoints = np.asarray(
            disentanglement.fractional_kpoints.magnitude
        )
        if eigenvalues.shape != (216, 20):
            raise RuntimeError("unexpected EIG table shape")
        if gauge.kpoint_count != 216 or disentanglement.kpoint_count != 216:
            raise RuntimeError("unexpected native gauge k-point count")
        if gauge.wannier_count != 10:
            raise RuntimeError("unexpected gauge Wannier rank")
        if disentanglement.band_count != 20 or disentanglement.wannier_count != 10:
            raise RuntimeError("unexpected disentanglement matrix dimensions")
        if not np.allclose(
            gauge_kpoints, disentanglement_kpoints, atol=1.0e-12, rtol=0.0
        ):
            raise RuntimeError("U and U-dis k-point inventories disagree")
        expected_grid = ReciprocalGrid.gamma_origin(6).points
        if not np.allclose(gauge_kpoints, expected_grid, atol=1.0e-10, rtol=0.0):
            raise RuntimeError(
                "native gauge k points are not the ordered 6 x 6 x 6 grid"
            )
        matrices: list[ComplexArray] = []
        for index in range(216):
            u_dis = disentanglement.matrices[index].magnitude
            u_matrix = gauge.matrices[index].magnitude
            composite = u_dis @ u_matrix
            matrices.append(
                composite.conj().T @ np.diag(eigenvalues[index]) @ composite
            )
        matrix_array = np.asarray(matrices, dtype=np.complex128)
        matrix_array.setflags(write=False)
        return cls(gauge_kpoints, np.asarray(eigenvalues), matrix_array)

    @property
    def eigenvalues_ev(self) -> RealArray:
        return np.linalg.eigvalsh(self.matrices_ev)


@dataclass(frozen=True, slots=True)
class LoadedCandidate:
    """Compose authenticated artifacts and their finite operators."""

    label: str
    artifacts: tuple[AuthenticatedArtifact, ...]
    finite_operator: FiniteWannierOperator
    native_gauge_operator: NativeGaugeOperator
    native_representative_count: int
    native_wannier_count: int
    native_degeneracies: tuple[int, ...]


def _require_decimal_places(payload: bytes, expected: int, label: str) -> None:
    matches = re.findall(rb"[+-]?\d+\.(\d+)(?:[Ee][+-]?\d+)?", payload)
    if not matches or any(len(value) != expected for value in matches):
        raise RuntimeError(f"{label} native decimal precision disagrees with policy")


class CandidateOperatorLoader:
    """Authenticate and construct one candidate without calculator execution."""

    __slots__ = ("_authenticator", "_eigenvalue_artifact")

    def __init__(
        self,
        authenticator: ArtifactAuthenticator,
        eigenvalue_artifact: AuthenticatedArtifact,
    ) -> None:
        self._authenticator = authenticator
        self._eigenvalue_artifact = eigenvalue_artifact

    def execute(self, declaration: CandidateArtifactDeclaration) -> LoadedCandidate:
        hamiltonian = self._authenticator.execute(declaration.hamiltonian)
        gauge = self._authenticator.execute(declaration.gauge)
        disentanglement = self._authenticator.execute(declaration.disentanglement)
        ws_vectors = self._authenticator.execute(declaration.ws_vectors)
        hamiltonian_payload = hamiltonian.path.read_bytes()
        gauge_payload = gauge.path.read_bytes()
        disentanglement_payload = disentanglement.path.read_bytes()
        eigenvalue_payload = self._eigenvalue_artifact.path.read_bytes()
        _require_decimal_places(hamiltonian_payload, 6, "HR")
        _require_decimal_places(gauge_payload, 10, "gauge")
        _require_decimal_places(disentanglement_payload, 10, "disentanglement")
        _require_decimal_places(eigenvalue_payload, 12, "eigenvalue")
        parsed_hamiltonian = Wannier90HamiltonianBlockParser().execute(
            hamiltonian_payload, ENERGY_UNIT
        )
        parsed_ws_vectors = Wannier90WsVectorParser().execute(
            ws_vectors.path.read_bytes(),
            parsed_hamiltonian.representatives,
            parsed_hamiltonian.wannier_count,
        )
        native_blocks = np.asarray(
            tuple(block.magnitude for block in parsed_hamiltonian.blocks),
            dtype=np.complex128,
        )
        finite_operator = FiniteWannierOperator.from_native(
            parsed_hamiltonian.representatives,
            parsed_hamiltonian.degeneracies,
            native_blocks,
            parsed_ws_vectors,
        )
        native_gauge_operator = NativeGaugeOperator.from_artifacts(
            eigenvalue_payload,
            gauge_payload,
            disentanglement_payload,
        )
        return LoadedCandidate(
            label=declaration.label,
            artifacts=(hamiltonian, gauge, disentanglement, ws_vectors),
            finite_operator=finite_operator,
            native_gauge_operator=native_gauge_operator,
            native_representative_count=len(parsed_hamiltonian.representatives),
            native_wannier_count=parsed_hamiltonian.wannier_count,
            native_degeneracies=parsed_hamiltonian.degeneracies,
        )


@dataclass(frozen=True, slots=True)
class ReciprocalGrid:
    """Represent one deterministic Gamma-origin Cartesian product in fractionals."""

    size: int
    points: RealArray

    @classmethod
    def gamma_origin(cls, size: int) -> Self:
        values = np.arange(size, dtype=np.float64) / size
        points = np.asarray(
            [(i, j, k) for i in values for j in values for k in values],
            dtype=np.float64,
        )
        points.setflags(write=False)
        return cls(size=size, points=points)


@dataclass(frozen=True, slots=True)
class ErrorStatistics:
    """Retain scalar error summaries for an explicitly aligned array."""

    maximum_absolute_ev: float
    rms_ev: float
    percentile_95_absolute_ev: float

    @classmethod
    def from_difference(cls, difference: RealArray) -> Self:
        absolute = np.abs(difference)
        return cls(
            maximum_absolute_ev=float(np.max(absolute)),
            rms_ev=float(np.sqrt(np.mean(np.square(difference)))),
            percentile_95_absolute_ev=float(np.percentile(absolute, 95.0)),
        )

    def to_json(self) -> JsonObject:
        return {
            "maximum_absolute_ev": self.maximum_absolute_ev,
            "rms_ev": self.rms_ev,
            "percentile_95_absolute_ev": self.percentile_95_absolute_ev,
        }


@dataclass(frozen=True, slots=True)
class SourceSerializationBounds:
    """Retain worst-case bounds derived from authenticated native precision."""

    reciprocal_degeneracy_sum: float
    maximum_parent_energy_absolute_ev: float
    hr_matrix_element_bound_ev: float
    native_gauge_matrix_frobenius_bound_ev: float
    matrix_element_bound_ev: float
    matrix_frobenius_bound_ev: float
    spectrum_bound_ev: float

    def to_json(self) -> JsonObject:
        return {
            "derivation": (
                "worst-case componentwise native decimal rounding propagated through "
                "HR degeneracy weights and the U-dis/U transformed parent spectrum"
            ),
            "reciprocal_degeneracy_sum": self.reciprocal_degeneracy_sum,
            "maximum_parent_energy_absolute_ev": (
                self.maximum_parent_energy_absolute_ev
            ),
            "hr_matrix_element_bound_ev": self.hr_matrix_element_bound_ev,
            "native_gauge_matrix_frobenius_bound_ev": (
                self.native_gauge_matrix_frobenius_bound_ev
            ),
            "matrix_element_bound_ev": self.matrix_element_bound_ev,
            "matrix_frobenius_bound_ev": self.matrix_frobenius_bound_ev,
            "spectrum_bound_ev": self.spectrum_bound_ev,
        }


class SourceReconstructionAnalyzer:
    """Compare HR reconstruction with its exact native gauge construction."""

    __slots__ = ("_policy",)

    def __init__(self, policy: QualificationPolicy) -> None:
        self._policy = policy

    def execute(self, candidate: LoadedCandidate) -> JsonObject:
        native = candidate.native_gauge_operator
        reconstructed = candidate.finite_operator.matrices(native.fractional_kpoints)
        difference = reconstructed - native.matrices_ev
        element_maximum = float(np.max(np.abs(difference)))
        frobenius = np.linalg.norm(difference, axis=(1, 2))
        frobenius_maximum = float(np.max(frobenius))
        spectrum_difference = np.linalg.eigvalsh(reconstructed) - native.eigenvalues_ev
        spectrum = ErrorStatistics.from_difference(spectrum_difference)
        frozen_errors: list[float] = []
        frozen_counts: list[int] = []
        for parent_values, candidate_values in zip(
            native.parent_eigenvalues_ev,
            native.eigenvalues_ev,
            strict=True,
        ):
            frozen = parent_values[
                parent_values <= self._policy.frozen_window_maximum_ev
            ]
            rows, columns = linear_sum_assignment(
                np.abs(frozen[:, np.newaxis] - candidate_values[np.newaxis, :])
            )
            frozen_errors.extend(
                float(abs(frozen[row] - candidate_values[column]))
                for row, column in zip(rows, columns, strict=True)
            )
            frozen_counts.append(len(frozen))
        frozen_maximum = max(frozen_errors)
        initial_fixed_checks: JsonObject = {
            "matrix_element_maximum": (
                element_maximum <= self._policy.source_matrix_element_maximum_ev
            ),
            "matrix_frobenius_maximum": (
                frobenius_maximum <= self._policy.source_matrix_frobenius_maximum_ev
            ),
            "spectrum_maximum": (
                spectrum.maximum_absolute_ev <= self._policy.source_spectrum_maximum_ev
            ),
            "frozen_state_maximum": (
                frozen_maximum <= self._policy.frozen_state_maximum_ev
            ),
        }
        serialization_bounds = self._serialization_bounds(candidate)
        serialization_checks: JsonObject = {
            "matrix_element_within_bound": (
                element_maximum <= serialization_bounds.matrix_element_bound_ev
            ),
            "matrix_frobenius_within_bound": (
                frobenius_maximum <= serialization_bounds.matrix_frobenius_bound_ev
            ),
            "spectrum_within_bound": (
                spectrum.maximum_absolute_ev <= serialization_bounds.spectrum_bound_ev
            ),
            "frozen_state_maximum": (
                frozen_maximum <= self._policy.frozen_state_maximum_ev
            ),
        }
        return {
            "matrix_element_maximum_absolute_ev": element_maximum,
            "matrix_frobenius_maximum_ev": frobenius_maximum,
            "spectrum": spectrum.to_json(),
            "frozen_state_matching": {
                "frozen_window_maximum_ev": (self._policy.frozen_window_maximum_ev),
                "minimum_frozen_state_count": min(frozen_counts),
                "maximum_frozen_state_count": max(frozen_counts),
                "matched_state_count": len(frozen_errors),
                "maximum_absolute_ev": frozen_maximum,
                "rms_ev": float(np.sqrt(np.mean(np.square(np.asarray(frozen_errors))))),
            },
            "initial_fixed_tolerance_checks": initial_fixed_checks,
            "initial_fixed_tolerances_passed": all(initial_fixed_checks.values()),
            "native_serialization_bounds": serialization_bounds.to_json(),
            "serialization_bound_checks": serialization_checks,
            "structural_verification_passed": all(serialization_checks.values()),
        }

    def _serialization_bounds(
        self, candidate: LoadedCandidate
    ) -> SourceSerializationBounds:
        hr_half_step = 0.5 * 10.0 ** (-self._policy.hamiltonian_decimal_places)
        matrix_complex_half_step = (
            np.sqrt(2.0) * 0.5 * 10.0 ** (-self._policy.matrix_decimal_places)
        )
        eigenvalue_half_step = 0.5 * 10.0 ** (-self._policy.eigenvalue_decimal_places)
        reciprocal_degeneracy_sum = sum(
            1.0 / value for value in candidate.native_degeneracies
        )
        hr_element_bound = np.sqrt(2.0) * hr_half_step * reciprocal_degeneracy_sum
        rank = candidate.native_wannier_count
        parent_bands = candidate.native_gauge_operator.parent_eigenvalues_ev.shape[1]
        disentanglement_frobenius_bound = (
            np.sqrt(parent_bands * rank) * matrix_complex_half_step
        )
        gauge_frobenius_bound = np.sqrt(rank * rank) * matrix_complex_half_step
        composite_frobenius_bound = (
            disentanglement_frobenius_bound * (1.0 + gauge_frobenius_bound)
            + gauge_frobenius_bound
        )
        maximum_parent_energy = float(
            np.max(np.abs(candidate.native_gauge_operator.parent_eigenvalues_ev))
        )
        native_gauge_frobenius_bound = (
            2.0 * maximum_parent_energy * composite_frobenius_bound
            + maximum_parent_energy * composite_frobenius_bound**2
            + np.sqrt(rank)
            * eigenvalue_half_step
            * (1.0 + composite_frobenius_bound) ** 2
        )
        matrix_element_bound = hr_element_bound + native_gauge_frobenius_bound
        matrix_frobenius_bound = rank * hr_element_bound + native_gauge_frobenius_bound
        return SourceSerializationBounds(
            reciprocal_degeneracy_sum=reciprocal_degeneracy_sum,
            maximum_parent_energy_absolute_ev=maximum_parent_energy,
            hr_matrix_element_bound_ev=float(hr_element_bound),
            native_gauge_matrix_frobenius_bound_ev=float(native_gauge_frobenius_bound),
            matrix_element_bound_ev=float(matrix_element_bound),
            matrix_frobenius_bound_ev=float(matrix_frobenius_bound),
            spectrum_bound_ev=float(matrix_frobenius_bound),
        )


@dataclass(frozen=True, slots=True)
class ValleyMinimum:
    """Retain one locally optimized member of the six-Delta-valley family."""

    axis: int
    sign: int
    energy_ev: float
    fractional: RealArray
    cartesian_inverse_angstrom: RealArray
    optimizer_success: bool
    optimizer_iterations: int

    @property
    def label(self) -> str:
        return f"{('-' if self.sign < 0 else '+')}{'xyz'[self.axis]}"

    @property
    def radius_inverse_angstrom(self) -> float:
        return float(np.linalg.norm(self.cartesian_inverse_angstrom))

    @property
    def axis_cosine(self) -> float:
        return float(
            abs(self.cartesian_inverse_angstrom[self.axis])
            / self.radius_inverse_angstrom
        )

    @property
    def identity_matches(self) -> bool:
        observed_axis = int(np.argmax(np.abs(self.cartesian_inverse_angstrom)))
        observed_sign = (
            -1 if self.cartesian_inverse_angstrom[observed_axis] < 0.0 else 1
        )
        return observed_axis == self.axis and observed_sign == self.sign


class ValleyFamilyAnalyzer:
    """Locate and test the six Cartesian Delta-valley candidates."""

    __slots__ = ("_lattice", "_policy")

    def __init__(self, lattice: SiliconLattice, policy: QualificationPolicy) -> None:
        self._lattice = lattice
        self._policy = policy

    def execute(
        self,
        operator: FiniteWannierOperator,
        dense_grid: ReciprocalGrid,
        dense_eigenvalues: RealArray,
    ) -> tuple[JsonObject, tuple[ValleyMinimum, ...]]:
        classified = self._classify_dense_points(dense_grid.points)
        conduction = self._policy.conduction_band_index_zero_based
        dense_conduction = dense_eigenvalues[:, conduction]
        minima: list[ValleyMinimum] = []
        for axis in range(3):
            for sign in (-1, 1):
                member_indices = np.flatnonzero(
                    (classified[:, 0] == axis) & (classified[:, 1] == sign)
                )
                if len(member_indices) < self._policy.optimizer_starts_per_valley:
                    raise RuntimeError("dense grid does not seed every Delta valley")
                order = member_indices[
                    np.argsort(dense_conduction[member_indices])[
                        : self._policy.optimizer_starts_per_valley
                    ]
                ]
                optimized = tuple(
                    self._optimize(operator, dense_grid.points[index], axis, sign)
                    for index in order
                )
                minima.append(min(optimized, key=lambda item: item.energy_ev))
        energies = np.asarray(tuple(item.energy_ev for item in minima))
        radii = np.asarray(tuple(item.radius_inverse_angstrom for item in minima))
        axis_cosines = np.asarray(tuple(item.axis_cosine for item in minima))
        opposite_splits: list[JsonValue] = []
        for axis in range(3):
            negative = next(
                item for item in minima if item.axis == axis and item.sign == -1
            )
            positive = next(
                item for item in minima if item.axis == axis and item.sign == 1
            )
            opposite_splits.append(abs(positive.energy_ev - negative.energy_ev))
        records: list[JsonValue] = []
        gamma_x_distance = (
            self._lattice.conventional_reciprocal_axis_length_inverse_angstrom
        )
        for item in minima:
            records.append(
                {
                    "label": item.label,
                    "energy_ev_native_reference": item.energy_ev,
                    "fractional_reciprocal_coordinates": item.fractional.tolist(),
                    "cartesian_inverse_angstrom": (
                        item.cartesian_inverse_angstrom.tolist()
                    ),
                    "radius_inverse_angstrom": (item.radius_inverse_angstrom),
                    "fraction_of_conventional_gamma_x_distance": (
                        item.radius_inverse_angstrom / gamma_x_distance
                    ),
                    "declared_axis_cosine": item.axis_cosine,
                    "declared_identity_preserved": item.identity_matches,
                    "optimizer_success": item.optimizer_success,
                    "optimizer_iterations": item.optimizer_iterations,
                }
            )
        result: JsonObject = {
            "valleys": records,
            "energy_spread_ev": float(np.ptp(energies)),
            "radius_spread_inverse_angstrom": float(np.ptp(radii)),
            "minimum_axis_cosine": float(np.min(axis_cosines)),
            "opposite_pair_energy_splits_ev": opposite_splits,
            "all_optimizers_succeeded": all(item.optimizer_success for item in minima),
            "all_declared_identities_preserved": all(
                item.identity_matches for item in minima
            ),
            "interpretation": (
                "candidate predictions to compare with withheld parent data; the "
                "observed spreads are not assigned a pass/fail disposition"
            ),
        }
        return result, tuple(minima)

    def _classify_dense_points(self, kpoints: RealArray) -> IntegerArray:
        shifts = np.asarray(
            [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)],
            dtype=np.float64,
        )
        reciprocal = self._lattice.reciprocal.primitive_basis_matrix
        result = np.empty((len(kpoints), 2), dtype=np.int64)
        for index, fractional in enumerate(kpoints):
            cartesian = (fractional[np.newaxis, :] + shifts) @ reciprocal.T
            closest = cartesian[int(np.argmin(np.linalg.norm(cartesian, axis=1)))]
            axis = int(np.argmax(np.abs(closest)))
            sign = -1 if closest[axis] < 0.0 else 1
            result[index] = (axis, sign)
        return result

    def _optimize(
        self,
        operator: FiniteWannierOperator,
        start: RealArray,
        axis: int,
        sign: int,
    ) -> ValleyMinimum:
        band_index = self._policy.conduction_band_index_zero_based
        result = minimize(
            lambda point: operator.eigenvalue(
                np.asarray(point, dtype=np.float64) % 1.0, band_index
            ),
            start,
            method="Nelder-Mead",
            options={"xatol": 1.0e-11, "fatol": 1.0e-12, "maxiter": 2500},
        )
        fractional = np.asarray(result.x, dtype=np.float64) % 1.0
        cartesian = self._lattice.closest_gamma_cartesian(fractional)
        return ValleyMinimum(
            axis=axis,
            sign=sign,
            energy_ev=float(result.fun),
            fractional=fractional,
            cartesian_inverse_angstrom=cartesian,
            optimizer_success=bool(result.success),
            optimizer_iterations=int(result.nit),
        )


class EffectiveMassAnalyzer:
    """Compute stencil-sensitive descriptive curvature masses at each valley."""

    __slots__ = ("_lattice", "_policy")

    def __init__(self, lattice: SiliconLattice, policy: QualificationPolicy) -> None:
        self._lattice = lattice
        self._policy = policy

    def execute(
        self,
        operator: FiniteWannierOperator,
        valleys: tuple[ValleyMinimum, ...],
    ) -> JsonObject:
        records: list[JsonValue] = []
        relative_spreads: list[float] = []
        positive_curvature = True
        for valley in valleys:
            step_records: list[JsonValue] = []
            mass_by_step: list[RealArray] = []
            for step in self._policy.curvature_steps_inverse_angstrom:
                hessian = self._hessian(operator, valley.fractional, step)
                curvatures, axes = np.linalg.eigh(hessian)
                positive_curvature = positive_curvature and bool(
                    np.all(curvatures > 0.0)
                )
                masses = ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 / curvatures
                mass_by_step.append(masses)
                step_records.append(
                    {
                        "step_inverse_angstrom": step,
                        "principal_curvatures_ev_angstrom_squared": (
                            curvatures.tolist()
                        ),
                        "principal_mass_ratios_to_electron_mass": masses.tolist(),
                        "principal_axes_cartesian_columns": axes.tolist(),
                    }
                )
            mass_array = np.asarray(mass_by_step)
            relative = np.ptp(mass_array, axis=0) / np.abs(
                mass_array[
                    self._policy.curvature_steps_inverse_angstrom.index(
                        self._policy.primary_curvature_step_inverse_angstrom
                    )
                ]
            )
            relative_spreads.append(float(np.max(relative)))
            records.append(
                {
                    "valley_label": valley.label,
                    "stencils": step_records,
                    "maximum_principal_mass_relative_spread": (float(np.max(relative))),
                }
            )
        return {
            "interpretation": (
                "descriptive candidate predictions only; no withheld parent "
                "validation has been performed"
            ),
            "valleys": records,
            "maximum_relative_spread": max(relative_spreads),
            "all_principal_curvatures_positive": positive_curvature,
        }

    def _hessian(
        self,
        operator: FiniteWannierOperator,
        minimum_fractional: RealArray,
        step_inverse_angstrom: float,
    ) -> RealArray:
        inverse_reciprocal = np.linalg.inv(
            self._lattice.reciprocal.primitive_basis_matrix
        )
        band_index = self._policy.conduction_band_index_zero_based
        origin = operator.eigenvalue(minimum_fractional, band_index)
        hessian = np.empty((3, 3), dtype=np.float64)
        for row in range(3):
            row_delta = inverse_reciprocal[:, row] * step_inverse_angstrom
            hessian[row, row] = (
                operator.eigenvalue(minimum_fractional + row_delta, band_index)
                - 2.0 * origin
                + operator.eigenvalue(minimum_fractional - row_delta, band_index)
            ) / step_inverse_angstrom**2
            for column in range(row):
                column_delta = inverse_reciprocal[:, column] * step_inverse_angstrom
                value = (
                    operator.eigenvalue(
                        minimum_fractional + row_delta + column_delta, band_index
                    )
                    - operator.eigenvalue(
                        minimum_fractional + row_delta - column_delta, band_index
                    )
                    - operator.eigenvalue(
                        minimum_fractional - row_delta + column_delta, band_index
                    )
                    + operator.eigenvalue(
                        minimum_fractional - row_delta - column_delta, band_index
                    )
                ) / (4.0 * step_inverse_angstrom**2)
                hessian[row, column] = value
                hessian[column, row] = value
        return hessian


class LocalityAnalyzer:
    """Resolve physical-radius shells and finite-cutoff interpolation sensitivity."""

    __slots__ = ("_lattice", "_policy")

    def __init__(self, lattice: SiliconLattice, policy: QualificationPolicy) -> None:
        self._lattice = lattice
        self._policy = policy

    def execute(
        self,
        operator: FiniteWannierOperator,
        grid: ReciprocalGrid,
    ) -> JsonObject:
        direct_vectors = self._lattice.direct.vector(operator.representatives)
        radii = np.linalg.norm(direct_vectors, axis=1)
        rounded_radii = np.round(radii, decimals=9)
        shells = np.unique(rounded_radii)
        full_eigenvalues = operator.eigenvalues(grid.points)
        conduction = self._policy.conduction_band_index_zero_based
        edge = float(np.min(full_eigenvalues[:, conduction]))
        edge_mask = (
            full_eigenvalues[:, conduction] <= edge + self._policy.edge_window_ev
        )
        phase = np.exp(2.0j * np.pi * (grid.points @ operator.representatives.T))
        cumulative = np.zeros(
            (len(grid.points), operator.dimension, operator.dimension),
            dtype=np.complex128,
        )
        frobenius_norms = np.linalg.norm(operator.blocks_ev, axis=(1, 2))
        spectral_norms = np.linalg.svd(operator.blocks_ev, compute_uv=False)[:, 0]
        records: list[JsonValue] = []
        reported_cutoff_radius: float | None = None
        for radius in shells:
            shell_mask = rounded_radii == radius
            shell_contribution = phase[:, shell_mask] @ operator.blocks_ev[
                shell_mask
            ].reshape((int(np.count_nonzero(shell_mask)), -1))
            cumulative += shell_contribution.reshape(cumulative.shape)
            hermitian = 0.5 * (cumulative + cumulative.conj().transpose(0, 2, 1))
            truncated = np.linalg.eigvalsh(hermitian)
            difference = truncated - full_eigenvalues
            all_bands = ErrorStatistics.from_difference(difference)
            lowest = ErrorStatistics.from_difference(difference[:, conduction])
            edge_lowest = ErrorStatistics.from_difference(
                difference[edge_mask, conduction]
            )
            tail_mask = rounded_radii > radius
            within_reported_cutoff = (
                radius
                <= self._policy.reported_locality_cutoff_lattice_parameters
                * self._lattice.lattice_parameter_angstrom
            )
            if within_reported_cutoff:
                reported_cutoff_radius = float(radius)
            records.append(
                {
                    "radius_angstrom": float(radius),
                    "shell_representative_count": int(np.count_nonzero(shell_mask)),
                    "included_representative_count": int(np.count_nonzero(~tail_mask)),
                    "excluded_representative_count": int(np.count_nonzero(tail_mask)),
                    "shell_frobenius_power_ev_squared": float(
                        np.sum(np.square(frobenius_norms[shell_mask]))
                    ),
                    "tail_frobenius_norm_ev": float(
                        np.sqrt(np.sum(np.square(frobenius_norms[tail_mask])))
                    ),
                    "tail_spectral_triangle_bound_ev": float(
                        np.sum(spectral_norms[tail_mask])
                    ),
                    "truncation_all_bands": all_bands.to_json(),
                    "truncation_lowest_conduction": lowest.to_json(),
                    "truncation_edge_lowest_conduction": edge_lowest.to_json(),
                    "within_reported_cutoff": bool(within_reported_cutoff),
                }
            )
        return {
            "grid_size": grid.size,
            "point_count": len(grid.points),
            "edge_window_ev": self._policy.edge_window_ev,
            "edge_point_count": int(np.count_nonzero(edge_mask)),
            "effective_representative_count": len(operator.representatives),
            "maximum_representative_radius_angstrom": float(np.max(radii)),
            "reported_cutoff_lattice_parameters": (
                self._policy.reported_locality_cutoff_lattice_parameters
            ),
            "reported_cutoff_radius_angstrom": reported_cutoff_radius,
            "shells": records,
            "interpretation": (
                "within-candidate truncation sensitivity only; no locality pass/fail "
                "threshold is applied"
            ),
        }


class UntruncatedOperatorCharacterization:
    """Orchestrate the authorized execution-free S30 characterization."""

    __slots__ = ("_policy",)

    def __init__(self, policy: QualificationPolicy) -> None:
        self._policy = policy

    def execute(self) -> JsonObject:
        authenticator = ArtifactAuthenticator()
        structure = authenticator.execute(ARTIFACTS["structure"])
        eigenvalues = authenticator.execute(ARTIFACTS["eig"])
        lattice = SiliconLattice.from_structure(structure.path)
        loader = CandidateOperatorLoader(authenticator, eigenvalues)
        candidate = loader.execute(ELIGIBLE_DECLARATION)
        dense_grid = ReciprocalGrid.gamma_origin(self._policy.dense_grid_size)
        locality_grid = ReciprocalGrid.gamma_origin(self._policy.locality_grid_size)
        candidate_dense = candidate.finite_operator.eigenvalues(dense_grid.points)
        source_reconstruction = SourceReconstructionAnalyzer(self._policy).execute(
            candidate
        )
        real_space_hermiticity = candidate.finite_operator.real_space_hermiticity(
            self._policy.real_space_pair_hermiticity_maximum_ev
        )
        valley_family, valleys = ValleyFamilyAnalyzer(lattice, self._policy).execute(
            candidate.finite_operator, dense_grid, candidate_dense
        )
        effective_masses = EffectiveMassAnalyzer(lattice, self._policy).execute(
            candidate.finite_operator, valleys
        )
        locality = LocalityAnalyzer(lattice, self._policy).execute(
            candidate.finite_operator, locality_grid
        )
        sections: JsonObject = {
            "real_space_hermiticity": real_space_hermiticity,
            "source_reconstruction": source_reconstruction,
            "valley_family": valley_family,
            "effective_mass_diagnostic": effective_masses,
            "locality": locality,
        }
        structural_verification_passed = bool(
            source_reconstruction["structural_verification_passed"]
            and real_space_hermiticity["passed"]
        )
        sources: JsonObject = {
            structure.label: structure.to_json(),
            eigenvalues.label: eigenvalues.to_json(),
        }
        for artifact in candidate.artifacts:
            sources[artifact.label] = artifact.to_json()
        return {
            "schema_version": 1,
            "status": "S30-untruncated-characterization-complete",
            "calculator_invocations": 0,
            "stage_id": "S30-untruncated-characterization",
            "route": "C6-B20-W21-aiida-precise",
            "implementation_disposition": (
                "calculation-local object-oriented prototype; migrate reusable "
                "domain objects before merge"
            ),
            "sources": sources,
            "lattice": {
                "direct_basis_columns_angstrom": (
                    lattice.direct.primitive_basis_matrix.tolist()
                ),
                "reciprocal_basis_columns_inverse_angstrom": (
                    lattice.reciprocal.primitive_basis_matrix.tolist()
                ),
                "lattice_parameter_angstrom": lattice.lattice_parameter_angstrom,
            },
            "policy": self._policy.to_json(),
            "operator_inventory": {
                "construction_kpoint_count": 216,
                "parent_band_count": 20,
                "wannier_rank": candidate.native_wannier_count,
                "native_representative_count": (candidate.native_representative_count),
                "effective_ws_representative_count": len(
                    candidate.finite_operator.representatives
                ),
                "spatial_truncation_applied": False,
            },
            "results": sections,
            "structural_reconstruction_verified": structural_verification_passed,
            "scientific_qualification_status": "not-assessed",
            "scientific_disposition": (
                "provider-eligible full untruncated operator characterized; S40 "
                "revealed-408 development comparison remains separate"
            ),
            "nonclaims": [
                "No Quantum ESPRESSO or Wannier90 process was invoked.",
                (
                    "Dense-grid values are finite Wannier interpolation, not "
                    "independent parent data."
                ),
                (
                    "Curvature-derived masses are descriptive candidate predictions, "
                    "not validated silicon effective masses."
                ),
                (
                    "Structural reconstruction and descriptive self-consistency do "
                    "not certify a global Wannier minimum."
                ),
                "No spatial truncation or Slater-Koster reduction was applied.",
                "The frozen 402-point confirmation values remain unobserved.",
            ],
        }


ARTIFACTS = {
    "structure": ArtifactIdentity(
        "structure",
        STRUCTURE,
        758,
        "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
    ),
    "eig": ArtifactIdentity(
        "eig",
        INTERFACE_EVIDENCE / "silicon.eig",
        168480,
        "a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2",
    ),
}
ELIGIBLE_DECLARATION = CandidateArtifactDeclaration(
    label="C6-B20-W21-aiida-precise-eligible",
    hamiltonian=ArtifactIdentity(
        "eligible_hr",
        ELIGIBLE_EXTERNAL / "silicon_hr.dat",
        1396475,
        "24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55",
    ),
    gauge=ArtifactIdentity(
        "eligible_u",
        ELIGIBLE_EXTERNAL / "silicon_u.mat",
        679824,
        "41758b721b79cae233689b4fb9fa359e750b82da8ed5bcd13b1d5faf3c5d8bf3",
    ),
    disentanglement=ArtifactIdentity(
        "eligible_u_dis",
        ELIGIBLE_EXTERNAL / "silicon_u_dis.mat",
        1349424,
        "3c1d3574f3bf783cf7b54d8e9fd00fa5811ef05a56240850d46f43a2c95b7ace",
    ),
    ws_vectors=ArtifactIdentity(
        "eligible_wsvec",
        ELIGIBLE_EXTERNAL / "silicon_wsvec.dat",
        1365185,
        "f40fa7f81afaa9bcf9614c6e3c53c14db0db6b0b429b84bfd10f2e40474de1a0",
    ),
)


def main() -> None:
    result = UntruncatedOperatorCharacterization(QualificationPolicy()).execute()
    (ROOT / "characterization-result.json").write_bytes(
        TypedJsonMappingSerializer().serialize(result)
    )
    if result["structural_reconstruction_verified"] is not True:
        raise RuntimeError("S30 structural reconstruction gate failed")


if __name__ == "__main__":
    main()
