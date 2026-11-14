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
from scipy.optimize import minimize  # type: ignore[import-untyped]

RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[4]
REQUEST = ROOT / "request.json"
OUTPUT = ROOT / "result.json"
STATUS = "post-hoc-refitted-ws-producer-checked-development-not-independently-verified"
WEIGHTS = (
    0.0,
    0.001,
    0.003,
    0.01,
    0.03,
    0.1,
    0.2,
    0.35,
    0.5,
    0.65,
    0.8,
    0.9,
    0.97,
    0.99,
    0.997,
    0.999,
    1.0,
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
        if (
            observed["byte_size"] != expected_size
            or observed["sha256"] != expected_digest
        ):
            raise RuntimeError(f"source identity mismatch: {path}")
        authenticated[label] = observed
    return authenticated


def load_adapter(path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "c6_b20_w21_refitted_ws_adapter", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load authenticated native-HR adapter")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def point_inventory(path: Path) -> RealArray:
    manifest_value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    manifest = mapping(manifest_value, "point manifest")
    points = values(manifest["points"], "manifest points")
    coordinates = np.asarray(
        [
            [
                numeric(component, "fractional coordinate")
                for component in values(
                    mapping(point, "point")["fractional_reciprocal_coordinates"],
                    "point coordinates",
                )
            ]
            for point in points
        ],
        dtype=np.float64,
    )
    if coordinates.shape != (408, 3):
        raise RuntimeError("development point inventory must have shape (408, 3)")
    return coordinates


@dataclass(frozen=True, slots=True)
class LossEvaluation:
    spectral_squared: float
    operator_squared: float
    spectral_rms: float
    operator_rms: float
    spectral_maximum: float
    operator_maximum: float
    spectral_gradient: RealArray
    operator_gradient: RealArray


class ShellScaleLoss:
    __slots__ = ("_full_matrices", "_full_spectrum", "_rank", "_shell_matrices")

    def __init__(
        self,
        *,
        shell_matrices: ComplexArray,
        full_matrices: ComplexArray,
        full_spectrum: RealArray,
    ) -> None:
        self._shell_matrices = shell_matrices
        self._full_matrices = full_matrices
        self._full_spectrum = full_spectrum
        self._rank = int(full_matrices.shape[-1])

    def evaluate(self, alpha: RealArray) -> LossEvaluation:
        candidate = np.einsum("s,skij->kij", alpha, self._shell_matrices, optimize=True)
        difference = candidate - self._full_matrices
        frobenius = np.linalg.norm(difference, axis=(-2, -1))
        operator_squared = float(np.mean(np.square(frobenius)) / self._rank)
        operator_gradient = np.asarray(
            2.0
            * np.real(
                np.einsum(
                    "kij,skij->s",
                    difference.conjugate(),
                    self._shell_matrices,
                    optimize=True,
                )
            )
            / (len(candidate) * self._rank),
            dtype=np.float64,
        )
        eigenvalues, eigenvectors = np.linalg.eigh(candidate)
        spectral_difference = eigenvalues - self._full_spectrum
        spectral_squared = float(np.mean(np.square(spectral_difference)))
        derivatives = np.asarray(
            np.einsum(
                "kin,skij,kjn->skn",
                eigenvectors.conjugate(),
                self._shell_matrices,
                eigenvectors,
                optimize=True,
            ).real,
            dtype=np.float64,
        )
        spectral_gradient = np.asarray(
            2.0
            * np.einsum("kn,skn->s", spectral_difference, derivatives, optimize=True)
            / spectral_difference.size,
            dtype=np.float64,
        )
        return LossEvaluation(
            spectral_squared=spectral_squared,
            operator_squared=operator_squared,
            spectral_rms=float(np.sqrt(spectral_squared)),
            operator_rms=float(np.sqrt(operator_squared)),
            spectral_maximum=float(np.max(np.abs(spectral_difference))),
            operator_maximum=float(np.max(frobenius) / np.sqrt(self._rank)),
            spectral_gradient=spectral_gradient,
            operator_gradient=operator_gradient,
        )

    def objective(self, alpha: RealArray, weight: float) -> tuple[float, RealArray]:
        evaluation = self.evaluate(alpha)
        value = (
            weight * evaluation.spectral_squared
            + (1.0 - weight) * evaluation.operator_squared
        )
        gradient = (
            weight * evaluation.spectral_gradient
            + (1.0 - weight) * evaluation.operator_gradient
        )
        return float(value), np.asarray(gradient, dtype=np.float64)


def witness_record(
    *,
    shell_id: str,
    support_index: int,
    representative_count: int,
    weight: float,
    start_id: str,
    alpha: RealArray,
    evaluation: LossEvaluation,
    success: bool,
    iterations: int,
    function_evaluations: int,
    message: str,
) -> JsonObject:
    return {
        "shell_id": shell_id,
        "support_index_zero_based": support_index,
        "included_representative_count": representative_count,
        "spectral_scalarization_weight": weight,
        "start_id": start_id,
        "alpha": alpha.tolist(),
        "tau_1_spectral_rms": evaluation.spectral_rms,
        "tau_2_operator_rms_per_state": evaluation.operator_rms,
        "spectral_maximum": evaluation.spectral_maximum,
        "operator_maximum_per_state": evaluation.operator_maximum,
        "optimizer_success": success,
        "optimizer_iterations": iterations,
        "optimizer_function_evaluations": function_evaluations,
        "optimizer_message": message,
        "lower_bound_active_count": int(np.count_nonzero(alpha <= 1.0e-10)),
        "upper_bound_active_count": int(np.count_nonzero(alpha >= 2.0 - 1.0e-10)),
    }


def nondominated_indices(witnesses: list[JsonObject]) -> tuple[int, ...]:
    selected: list[int] = []
    for index, witness in enumerate(witnesses):
        spectral = numeric(witness["tau_1_spectral_rms"], "spectral RMS")
        operator = numeric(witness["tau_2_operator_rms_per_state"], "operator RMS")
        dominated = False
        for other_index, other in enumerate(witnesses):
            if other_index == index:
                continue
            other_spectral = numeric(other["tau_1_spectral_rms"], "spectral RMS")
            other_operator = numeric(
                other["tau_2_operator_rms_per_state"], "operator RMS"
            )
            if (
                other_spectral <= spectral
                and other_operator <= operator
                and (other_spectral < spectral or other_operator < operator)
            ):
                dominated = True
                break
        if not dominated:
            selected.append(index)
    return tuple(selected)


def finite_difference_gradient_check(
    loss: ShellScaleLoss, alpha: RealArray, weight: float
) -> JsonObject:
    value, analytic = loss.objective(alpha, weight)
    step = 1.0e-6
    finite = np.empty_like(alpha)
    for index in range(len(alpha)):
        plus = alpha.copy()
        minus = alpha.copy()
        plus[index] += step
        minus[index] -= step
        plus_value, _ = loss.objective(plus, weight)
        minus_value, _ = loss.objective(minus, weight)
        finite[index] = (plus_value - minus_value) / (2.0 * step)
    difference = analytic - finite
    scale = max(1.0, float(np.max(np.abs(analytic))), float(np.max(np.abs(finite))))
    return {
        "objective": value,
        "weight": weight,
        "maximum_absolute_gradient_difference": float(np.max(np.abs(difference))),
        "maximum_scaled_gradient_difference": float(np.max(np.abs(difference)) / scale),
    }


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
    design_value: JsonValue = json.loads(
        source_path(
            mapping(sources["truncation_design"], "truncation design"),
            "truncation design",
        ).read_text(encoding="utf-8")
    )
    design = mapping(design_value, "truncation design")
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
    coordinates = point_inventory(
        source_path(mapping(sources["point_manifest"], "point manifest"), "manifest")
    )
    cartesian = np.asarray(operator.representatives, dtype=np.float64) @ direct_basis.T
    rounded_radii = np.round(np.linalg.norm(cartesian, axis=1), decimals=9)
    shell_fields: list[ComplexArray] = []
    previous_radius = -1.0
    for shell in shells:
        radius = numeric(shell["display_radius_angstrom"], "shell radius")
        mask = (rounded_radii > previous_radius) & (rounded_radii <= radius)
        expected_count = int(
            numeric(shell["shell_representative_count"], "shell count")
        )
        if int(np.count_nonzero(mask)) != expected_count:
            raise RuntimeError(
                f"shell membership mismatch for {string(shell['shell_id'], 'shell id')}"
            )
        subset = adapter.FiniteWannierOperator(
            representatives=operator.representatives[mask],
            blocks_ev=operator.blocks_ev[mask],
            native_representative_count=operator.native_representative_count,
        )
        shell_fields.append(subset.matrices(coordinates))
        previous_radius = radius
    shell_matrices = np.asarray(shell_fields, dtype=np.complex128)
    full_matrices = operator.matrices(coordinates)
    reconstruction = np.sum(shell_matrices, axis=0) - full_matrices
    reconstruction_maximum = float(
        np.max(np.linalg.norm(reconstruction, axis=(-2, -1)))
    )
    if reconstruction_maximum > 1.0e-12:
        raise RuntimeError("native shell fields do not reconstruct the full operator")
    full_spectrum = np.linalg.eigvalsh(full_matrices)

    all_witnesses: list[JsonObject] = []
    support_summaries: list[JsonValue] = []
    gradient_check: JsonObject | None = None
    for support_index, shell in enumerate(shells[:-1]):
        shell_id = string(shell["shell_id"], "shell id")
        representative_count = int(
            numeric(shell["included_representative_count"], "representative count")
        )
        retained = np.asarray(shell_matrices[: support_index + 1], dtype=np.complex128)
        loss = ShellScaleLoss(
            shell_matrices=retained,
            full_matrices=full_matrices,
            full_spectrum=full_spectrum,
        )
        dimension = support_index + 1
        literal_alpha = np.ones(dimension, dtype=np.float64)
        alternating_alpha = np.asarray(
            [0.75 if index % 2 == 0 else 1.25 for index in range(dimension)],
            dtype=np.float64,
        )
        if support_index == 8:
            gradient_check = finite_difference_gradient_check(
                loss,
                np.linspace(0.85, 1.15, dimension, dtype=np.float64),
                0.5,
            )
        support_witnesses: list[JsonObject] = []
        literal_evaluation = loss.evaluate(literal_alpha)
        support_witnesses.append(
            witness_record(
                shell_id=shell_id,
                support_index=support_index,
                representative_count=representative_count,
                weight=-1.0,
                start_id="literal-alpha-one",
                alpha=literal_alpha,
                evaluation=literal_evaluation,
                success=True,
                iterations=0,
                function_evaluations=1,
                message="unoptimized literal truncation control",
            )
        )
        previous_best = literal_alpha
        for weight in WEIGHTS:
            starts = (
                ("literal-alpha-one", literal_alpha),
                ("alternating-0.75-1.25", alternating_alpha),
                ("continuation", previous_best),
            )
            best_value = np.inf
            best_alpha = previous_best
            for start_id, initial in starts:
                result = minimize(
                    fun=lambda alpha, bound_weight=weight, bound_loss=loss: (
                        bound_loss.objective(
                            np.asarray(alpha, dtype=np.float64), bound_weight
                        )
                    ),
                    x0=initial,
                    method="L-BFGS-B",
                    jac=True,
                    bounds=tuple((0.0, 2.0) for _ in range(dimension)),
                    options={
                        "maxiter": 300,
                        "ftol": 1.0e-14,
                        "gtol": 1.0e-10,
                        "maxls": 40,
                    },
                )
                alpha = np.asarray(result.x, dtype=np.float64)
                evaluation = loss.evaluate(alpha)
                record = witness_record(
                    shell_id=shell_id,
                    support_index=support_index,
                    representative_count=representative_count,
                    weight=weight,
                    start_id=start_id,
                    alpha=alpha,
                    evaluation=evaluation,
                    success=bool(result.success),
                    iterations=int(result.nit),
                    function_evaluations=int(result.nfev),
                    message=str(result.message),
                )
                support_witnesses.append(record)
                scalar_value = (
                    weight * evaluation.spectral_squared
                    + (1.0 - weight) * evaluation.operator_squared
                )
                if scalar_value < best_value:
                    best_value = scalar_value
                    best_alpha = alpha
            previous_best = best_alpha
        unique: dict[tuple[float, ...], JsonObject] = {}
        for witness in support_witnesses:
            alpha_key = tuple(
                round(numeric(value, "alpha"), 11)
                for value in values(witness["alpha"], "alpha")
            )
            existing = unique.get(alpha_key)
            if existing is None:
                unique[alpha_key] = witness
                continue
            existing_success = existing["optimizer_success"] is True
            witness_success = witness["optimizer_success"] is True
            if witness_success and not existing_success:
                unique[alpha_key] = witness
        retained_witnesses = list(unique.values())
        nondominated = nondominated_indices(retained_witnesses)
        for local_index, witness in enumerate(retained_witnesses):
            witness["support_local_nondominated"] = local_index in nondominated
            all_witnesses.append(witness)
        spectral_best = min(
            retained_witnesses,
            key=lambda item: numeric(item["tau_1_spectral_rms"], "spectral RMS"),
        )
        operator_best = min(
            retained_witnesses,
            key=lambda item: numeric(
                item["tau_2_operator_rms_per_state"], "operator RMS"
            ),
        )
        support_summaries.append(
            {
                "shell_id": shell_id,
                "support_index_zero_based": support_index,
                "included_representative_count": representative_count,
                "retained_unique_witness_count": len(retained_witnesses),
                "support_local_nondominated_witness_count": len(nondominated),
                "literal_tau_1": literal_evaluation.spectral_rms,
                "literal_tau_2": literal_evaluation.operator_rms,
                "minimum_observed_tau_1": numeric(
                    spectral_best["tau_1_spectral_rms"], "spectral minimum"
                ),
                "tau_2_at_minimum_observed_tau_1": numeric(
                    spectral_best["tau_2_operator_rms_per_state"],
                    "operator at spectral minimum",
                ),
                "minimum_observed_tau_2": numeric(
                    operator_best["tau_2_operator_rms_per_state"],
                    "operator minimum",
                ),
                "tau_1_at_minimum_observed_tau_2": numeric(
                    operator_best["tau_1_spectral_rms"],
                    "spectral at operator minimum",
                ),
            }
        )
    if gradient_check is None:
        raise RuntimeError("gradient check was not executed")
    successful_witnesses = [
        witness
        for witness in all_witnesses
        if witness["optimizer_success"] is True
        or witness["start_id"] == "literal-alpha-one"
    ]
    global_nondominated = nondominated_indices(successful_witnesses)
    for index, witness in enumerate(successful_witnesses):
        witness["global_loss_pair_nondominated"] = index in global_nondominated
    result: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "post_hoc": True,
        "calculator_invocations": 0,
        "independent_reconstruction_performed": False,
        "request": identity(REQUEST),
        "producer": identity(Path(__file__)),
        "authenticated_sources": authenticated,
        "model_family": {
            "proper_support_count": 17,
            "full_support_control_excluded": True,
            "parameterization": "one bounded real scale per retained native shell",
            "alpha_bounds": [0.0, 2.0],
            "alignment": "identity in the fixed authenticated rank-10 Wannier basis",
        },
        "optimization": {
            "method": "bounded L-BFGS-B with analytic gradients",
            "weights": list(WEIGHTS),
            "starts_per_weight": 3,
            "constructive_only": True,
            "failure_to_find_is_not_infeasibility": True,
            "successful_or_literal_witness_count": len(successful_witnesses),
            "global_loss_pair_nondominated_witness_count": len(global_nondominated),
        },
        "producer_checks": {
            "native_shell_reconstruction_maximum_frobenius_ev": reconstruction_maximum,
            "analytic_gradient_check": gradient_check,
        },
        "support_summaries": support_summaries,
        "witnesses": successful_witnesses,
        "evaluation": {
            "point_count": len(coordinates),
            "weights": "uniform 1/408",
            "energy_scale_ev": 1.0,
            "parent_values_consumed": False,
            "confirmation_402_geometry_consumed": False,
        },
        "execution": {
            "elapsed_seconds": float(time.perf_counter() - start),
            "output_path": str(OUTPUT),
        },
        "limitations": [
            "This is post-hoc bounded optimization, not prospective model acceptance.",
            "Scalarized multistart L-BFGS-B supplies constructive witnesses but no global infeasibility certificate.",
            "Ordered eigenvalue losses are nonsmooth at exact crossings or degeneracies; analytic gradients are interpreted as local binary64 derivatives.",
            "One scalar per complete shell preserves native block patterns and cannot explore arbitrary same-basis matrix refits.",
            "No Slater-Koster semantics, DFT-parent fidelity, experimental validation, or independent reconstruction is claimed.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
