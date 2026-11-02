from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import numpy as np
from numpy.typing import NDArray
from scipy import constants  # type: ignore[import-untyped]
from scipy.optimize import linear_sum_assignment, minimize  # type: ignore[import-untyped]

RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
IntegerArray = NDArray[np.int64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[4]
REQUEST = ROOT / "request-v2.json"
OUTPUT = ROOT / "result-v2.json"
STATUS = "wannier-only-fidelity-ladder-producer-checked-development-not-independently-verified"
ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 = (
    constants.hbar**2 / constants.m_e / constants.electron_volt * 1.0e20
)


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


def authenticate_sources(request: JsonObject) -> JsonObject:
    authenticated: JsonObject = {}
    for label, declaration_value in mapping(request["sources"], "sources").items():
        declaration = mapping(declaration_value, label)
        path = source_path(declaration, label)
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"source absent or symlinked: {path}")
        observed = identity(path)
        expected_size = int(numeric(declaration["byte_size"], f"{label} size"))
        expected_digest = string(declaration["sha256"], f"{label} digest")
        if observed["byte_size"] != expected_size or observed["sha256"] != expected_digest:
            raise RuntimeError(f"source identity mismatch: {path}")
        authenticated[label] = observed
    return authenticated


def load_adapter(path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "c6_b20_w21_wannier_fidelity_adapter", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load authenticated native-HR adapter")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def gamma_grid(size: int) -> RealArray:
    axis = np.arange(size, dtype=np.float64) / float(size)
    return np.asarray(
        np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1).reshape(-1, 3),
        dtype=np.float64,
    )


def closest_gamma_cartesian(
    fractional: RealArray, reciprocal_basis: RealArray
) -> RealArray:
    shifts = np.asarray(
        [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)],
        dtype=np.float64,
    )
    cartesian = (fractional[None, :] + shifts) @ reciprocal_basis.T
    return np.asarray(
        cartesian[int(np.argmin(np.linalg.norm(cartesian, axis=1)))],
        dtype=np.float64,
    )


def periodic_cartesian_displacement(
    left: RealArray, right: RealArray, reciprocal_basis: RealArray
) -> RealArray:
    shifts = np.asarray(
        [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)],
        dtype=np.float64,
    )
    cartesian = (left[None, :] - right[None, :] + shifts) @ reciprocal_basis.T
    return np.asarray(
        cartesian[int(np.argmin(np.linalg.norm(cartesian, axis=1)))],
        dtype=np.float64,
    )


def expected_label(cartesian: RealArray) -> str:
    axis = int(np.argmax(np.abs(cartesian)))
    return ("+" if cartesian[axis] >= 0.0 else "-") + "xyz"[axis]


@dataclass(frozen=True, slots=True)
class FrozenModel:
    shell_id: str
    included_representative_count: int
    alpha: RealArray
    coefficients_ev: ComplexArray


@dataclass(frozen=True, slots=True)
class ValleyRecord:
    label: str
    fractional: RealArray
    cartesian: RealArray
    energy_ev: float
    optimizer_success: bool
    iterations: int
    local_bound_active: bool
    hessian_ev_angstrom_squared: RealArray
    principal_curvatures_ev_angstrom_squared: RealArray
    principal_axes_cartesian_columns: RealArray
    principal_masses_electron: RealArray


class CoefficientEvaluator:
    __slots__ = ("_coefficients", "_flat", "_rank", "_representatives")

    def __init__(
        self, representatives: IntegerArray, coefficients: ComplexArray
    ) -> None:
        self._representatives = representatives
        self._coefficients = coefficients
        self._rank = int(coefficients.shape[-1])
        self._flat = np.asarray(
            coefficients.transpose(1, 0, 2, 3).reshape(
                len(representatives), coefficients.shape[0] * self._rank * self._rank
            ),
            dtype=np.complex128,
        )

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def model_count(self) -> int:
        return int(self._coefficients.shape[0])

    def matrices(self, points: RealArray) -> ComplexArray:
        phases = np.exp(2.0j * np.pi * (points @ self._representatives.T))
        matrices = (phases @ self._flat).reshape(
            len(points), self.model_count, self.rank, self.rank
        )
        return np.asarray(
            0.5 * (matrices + matrices.conj().transpose(0, 1, 3, 2)),
            dtype=np.complex128,
        )

    def eigenvalues(self, points: RealArray) -> RealArray:
        return np.asarray(np.linalg.eigvalsh(self.matrices(points)), dtype=np.float64)

    def one_model_eigenvalues(self, model_index: int, points: RealArray) -> RealArray:
        coefficients = self._coefficients[model_index].reshape(
            len(self._representatives), self.rank * self.rank
        )
        phases = np.exp(2.0j * np.pi * (points @ self._representatives.T))
        matrices = (phases @ coefficients).reshape(len(points), self.rank, self.rank)
        matrices = 0.5 * (matrices + matrices.conj().transpose(0, 2, 1))
        return np.asarray(np.linalg.eigvalsh(matrices), dtype=np.float64)


