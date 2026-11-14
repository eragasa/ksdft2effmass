from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from types import ModuleType

import numpy as np
from numpy.typing import NDArray
from scipy import constants  # type: ignore[import-untyped]

RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[4]
REQUEST = ROOT / "request.json"
OUTPUT = ROOT / "result.json"
STATUS = "comprehensive-nonsoc-wannier-band-edge-producer-checked-development-not-independently-verified"
ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 = (
    constants.hbar**2 / constants.m_e / constants.electron_volt * 1.0e20
)
MODEL_NAMES = ("full-source", "H-shell-05", "H-shell-10", "H-shell-16")
DIRECTIONS = {
    "100": np.asarray([1.0, 0.0, 0.0], dtype=np.float64),
    "110": np.asarray([1.0, 1.0, 0.0], dtype=np.float64) / np.sqrt(2.0),
    "111": np.asarray([1.0, 1.0, 1.0], dtype=np.float64) / np.sqrt(3.0),
}
CURVATURE_STEPS = (0.001, 0.002, 0.005, 0.01)
VALENCE_WINDOWS = (0.005, 0.01, 0.02)


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
        if (
            observed["byte_size"] != expected_size
            or observed["sha256"] != expected_digest
        ):
            raise RuntimeError(f"source identity mismatch: {path}")
        authenticated[label] = observed
    return authenticated


