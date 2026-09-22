"""Run independently separated continuum-refinement axes for the synthetic 1D defect."""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type IntegerVector = npt.NDArray[np.int64]
type ProfileFamily = str


@dataclass(frozen=True, slots=True)
class SourceIdentity:
    """Identify one immutable source artifact."""

    path: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.path or len(self.sha256) != 64:
            raise ValueError("source identity is invalid")


@dataclass(frozen=True, slots=True)
class RepresentedContract:
    """Define units, basis, reference, and profile normalizations."""

    reference_lattice_period: float
    length_unit: str
    energy_unit: str
    basis: str
    energy_reference: str
    fixed_integrated_magnitude: float
    fixed_peak_magnitude: float

    def __post_init__(self) -> None:
        if (
            self.reference_lattice_period <= 0.0
            or not self.length_unit
            or not self.energy_unit
            or not self.basis
            or not self.energy_reference
            or self.fixed_integrated_magnitude <= 0.0
            or self.fixed_peak_magnitude <= 0.0
        ):
            raise ValueError("represented contract is invalid")


@dataclass(frozen=True, slots=True)
class ComparisonContract:
    """Own frozen numerical and crossover criteria."""

    physical_low_momentum_cutoff: float
    brillouin_edge_fraction: float
    bound_state_edge_margin: float
    continuum_mesh_binding_tolerance: float
    continuum_mesh_projector_tolerance: float
    finite_domain_binding_tolerance: float
    finite_domain_boundary_probability_tolerance: float
    lattice_supercell_binding_tolerance: float
    lattice_supercell_boundary_probability_tolerance: float
    relative_binding_tolerance: float
    projector_frobenius_tolerance: float
    compressed_operator_tolerance: float
    cross_coupling_tolerance: float
    brillouin_edge_weight_tolerance: float
    require_equal_bound_state_count: bool

    def __post_init__(self) -> None:
        numeric = (
            self.physical_low_momentum_cutoff,
            self.brillouin_edge_fraction,
            self.bound_state_edge_margin,
            self.continuum_mesh_binding_tolerance,
            self.continuum_mesh_projector_tolerance,
            self.finite_domain_binding_tolerance,
            self.finite_domain_boundary_probability_tolerance,
            self.lattice_supercell_binding_tolerance,
            self.lattice_supercell_boundary_probability_tolerance,
            self.relative_binding_tolerance,
            self.projector_frobenius_tolerance,
            self.compressed_operator_tolerance,
            self.cross_coupling_tolerance,
            self.brillouin_edge_weight_tolerance,
        )
        if any(value <= 0.0 or not np.isfinite(value) for value in numeric):
            raise ValueError("comparison tolerances must be finite and positive")
        if self.brillouin_edge_fraction >= 0.5:
            raise ValueError("Brillouin edge fraction must be below one half")


@dataclass(frozen=True, slots=True)
class ExperimentInput:
    """Represent every frozen refinement axis."""

    experiment_id: str
    sources: tuple[SourceIdentity, ...]
    represented: RepresentedContract
    mesh_domain: float
    mesh_width: float
    mesh_family: ProfileFamily
    mesh_counts: tuple[int, ...]
    domain_width: float
    domain_family: ProfileFamily
    domain_spacing: float
    domain_lengths: tuple[float, ...]
    supercell_spacing: float
    supercell_width: float
    supercell_family: ProfileFamily
    supercell_counts: tuple[int, ...]
    scale_domain: float
    scale_width: float
    scale_family: ProfileFamily
    scale_spacings: tuple[float, ...]
    profile_domain: float
    profile_spacing: float
    profile_widths: tuple[float, ...]
    profile_families: tuple[ProfileFamily, ...]
    comparison: ComparisonContract

    def __post_init__(self) -> None:
        if not self.experiment_id or len(self.sources) != 3:
            raise ValueError("experiment identity or sources are invalid")
        for values in (self.mesh_counts, self.supercell_counts):
            if not values or any(value < 8 or value % 2 for value in values):
                raise ValueError("mode and cell counts must be positive even values")
        if tuple(sorted(self.mesh_counts)) != self.mesh_counts:
            raise ValueError("mesh counts must be strictly ordered")
        if tuple(sorted(self.supercell_counts)) != self.supercell_counts:
            raise ValueError("supercell counts must be strictly ordered")
        if tuple(sorted(self.domain_lengths)) != self.domain_lengths:
            raise ValueError("domain lengths must be strictly ordered")
        if tuple(sorted(self.profile_widths)) != self.profile_widths:
            raise ValueError("profile widths must be strictly ordered")
        if tuple(sorted(self.scale_spacings, reverse=True)) != self.scale_spacings:
            raise ValueError("lattice spacings must be ordered coarse to fine")
        if self.profile_families != ("fixed-integrated", "fixed-peak"):
            raise ValueError("profile families are not the frozen pair")
        positive = (
            self.mesh_domain,
            self.mesh_width,
            self.domain_width,
            self.domain_spacing,
            self.supercell_spacing,
            self.supercell_width,
            self.scale_domain,
            self.scale_width,
            self.profile_domain,
            self.profile_spacing,
            *self.domain_lengths,
            *self.scale_spacings,
            *self.profile_widths,
        )
        if any(value <= 0.0 or not np.isfinite(value) for value in positive):
            raise ValueError("refinement values must be finite and positive")