class DenseMeshAnalyzer:
    __slots__ = ("_evaluator", "_model_names")

    def __init__(self, evaluator: CoefficientEvaluator, model_names: tuple[str, ...]) -> None:
        self._evaluator = evaluator
        self._model_names = model_names

    def execute(self, size: int, chunk_size: int = 2048) -> JsonObject:
        points = gamma_grid(size)
        spectral_values: list[list[RealArray]] = [
            [] for _ in range(self._evaluator.model_count - 1)
        ]
        conduction_values: list[list[RealArray]] = [
            [] for _ in range(self._evaluator.model_count - 1)
        ]
        operator_power = np.zeros(self._evaluator.model_count - 1, dtype=np.float64)
        operator_maximum = np.zeros(self._evaluator.model_count - 1, dtype=np.float64)
        for start in range(0, len(points), chunk_size):
            matrices = self._evaluator.matrices(points[start : start + chunk_size])
            eigenvalues = np.asarray(np.linalg.eigvalsh(matrices), dtype=np.float64)
            source = matrices[:, 0]
            source_spectrum = eigenvalues[:, 0]
            for model_index in range(1, self._evaluator.model_count):
                local_index = model_index - 1
                difference = matrices[:, model_index] - source
                frobenius_squared = np.sum(np.abs(difference) ** 2, axis=(1, 2))
                operator_power[local_index] += float(np.sum(frobenius_squared))
                operator_maximum[local_index] = max(
                    operator_maximum[local_index],
                    float(
                        np.max(
                            np.sqrt(frobenius_squared / self._evaluator.rank)
                        )
                    ),
                )
                spectral_difference = eigenvalues[:, model_index] - source_spectrum
                spectral_values[local_index].append(spectral_difference.reshape(-1))
                conduction_values[local_index].append(spectral_difference[:, 4])
        records: JsonObject = {}
        point_count = len(points)
        for local_index, name in enumerate(self._model_names):
            spectral = np.concatenate(spectral_values[local_index])
            conduction = np.concatenate(conduction_values[local_index])
            absolute = np.abs(spectral)
            conduction_absolute = np.abs(conduction)
            records[name] = {
                "ordered_spectrum_all_bands": {
                    "rms_ev": float(np.sqrt(np.mean(np.square(spectral)))),
                    "maximum_absolute_ev": float(np.max(absolute)),
                    "percentile_95_absolute_ev": float(np.percentile(absolute, 95.0)),
                },
                "lowest_conduction_band": {
                    "rms_ev": float(np.sqrt(np.mean(np.square(conduction)))),
                    "maximum_absolute_ev": float(np.max(conduction_absolute)),
                    "percentile_95_absolute_ev": float(
                        np.percentile(conduction_absolute, 95.0)
                    ),
                },
                "sampled_operator": {
                    "rms_frobenius_per_state_ev": float(
                        np.sqrt(
                            operator_power[local_index]
                            / (point_count * self._evaluator.rank)
                        )
                    ),
                    "maximum_frobenius_per_state_ev": float(
                        operator_maximum[local_index]
                    ),
                },
            }
        return {
            "mesh_size": size,
            "point_count": point_count,
            "coordinates": "Gamma-origin i/N tensor product on [0,1)^3",
            "models": records,
        }