def load_module(path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "c6_b20_w21_comprehensive_edge_ladder", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load authenticated ladder producer")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def eigenvalues_at(evaluator: object, model_index: int, points: RealArray) -> RealArray:
    result = evaluator.one_model_eigenvalues(model_index, points)
    return np.asarray(result, dtype=np.float64)


def band_energy(
    evaluator: object, model_index: int, fractional: RealArray, band_index: int
) -> float:
    return float(
        eigenvalues_at(evaluator, model_index, fractional.reshape(1, 3))[0, band_index]
    )


def cartesian_point(
    fractional: RealArray,
    cartesian_displacement: RealArray,
    inverse_reciprocal: RealArray,
) -> RealArray:
    return np.asarray(
        (fractional + inverse_reciprocal @ cartesian_displacement) % 1.0,
        dtype=np.float64,
    )


def hessian_and_gradient(
    evaluator: object,
    model_index: int,
    fractional: RealArray,
    band_index: int,
    inverse_reciprocal: RealArray,
    step: float,
) -> tuple[RealArray, RealArray]:
    origin = np.zeros(3, dtype=np.float64)

    def energy(displacement: RealArray) -> float:
        return band_energy(
            evaluator,
            model_index,
            cartesian_point(fractional, displacement, inverse_reciprocal),
            band_index,
        )

    center = energy(origin)
    gradient = np.empty(3, dtype=np.float64)
    hessian = np.empty((3, 3), dtype=np.float64)
    for left in range(3):
        plus = origin.copy()
        minus = origin.copy()
        plus[left] = step
        minus[left] = -step
        plus_energy = energy(plus)
        minus_energy = energy(minus)
        gradient[left] = (plus_energy - minus_energy) / (2.0 * step)
        hessian[left, left] = (plus_energy - 2.0 * center + minus_energy) / step**2
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
            cross = (
                energy(plus_plus)
                - energy(plus_minus)
                - energy(minus_plus)
                + energy(minus_minus)
            ) / (4.0 * step**2)
            hessian[left, right] = cross
            hessian[right, left] = cross
    return np.asarray(hessian, dtype=np.float64), np.asarray(gradient, dtype=np.float64)


def electron_analysis(
    evaluator: object,
    ladder_result: JsonObject,
    inverse_reciprocal: RealArray,
) -> JsonObject:
    features = mapping(ladder_result["level_3_source_relative_features"], "features")
    models: JsonObject = {}
    for model_index, model_name in enumerate(MODEL_NAMES):
        feature_model = mapping(features[model_name], "feature model")
        valley_source = (
            mapping(feature_model["valleys"], "source valleys")
            if model_name == "full-source"
            else {
                label: mapping(item, "candidate comparison")["candidate"]
                for label, item in mapping(
                    feature_model["valleys"], "candidate valleys"
                ).items()
            }
        )
        valley_records: JsonObject = {}
        density_terms: list[float] = []
        inverse_tensors: list[RealArray] = []
        conductivity_masses: list[float] = []
        for label, valley_value in valley_source.items():
            valley = mapping(valley_value, "valley")
            fractional = np.asarray(
                values(
                    valley["fractional_reciprocal_coordinates"],
                    "valley fractional coordinates",
                ),
                dtype=np.float64,
            )
            stencil_records: list[JsonValue] = []
            primary_masses: RealArray | None = None
            primary_inverse_tensor: RealArray | None = None
            primary_mass_tensor: RealArray | None = None
            for step in CURVATURE_STEPS:
                hessian, gradient = hessian_and_gradient(
                    evaluator,
                    model_index,
                    fractional,
                    4,
                    inverse_reciprocal,
                    step,
                )
                curvatures, axes = np.linalg.eigh(hessian)
                masses = ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 / curvatures
                inverse_tensor = hessian / ELECTRON_MASS_CURVATURE_EV_ANGSTROM2
                mass_tensor = ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 * np.linalg.inv(
                    hessian
                )
                dos_mass = float(np.cbrt(np.prod(masses)))
                conductivity_mass = float(3.0 / np.sum(1.0 / masses))
                if step == 0.002:
                    primary_masses = np.asarray(masses, dtype=np.float64)
                    primary_inverse_tensor = np.asarray(
                        inverse_tensor, dtype=np.float64
                    )
                    primary_mass_tensor = np.asarray(mass_tensor, dtype=np.float64)
                    density_terms.append(float(np.sqrt(np.prod(masses))))
                    inverse_tensors.append(primary_inverse_tensor)
                    conductivity_masses.append(conductivity_mass)
                stencil_records.append(
                    {
                        "step_inverse_angstrom": step,
                        "gradient_ev_angstrom": gradient.tolist(),
                        "gradient_norm_ev_angstrom": float(np.linalg.norm(gradient)),
                        "hessian_ev_angstrom_squared": hessian.tolist(),
                        "principal_curvatures_ev_angstrom_squared": curvatures.tolist(),
                        "principal_axes_cartesian_columns": axes.tolist(),
                        "principal_masses_electron": masses.tolist(),
                        "single_valley_dos_mass_electron": dos_mass,
                        "single_valley_conductivity_mass_electron": conductivity_mass,
                    }
                )
            if (
                primary_masses is None
                or primary_inverse_tensor is None
                or primary_mass_tensor is None
            ):
                raise RuntimeError("primary electron-mass stencil was not evaluated")
            all_masses = np.asarray(
                [
                    mapping(item, "stencil")["principal_masses_electron"]
                    for item in stencil_records
                ],
                dtype=np.float64,
            )
            relative_spread = np.max(all_masses, axis=0) - np.min(all_masses, axis=0)
            relative_spread = relative_spread / np.abs(primary_masses)
            valley_records[label] = {
                "fractional_reciprocal_coordinates": fractional.tolist(),
                "primary_step_inverse_angstrom": 0.002,
                "primary_inverse_mass_tensor_in_inverse_electron_masses": (
                    primary_inverse_tensor.tolist()
                ),
                "primary_mass_tensor_in_electron_masses": primary_mass_tensor.tolist(),
                "maximum_principal_mass_relative_stencil_spread": float(
                    np.max(relative_spread)
                ),
                "stencils": stencil_records,
            }
        average_inverse_tensor = np.mean(np.asarray(inverse_tensors), axis=0)
        family_dos_mass = float(np.sum(density_terms) ** (2.0 / 3.0))
        family_conductivity_mass = float(3.0 / np.trace(average_inverse_tensor))
        models[model_name] = {
            "valleys": valley_records,
            "six_valley_dos_mass_convention_electron": family_dos_mass,
            "equal_population_average_inverse_mass_tensor_in_inverse_electron_masses": (
                average_inverse_tensor.tolist()
            ),
            "equal_population_conductivity_mass_convention_electron": (
                family_conductivity_mass
            ),
            "single_valley_conductivity_mass_range_electron": [
                min(conductivity_masses),
                max(conductivity_masses),
            ],
        }
    source = mapping(models["full-source"], "source electron analysis")
    for model_name in MODEL_NAMES[1:]:
        model = mapping(models[model_name], "candidate electron analysis")
        model["source_relative_derived_changes"] = {
            "six_valley_dos_mass_absolute_relative_change": abs(
                numeric(
                    model["six_valley_dos_mass_convention_electron"],
                    "candidate DOS mass",
                )
                - numeric(
                    source["six_valley_dos_mass_convention_electron"],
                    "source DOS mass",
                )
            )
            / abs(
                numeric(
                    source["six_valley_dos_mass_convention_electron"],
                    "source DOS mass",
                )
            ),
            "equal_population_conductivity_mass_absolute_relative_change": abs(
                numeric(
                    model["equal_population_conductivity_mass_convention_electron"],
                    "candidate conductivity mass",
                )
                - numeric(
                    source["equal_population_conductivity_mass_convention_electron"],
                    "source conductivity mass",
                )
            )
            / abs(
                numeric(
                    source["equal_population_conductivity_mass_convention_electron"],
                    "source conductivity mass",
                )
            ),
        }
    return models


def gamma_cluster_analysis(evaluator: object) -> JsonObject:
    gamma = np.zeros((1, 3), dtype=np.float64)
    matrices = np.asarray(evaluator.matrices(gamma)[0], dtype=np.complex128)
    records: JsonObject = {}
    source_values, source_vectors = np.linalg.eigh(matrices[0])
    source_cluster = source_vectors[:, 1:4]
    source_projector = source_cluster @ source_cluster.conj().T
    source_centroid = float(np.mean(source_values[1:4]))
    for model_index, model_name in enumerate(MODEL_NAMES):
        eigenvalues, eigenvectors = np.linalg.eigh(matrices[model_index])
        cluster_values = np.asarray(eigenvalues[1:4], dtype=np.float64)
        cluster_vectors = np.asarray(eigenvectors[:, 1:4], dtype=np.complex128)
        projector = cluster_vectors @ cluster_vectors.conj().T
        singular_values = np.linalg.svd(
            source_cluster.conj().T @ cluster_vectors, compute_uv=False
        )
        angles = np.arccos(np.clip(singular_values, 0.0, 1.0))
        records[model_name] = {
            "cluster_band_indices_zero_based": [1, 2, 3],
            "cluster_energies_ev": cluster_values.tolist(),
            "cluster_centroid_ev": float(np.mean(cluster_values)),
            "cluster_centroid_change_from_source_ev": float(
                np.mean(cluster_values) - source_centroid
            ),
            "cluster_splitting_ev": float(np.ptp(cluster_values)),
            "cluster_projector_frobenius_distance_from_source": float(
                np.linalg.norm(projector - source_projector)
            ),
            "cluster_overlap_singular_values": singular_values.tolist(),
            "cluster_principal_angles_radians": angles.tolist(),
            "maximum_cluster_principal_angle_radians": float(np.max(angles)),
        }
    return records


def valence_directional_analysis(
    evaluator: object,
    inverse_reciprocal: RealArray,
) -> JsonObject:
    gamma = np.zeros(3, dtype=np.float64)
    records: JsonObject = {}
    for model_index, model_name in enumerate(MODEL_NAMES):
        gamma_values = eigenvalues_at(evaluator, model_index, gamma.reshape(1, 3))[
            0, 1:4
        ]
        direction_records: JsonObject = {}
        for direction_name, direction in DIRECTIONS.items():
            window_records: list[JsonValue] = []
            masses_by_window: list[RealArray] = []
            for window in VALENCE_WINDOWS:
                radii = np.linspace(window / 5.0, window, 5, dtype=np.float64)
                plus_points = np.asarray(
                    [
                        cartesian_point(gamma, radius * direction, inverse_reciprocal)
                        for radius in radii
                    ],
                    dtype=np.float64,
                )
                minus_points = np.asarray(
                    [
                        cartesian_point(gamma, -radius * direction, inverse_reciprocal)
                        for radius in radii
                    ],
                    dtype=np.float64,
                )
                plus = eigenvalues_at(evaluator, model_index, plus_points)[:, 1:4]
                minus = eigenvalues_at(evaluator, model_index, minus_points)[:, 1:4]
                even = 0.5 * (plus + minus)
                odd = 0.5 * (plus - minus)
                q = np.concatenate(([0.0], radii))
                design = np.column_stack((np.ones_like(q), q**2, q**4))
                branch_records: list[JsonValue] = []
                branch_masses = np.full(3, np.nan, dtype=np.float64)
                for branch_index, branch_name in enumerate(
                    ("lower", "middle", "upper")
                ):
                    energy = np.concatenate(
                        ([gamma_values[branch_index]], even[:, branch_index])
                    )
                    coefficients, *_ = np.linalg.lstsq(design, energy, rcond=None)
                    fitted = design @ coefficients
                    curvature = float(2.0 * coefficients[1])
                    hole_mass = (
                        float(-ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 / curvature)
                        if curvature < 0.0
                        else None
                    )
                    if hole_mass is not None:
                        branch_masses[branch_index] = hole_mass
                    branch_records.append(
                        {
                            "branch": branch_name,
                            "ordered_cluster_index_zero_based": branch_index,
                            "curvature_ev_angstrom_squared": curvature,
                            "apparent_directional_hole_mass_electron": hole_mass,
                            "quartic_coefficient_ev_angstrom_fourth": float(
                                coefficients[2]
                            ),
                            "fit_rms_ev": float(
                                np.sqrt(np.mean(np.square(energy - fitted)))
                            ),
                            "maximum_plus_minus_half_difference_ev": float(
                                np.max(np.abs(odd[:, branch_index]))
                            ),
                        }
                    )
                masses_by_window.append(branch_masses)
                window_records.append(
                    {
                        "fit_window_inverse_angstrom": window,
                        "positive_radii_inverse_angstrom": radii.tolist(),
                        "branches": branch_records,
                    }
                )
            mass_array = np.asarray(masses_by_window, dtype=np.float64)
            sensitivity: list[JsonValue] = []
            for branch_index, branch_name in enumerate(("lower", "middle", "upper")):
                branch_values = mass_array[:, branch_index]
                finite = branch_values[np.isfinite(branch_values)]
                sensitivity.append(
                    {
                        "branch": branch_name,
                        "all_windows_hole_like": len(finite) == len(VALENCE_WINDOWS),
                        "minimum_mass_electron": (
                            float(np.min(finite)) if len(finite) else None
                        ),
                        "maximum_mass_electron": (
                            float(np.max(finite)) if len(finite) else None
                        ),
                        "relative_range_about_0.01_window": (
                            float(
                                (np.max(finite) - np.min(finite))
                                / abs(branch_values[1])
                            )
                            if len(finite) == len(VALENCE_WINDOWS)
                            and branch_values[1] != 0.0
                            else None
                        ),
                    }
                )
            direction_records[direction_name] = {
                "unit_cartesian_direction": direction.tolist(),
                "windows": window_records,
                "fit_window_sensitivity": sensitivity,
            }
        records[model_name] = direction_records
    return records


def high_symmetry_analysis(
    evaluator: object,
    reciprocal_basis: RealArray,
    lattice_parameter_angstrom: float,
) -> JsonObject:
    inverse = np.linalg.inv(reciprocal_basis)
    reciprocal_axis = 2.0 * np.pi / lattice_parameter_angstrom
    gamma = np.zeros((1, 3), dtype=np.float64)
    x_cartesian = np.asarray(
        [
            sign * reciprocal_axis * np.eye(3, dtype=np.float64)[axis]
            for axis in range(3)
            for sign in (-1.0, 1.0)
        ],
        dtype=np.float64,
    )
    l_cartesian = np.asarray(
        [
            0.5 * reciprocal_axis * np.asarray((sx, sy, sz), dtype=np.float64)
            for sx in (-1.0, 1.0)
            for sy in (-1.0, 1.0)
            for sz in (-1.0, 1.0)
        ],
        dtype=np.float64,
    )
    point_sets = {
        "Gamma": gamma,
        "X": np.asarray([(inverse @ point) % 1.0 for point in x_cartesian]),
        "L": np.asarray([(inverse @ point) % 1.0 for point in l_cartesian]),
    }
    records: JsonObject = {}
    for model_index, model_name in enumerate(MODEL_NAMES):
        model_records: JsonObject = {}
        for label, points in point_sets.items():
            spectrum = eigenvalues_at(evaluator, model_index, points)
            gaps = spectrum[:, 4] - spectrum[:, 3]
            model_records[label] = {
                "point_count": len(points),
                "direct_gaps_ev": gaps.tolist(),
                "minimum_direct_gap_ev": float(np.min(gaps)),
                "maximum_direct_gap_ev": float(np.max(gaps)),
                "symmetry_spread_ev": float(np.ptp(gaps)),
                "valence_edge_energies_ev": spectrum[:, 3].tolist(),
                "conduction_edge_energies_ev": spectrum[:, 4].tolist(),
            }
        records[model_name] = model_records
    return records


def dense_band_analysis(evaluator: object, ladder: ModuleType) -> JsonObject:
    points = ladder.gamma_grid(32)
    minima = np.full((4, 10), np.inf, dtype=np.float64)
    maxima = np.full((4, 10), -np.inf, dtype=np.float64)
    vbm_values = np.full(4, -np.inf, dtype=np.float64)
    cbm_values = np.full(4, np.inf, dtype=np.float64)
    vbm_points = np.zeros((4, 3), dtype=np.float64)
    cbm_points = np.zeros((4, 3), dtype=np.float64)
    for start in range(0, len(points), 2048):
        chunk = points[start : start + 2048]
        spectrum = np.asarray(evaluator.eigenvalues(chunk), dtype=np.float64)
        minima = np.minimum(minima, np.min(spectrum, axis=0))
        maxima = np.maximum(maxima, np.max(spectrum, axis=0))
        for model_index in range(4):
            local_vbm = int(np.argmax(spectrum[:, model_index, 3]))
            local_cbm = int(np.argmin(spectrum[:, model_index, 4]))
            if spectrum[local_vbm, model_index, 3] > vbm_values[model_index]:
                vbm_values[model_index] = spectrum[local_vbm, model_index, 3]
                vbm_points[model_index] = chunk[local_vbm]
            if spectrum[local_cbm, model_index, 4] < cbm_values[model_index]:
                cbm_values[model_index] = spectrum[local_cbm, model_index, 4]
                cbm_points[model_index] = chunk[local_cbm]
    records: JsonObject = {}
    for model_index, model_name in enumerate(MODEL_NAMES):
        records[model_name] = {
            "mesh_size": 32,
            "point_count": len(points),
            "band_minima_ev": minima[model_index].tolist(),
            "band_maxima_ev": maxima[model_index].tolist(),
            "bandwidths_ev": (maxima[model_index] - minima[model_index]).tolist(),
            "mesh_vbm_ev": float(vbm_values[model_index]),
            "mesh_vbm_fractional_reciprocal_coordinates": vbm_points[
                model_index
            ].tolist(),
            "mesh_cbm_ev": float(cbm_values[model_index]),
            "mesh_cbm_fractional_reciprocal_coordinates": cbm_points[
                model_index
            ].tolist(),
            "mesh_indirect_gap_ev": float(
                cbm_values[model_index] - vbm_values[model_index]
            ),
        }
    return records


def reconstruct() -> tuple[ModuleType, object, JsonObject, RealArray, float]:
    request_value: JsonValue = json.loads(REQUEST.read_text(encoding="utf-8"))
    request = mapping(request_value, "request")
    sources = mapping(request["sources"], "sources")
    ladder_path = source_path(
        mapping(sources["ladder_producer"], "ladder producer"), "ladder producer"
    )
    ladder = load_module(ladder_path)
    ladder_request_path = source_path(
        mapping(sources["ladder_request"], "ladder request"), "ladder request"
    )
    ladder_request_value: JsonValue = json.loads(
        ladder_request_path.read_text(encoding="utf-8")
    )
    ladder_request = ladder.mapping(ladder_request_value, "ladder request")
    ladder_sources = ladder.mapping(ladder_request["sources"], "ladder sources")
    adapter = ladder.load_adapter(
        ladder.source_path(
            ladder.mapping(ladder_sources["authenticated_adapter"], "adapter"),
            "adapter",
        )
    )
    native = adapter.parse_hr(
        ladder.source_path(
            ladder.mapping(ladder_sources["hamiltonian"], "Hamiltonian"),
            "Hamiltonian",
        )
    )
    operator = adapter.FiniteWannierOperator.from_native(
        native,
        ladder.source_path(
            ladder.mapping(ladder_sources["ws_vectors"], "WS vectors"),
            "WS vectors",
        ),
    )
    design = json.loads(
        ladder.source_path(
            ladder.mapping(ladder_sources["truncation_design"], "design"),
            "design",
        ).read_text(encoding="utf-8")
    )
    surface = json.loads(
        ladder.source_path(
            ladder.mapping(ladder_sources["witness_surface"], "surface"),
            "surface",
        ).read_text(encoding="utf-8")
    )
    models, _ = ladder.build_models(
        ladder_request,
        ladder.mapping(design, "design"),
        np.asarray(operator.representatives, dtype=np.int64),
        np.asarray(operator.blocks_ev, dtype=np.complex128),
        ladder.mapping(surface, "surface"),
    )
    coefficients = np.asarray(
        [operator.blocks_ev, *(model.coefficients_ev for model in models)],
        dtype=np.complex128,
    )
    evaluator = ladder.CoefficientEvaluator(
        np.asarray(operator.representatives, dtype=np.int64), coefficients
    )
    characterization_path = source_path(
        mapping(sources["characterization_result"], "characterization"),
        "characterization",
    )
    characterization = mapping(
        json.loads(characterization_path.read_text(encoding="utf-8")),
        "characterization",
    )
    lattice = mapping(characterization["lattice"], "lattice")
    reciprocal = np.asarray(
        values(
            lattice["reciprocal_basis_columns_inverse_angstrom"],
            "reciprocal basis",
        ),
        dtype=np.float64,
    )
    lattice_parameter = numeric(
        lattice["lattice_parameter_angstrom"], "lattice parameter"
    )
    ladder_result_path = source_path(
        mapping(sources["ladder_result"], "ladder result"), "ladder result"
    )
    ladder_result = mapping(
        json.loads(ladder_result_path.read_text(encoding="utf-8")), "ladder result"
    )
    return ladder, evaluator, ladder_result, reciprocal, lattice_parameter


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"refusing to overwrite retained result: {OUTPUT}")
    start = time.perf_counter()
    request_value: JsonValue = json.loads(REQUEST.read_text(encoding="utf-8"))
    request = mapping(request_value, "request")
    authenticated = authenticate_sources(request)
    ladder, evaluator, ladder_result, reciprocal, lattice_parameter = reconstruct()
    inverse_reciprocal = np.linalg.inv(reciprocal)
    result: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "calculator_invocations": 0,
        "refitting_performed": False,
        "soc_present": False,
        "independent_reconstruction_performed": False,
        "request": identity(REQUEST),
        "producer": identity(Path(__file__)),
        "authenticated_sources": authenticated,
        "electron_edge": electron_analysis(
            evaluator, ladder_result, inverse_reciprocal
        ),
        "gamma_valence_cluster": gamma_cluster_analysis(evaluator),
        "directional_valence_cluster": valence_directional_analysis(
            evaluator, inverse_reciprocal
        ),
        "high_symmetry_edges": high_symmetry_analysis(
            evaluator, reciprocal, lattice_parameter
        ),
        "dense_ordered_bands": dense_band_analysis(evaluator, ladder),
        "execution": {
            "elapsed_seconds": float(time.perf_counter() - start),
            "output_path": str(OUTPUT),
        },
        "limitations": [
            "The valence edge is degenerate and warped; no single scalar or Cartesian hole-mass tensor is asserted.",
            "Directional apparent hole masses are ordered-branch diagnostics of the scalar-relativistic non-SOC Wannier models.",
            "No physical heavy-hole, light-hole, split-off, Luttinger-parameter, acceptor, transport, or DOS claim is made.",
            "All reduced-model comparisons are relative to a full Wannier source that fails declared DFT-parent gap and electron-mass targets.",
            "No Quantum ESPRESSO or Wannier90 process was invoked.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