@dataclass(frozen=True, slots=True)
class ParentRecord:
    """Retain the accepted scalar parent as an immutable represented dispersion."""

    displacements: IntegerVector
    hoppings: ComplexVector
    lower_edge: float
    parabolic_coefficient: float

    def __post_init__(self) -> None:
        displacements = np.asarray(self.displacements, dtype=np.int64)
        hoppings = np.asarray(self.hoppings, dtype=np.complex128)
        if (
            displacements.ndim != 1
            or hoppings.shape != displacements.shape
            or displacements.size < 3
            or not np.all(np.isfinite(hoppings))
            or not np.isfinite(self.lower_edge)
            or self.parabolic_coefficient <= 0.0
        ):
            raise ValueError("parent record is invalid")
        immutable_r = np.frombuffer(displacements.tobytes(), dtype=np.int64)
        immutable_t = np.frombuffer(hoppings.tobytes(), dtype=np.complex128)
        object.__setattr__(self, "displacements", immutable_r)
        object.__setattr__(self, "hoppings", immutable_t)


@dataclass(frozen=True, slots=True)
class SpectrumResult:
    """Record the lowest state and all below-edge eigenvalues."""

    energy: float
    binding: float
    bound_count: int
    state: ComplexVector
    boundary_probability: float

    def __post_init__(self) -> None:
        state = np.asarray(self.state, dtype=np.complex128)
        if (
            state.ndim != 1
            or not np.all(np.isfinite(state))
            or not np.isfinite(self.energy)
            or self.binding < 0.0
            or self.bound_count < 0
            or not 0.0 <= self.boundary_probability <= 1.0
        ):
            raise ValueError("spectrum result is invalid")
        immutable = np.frombuffer(state.tobytes(), dtype=np.complex128)
        object.__setattr__(self, "state", immutable)