class FeatureAnalyzer:
    __slots__ = (
        "_evaluator",
        "_coarse_labels",
        "_coarse_points",
        "_inverse_reciprocal",
        "_reciprocal",
        "_source_starts",
    )

    def __init__(
        self,
        evaluator: CoefficientEvaluator,
        reciprocal_basis: RealArray,
        source_starts: dict[str, RealArray],
    ) -> None:
        self._evaluator = evaluator
        self._reciprocal = reciprocal_basis
        self._inverse_reciprocal = np.linalg.inv(reciprocal_basis)
        self._source_starts = source_starts
        self._coarse_points = gamma_grid(32)
        self._coarse_labels = tuple(
            expected_label(closest_gamma_cartesian(point, reciprocal_basis))
            for point in self._coarse_points
        )

    def execute(self, model_names: tuple[str, ...]) -> JsonObject:
        names = ("full-source", *model_names)
        valleys_by_model: list[dict[str, ValleyRecord]] = []
        gap_by_model: list[float] = []
        for model_index, _name in enumerate(names):
            coarse_spectrum = self._evaluator.one_model_eigenvalues(
                model_index, self._coarse_points
            )[:, 4]
            coarse_starts: dict[str, tuple[RealArray, ...]] = {}
            for label in self._source_starts:
                indices = np.asarray(
                    [
                        index
                        for index, observed_label in enumerate(self._coarse_labels)
                        if observed_label == label
                    ],
                    dtype=np.int64,
                )
                selected = indices[np.argsort(coarse_spectrum[indices])[:8]]
                coarse_starts[label] = tuple(
                    np.asarray(self._coarse_points[index], dtype=np.float64)
                    for index in selected
                )
            valleys = {
                label: self._valley(
                    model_index,
                    label,
                    fractional,
                    coarse_starts[label],
                )
                for label, fractional in self._source_starts.items()
            }
            valleys_by_model.append(valleys)
            gamma = self._evaluator.one_model_eigenvalues(
                model_index, np.zeros((1, 3), dtype=np.float64)
            )[0]
            gap_by_model.append(
                min(record.energy_ev for record in valleys.values()) - float(gamma[3])
            )
        source_valleys = valleys_by_model[0]
        result: JsonObject = {
            "full-source": {
                "indirect_gap_ev": gap_by_model[0],
                "valleys": {
                    label: self._valley_json(record)
                    for label, record in source_valleys.items()
                },
            }
        }
        for model_index, name in enumerate(model_names, start=1):
            candidate_valleys = valleys_by_model[model_index]
            valley_comparisons: JsonObject = {}
            for label in self._source_starts:
                source = source_valleys[label]
                candidate = candidate_valleys[label]
                row_indices, column_indices = linear_sum_assignment(
                    -np.abs(
                        source.principal_axes_cartesian_columns.T
                        @ candidate.principal_axes_cartesian_columns
                    )
                )
                matches: list[JsonValue] = []
                for source_index, candidate_index in zip(
                    row_indices, column_indices, strict=True
                ):
                    source_curvature = source.principal_curvatures_ev_angstrom_squared[
                        source_index
                    ]
                    candidate_curvature = (
                        candidate.principal_curvatures_ev_angstrom_squared[
                            candidate_index
                        ]
                    )
                    source_mass = source.principal_masses_electron[source_index]
                    candidate_mass = candidate.principal_masses_electron[
                        candidate_index
                    ]
                    matches.append(
                        {
                            "source_principal_index": int(source_index),
                            "candidate_principal_index": int(candidate_index),
                            "axis_absolute_overlap": float(
                                abs(
                                    source.principal_axes_cartesian_columns[
                                        :, source_index
                                    ]
                                    @ candidate.principal_axes_cartesian_columns[
                                        :, candidate_index
                                    ]
                                )
                            ),
                            "source_curvature_ev_angstrom_squared": float(
                                source_curvature
                            ),
                            "candidate_curvature_ev_angstrom_squared": float(
                                candidate_curvature
                            ),
                            "curvature_absolute_relative_change": float(
                                abs(candidate_curvature - source_curvature)
                                / abs(source_curvature)
                            ),
                            "source_mass_electron": float(source_mass),
                            "candidate_mass_electron": float(candidate_mass),
                            "mass_absolute_relative_change": float(
                                abs(candidate_mass - source_mass) / abs(source_mass)
                            ),
                        }
                    )
                displacement = periodic_cartesian_displacement(
                    candidate.fractional, source.fractional, self._reciprocal
                )
                hessian_difference = (
                    candidate.hessian_ev_angstrom_squared
                    - source.hessian_ev_angstrom_squared
                )
                valley_comparisons[label] = {
                    "candidate": self._valley_json(candidate),
                    "source_energy_ev": source.energy_ev,
                    "energy_change_ev": candidate.energy_ev - source.energy_ev,
                    "periodic_cartesian_displacement_inverse_angstrom": (
                        displacement.tolist()
                    ),
                    "displacement_norm_inverse_angstrom": float(
                        np.linalg.norm(displacement)
                    ),
                    "hessian_frobenius_change_ev_angstrom_squared": float(
                        np.linalg.norm(hessian_difference)
                    ),
                    "hessian_frobenius_relative_change": float(
                        np.linalg.norm(hessian_difference)
                        / np.linalg.norm(source.hessian_ev_angstrom_squared)
                    ),
                    "matched_principal_diagnostics": matches,
                }
            result[name] = {
                "indirect_gap_ev": gap_by_model[model_index],
                "indirect_gap_change_ev": gap_by_model[model_index] - gap_by_model[0],
                "maximum_valley_displacement_inverse_angstrom": max(
                    numeric(
                        mapping(value, "valley comparison")[
                            "displacement_norm_inverse_angstrom"
                        ],
                        "displacement",
                    )
                    for value in valley_comparisons.values()
                ),
                "maximum_valley_energy_absolute_change_ev": max(
                    abs(
                        numeric(
                            mapping(value, "valley comparison")["energy_change_ev"],
                            "energy change",
                        )
                    )
                    for value in valley_comparisons.values()
                ),
                "maximum_hessian_frobenius_relative_change": max(
                    numeric(
                        mapping(value, "valley comparison")[
                            "hessian_frobenius_relative_change"
                        ],
                        "Hessian change",
                    )
                    for value in valley_comparisons.values()
                ),
                "maximum_principal_mass_absolute_relative_change": max(
                    numeric(match["mass_absolute_relative_change"], "mass change")
                    for value in valley_comparisons.values()
                    for match in values(
                        mapping(value, "valley comparison")[
                            "matched_principal_diagnostics"
                        ],
                        "matched diagnostics",
                    )
                ),
                "valleys": valley_comparisons,
            }
        return result

    def _valley(
        self,
        model_index: int,
        label: str,
        source_fractional: RealArray,
        coarse_starts: tuple[RealArray, ...],
    ) -> ValleyRecord:
        starts = (source_fractional, *coarse_starts)
        outcomes: list[tuple[object, RealArray, RealArray, str]] = []
        for start_fractional in starts:
            def energy(displacement: RealArray) -> float:
                fractional = (
                    start_fractional + self._inverse_reciprocal @ displacement
                ) % 1.0
                eigenvalues = self._evaluator.one_model_eigenvalues(
                    model_index, fractional.reshape(1, 3)
                )
                return float(eigenvalues[0, 4])

            outcome = minimize(
                energy,
                np.zeros(3, dtype=np.float64),
                method="L-BFGS-B",
                bounds=((-0.12, 0.12), (-0.12, 0.12), (-0.12, 0.12)),
                options={"maxiter": 240, "ftol": 1.0e-14, "gtol": 1.0e-10},
            )
            displacement = np.asarray(outcome.x, dtype=np.float64)
            fractional = (
                start_fractional + self._inverse_reciprocal @ displacement
            ) % 1.0
            observed_label = expected_label(
                closest_gamma_cartesian(fractional, self._reciprocal)
            )
            outcomes.append((outcome, displacement, fractional, observed_label))
        matching = [item for item in outcomes if item[3] == label]
        if not matching:
            raise RuntimeError(f"no global-axis valley search retained identity {label}")
        successful = [item for item in matching if bool(item[0].success)]
        selected, displacement, fractional, observed_label = min(
            successful or matching,
            key=lambda item: float(item[0].fun),
        )
        cartesian = closest_gamma_cartesian(fractional, self._reciprocal)
        if observed_label != label:
            raise RuntimeError(
                f"global-axis valley search changed identity from {label} to {observed_label}"
            )
        hessian = self._hessian(model_index, fractional)
        curvatures, axes = np.linalg.eigh(hessian)
        masses = ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 / curvatures
        return ValleyRecord(
            label=label,
            fractional=np.asarray(fractional, dtype=np.float64),
            cartesian=cartesian,
            energy_ev=float(selected.fun),
            optimizer_success=bool(selected.success),
            iterations=int(selected.nit),
            local_bound_active=bool(np.any(np.abs(displacement) >= 0.12 - 1.0e-8)),
            hessian_ev_angstrom_squared=hessian,
            principal_curvatures_ev_angstrom_squared=np.asarray(
                curvatures, dtype=np.float64
            ),
            principal_axes_cartesian_columns=np.asarray(axes, dtype=np.float64),
            principal_masses_electron=np.asarray(masses, dtype=np.float64),
        )

    def _hessian(self, model_index: int, fractional: RealArray) -> RealArray:
        step = 0.002

        def energy(cartesian_displacement: RealArray) -> float:
            point = (
                fractional + self._inverse_reciprocal @ cartesian_displacement
            ) % 1.0
            return float(
                self._evaluator.one_model_eigenvalues(
                    model_index, point.reshape(1, 3)
                )[0, 4]
            )

        origin = np.zeros(3, dtype=np.float64)
        center = energy(origin)
        hessian = np.empty((3, 3), dtype=np.float64)
        for left in range(3):
            plus = origin.copy()
            minus = origin.copy()
            plus[left] = step
            minus[left] = -step
            hessian[left, left] = (energy(plus) - 2.0 * center + energy(minus)) / (
                step**2
            )
            for right in range(left + 1, 3):
                plus_plus = origin.copy()
                plus_minus = origin.copy()
                minus_plus = origin.copy()
                minus_minus = origin.copy()
                plus_plus[left] = step
                plus_plus[right] = step
                plus_minus[left] = step
                plus_minus[right] = -step
                minus_plus[left] = -step
                minus_plus[right] = step
                minus_minus[left] = -step
                minus_minus[right] = -step
                value = (
                    energy(plus_plus)
                    - energy(plus_minus)
                    - energy(minus_plus)
                    + energy(minus_minus)
                ) / (4.0 * step**2)
                hessian[left, right] = value
                hessian[right, left] = value
        return np.asarray(hessian, dtype=np.float64)

    @staticmethod
    def _valley_json(record: ValleyRecord) -> JsonObject:
        return {
            "label": record.label,
            "fractional_reciprocal_coordinates": record.fractional.tolist(),
            "cartesian_inverse_angstrom": record.cartesian.tolist(),
            "energy_ev": record.energy_ev,
            "optimizer_success": record.optimizer_success,
            "optimizer_iterations": record.iterations,
            "local_bound_active": record.local_bound_active,
            "hessian_ev_angstrom_squared": (
                record.hessian_ev_angstrom_squared.tolist()
            ),
            "principal_curvatures_ev_angstrom_squared": (
                record.principal_curvatures_ev_angstrom_squared.tolist()
            ),
            "principal_axes_cartesian_columns": (
                record.principal_axes_cartesian_columns.tolist()
            ),
            "principal_masses_electron": record.principal_masses_electron.tolist(),
        }


