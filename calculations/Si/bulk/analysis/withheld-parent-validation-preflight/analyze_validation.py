from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import numpy as np
from numpy.typing import NDArray
from projectkoios.integrations.quantumespresso.pw.nscf.data_extraction import (
    QeNscfDataExtractor,
)
from projectkoios.integrations.quantumespresso.saved_state import (
    QeSavedStateManifestJsonCodec,
    QeSavedStateManifestVerifier,
)
from projectkoios.physkit import units as _physkit_units

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (  # type: ignore[attr-defined]
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER
    )

from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.serialization import TypedJsonMappingSerializer

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-withheld-parent-nscf-v1"
)
RUN = ROOT / "run"
QEXSD = RUN / "tmp/system.save/data-file-schema.xml"
SAVED_STATE_MANIFEST = RUN / "nscf-saved-state-manifest.json"
POINT_MANIFEST = ROOT / "preflight-source/withheld-kpoint-manifest.json"
CRITERIA = ROOT / "preflight-source/validation-criteria.json"
CAMPAIGN_RESULT = ROOT / "campaign-result.json"
KSD_ROOT = Path("/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint")
QUALIFICATION_SCRIPT = (
    KSD_ROOT / "calculations/Si/bulk/analysis/provider-eligible-operator-qualification/"
    "run_analysis.py"
)
QUALIFICATION_RESULT = QUALIFICATION_SCRIPT.parent / "qualification-result.json"
GAMMA_PARENT_QEXSD = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-4x4x4-b12-david-20261031T072258Z/"
    "run/tmp/system.save/data-file-schema.xml"
)
OUTPUT = ROOT / "validation-result.json"
NSCF_OUTPUT = ROOT / "nscf-result.json"
HARTREE_TO_EV = 27.211386245988
WARNING = re.compile(rb"c_bands:\s+(\d+) eigenvalues? not converged")
EXPECTED = {
    QEXSD: "792898753c87d92328e6c511259c77c843c3ae59b212c1d8502b3e53563b8fb2",
    SAVED_STATE_MANIFEST: (
        "8de35151ad55bca4658c472ec51ddd1468902e7ba6e6529d42c6df463f726d20"
    ),
    POINT_MANIFEST: (
        "754bce5030ef0e34eb092406b27d9094287b4f749e358ef36404040f44b8d2b4"
    ),
    CRITERIA: "ab2a9f18876f773e8c6535e00a6ce65be5c65b32117b258d503423007389c5cb",
    CAMPAIGN_RESULT: (
        "babd24f429f4eb51082235c2d7f6afaeccf193160a139cd295f14916b1cbb7cd"
    ),
    QUALIFICATION_RESULT: (
        "e82995489fd5e5084008c0a7d8bf6bc42c6c219838b073f0b0d9a56d24e04c53"
    ),
    GAMMA_PARENT_QEXSD: (
        "cc389a14d6b9f809eab69ba30b86129a01951788a3fdbc290589ef8f5f69adb0"
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observation(path: Path) -> JsonObject:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


@dataclass(frozen=True, slots=True)
class ParentSpectrum:
    """Retain authenticated withheld parent eigenvalues in manifest order."""

    fractional_kpoints: RealArray
    eigenvalues_ev: RealArray
    native_weights: RealArray
    qexsd: object


@dataclass(frozen=True, slots=True)
class CandidateSpectrum:
    """Retain the authenticated finite Wannier prediction on withheld points."""

    eigenvalues_ev: RealArray
    operator: object
    module: ModuleType


@dataclass(frozen=True, slots=True)
class QuadraticFit:
    """Represent one local Cartesian energy fit."""

    constant_ev: float
    gradient_ev_angstrom: RealArray
    hessian_ev_angstrom2: RealArray
    residual_rms_ev: float
    residual_maximum_ev: float
    design_condition_number: float

    def minimum_delta(self) -> RealArray:
        return -np.linalg.solve(self.hessian_ev_angstrom2, self.gradient_ev_angstrom)

    def minimum_energy(self) -> float:
        delta = self.minimum_delta()
        return float(
            self.constant_ev
            + self.gradient_ev_angstrom @ delta
            + 0.5 * delta @ self.hessian_ev_angstrom2 @ delta
        )


class SourceAuthenticator:
    """Fail closed before interpreting any retained result."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        records: JsonObject = {}
        for path, expected in EXPECTED.items():
            if not path.is_file() or path.is_symlink() or sha256(path) != expected:
                raise RuntimeError(f"source identity mismatch: {path}")
            records[path.name + ":" + str(len(records))] = observation(path)
        return records


class QexsdLoader:
    """Parse the withheld QEXSD and prove its ordering matches the frozen manifest."""

    __slots__ = ("_summary",)

    def __init__(self) -> None:
        self._summary: JsonObject | None = None

    @property
    def summary(self) -> JsonObject:
        if self._summary is None:
            raise RuntimeError("QEXSD summary requested before loading")
        return self._summary

    def execute(self, point_record: JsonObject) -> ParentSpectrum:
        execution = json.loads((RUN / "execution.json").read_text(encoding="utf-8"))
        if execution["status"] != "succeeded" or execution["returncode"] != 0:
            raise RuntimeError("withheld NSCF did not succeed")
        saved_payload = SAVED_STATE_MANIFEST.read_bytes()
        saved_manifest = QeSavedStateManifestJsonCodec().loads(saved_payload)
        QeSavedStateManifestVerifier().verify(saved_manifest, RUN / "tmp")
        document = parse_qexsd(QEXSD)
        stdout = (RUN / "pw.out").read_bytes()
        stderr = (RUN / "pw.err").read_bytes()
        extracted = QeNscfDataExtractor().extract(
            stdout_payload=stdout,
            stderr_payload=stderr,
            qexsd_document=document,
            expected_band_count=12,
            expected_kpoint_count=408,
        )
        warnings = tuple(int(item.group(1)) for item in WARNING.finditer(stdout))
        if warnings:
            raise RuntimeError("withheld NSCF contains unconverged-eigenvalue warnings")
        points_value = point_record["points"]
        coordinate_value = point_record["coordinate_convention"]
        if not isinstance(points_value, list) or not isinstance(coordinate_value, dict):
            raise TypeError("point manifest has unexpected shape")
        fractional = np.asarray(
            [item["fractional_reciprocal_coordinates"] for item in points_value],
            dtype=np.float64,
        )
        reciprocal_coefficients = np.asarray(
            document.reciprocal_lattice_coefficients, dtype=np.float64
        )
        expected_native = fractional @ reciprocal_coefficients
        observed_native = np.asarray(document.k_points, dtype=np.float64)
        maximum_coordinate_error = float(
            np.max(np.abs(expected_native - observed_native))
        )
        if maximum_coordinate_error > 5.0e-12:
            raise RuntimeError("QEXSD k-point ordering disagrees with frozen manifest")
        eigenvalues = np.asarray(document.eigenvalues, dtype=np.float64) * HARTREE_TO_EV
        if eigenvalues.shape != (408, 12) or not np.all(np.isfinite(eigenvalues)):
            raise RuntimeError("withheld eigenvalue table is invalid")
        native_weights = np.asarray(document.k_point_weights, dtype=np.float64)
        if not np.isclose(np.sum(native_weights), 2.0, atol=1.0e-12, rtol=0.0):
            raise RuntimeError("native k-point weights have unexpected sum")
        self._summary = {
            "qexsd": observation(QEXSD),
            "qexsd_version": extracted.qexsd_version,
            "producing_application": extracted.producing_application,
            "producing_application_version": extracted.producing_application_version,
            "declared_unit_system_label": extracted.declared_unit_system_label,
            "exit_status": extracted.exit_status,
            "sampled_k_point_count": extracted.sampled_k_point_count,
            "band_count": extracted.band_count,
            "job_completed": extracted.streams.stdout.job_completed,
            "warning_line_count": 0,
            "total_reported_unconverged_eigenvalues": 0,
            "all_eigenvalues_finite": True,
            "all_occupations_finite": True,
            "native_weight_sum": float(np.sum(native_weights)),
            "maximum_manifest_to_qexsd_native_coordinate_error": (
                maximum_coordinate_error
            ),
            "stderr": observation(RUN / "pw.err"),
            "stdout": observation(RUN / "pw.out"),
            "ieee_flags_disposition": (
                "diagnostic only: native convergence succeeded, all parsed values are "
                "finite, and no unconverged-eigenvalue warning was emitted"
            ),
        }
        return ParentSpectrum(fractional, eigenvalues, native_weights, document)


class CandidateLoader:
    """Reuse the authenticated finite-operator prototype without calculator access."""

    __slots__ = ()

    def execute(self, fractional: RealArray) -> CandidateSpectrum:
        spec = importlib.util.spec_from_file_location(
            "provider_eligible_operator_qualification", QUALIFICATION_SCRIPT
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load candidate qualification module")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        authenticator = module.ArtifactAuthenticator()
        eig = authenticator.execute(module.ARTIFACTS["eig"])
        candidate = module.CandidateOperatorLoader(authenticator, eig).execute(
            module.ELIGIBLE_DECLARATION
        )
        eigenvalues = candidate.finite_operator.eigenvalues(fractional)
        if eigenvalues.shape != (408, 10) or not np.all(np.isfinite(eigenvalues)):
            raise RuntimeError("candidate spectrum has unexpected shape")
        return CandidateSpectrum(eigenvalues, candidate.finite_operator, module)


class InjectiveSpectralMatcher:
    """Match a sorted rank-10 spectrum injectively into a sorted rank-12 spectrum."""

    __slots__ = ()

    def execute(self, candidate: RealArray, parent: RealArray) -> JsonObject:
        point_records: list[JsonValue] = []
        residuals: list[float] = []
        for index, (candidate_row, parent_row) in enumerate(
            zip(candidate, parent, strict=True)
        ):
            best_cost = math.inf
            best_indices: tuple[int, ...] | None = None
            for first_omitted in range(12):
                for second_omitted in range(first_omitted + 1, 12):
                    indices = tuple(
                        item
                        for item in range(12)
                        if item not in {first_omitted, second_omitted}
                    )
                    differences = candidate_row - parent_row[list(indices)]
                    cost = float(differences @ differences)
                    if cost < best_cost:
                        best_cost = cost
                        best_indices = indices
            assert best_indices is not None
            differences = candidate_row - parent_row[list(best_indices)]
            absolute = np.abs(differences)
            residuals.extend(float(value) for value in absolute)
            point_records.append(
                {
                    "point_index_zero_based": index,
                    "matched_parent_band_indices_zero_based": list(best_indices),
                    "omitted_parent_band_indices_zero_based": [
                        item for item in range(12) if item not in best_indices
                    ],
                    "maximum_absolute_error_ev": float(np.max(absolute)),
                    "rms_error_ev": float(np.sqrt(np.mean(differences**2))),
                }
            )
        array = np.asarray(residuals, dtype=np.float64)
        return {
            "method": (
                "minimum-square order-preserving injective matching of ten sorted "
                "candidate eigenvalues into twelve sorted parent eigenvalues"
            ),
            "point_count": len(point_records),
            "scalar_residual_count": len(array),
            "maximum_absolute_error_ev": float(np.max(array)),
            "rms_error_ev": float(np.sqrt(np.mean(array**2))),
            "percentile_95_absolute_error_ev": float(np.percentile(array, 95.0)),
            "gating": False,
            "points": point_records,
        }


class ValleyPointIndex:
    """Resolve frozen semantic roles to exact spectrum rows."""

    __slots__ = ("_points",)

    def __init__(self, points: list[JsonValue]) -> None:
        self._points = points

    def center(self, label: str) -> int:
        matches = self._matching(label, "candidate-center", None)
        if len(matches) != 1:
            raise RuntimeError(f"candidate center count mismatch for {label}")
        return matches[0][0]

    def role(
        self,
        label: str,
        kind: str,
        step: float,
        axes: tuple[int, ...],
        signs: tuple[int, ...],
    ) -> int:
        matches = self._matching(label, kind, step)
        selected = [
            index
            for index, role in matches
            if tuple(role["cartesian_axes_zero_based"]) == axes
            and tuple(role["signs"]) == signs
        ]
        if len(selected) != 1:
            raise RuntimeError(
                f"point-role count mismatch: {label} {kind} {step} {axes} {signs}"
            )
        return selected[0]

    def hessian_rows(self, label: str) -> tuple[tuple[int, RealArray], ...]:
        rows: list[tuple[int, RealArray]] = [
            (self.center(label), np.zeros(3, dtype=np.float64))
        ]
        for step in (0.002, 0.005, 0.010):
            for index, role in self._matching(label, "hessian-axial", step):
                delta = np.zeros(3, dtype=np.float64)
                axis = int(role["cartesian_axes_zero_based"][0])
                delta[axis] = int(role["signs"][0]) * step
                rows.append((index, delta))
            for index, role in self._matching(label, "hessian-mixed", step):
                delta = np.zeros(3, dtype=np.float64)
                for axis, sign in zip(
                    role["cartesian_axes_zero_based"], role["signs"], strict=True
                ):
                    delta[int(axis)] = int(sign) * step
                rows.append((index, delta))
        if len(rows) != 55:
            raise RuntimeError(f"joint Hessian row count mismatch for {label}")
        return tuple(rows)

    def _matching(
        self, label: str, kind: str, step: float | None
    ) -> list[tuple[int, dict[str, JsonValue]]]:
        matches: list[tuple[int, dict[str, JsonValue]]] = []
        for index, point in enumerate(self._points):
            if not isinstance(point, dict):
                raise TypeError("point records must be mappings")
            roles = point["roles"]
            if not isinstance(roles, list):
                raise TypeError("point roles must be a list")
            for role in roles:
                if not isinstance(role, dict):
                    raise TypeError("point role must be a mapping")
                if (
                    role["valley_label"] == label
                    and role["kind"] == kind
                    and role["step_inverse_angstrom"] == step
                ):
                    matches.append((index, role))
        return matches


class LocalQuadraticAnalyzer:
    """Fit locations and reconstruct the exact finite-difference Hessians."""

    __slots__ = ("_index",)

    def __init__(self, index: ValleyPointIndex) -> None:
        self._index = index

    def fit_joint(self, label: str, energies: RealArray) -> QuadraticFit:
        rows = self._index.hessian_rows(label)
        deltas = np.asarray([delta for _, delta in rows], dtype=np.float64)
        values = np.asarray([energies[index] for index, _ in rows], dtype=np.float64)
        scale = 0.010
        x = deltas / scale
        design = np.column_stack(
            (
                np.ones(len(x)),
                x,
                0.5 * x[:, 0] ** 2,
                0.5 * x[:, 1] ** 2,
                0.5 * x[:, 2] ** 2,
                x[:, 0] * x[:, 1],
                x[:, 0] * x[:, 2],
                x[:, 1] * x[:, 2],
            )
        )
        coefficients, _, rank, _ = np.linalg.lstsq(design, values, rcond=None)
        if rank != 10:
            raise RuntimeError(f"quadratic design is rank deficient for {label}")
        fitted = design @ coefficients
        hessian = (
            np.asarray(
                [
                    [coefficients[4], coefficients[7], coefficients[8]],
                    [coefficients[7], coefficients[5], coefficients[9]],
                    [coefficients[8], coefficients[9], coefficients[6]],
                ],
                dtype=np.float64,
            )
            / scale**2
        )
        return QuadraticFit(
            constant_ev=float(coefficients[0]),
            gradient_ev_angstrom=np.asarray(coefficients[1:4]) / scale,
            hessian_ev_angstrom2=hessian,
            residual_rms_ev=float(np.sqrt(np.mean((values - fitted) ** 2))),
            residual_maximum_ev=float(np.max(np.abs(values - fitted))),
            design_condition_number=float(np.linalg.cond(design)),
        )

    def hessian(self, label: str, energies: RealArray, step: float) -> RealArray:
        origin = energies[self._index.center(label)]
        hessian = np.empty((3, 3), dtype=np.float64)
        for row in range(3):
            plus = energies[
                self._index.role(label, "hessian-axial", step, (row,), (1,))
            ]
            minus = energies[
                self._index.role(label, "hessian-axial", step, (row,), (-1,))
            ]
            hessian[row, row] = (plus - 2.0 * origin + minus) / step**2
            for column in range(row):
                values: dict[tuple[int, int], float] = {}
                for row_sign in (-1, 1):
                    for column_sign in (-1, 1):
                        values[(row_sign, column_sign)] = energies[
                            self._index.role(
                                label,
                                "hessian-mixed",
                                step,
                                (column, row),
                                (column_sign, row_sign),
                            )
                        ]
                value = (
                    values[(1, 1)]
                    - values[(1, -1)]
                    - values[(-1, 1)]
                    + values[(-1, -1)]
                ) / (4.0 * step**2)
                hessian[row, column] = value
                hessian[column, row] = value
        return hessian


class EffectiveMassComparator:
    """Compare full tensors and direction-matched principal masses."""

    __slots__ = ("_constant",)

    def __init__(self, electron_mass_curvature_ev_angstrom2: float) -> None:
        self._constant = electron_mass_curvature_ev_angstrom2

    def execute(
        self, label: str, candidate_hessian: RealArray, parent_hessian: RealArray
    ) -> JsonObject:
        candidate_curvature, candidate_axes = np.linalg.eigh(candidate_hessian)
        parent_curvature, parent_axes = np.linalg.eigh(parent_hessian)
        if np.any(candidate_curvature <= 0.0) or np.any(parent_curvature <= 0.0):
            raise RuntimeError(f"nonpositive principal curvature for {label}")
        candidate_masses = self._constant / candidate_curvature
        parent_masses = self._constant / parent_curvature
        axis_index = "xyz".index(label[-1])
        candidate_longitudinal = int(np.argmax(np.abs(candidate_axes[axis_index, :])))
        parent_longitudinal = int(np.argmax(np.abs(parent_axes[axis_index, :])))
        candidate_transverse = [
            item for item in range(3) if item != candidate_longitudinal
        ]
        parent_transverse = [item for item in range(3) if item != parent_longitudinal]
        direct_score = sum(
            abs(candidate_axes[:, c] @ parent_axes[:, p])
            for c, p in zip(candidate_transverse, parent_transverse, strict=True)
        )
        swapped_parent = list(reversed(parent_transverse))
        swapped_score = sum(
            abs(candidate_axes[:, c] @ parent_axes[:, p])
            for c, p in zip(candidate_transverse, swapped_parent, strict=True)
        )
        if swapped_score > direct_score:
            parent_transverse = swapped_parent
        matches = [("longitudinal", candidate_longitudinal, parent_longitudinal)]
        matches.extend(
            (f"transverse_{index + 1}", candidate_index, parent_index)
            for index, (candidate_index, parent_index) in enumerate(
                zip(candidate_transverse, parent_transverse, strict=True)
            )
        )
        comparisons: list[JsonValue] = []
        for name, candidate_index, parent_index in matches:
            relative_error = abs(
                candidate_masses[candidate_index] - parent_masses[parent_index]
            ) / abs(parent_masses[parent_index])
            comparisons.append(
                {
                    "name": name,
                    "candidate_principal_index": candidate_index,
                    "parent_principal_index": parent_index,
                    "candidate_mass_ratio_to_electron_mass": float(
                        candidate_masses[candidate_index]
                    ),
                    "parent_mass_ratio_to_electron_mass": float(
                        parent_masses[parent_index]
                    ),
                    "absolute_relative_error": float(relative_error),
                    "maximum": 0.08,
                    "passed": bool(relative_error <= 0.08),
                    "axis_absolute_overlap": float(
                        abs(
                            candidate_axes[:, candidate_index]
                            @ parent_axes[:, parent_index]
                        )
                    ),
                }
            )
        candidate_tensor = self._constant * np.linalg.inv(candidate_hessian)
        parent_tensor = self._constant * np.linalg.inv(parent_hessian)
        return {
            "coordinate_basis": "Cartesian reciprocal axes",
            "candidate_hessian_ev_angstrom_squared": candidate_hessian.tolist(),
            "parent_hessian_ev_angstrom_squared": parent_hessian.tolist(),
            "candidate_mass_tensor_in_electron_masses": candidate_tensor.tolist(),
            "parent_mass_tensor_in_electron_masses": parent_tensor.tolist(),
            "candidate_principal_curvatures_ev_angstrom_squared": (
                candidate_curvature.tolist()
            ),
            "parent_principal_curvatures_ev_angstrom_squared": (
                parent_curvature.tolist()
            ),
            "candidate_principal_axes_cartesian_columns": candidate_axes.tolist(),
            "parent_principal_axes_cartesian_columns": parent_axes.tolist(),
            "comparisons": comparisons,
            "passed": all(bool(item["passed"]) for item in comparisons),
        }


class WithheldParentValidator:
    """Apply only the frozen intended-use criteria after structural verification."""

    __slots__ = ()

    def execute(self) -> tuple[JsonObject, JsonObject]:
        sources = SourceAuthenticator().execute()
        points = json.loads(POINT_MANIFEST.read_text(encoding="utf-8"))
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
        loader = QexsdLoader()
        parent = loader.execute(points)
        candidate = CandidateLoader().execute(parent.fractional_kpoints)
        point_values = points["points"]
        if not isinstance(point_values, list):
            raise TypeError("manifest points must be a list")
        index = ValleyPointIndex(point_values)
        local = LocalQuadraticAnalyzer(index)
        mass_comparator = EffectiveMassComparator(
            candidate.module.ELECTRON_MASS_CURVATURE_EV_ANGSTROM2
        )
        qualification = json.loads(QUALIFICATION_RESULT.read_text(encoding="utf-8"))
        frozen_valleys = qualification["results"]["valley_family"]["valleys"]
        frozen_masses = qualification["results"]["effective_mass_diagnostic"]["valleys"]
        frozen_valley_by_label = {item["label"]: item for item in frozen_valleys}
        frozen_mass_by_label = {item["valley_label"]: item for item in frozen_masses}
        labels = ("-x", "+x", "-y", "+y", "-z", "+z")
        direct_basis = np.asarray(
            points["coordinate_convention"]["direct_basis_columns_angstrom"],
            dtype=np.float64,
        )
        reciprocal_basis = 2.0 * np.pi * np.linalg.inv(direct_basis).T
        inverse_reciprocal = np.linalg.inv(reciprocal_basis)
        valley_records: list[JsonValue] = []
        location_passes: list[bool] = []
        mass_passes: list[bool] = []
        parent_minimum_energies: list[float] = []
        candidate_minimum_energies: list[float] = []
        frozen_reconstruction_differences: list[float] = []
        for label in labels:
            center_index = index.center(label)
            parent_conduction = parent.eigenvalues_ev[:, 4]
            candidate_conduction = candidate.eigenvalues_ev[:, 4]
            parent_fit = local.fit_joint(label, parent_conduction)
            parent_hessian_eigenvalues = np.linalg.eigvalsh(
                parent_fit.hessian_ev_angstrom2
            )
            if np.any(parent_hessian_eigenvalues <= 0.0):
                raise RuntimeError(f"joint parent fit is not positive at {label}")
            parent_delta = parent_fit.minimum_delta()
            within_capture = bool(np.max(np.abs(parent_delta)) <= 0.040)
            if not within_capture:
                raise RuntimeError(f"parent minimum escaped capture domain at {label}")
            parent_fractional = (
                parent.fractional_kpoints[center_index]
                + inverse_reciprocal @ parent_delta
            ) % 1.0
            location_error = float(np.linalg.norm(parent_delta))
            location_limit = float(
                criteria["gating_comparisons"]["valley_position"][
                    "maximum_inverse_angstrom"
                ]
            )
            location_pass = location_error <= location_limit
            candidate_hessian = local.hessian(label, candidate_conduction, 0.002)
            parent_hessian = local.hessian(label, parent_conduction, 0.002)
            mass_comparison = mass_comparator.execute(
                label, candidate_hessian, parent_hessian
            )
            sensitivity: list[JsonValue] = []
            for step in (0.005, 0.010):
                candidate_step_hessian = local.hessian(
                    label, candidate_conduction, step
                )
                parent_step_hessian = local.hessian(label, parent_conduction, step)
                sensitivity.append(
                    {
                        "step_inverse_angstrom": step,
                        "candidate_principal_masses": (
                            candidate.module.ELECTRON_MASS_CURVATURE_EV_ANGSTROM2
                            / np.linalg.eigvalsh(candidate_step_hessian)
                        ).tolist(),
                        "parent_principal_masses": (
                            candidate.module.ELECTRON_MASS_CURVATURE_EV_ANGSTROM2
                            / np.linalg.eigvalsh(parent_step_hessian)
                        ).tolist(),
                    }
                )
            frozen_record = frozen_valley_by_label[label]
            frozen_energy = float(frozen_record["energy_ev_native_reference"])
            candidate_energy = float(candidate_conduction[center_index])
            frozen_reconstruction_differences.append(
                abs(candidate_energy - frozen_energy)
            )
            frozen_primary = next(
                item
                for item in frozen_mass_by_label[label]["stencils"]
                if item["step_inverse_angstrom"] == 0.002
            )
            frozen_curvatures = np.asarray(
                frozen_primary["principal_curvatures_ev_angstrom_squared"],
                dtype=np.float64,
            )
            reconstructed_curvatures = np.linalg.eigvalsh(candidate_hessian)
            frozen_curvature_difference = float(
                np.max(np.abs(frozen_curvatures - reconstructed_curvatures))
            )
            parent_minimum_energy = parent_fit.minimum_energy()
            parent_minimum_energies.append(parent_minimum_energy)
            candidate_minimum_energies.append(candidate_energy)
            location_passes.append(location_pass)
            mass_passes.append(bool(mass_comparison["passed"]))
            valley_records.append(
                {
                    "label": label,
                    "candidate_center_fractional": parent.fractional_kpoints[
                        center_index
                    ].tolist(),
                    "frozen_candidate_energy_ev": frozen_energy,
                    "reconstructed_candidate_energy_ev": candidate_energy,
                    "candidate_energy_reconstruction_difference_ev": abs(
                        candidate_energy - frozen_energy
                    ),
                    "parent_minimum_fractional": parent_fractional.tolist(),
                    "parent_minimum_energy_ev": parent_minimum_energy,
                    "parent_minimum_delta_cartesian_inverse_angstrom": (
                        parent_delta.tolist()
                    ),
                    "parent_minimum_displacement_inverse_angstrom": location_error,
                    "location_maximum_inverse_angstrom": location_limit,
                    "location_passed": location_pass,
                    "within_capture_domain": within_capture,
                    "parent_joint_fit": {
                        "gradient_ev_angstrom": (
                            parent_fit.gradient_ev_angstrom.tolist()
                        ),
                        "hessian_ev_angstrom_squared": (
                            parent_fit.hessian_ev_angstrom2.tolist()
                        ),
                        "principal_curvatures_ev_angstrom_squared": (
                            parent_hessian_eigenvalues.tolist()
                        ),
                        "residual_rms_ev": parent_fit.residual_rms_ev,
                        "residual_maximum_ev": parent_fit.residual_maximum_ev,
                        "design_condition_number": (parent_fit.design_condition_number),
                    },
                    "primary_mass_comparison": mass_comparison,
                    (
                        "candidate_primary_curvature_reconstruction_"
                        "maximum_ev_angstrom_squared"
                    ): frozen_curvature_difference,
                    "scale_sensitivity": sensitivity,
                }
            )
        gamma_parent = parse_qexsd(GAMMA_PARENT_QEXSD)
        gamma_parent_ev = (
            np.asarray(gamma_parent.eigenvalues, dtype=np.float64) * HARTREE_TO_EV
        )
        gamma_index = int(
            np.argmin(np.linalg.norm(np.asarray(gamma_parent.k_points), axis=1))
        )
        parent_vbm = float(gamma_parent_ev[gamma_index, 3])
        candidate_vbm = float(
            candidate.operator.eigenvalues(np.zeros((1, 3), dtype=np.float64))[0, 3]
        )
        parent_gap = min(parent_minimum_energies) - parent_vbm
        candidate_gap = min(candidate_minimum_energies) - candidate_vbm
        gap_error = abs(candidate_gap - parent_gap) / abs(parent_gap)
        gap_pass = gap_error <= 0.05
        spectral = InjectiveSpectralMatcher().execute(
            candidate.eigenvalues_ev, parent.eigenvalues_ev
        )
        all_gates = [gap_pass, *location_passes, *mass_passes]
        scientific_status = (
            "adequate-for-declared-intended-use"
            if all(all_gates)
            else "not-adequate-for-declared-intended-use"
        )
        validation: JsonObject = {
            "schema_version": 1,
            "status": "withheld-parent-validation-complete",
            "calculator_invocations_in_postprocessing": 0,
            "calculator_occurrence": {
                "invocation_count": 1,
                "retry_count": 0,
                "execution_status": "succeeded",
                "return_code": 0,
            },
            "sources": sources,
            "native_parent": loader.summary,
            "criteria": observation(CRITERIA),
            "candidate_prediction_source": observation(QUALIFICATION_RESULT),
            "structural_checks": {
                "point_order_verified": True,
                "saved_state_verified": True,
                "candidate_operator_authenticated": True,
                "maximum_frozen_candidate_energy_reconstruction_difference_ev": max(
                    frozen_reconstruction_differences
                ),
            },
            "indirect_gap": {
                "parent_vbm_ev_native_reference": parent_vbm,
                "candidate_vbm_ev_native_reference": candidate_vbm,
                "parent_indirect_gap_ev": parent_gap,
                "candidate_indirect_gap_ev": candidate_gap,
                "absolute_relative_error": gap_error,
                "maximum": 0.05,
                "passed": gap_pass,
            },
            "valleys": valley_records,
            "spectral_residuals": spectral,
            "gate_summary": {
                "indirect_gap_passed": gap_pass,
                "all_valley_locations_passed": all(location_passes),
                "all_effective_masses_passed": all(mass_passes),
                "scientific_qualification_status": scientific_status,
            },
            "scope_note": (
                "A failure denotes inadequacy for the frozen SSSP-pilot intended-use "
                "targets, not intrinsic invalidity of the finite Wannier operator. "
                "The PseudoDojo and independent-toolchain gates remain unsatisfied."
            ),
        }
        nscf: JsonObject = {
            "schema_version": 1,
            "native_execution": loader.summary,
            "saved_state": {
                "manifest": observation(SAVED_STATE_MANIFEST),
                "verified": True,
            },
            "diagonalization_diagnostics": {
                "algorithm": "david",
                "warning_line_count": 0,
                "total_reported_unconverged_eigenvalues": 0,
                "disposition": "NO_ACTION_REQUIRED",
            },
            "scientific_disposition": (
                "Eligible as the exact direct-parent handoff for the frozen withheld "
                "comparison; native success alone is not scientific acceptance."
            ),
        }
        return nscf, validation


def parse_qexsd(path: Path) -> object:
    payload = path.read_bytes()
    return QuantumEspressoXsdDocumentParser().execute(
        QexsdSource(
            canonical_path=str(path),
            sha256=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
            content=payload,
        )
    )


def main() -> None:
    if OUTPUT.exists() or NSCF_OUTPUT.exists():
        raise RuntimeError("postprocessing result already exists")
    nscf, validation = WithheldParentValidator().execute()
    serializer = TypedJsonMappingSerializer()
    NSCF_OUTPUT.write_bytes(serializer.serialize(nscf))
    OUTPUT.write_bytes(serializer.serialize(validation))


if __name__ == "__main__":
    main()