class JsonRecordParser:
    """Parse the closed version-1 refinement input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExperimentInput:
        root = self._mapping(cast(JsonValue, json.loads(payload)), "input")
        if self._integer(root["schema_version"], "schema version") != 1:
            raise ValueError("unsupported schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        sources = tuple(
            SourceIdentity(
                self._string(item["path"], "source path"),
                self._string(item["sha256"], "source sha256"),
            )
            for item in self._records(root["source_identities"], "sources")
        )
        represented = self._mapping(root["represented_contract"], "represented")
        mesh = self._mapping(root["continuum_mesh_axis"], "mesh")
        domain = self._mapping(root["continuum_domain_axis"], "domain")
        supercell = self._mapping(root["lattice_supercell_axis"], "supercell")
        scale = self._mapping(root["lattice_scale_axis"], "scale")
        profile = self._mapping(root["profile_width_axis"], "profile")
        comparison = self._mapping(root["comparison_contract"], "comparison")
        return ExperimentInput(
            self._string(root["experiment_id"], "experiment id"),
            sources,
            RepresentedContract(
                self._real(represented["reference_lattice_period"], "period"),
                self._string(represented["length_unit"], "length unit"),
                self._string(represented["energy_unit"], "energy unit"),
                self._string(represented["basis"], "basis"),
                self._string(represented["energy_reference"], "energy reference"),
                self._real(
                    represented["fixed_integrated_magnitude"], "integrated magnitude"
                ),
                self._real(represented["fixed_peak_magnitude"], "peak magnitude"),
            ),
            self._real(mesh["domain_length"], "mesh domain"),
            self._real(mesh["profile_width"], "mesh width"),
            self._string(mesh["profile_family"], "mesh family"),
            self._integers(mesh["mode_counts"], "mesh counts"),
            self._real(domain["profile_width"], "domain width"),
            self._string(domain["profile_family"], "domain family"),
            self._real(domain["spectral_spacing"], "domain spacing"),
            self._reals(domain["domain_lengths"], "domain lengths"),
            self._real(supercell["lattice_spacing"], "supercell spacing"),
            self._real(supercell["profile_width"], "supercell width"),
            self._string(supercell["profile_family"], "supercell family"),
            self._integers(supercell["cell_counts"], "supercell counts"),
            self._real(scale["domain_length"], "scale domain"),
            self._real(scale["profile_width"], "scale width"),
            self._string(scale["profile_family"], "scale family"),
            self._reals(scale["lattice_spacings"], "scale spacings"),
            self._real(profile["domain_length"], "profile domain"),
            self._real(profile["lattice_spacing"], "profile spacing"),
            self._reals(profile["widths"], "profile widths"),
            self._strings(profile["families"], "profile families"),
            ComparisonContract(
                self._real(comparison["physical_low_momentum_cutoff"], "cutoff"),
                self._real(comparison["brillouin_edge_fraction"], "edge fraction"),
                self._real(comparison["bound_state_edge_margin"], "edge margin"),
                self._real(
                    comparison["continuum_mesh_binding_tolerance"],
                    "mesh binding tolerance",
                ),
                self._real(
                    comparison["continuum_mesh_projector_tolerance"],
                    "mesh projector tolerance",
                ),
                self._real(
                    comparison["finite_domain_binding_tolerance"],
                    "domain binding tolerance",
                ),
                self._real(
                    comparison["finite_domain_boundary_probability_tolerance"],
                    "domain boundary tolerance",
                ),
                self._real(
                    comparison["lattice_supercell_binding_tolerance"],
                    "supercell binding tolerance",
                ),
                self._real(
                    comparison["lattice_supercell_boundary_probability_tolerance"],
                    "supercell boundary tolerance",
                ),
                self._real(
                    comparison["relative_binding_tolerance"],
                    "relative binding tolerance",
                ),
                self._real(
                    comparison["projector_frobenius_tolerance"],
                    "projector tolerance",
                ),
                self._real(
                    comparison["compressed_operator_tolerance"],
                    "operator tolerance",
                ),
                self._real(comparison["cross_coupling_tolerance"], "cross tolerance"),
                self._real(
                    comparison["brillouin_edge_weight_tolerance"],
                    "edge weight tolerance",
                ),
                self._boolean(
                    comparison["require_equal_bound_state_count"],
                    "count requirement",
                ),
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, field: str) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{field} must be an object")
        return value

    @classmethod
    def _records(cls, value: JsonValue, field: str) -> tuple[dict[str, JsonValue], ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._mapping(item, field) for item in value)

    @staticmethod
    def _string(value: JsonValue, field: str) -> str:
        if type(value) is not str or not value:
            raise TypeError(f"{field} must be a nonempty string")
        return value

    @classmethod
    def _strings(cls, value: JsonValue, field: str) -> tuple[str, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._string(item, field) for item in value)

    @staticmethod
    def _integer(value: JsonValue, field: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{field} must be an int excluding bool")
        return value

    @classmethod
    def _integers(cls, value: JsonValue, field: str) -> tuple[int, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._integer(item, field) for item in value)

    @staticmethod
    def _real(value: JsonValue, field: str) -> float:
        if type(value) is int:
            result = float(value)
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{field} must be a real number excluding bool")
        if not np.isfinite(result):
            raise ValueError(f"{field} must be finite")
        return result

    @classmethod
    def _reals(cls, value: JsonValue, field: str) -> tuple[float, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._real(item, field) for item in value)

    @staticmethod
    def _boolean(value: JsonValue, field: str) -> bool:
        if type(value) is not bool:
            raise TypeError(f"{field} must be bool")
        return value


class ParentRecordLoader:
    """Verify source identities and load the accepted scalar parent."""

    __slots__ = ()

    def execute(self, repository_root: Path, config: ExperimentInput) -> ParentRecord:
        values: dict[str, JsonValue] | None = None
        for source in config.sources:
            path = repository_root / source.path
            payload = path.read_bytes()
            if hashlib.sha256(payload).hexdigest() != source.sha256:
                raise ValueError(f"source identity mismatch: {source.path}")
            if source.path.endswith("periodic-1d/result.json"):
                parsed = cast(JsonValue, json.loads(payload))
                values = JsonRecordParser._mapping(parsed, "periodic result")
        if values is None:
            raise ValueError("periodic parent source is missing")
        reduction = JsonRecordParser._mapping(
            values["isolated_band_reduction"], "isolated reduction"
        )
        representatives = JsonRecordParser._integers(
            reduction["hopping_representatives_cells"], "displacements"
        )
        encoded = reduction["hopping_coefficients"]
        if type(encoded) is not list:
            raise TypeError("hopping coefficients must be an array")
        coefficients: list[complex] = []
        for item in encoded:
            if type(item) is not list or len(item) != 2:
                raise TypeError("hopping coefficient must be a real-imaginary pair")
            coefficients.append(
                complex(
                    JsonRecordParser._real(item[0], "hopping real"),
                    JsonRecordParser._real(item[1], "hopping imaginary"),
                )
            )
        displacements = np.asarray(representatives, dtype=np.int64)
        hoppings = np.asarray(coefficients, dtype=np.complex128)
        lower_edge = float(np.real(np.sum(hoppings)))
        coefficient = float(
            np.real(-0.5 * np.sum((2.0 * np.pi * displacements) ** 2 * hoppings))
        )
        return ParentRecord(displacements, hoppings, lower_edge, coefficient)


class RepresentedHamiltonianBuilder:
    """Construct compatible continuum and scaled-lattice Fourier matrices."""

    __slots__ = ("_contract", "_parent")

    def __init__(self, parent: ParentRecord, contract: RepresentedContract) -> None:
        self._parent = parent
        self._contract = contract

    @staticmethod
    def modes(count: int) -> IntegerVector:
        """Return centered integer Fourier-mode labels."""
        return np.arange(-count // 2, count // 2, dtype=np.int64)

    def continuum(
        self, count: int, length: float, width: float, family: ProfileFamily
    ) -> ComplexMatrix:
        """Construct a spectral continuum representation with exact coefficients."""
        modes = self.modes(count)
        wave_numbers = modes.astype(np.float64) / length
        kinetic = self._parent.lower_edge + self._parent.parabolic_coefficient * (
            wave_numbers**2
        )
        differences = modes[:, None] - modes[None, :]
        exponent = (
            -2.0 * np.pi**2 * width**2 * (differences.astype(np.float64) / length) ** 2
        )
        if family == "fixed-integrated":
            prefactor = -self._contract.fixed_integrated_magnitude / length
        elif family == "fixed-peak":
            prefactor = (
                -self._contract.fixed_peak_magnitude
                * np.sqrt(2.0 * np.pi)
                * width
                / length
            )
        else:
            raise ValueError(f"unsupported profile family {family}")
        matrix = np.diag(kinetic).astype(np.complex128)
        matrix += prefactor * np.exp(exponent)
        self._check_hermitian(matrix)
        return matrix

    def lattice(
        self, count: int, spacing: float, width: float, family: ProfileFamily
    ) -> ComplexMatrix:
        """Construct the scaled lattice representation in the same Fourier ordering."""
        length = count * spacing
        modes = self.modes(count)
        physical_wave_numbers = modes.astype(np.float64) / length
        reduced_momenta = spacing * physical_wave_numbers
        phases = np.exp(
            2j * np.pi * reduced_momenta[:, None] * self._parent.displacements[None, :]
        )
        base_dispersion = np.real(phases @ self._parent.hoppings)
        kinetic = (
            self._parent.lower_edge
            + (base_dispersion - self._parent.lower_edge) / spacing**2
        )
        potential = self._sampled_profile(count, spacing, width, family)
        coefficients = np.fft.fft(potential) / count
        differences = (modes[:, None] - modes[None, :]) % count
        matrix = np.diag(kinetic).astype(np.complex128)
        matrix += coefficients[differences]
        self._check_hermitian(matrix)
        return matrix

    def _sampled_profile(
        self, count: int, spacing: float, width: float, family: ProfileFamily
    ) -> RealVector:
        length = count * spacing
        positions = spacing * np.arange(count, dtype=np.float64)
        periodic = np.zeros(count, dtype=np.float64)
        for image in range(-4, 5):
            periodic += np.exp(-0.5 * ((positions + image * length) / width) ** 2)
        if family == "fixed-integrated":
            scale = -self._contract.fixed_integrated_magnitude / (
                np.sqrt(2.0 * np.pi) * width
            )
        elif family == "fixed-peak":
            scale = -self._contract.fixed_peak_magnitude
        else:
            raise ValueError(f"unsupported profile family {family}")
        return np.asarray(scale * periodic, dtype=np.float64)

    @staticmethod
    def _check_hermitian(matrix: ComplexMatrix) -> None:
        residual = float(np.max(np.abs(matrix - matrix.conj().T)))
        if residual > 1e-12 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"represented Hamiltonian is not Hermitian: {residual}")


class SpectrumAnalyzer:
    """Resolve finite spectra and localization diagnostics."""

    __slots__ = ("_edge", "_margin")

    def __init__(self, edge: float, margin: float) -> None:
        self._edge = edge
        self._margin = margin

    def execute(self, matrix: ComplexMatrix, length: float) -> SpectrumResult:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        state = np.asarray(eigenvectors[:, 0], dtype=np.complex128)
        energy = float(eigenvalues[0])
        binding = max(0.0, self._edge - energy)
        bound_count = int(np.count_nonzero(eigenvalues < self._edge - self._margin))
        boundary = self._boundary_probability(state, length)
        return SpectrumResult(energy, binding, bound_count, state, boundary)

    @staticmethod
    def _boundary_probability(state: ComplexVector, length: float) -> float:
        count = state.size
        modes = RepresentedHamiltonianBuilder.modes(count)
        points = np.arange(count, dtype=np.float64)
        transform = np.exp(2j * np.pi * np.outer(points, modes) / count) / np.sqrt(
            count
        )
        real_state = transform @ state
        distances = np.minimum(
            points * length / count, length - points * length / count
        )
        return float(np.sum(np.abs(real_state[distances >= length / 4.0]) ** 2))


class StateComparator:
    """Compare one-dimensional projectors across compatible Fourier label sets."""

    __slots__ = ()

    def execute(
        self,
        left: ComplexVector,
        left_modes: IntegerVector,
        right: ComplexVector,
        right_modes: IntegerVector,
    ) -> float:
        right_by_mode = {
            int(mode): right[index] for index, mode in enumerate(right_modes)
        }
        overlap = sum(
            np.conj(left[index]) * right_by_mode.get(int(mode), 0.0j)
            for index, mode in enumerate(left_modes)
        )
        left_norm = float(np.vdot(left, left).real)
        right_norm = float(np.vdot(right, right).real)
        fidelity = min(
            1.0,
            max(0.0, float(abs(overlap) ** 2 / (left_norm * right_norm))),
        )
        return float(np.sqrt(2.0 * (1.0 - fidelity)))


class OperatorDifferenceAnalyzer:
    """Analyze compatible lattice-minus-continuum represented differences."""

    __slots__ = ("_cutoff", "_edge_fraction")

    def __init__(self, cutoff: float, edge_fraction: float) -> None:
        self._cutoff = cutoff
        self._edge_fraction = edge_fraction

    def execute(
        self,
        lattice: ComplexMatrix,
        continuum: ComplexMatrix,
        state: ComplexVector,
        length: float,
        spacing: float,
    ) -> tuple[float, float, float]:
        if lattice.shape != continuum.shape:
            raise ValueError(
                "operator comparison requires equal represented dimensions"
            )
        modes = RepresentedHamiltonianBuilder.modes(lattice.shape[0])
        wave_numbers = modes.astype(np.float64) / length
        low = np.abs(wave_numbers) <= self._cutoff
        high = ~low
        difference = lattice - continuum
        compressed = difference[np.ix_(low, low)]
        compressed_norm = float(np.max(np.abs(np.linalg.eigvalsh(compressed))))
        cross = difference[np.ix_(low, high)]
        cross_norm = (
            float(np.linalg.svd(cross, compute_uv=False)[0]) if cross.size else 0.0
        )
        edge = np.abs(spacing * wave_numbers) >= self._edge_fraction
        edge_weight = float(np.sum(np.abs(state[edge]) ** 2))
        return compressed_norm, cross_norm, edge_weight


class ContinuumRefinementRunner:
    """Execute the separated refinement axes and frozen crossover decisions."""

    __slots__ = ("_builder", "_config", "_operators", "_parent", "_spectrum", "_states")

    def __init__(self, config: ExperimentInput, parent: ParentRecord) -> None:
        self._config = config
        self._parent = parent
        self._builder = RepresentedHamiltonianBuilder(parent, config.represented)
        self._spectrum = SpectrumAnalyzer(
            parent.lower_edge, config.comparison.bound_state_edge_margin
        )
        self._states = StateComparator()
        self._operators = OperatorDifferenceAnalyzer(
            config.comparison.physical_low_momentum_cutoff,
            config.comparison.brillouin_edge_fraction,
        )

    def execute(self, input_sha256: str) -> dict[str, JsonValue]:
        mesh_records, mesh_pass = self._mesh_axis()
        domain_records, domain_pass = self._domain_axis()
        supercell_records, supercell_pass = self._supercell_axis()
        scale_records, scale_boundary = self._scale_axis()
        profile_families = self._profile_axis()
        support_pass = mesh_pass and domain_pass and supercell_pass
        family_boundaries: dict[str, JsonValue] = {}
        for family_value in profile_families:
            family = cast(dict[str, JsonValue], family_value)
            family_boundaries[cast(str, family["family"])] = family["crossover_width"]
        fixed_integrated = family_boundaries["fixed-integrated"]
        stable_comparison = support_pass and scale_boundary is not None
        profile_crossover = fixed_integrated is not None
        return {
            "schema_version": 1,
            "experiment_id": self._config.experiment_id,
            "calculation_status": "calculated synthetic numerical-verification result",
            "evidence_status": "synthetic test data",
            "represented_contract": {
                "basis": self._config.represented.basis,
                "length_unit": self._config.represented.length_unit,
                "energy_unit": self._config.represented.energy_unit,
                "energy_reference": self._config.represented.energy_reference,
                "operator_difference_order": "scaled lattice minus parabolic continuum",
                "parent_lower_edge": self._parent.lower_edge,
                "parabolic_coefficient": self._parent.parabolic_coefficient,
            },
            "continuum_mesh_axis": {
                "records": mesh_records,
                "latest_step_pass": mesh_pass,
            },
            "continuum_domain_axis": {
                "records": domain_records,
                "latest_step_pass": domain_pass,
            },
            "lattice_supercell_axis": {
                "records": supercell_records,
                "latest_step_pass": supercell_pass,
            },
            "lattice_scale_axis": {
                "records": scale_records,
                "largest_spacing_with_persistent_pass": scale_boundary,
            },
            "profile_width_axis": {"families": profile_families},
            "crossover_assessment": {
                "supporting_axes_pass": support_pass,
                "fixed_integrated_crossover_width": fixed_integrated,
                "fixed_peak_crossover_width": family_boundaries["fixed-peak"],
                "lattice_scale_persistent_pass_spacing": scale_boundary,
                "stable_lattice_scale_comparison": stable_comparison,
                "profile_defined_crossover_established": profile_crossover,
                "interpretation": (
                    "The lattice-scale sequence has a persistent bounded pass under "
                    "the frozen criteria, while neither profile-width family defines "
                    "a crossover because at least one separate criterion continues "
                    "to fail. This is not an infinite-volume theorem, material "
                    "validation, or uncertainty quantification."
                    if stable_comparison and not profile_crossover
                    else (
                        "A bounded synthetic comparison and profile-defined crossover "
                        "are established only for the frozen represented problem."
                        if stable_comparison
                        else (
                            "No bounded continuum comparison satisfies every frozen "
                            "criterion."
                        )
                    )
                ),
            },
            "error_accounting": {
                "continuum_discretization": (
                    "isolated by mode-count refinement at fixed domain and profile"
                ),
                "finite_domain": (
                    "isolated by continuum-domain refinement at fixed spectral "
                    "spacing and profile"
                ),
                "periodic_image": (
                    "isolated by lattice-supercell refinement at fixed lattice "
                    "spacing and profile"
                ),
                "lattice_scale": (
                    "isolated by scaling the accepted dispersion at fixed physical "
                    "domain and profile"
                ),
                "profile_model": (
                    "fixed-integrated and fixed-peak width families remain separate"
                ),
                "operator_model": (
                    "compressed and cross-block lattice-minus-continuum residuals "
                    "remain separate"
                ),
                "spectral_and_state": (
                    "binding, bound-state count, projector defect, and "
                    "Brillouin-edge weight remain separate"
                ),
                "scientific_validation": "not performed",
                "uncertainty_quantification": "not performed",
            },
            "literature_map": [
                {
                    "limit": "finite-rank impurity resolvent",
                    "references": ["Koster and Slater (1954)"],
                    "applicability": "method precedent, not a continuum result",
                },
                {
                    "limit": "weak slowly varying band-edge homogenization",
                    "references": [
                        "Hoefer and Weinstein (2011)",
                        "Duchene, Vukicevic, and Weinstein (2015)",
                    ],
                    "applicability": (
                        "motivates the scale-separated envelope comparison; theorem "
                        "hypotheses are not claimed for this finite synthetic parent"
                    ),
                },
                {
                    "limit": "discrete-to-continuum norm-resolvent convergence",
                    "references": ["Nakamura and Tadano (2021)"],
                    "applicability": (
                        "motivates explicit changing-space and lattice-scale control; "
                        "no theorem is reproduced"
                    ),
                },
                {
                    "limit": "finite-volume bound-state effects",
                    "references": ["Koenig, Lee, and Hammer (2011)"],
                    "applicability": (
                        "general precedent only; the represented one-dimensional "
                        "image law is measured directly"
                    ),
                },
                {
                    "limit": "semiconductor effective-mass and central-cell boundary",
                    "references": [
                        "Kohn and Luttinger (1955)",
                        "Gamble et al. (2015)",
                    ],
                    "applicability": (
                        "scope boundary only; no silicon or multivalley calculation "
                        "is performed"
                    ),
                },
            ],
            "limitations": [
                (
                    "The accepted isolated-band parent is a finite represented "
                    "synthetic model."
                ),
                (
                    "A profile-width crossover changes the defect family and is not "
                    "itself a continuum limit."
                ),
                (
                    "The lattice-scale sequence is finite and does not prove "
                    "asymptotic convergence."
                ),
                "Only the lowest nondegenerate bound-state projector is compared.",
                (
                    "No silicon, dopant, DFT, production Wannier, scientific "
                    "validation, transferability, or UQ claim is made."
                ),
            ],
            "provenance": {
                "input_sha256": input_sha256,
                "implementation_identities": [
                    {
                        "path": (
                            "calculations/research-monograph/"
                            "impurity-defect-1d-continuum-refinement/"
                            "continuum_refinement_calculation/run_experiment.py"
                        ),
                        "sha256": hashlib.sha256(
                            Path(__file__).resolve().read_bytes()
                        ).hexdigest(),
                    }
                ],
                "source_identities": [
                    {"path": source.path, "sha256": source.sha256}
                    for source in self._config.sources
                ],
                "python": platform.python_version(),
                "numpy": np.__version__,
            },
        }

    def _mesh_axis(self) -> tuple[list[JsonValue], bool]:
        spectra: list[SpectrumResult] = []
        matrices: list[ComplexMatrix] = []
        for count in self._config.mesh_counts:
            matrix = self._builder.continuum(
                count,
                self._config.mesh_domain,
                self._config.mesh_width,
                self._config.mesh_family,
            )
            matrices.append(matrix)
            spectra.append(self._spectrum.execute(matrix, self._config.mesh_domain))
        reference = spectra[-1]
        reference_modes = self._builder.modes(self._config.mesh_counts[-1])
        records: list[JsonValue] = []
        for count, matrix, spectrum in zip(
            self._config.mesh_counts, matrices, spectra, strict=True
        ):
            defect = self._states.execute(
                spectrum.state,
                self._builder.modes(count),
                reference.state,
                reference_modes,
            )
            records.append(
                {
                    "mode_count": count,
                    "spectral_spacing": self._config.mesh_domain / count,
                    "binding_energy": spectrum.binding,
                    "bound_state_count": spectrum.bound_count,
                    "boundary_probability": spectrum.boundary_probability,
                    "binding_defect_from_finest": abs(
                        spectrum.binding - reference.binding
                    ),
                    "projector_defect_from_finest": defect,
                    "operator_sha256": self._matrix_sha256(matrix),
                }
            )
        previous = spectra[-2]
        latest_defect = self._states.execute(
            previous.state,
            self._builder.modes(self._config.mesh_counts[-2]),
            reference.state,
            reference_modes,
        )
        passed = (
            abs(previous.binding - reference.binding)
            <= self._config.comparison.continuum_mesh_binding_tolerance
            and latest_defect
            <= self._config.comparison.continuum_mesh_projector_tolerance
        )
        return records, passed

    def _domain_axis(self) -> tuple[list[JsonValue], bool]:
        spectra: list[SpectrumResult] = []
        records: list[JsonValue] = []
        for length in self._config.domain_lengths:
            count = round(length / self._config.domain_spacing)
            matrix = self._builder.continuum(
                count, length, self._config.domain_width, self._config.domain_family
            )
            spectrum = self._spectrum.execute(matrix, length)
            spectra.append(spectrum)
            records.append(
                {
                    "domain_length": length,
                    "mode_count": count,
                    "binding_energy": spectrum.binding,
                    "bound_state_count": spectrum.bound_count,
                    "boundary_probability": spectrum.boundary_probability,
                    "operator_sha256": self._matrix_sha256(matrix),
                }
            )
        reference = spectra[-1]
        for record, spectrum in zip(records, spectra, strict=True):
            cast(dict[str, JsonValue], record)["binding_defect_from_largest_domain"] = (
                abs(spectrum.binding - reference.binding)
            )
        passed = (
            abs(spectra[-2].binding - spectra[-1].binding)
            <= self._config.comparison.finite_domain_binding_tolerance
            and spectra[-1].boundary_probability
            <= self._config.comparison.finite_domain_boundary_probability_tolerance
        )
        return records, passed

    def _supercell_axis(self) -> tuple[list[JsonValue], bool]:
        spectra: list[SpectrumResult] = []
        records: list[JsonValue] = []
        for count in self._config.supercell_counts:
            length = count * self._config.supercell_spacing
            matrix = self._builder.lattice(
                count,
                self._config.supercell_spacing,
                self._config.supercell_width,
                self._config.supercell_family,
            )
            spectrum = self._spectrum.execute(matrix, length)
            spectra.append(spectrum)
            records.append(
                {
                    "cell_count": count,
                    "domain_length": length,
                    "binding_energy": spectrum.binding,
                    "bound_state_count": spectrum.bound_count,
                    "boundary_probability": spectrum.boundary_probability,
                    "operator_sha256": self._matrix_sha256(matrix),
                }
            )
        reference = spectra[-1]
        for record, spectrum in zip(records, spectra, strict=True):
            cast(dict[str, JsonValue], record)[
                "binding_defect_from_largest_supercell"
            ] = abs(spectrum.binding - reference.binding)
        passed = (
            abs(spectra[-2].binding - spectra[-1].binding)
            <= self._config.comparison.lattice_supercell_binding_tolerance
            and spectra[-1].boundary_probability
            <= self._config.comparison.lattice_supercell_boundary_probability_tolerance
        )
        return records, passed

    def _scale_axis(self) -> tuple[list[JsonValue], JsonValue]:
        records: list[JsonValue] = []
        for spacing in self._config.scale_spacings:
            count = round(self._config.scale_domain / spacing)
            lattice = self._builder.lattice(
                count, spacing, self._config.scale_width, self._config.scale_family
            )
            continuum = self._builder.continuum(
                count,
                self._config.scale_domain,
                self._config.scale_width,
                self._config.scale_family,
            )
            lattice_spectrum = self._spectrum.execute(
                lattice, self._config.scale_domain
            )
            continuum_spectrum = self._spectrum.execute(
                continuum, self._config.scale_domain
            )
            records.append(
                self._comparison_record(
                    lattice,
                    continuum,
                    lattice_spectrum,
                    continuum_spectrum,
                    self._config.scale_domain,
                    spacing,
                    {"lattice_spacing": spacing, "site_count": count},
                )
            )
        boundary: JsonValue = None
        for index, record in enumerate(records):
            if all(
                bool(cast(dict[str, JsonValue], later)["all_criteria_pass"])
                for later in records[index:]
            ):
                boundary = cast(dict[str, JsonValue], record)["lattice_spacing"]
                break
        return records, boundary

    def _profile_axis(self) -> list[JsonValue]:
        count = round(self._config.profile_domain / self._config.profile_spacing)
        families: list[JsonValue] = []
        for family in self._config.profile_families:
            records: list[JsonValue] = []
            for width in self._config.profile_widths:
                lattice = self._builder.lattice(
                    count, self._config.profile_spacing, width, family
                )
                continuum = self._builder.continuum(
                    count, self._config.profile_domain, width, family
                )
                lattice_spectrum = self._spectrum.execute(
                    lattice, self._config.profile_domain
                )
                continuum_spectrum = self._spectrum.execute(
                    continuum, self._config.profile_domain
                )
                records.append(
                    self._comparison_record(
                        lattice,
                        continuum,
                        lattice_spectrum,
                        continuum_spectrum,
                        self._config.profile_domain,
                        self._config.profile_spacing,
                        {"width": width},
                    )
                )
            crossover: JsonValue = None
            for index, record in enumerate(records):
                if all(
                    bool(cast(dict[str, JsonValue], later)["all_criteria_pass"])
                    for later in records[index:]
                ):
                    crossover = cast(dict[str, JsonValue], record)["width"]
                    break
            families.append(
                {"family": family, "records": records, "crossover_width": crossover}
            )
        return families

    def _comparison_record(
        self,
        lattice: ComplexMatrix,
        continuum: ComplexMatrix,
        lattice_spectrum: SpectrumResult,
        continuum_spectrum: SpectrumResult,
        length: float,
        spacing: float,
        identity: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        projector = self._states.execute(
            lattice_spectrum.state,
            self._builder.modes(lattice.shape[0]),
            continuum_spectrum.state,
            self._builder.modes(continuum.shape[0]),
        )
        compressed, cross, edge_weight = self._operators.execute(
            lattice, continuum, lattice_spectrum.state, length, spacing
        )
        binding_error = abs(lattice_spectrum.binding - continuum_spectrum.binding)
        relative = binding_error / max(continuum_spectrum.binding, np.finfo(float).tiny)
        count_equal = lattice_spectrum.bound_count == continuum_spectrum.bound_count
        criteria_bool = {
            "relative_binding": relative
            <= self._config.comparison.relative_binding_tolerance,
            "projector": projector
            <= self._config.comparison.projector_frobenius_tolerance,
            "compressed_operator": compressed
            <= self._config.comparison.compressed_operator_tolerance,
            "cross_coupling": cross <= self._config.comparison.cross_coupling_tolerance,
            "brillouin_edge_weight": edge_weight
            <= self._config.comparison.brillouin_edge_weight_tolerance,
            "bound_state_count": count_equal
            or not self._config.comparison.require_equal_bound_state_count,
        }
        criteria: dict[str, JsonValue] = dict(criteria_bool)
        return {
            **identity,
            "lattice_binding_energy": lattice_spectrum.binding,
            "continuum_binding_energy": continuum_spectrum.binding,
            "absolute_binding_error": binding_error,
            "relative_binding_error": relative,
            "lattice_bound_state_count": lattice_spectrum.bound_count,
            "continuum_bound_state_count": continuum_spectrum.bound_count,
            "projector_frobenius_defect": projector,
            "compressed_operator_spectral_norm": compressed,
            "cross_coupling_spectral_norm": cross,
            "brillouin_edge_weight": edge_weight,
            "criteria": criteria,
            "all_criteria_pass": all(criteria_bool.values()),
            "lattice_operator_sha256": self._matrix_sha256(lattice),
            "continuum_operator_sha256": self._matrix_sha256(continuum),
        }

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.asarray(matrix, dtype=np.complex128).copy()
        canonical.real = np.round(canonical.real, decimals=9)
        canonical.imag = np.round(canonical.imag, decimals=9)
        canonical.real[canonical.real == 0.0] = 0.0
        canonical.imag[canonical.imag == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


class JsonResultSerializer:
    """Serialize a finite JSON result deterministically."""

    __slots__ = ()

    def execute(self, value: dict[str, JsonValue]) -> bytes:
        return (
            json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")


class ContinuumRefinementWorkflow:
    """Load, execute, and serialize one continuum-refinement operation."""

    __slots__ = ()

    def execute(self, input_path: Path, output_path: Path) -> None:
        payload = input_path.read_bytes()
        config = JsonRecordParser().execute(payload)
        repository_root = input_path.parents[3]
        parent = ParentRecordLoader().execute(repository_root, config)
        result = ContinuumRefinementRunner(config, parent).execute(
            hashlib.sha256(payload).hexdigest()
        )
        output_path.write_bytes(JsonResultSerializer().execute(result))