def build_models(
    request: JsonObject,
    design: JsonObject,
    representatives: IntegerArray,
    blocks_ev: ComplexArray,
    witness_surface: JsonObject,
) -> tuple[tuple[FrozenModel, ...], ComplexArray]:
    direct_basis = np.asarray(
        values(
            mapping(design["fixed_reduction_source"], "fixed source")[
                "direct_basis_columns_angstrom"
            ],
            "direct basis",
        ),
        dtype=np.float64,
    )
    shells = [
        mapping(item, "shell")
        for item in values(
            mapping(design["truncation_family"], "truncation family")["shells"],
            "shells",
        )
    ]
    radii = np.round(
        np.linalg.norm(representatives.astype(np.float64) @ direct_basis.T, axis=1),
        decimals=9,
    )
    models: list[FrozenModel] = []
    surface_examples = {
        string(item["shell_id"], "surface shell id"): mapping(item, "surface example")
        for item in values(
            witness_surface["illustrative_threshold_witnesses"],
            "illustrative witnesses",
        )
        if mapping(item, "surface example").get("witness_found") is True
    }
    for declaration_value in values(request["frozen_witnesses"], "frozen witnesses"):
        declaration = mapping(declaration_value, "frozen witness")
        shell_id = string(declaration["shell_id"], "shell id")
        shell = next(item for item in shells if item["shell_id"] == shell_id)
        support_index = int(numeric(shell["shell_index_zero_based"], "support index"))
        alpha = np.asarray(
            [numeric(item, "alpha") for item in values(declaration["alpha"], "alpha")],
            dtype=np.float64,
        )
        if len(alpha) != support_index + 1:
            raise RuntimeError(f"alpha dimension mismatch for {shell_id}")
        surface = surface_examples[shell_id]
        surface_alpha = np.asarray(
            [numeric(item, "surface alpha") for item in values(surface["alpha"], "alpha")],
            dtype=np.float64,
        )
        if not np.array_equal(alpha, surface_alpha):
            raise RuntimeError(f"frozen alpha differs from retained surface for {shell_id}")
        coefficients = np.zeros_like(blocks_ev)
        previous_radius = -1.0
        for shell_index in range(support_index + 1):
            radius = numeric(shells[shell_index]["display_radius_angstrom"], "radius")
            mask = (radii > previous_radius) & (radii <= radius)
            coefficients[mask] = alpha[shell_index] * blocks_ev[mask]
            previous_radius = radius
        count = int(np.count_nonzero(radii <= previous_radius))
        declared_count = int(
            numeric(
                declaration["included_representative_count"],
                "included representative count",
            )
        )
        if count != declared_count:
            raise RuntimeError(f"representative count mismatch for {shell_id}")
        models.append(
            FrozenModel(
                shell_id=shell_id,
                included_representative_count=count,
                alpha=alpha,
                coefficients_ev=np.asarray(coefficients, dtype=np.complex128),
            )
        )
    return tuple(models), direct_basis


def exact_operator_records(
    blocks_ev: ComplexArray, models: tuple[FrozenModel, ...]
) -> JsonObject:
    rank = blocks_ev.shape[-1]
    records: JsonObject = {}
    for model in models:
        difference = model.coefficients_ev - blocks_ev
        coefficient_power = float(np.sum(np.abs(difference) ** 2))
        records[model.shell_id] = {
            "normalized_brillouin_zone_rms_frobenius_per_state_ev": float(
                np.sqrt(coefficient_power / rank)
            ),
            "coefficient_frobenius_power_ev_squared": coefficient_power,
            "identity": (
                "Parseval for distinct integer Fourier representatives on the "
                "normalized reciprocal torus"
            ),
        }
    return records


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"refusing to overwrite retained result: {OUTPUT}")
    start = time.perf_counter()
    request_value: JsonValue = json.loads(REQUEST.read_text(encoding="utf-8"))
    request = mapping(request_value, "request")
    authenticated = authenticate_sources(request)
    sources = mapping(request["sources"], "sources")
    adapter = load_adapter(
        source_path(mapping(sources["authenticated_adapter"], "adapter"), "adapter")
    )
    native = adapter.parse_hr(
        source_path(mapping(sources["hamiltonian"], "Hamiltonian"), "Hamiltonian")
    )
    operator = adapter.FiniteWannierOperator.from_native(
        native,
        source_path(mapping(sources["ws_vectors"], "WS vectors"), "WS vectors"),
    )
    representatives = np.asarray(operator.representatives, dtype=np.int64)
    blocks_ev = np.asarray(operator.blocks_ev, dtype=np.complex128)
    if len(np.unique(representatives, axis=0)) != len(representatives):
        raise RuntimeError("effective Fourier representatives are not unique")
    design_value: JsonValue = json.loads(
        source_path(
            mapping(sources["truncation_design"], "truncation design"),
            "truncation design",
        ).read_text(encoding="utf-8")
    )
    design = mapping(design_value, "truncation design")
    surface_value: JsonValue = json.loads(
        source_path(
            mapping(sources["witness_surface"], "witness surface"),
            "witness surface",
        ).read_text(encoding="utf-8")
    )
    witness_surface = mapping(surface_value, "witness surface")
    characterization_value: JsonValue = json.loads(
        source_path(
            mapping(sources["characterization_result"], "characterization result"),
            "characterization result",
        ).read_text(encoding="utf-8")
    )
    characterization = mapping(characterization_value, "characterization result")
    models, _direct_basis = build_models(
        request, design, representatives, blocks_ev, witness_surface
    )
    coefficients = np.asarray(
        [blocks_ev, *(model.coefficients_ev for model in models)],
        dtype=np.complex128,
    )
    evaluator = CoefficientEvaluator(representatives, coefficients)
    model_names = tuple(model.shell_id for model in models)
    dense_analyzer = DenseMeshAnalyzer(evaluator, model_names)
    dense_results = [dense_analyzer.execute(size) for size in (12, 20, 32)]

    lattice = mapping(characterization["lattice"], "lattice")
    reciprocal = np.asarray(
        values(
            lattice["reciprocal_basis_columns_inverse_angstrom"],
            "reciprocal basis",
        ),
        dtype=np.float64,
    )
    valleys = values(
        mapping(
            mapping(characterization["results"], "characterization results")[
                "valley_family"
            ],
            "valley family",
        )["valleys"],
        "source valleys",
    )
    source_starts = {
        string(mapping(item, "source valley")["label"], "valley label"): np.asarray(
            values(
                mapping(item, "source valley")[
                    "fractional_reciprocal_coordinates"
                ],
                "valley coordinates",
            ),
            dtype=np.float64,
        )
        for item in valleys
    }
    feature_results = FeatureAnalyzer(
        evaluator, reciprocal, source_starts
    ).execute(model_names)

    exact_operator = exact_operator_records(blocks_ev, models)
    mesh_consistency: JsonObject = {}
    for model in models:
        exact = numeric(
            mapping(exact_operator[model.shell_id], "exact operator")[
                "normalized_brillouin_zone_rms_frobenius_per_state_ev"
            ],
            "exact RMS",
        )
        sampled = [
            numeric(
                mapping(
                    mapping(item["models"], "dense models")[model.shell_id],
                    "dense model",
                )["sampled_operator"]["rms_frobenius_per_state_ev"],
                "sampled RMS",
            )
            for item in dense_results
        ]
        mesh_consistency[model.shell_id] = {
            "maximum_sampled_minus_exact_absolute_ev": max(
                abs(value - exact) for value in sampled
            ),
            "sampled_values_ev": sampled,
        }

    result: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "calculator_invocations": 0,
        "refitting_performed": False,
        "independent_reconstruction_performed": False,
        "request": identity(REQUEST),
        "producer": identity(Path(__file__)),
        "authenticated_sources": authenticated,
        "source_inventory": {
            "wannier_rank": int(blocks_ev.shape[-1]),
            "effective_representative_count": len(representatives),
            "unique_effective_representatives": True,
        },
        "frozen_models": [
            {
                "shell_id": model.shell_id,
                "included_representative_count": model.included_representative_count,
                "alpha": model.alpha.tolist(),
            }
            for model in models
        ],
        "level_1_exact_operator": exact_operator,
        "level_2_dense_meshes": dense_results,
        "level_2_parseval_consistency": mesh_consistency,
        "level_3_source_relative_features": feature_results,
        "execution": {
            "elapsed_seconds": float(time.perf_counter() - start),
            "output_path": str(OUTPUT),
        },
        "limitations": [
            "All comparisons are relative to the full C6-B20-W21 Wannier source.",
            "The source fails declared DFT-parent gap and effective-mass fidelity targets.",
            "Dense meshes are deterministic interpolation checks, not independent DFT data.",
            "Local valley searches are bounded around the six frozen source valleys and do not certify absence of other minima.",
            "No prospective acceptance threshold, global model-selection certificate, or independent reconstruction is supplied.",
            "No Quantum ESPRESSO or Wannier90 process was invoked.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
