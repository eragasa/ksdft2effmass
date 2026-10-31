from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array as RealArray
from scipy import constants  # type: ignore[import-untyped]

from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.serialization import TypedJsonMappingSerializer

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
S30_ROOT = BULK / "analysis/c6-b20-w21-untruncated-characterization"
S30_SCRIPT = S30_ROOT / "run_analysis.py"
S30_RESULT = S30_ROOT / "characterization-result.json"
PARENT_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-withheld-parent-nscf-v1"
)
PARENT_RESULT = PARENT_ROOT / "validation-result.json"
PARENT_QEXSD = PARENT_ROOT / "run/tmp/system.save/data-file-schema.xml"
POINT_MANIFEST = PARENT_ROOT / "preflight-source/withheld-kpoint-manifest.json"
CRITERIA = PARENT_ROOT / "preflight-source/validation-criteria.json"
OUTPUT = ROOT / "development-result.json"
HARTREE_TO_EV = 27.211386245988
ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 = (
    constants.hbar**2 / constants.m_e / constants.electron_volt * 1.0e20
)
EXPECTED = {
    S30_SCRIPT: "985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e",
    S30_RESULT: "37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18",
    PARENT_RESULT: "46f3716e20037187989863fccad9181402a7dc4f4b89e3c143527b10353c7aa6",
    PARENT_QEXSD: "792898753c87d92328e6c511259c77c843c3ae59b212c1d8502b3e53563b8fb2",
    POINT_MANIFEST: "754bce5030ef0e34eb092406b27d9094287b4f749e358ef36404040f44b8d2b4",
    CRITERIA: "ab2a9f18876f773e8c6535e00a6ce65be5c65b32117b258d503423007389c5cb",
}


class FiniteOperator(Protocol):
    """Expose only the finite-operator behavior consumed by S40."""

    def eigenvalues(self, kpoints: RealArray, chunk_size: int = 2048) -> RealArray: ...


@dataclass(frozen=True, slots=True)
class ErrorStatistics:
    """Retain scalar summaries for an explicitly aligned difference."""

    maximum_absolute_ev: float
    rms_ev: float
    percentile_95_absolute_ev: float

    @classmethod
    def from_values(cls, values: RealArray) -> ErrorStatistics:
        absolute = np.abs(values)
        return cls(
            maximum_absolute_ev=float(np.max(absolute)),
            rms_ev=float(np.sqrt(np.mean(np.square(values)))),
            percentile_95_absolute_ev=float(np.percentile(absolute, 95.0)),
        )

    def to_json(self) -> JsonObject:
        return {
            "maximum_absolute_ev": self.maximum_absolute_ev,
            "rms_ev": self.rms_ev,
            "percentile_95_absolute_ev": self.percentile_95_absolute_ev,
        }


@dataclass(frozen=True, slots=True)
class MassComparison:
    """Retain one direction-matched three-principal-mass comparison."""

    record: JsonObject
    passed: bool


class SourceAuthenticator:
    """Authenticate every retained input before parsing."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        sources: JsonObject = {}
        for index, (path, expected) in enumerate(EXPECTED.items()):
            if not path.is_file() or path.is_symlink() or sha256(path) != expected:
                raise RuntimeError(f"source identity mismatch: {path}")
            sources[f"source_{index}"] = identity(path)
        return sources


class CandidateLoader:
    """Load the exact S30 operator and predictions without calculator access."""

    __slots__ = ()

    def execute(self) -> tuple[FiniteOperator, ModuleType, JsonObject]:
        specification = importlib.util.spec_from_file_location(
            "c6_b20_w21_s30", S30_SCRIPT
        )
        if specification is None or specification.loader is None:
            raise RuntimeError("cannot load S30 implementation")
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        specification.loader.exec_module(module)
        authenticator = module.ArtifactAuthenticator()
        eig = authenticator.execute(module.ARTIFACTS["eig"])
        candidate = module.CandidateOperatorLoader(authenticator, eig).execute(
            module.ELIGIBLE_DECLARATION
        )
        operator = cast(FiniteOperator, candidate.finite_operator)
        result = json.loads(S30_RESULT.read_text(encoding="utf-8"))
        if not isinstance(result, dict):
            raise TypeError("S30 result must be a mapping")
        return operator, module, cast(JsonObject, result)


class ParentLoader:
    """Load and correlate the revealed 408-point parent spectrum."""

    __slots__ = ()

    def execute(self, manifest: JsonObject) -> tuple[RealArray, RealArray]:
        payload = PARENT_QEXSD.read_bytes()
        document = QuantumEspressoXsdDocumentParser().execute(
            QexsdSource(
                canonical_path=str(PARENT_QEXSD),
                sha256=hashlib.sha256(payload).hexdigest(),
                byte_count=len(payload),
                content=payload,
            )
        )
        point_values = list_values(manifest["points"], "point manifest points")
        fractional = np.asarray(
            [
                vector3(
                    point["fractional_reciprocal_coordinates"],
                    "point fractional coordinates",
                )
                for point in point_values
            ],
            dtype=np.float64,
        )
        reciprocal_coefficients = np.asarray(
            document.reciprocal_lattice_coefficients, dtype=np.float64
        )
        expected_native = fractional @ reciprocal_coefficients
        observed_native = np.asarray(document.k_points, dtype=np.float64)
        if np.max(np.abs(expected_native - observed_native)) > 5.0e-12:
            raise RuntimeError("parent QEXSD order disagrees with point manifest")
        eigenvalues = np.asarray(document.eigenvalues, dtype=np.float64) * HARTREE_TO_EV
        if eigenvalues.shape != (408, 12) or not np.all(np.isfinite(eigenvalues)):
            raise RuntimeError("parent spectrum is invalid")
        return fractional, eigenvalues


class InjectiveSpectralMatcher:
    """Match each ordered rank-10 spectrum injectively into 12 parent bands."""

    __slots__ = ()

    def execute(self, candidate: RealArray, parent: RealArray) -> JsonObject:
        residuals: list[float] = []
        selected_records: list[JsonValue] = []
        combinations = tuple(itertools.combinations(range(12), 10))
        for point_index, (candidate_row, parent_row) in enumerate(
            zip(candidate, parent, strict=True)
        ):
            best_indices = min(
                combinations,
                key=lambda indices: float(
                    np.sum(np.square(candidate_row - parent_row[list(indices)]))
                ),
            )
            difference = candidate_row - parent_row[list(best_indices)]
            residuals.extend(float(value) for value in difference)
            selected_records.append(
                {
                    "point_index_zero_based": point_index,
                    "parent_band_indices_one_based": [
                        value + 1 for value in best_indices
                    ],
                }
            )
        values = np.asarray(residuals, dtype=np.float64)
        return {
            "alignment": (
                "gauge-invariant injective ordered-spectrum matching without fitted "
                "energy alignment"
            ),
            "statistics": ErrorStatistics.from_values(values).to_json(),
            "selected_parent_bands": selected_records,
        }


class EffectiveMassComparator:
    """Apply the frozen direction-matched principal-mass rule."""

    __slots__ = ("_constant",)

    def __init__(self, electron_mass_curvature_ev_angstrom2: float) -> None:
        self._constant = electron_mass_curvature_ev_angstrom2

    def execute(
        self,
        label: str,
        candidate_curvatures: RealArray,
        candidate_axes: RealArray,
        parent_record: JsonObject,
    ) -> MassComparison:
        parent_comparison = parent_record["primary_mass_comparison"]
        if not isinstance(parent_comparison, dict):
            raise TypeError("parent mass comparison must be a mapping")
        parent_curvatures = np.asarray(
            parent_comparison["parent_principal_curvatures_ev_angstrom_squared"],
            dtype=np.float64,
        )
        parent_masses = self._constant / parent_curvatures
        parent_axes = np.asarray(
            parent_comparison["parent_principal_axes_cartesian_columns"],
            dtype=np.float64,
        )
        candidate_masses = self._constant / candidate_curvatures
        axis_index = "xyz".index(label[-1])
        candidate_longitudinal = int(np.argmax(np.abs(candidate_axes[axis_index, :])))
        parent_longitudinal = int(np.argmax(np.abs(parent_axes[axis_index, :])))
        candidate_transverse = [
            value for value in range(3) if value != candidate_longitudinal
        ]
        parent_transverse = [
            value for value in range(3) if value != parent_longitudinal
        ]
        direct = sum(
            abs(candidate_axes[:, c] @ parent_axes[:, p])
            for c, p in zip(candidate_transverse, parent_transverse, strict=True)
        )
        swapped = list(reversed(parent_transverse))
        swapped_score = sum(
            abs(candidate_axes[:, c] @ parent_axes[:, p])
            for c, p in zip(candidate_transverse, swapped, strict=True)
        )
        if swapped_score > direct:
            parent_transverse = swapped
        matches = [("longitudinal", candidate_longitudinal, parent_longitudinal)]
        matches.extend(
            (f"transverse_{index + 1}", candidate_index, parent_index)
            for index, (candidate_index, parent_index) in enumerate(
                zip(candidate_transverse, parent_transverse, strict=True)
            )
        )
        comparisons: list[JsonValue] = []
        passes: list[bool] = []
        for name, candidate_index, parent_index in matches:
            relative = abs(
                candidate_masses[candidate_index] - parent_masses[parent_index]
            ) / abs(parent_masses[parent_index])
            passed = bool(relative <= 0.08)
            passes.append(passed)
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
                    "absolute_relative_error": float(relative),
                    "maximum": 0.08,
                    "passed": passed,
                    "axis_absolute_overlap": float(
                        abs(
                            candidate_axes[:, candidate_index]
                            @ parent_axes[:, parent_index]
                        )
                    ),
                }
            )
        record: JsonObject = {
            "coordinate_basis": "Cartesian reciprocal axes",
            "candidate_principal_curvatures_ev_angstrom_squared": (
                candidate_curvatures.tolist()
            ),
            "candidate_principal_axes_cartesian_columns": candidate_axes.tolist(),
            "parent_principal_axes_cartesian_columns": parent_axes.tolist(),
            "comparisons": comparisons,
            "passed": all(passes),
        }
        return MassComparison(record, all(passes))


class DevelopmentComparator:
    """Apply the frozen S40 targets to the full untruncated operator."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        sources = SourceAuthenticator().execute()
        manifest = load_json(POINT_MANIFEST)
        criteria = load_json(CRITERIA)
        parent_result = load_json(PARENT_RESULT)
        operator, _module, s30 = CandidateLoader().execute()
        fractional, parent_spectrum = ParentLoader().execute(manifest)
        candidate_spectrum = operator.eigenvalues(fractional)
        if candidate_spectrum.shape != (408, 10):
            raise RuntimeError("candidate development spectrum has unexpected shape")
        s30_results = mapping(s30["results"], "S30 results")
        candidate_valleys = list_values(
            mapping(s30_results["valley_family"], "S30 valley family")["valleys"],
            "S30 valleys",
        )
        candidate_masses = list_values(
            mapping(s30_results["effective_mass_diagnostic"], "S30 mass diagnostic")[
                "valleys"
            ],
            "S30 masses",
        )
        parent_valleys = list_values(parent_result["valleys"], "parent valleys")
        candidate_valley_by_label = {
            string_value(item["label"], "candidate valley label"): item
            for item in candidate_valleys
        }
        candidate_mass_by_label = {
            string_value(item["valley_label"], "candidate mass label"): item
            for item in candidate_masses
        }
        parent_by_label = {
            string_value(item["label"], "parent valley label"): item
            for item in parent_valleys
        }
        lattice = mapping(s30["lattice"], "S30 lattice")
        reciprocal = np.asarray(
            lattice["reciprocal_basis_columns_inverse_angstrom"], dtype=np.float64
        )
        labels = ("-x", "+x", "-y", "+y", "-z", "+z")
        valley_records: list[JsonValue] = []
        location_passes: list[bool] = []
        mass_passes: list[bool] = []
        candidate_energies: list[float] = []
        mass_comparator = EffectiveMassComparator(ELECTRON_MASS_CURVATURE_EV_ANGSTROM2)
        location_limit = numeric_value(
            mapping(
                mapping(criteria["gating_comparisons"], "criteria gates")[
                    "valley_position"
                ],
                "valley gate",
            )["maximum_inverse_angstrom"],
            "valley location limit",
        )
        for label in labels:
            candidate_valley = candidate_valley_by_label[label]
            parent_valley = parent_by_label[label]
            candidate_fractional = np.asarray(
                candidate_valley["fractional_reciprocal_coordinates"],
                dtype=np.float64,
            )
            parent_fractional = np.asarray(
                parent_valley["parent_minimum_fractional"], dtype=np.float64
            )
            displacement = minimum_periodic_cartesian_displacement(
                candidate_fractional, parent_fractional, reciprocal
            )
            location_error = float(np.linalg.norm(displacement))
            location_passed = bool(location_error <= location_limit)
            primary = next(
                item
                for item in list_values(
                    candidate_mass_by_label[label]["stencils"], "candidate stencils"
                )
                if numeric_value(item["step_inverse_angstrom"], "stencil step") == 0.002
            )
            curvatures = np.asarray(
                primary["principal_curvatures_ev_angstrom_squared"], dtype=np.float64
            )
            axes = np.asarray(
                primary["principal_axes_cartesian_columns"], dtype=np.float64
            )
            mass = mass_comparator.execute(label, curvatures, axes, parent_valley)
            energy = numeric_value(
                candidate_valley["energy_ev_native_reference"], "candidate energy"
            )
            candidate_energies.append(energy)
            location_passes.append(location_passed)
            mass_passes.append(mass.passed)
            valley_records.append(
                {
                    "label": label,
                    "candidate_minimum_fractional": candidate_fractional.tolist(),
                    "parent_minimum_fractional": parent_fractional.tolist(),
                    "candidate_to_parent_displacement_cartesian_inverse_angstrom": (
                        displacement.tolist()
                    ),
                    "candidate_to_parent_displacement_inverse_angstrom": (
                        location_error
                    ),
                    "location_maximum_inverse_angstrom": location_limit,
                    "location_passed": location_passed,
                    "primary_mass_comparison": mass.record,
                }
            )
        candidate_vbm = float(
            operator.eigenvalues(np.zeros((1, 3), dtype=np.float64))[0, 3]
        )
        candidate_gap = min(candidate_energies) - candidate_vbm
        parent_gap = numeric_value(
            mapping(parent_result["indirect_gap"], "parent gap")[
                "parent_indirect_gap_ev"
            ],
            "parent indirect gap",
        )
        gap_error = abs(candidate_gap - parent_gap) / abs(parent_gap)
        gap_passed = bool(gap_error <= 0.05)
        all_passed = gap_passed and all(location_passes) and all(mass_passes)
        return {
            "schema_version": 1,
            "status": "S40-revealed-408-development-complete",
            "calculator_invocations": 0,
            "sources": sources,
            "candidate": {
                "route": "C6-B20-W21-aiida-precise",
                "operator_kind": "full-untruncated",
                "S30_result": identity(S30_RESULT),
            },
            "criteria": {
                "role": (
                    "revealed-parent oracle-evaluation criteria, not operational "
                    "reduction gates"
                ),
                "indirect_gap_relative_maximum": 0.05,
                "valley_position_fraction_of_gamma_x_maximum": 0.03,
                "valley_position_maximum_inverse_angstrom": location_limit,
                "each_effective_mass_relative_maximum": 0.08,
            },
            "indirect_gap": {
                "parent_indirect_gap_ev": parent_gap,
                "candidate_indirect_gap_ev": candidate_gap,
                "candidate_vbm_ev_native_reference": candidate_vbm,
                "absolute_relative_error": gap_error,
                "maximum": 0.05,
                "passed": gap_passed,
            },
            "valleys": valley_records,
            "spectral_residuals": InjectiveSpectralMatcher().execute(
                candidate_spectrum, parent_spectrum
            ),
            "gate_summary": {
                "indirect_gap_passed": gap_passed,
                "all_valley_locations_passed": all(location_passes),
                "all_effective_masses_passed": all(mass_passes),
                "all_development_targets_passed": all_passed,
                "development_disposition": (
                    "passes-parent-fidelity-development-criteria"
                    if all_passed
                    else "fails-parent-fidelity-development-criteria"
                ),
                "operational_reduction_gate": False,
                "controlled_reduction_source_eligibility_changed": False,
            },
            "confirmation_boundary": {
                "confirmation_point_count": 402,
                "parent_values_observed": False,
                "prediction_freeze_performed": False,
            },
            "scientific_disposition": (
                "revealed development-oracle comparison only; failure limits physical-"
                "fidelity claims but does not invalidate provider eligibility, "
                "structural reconstruction, or use of the full operator as the fixed "
                "source for a "
                "separately gated controlled reduction"
            ),
        }


def minimum_periodic_cartesian_displacement(
    candidate: RealArray, parent: RealArray, reciprocal: RealArray
) -> RealArray:
    shifts = np.asarray(
        tuple(itertools.product((-1, 0, 1), repeat=3)), dtype=np.float64
    )
    values = (candidate[np.newaxis, :] - parent[np.newaxis, :] + shifts) @ reciprocal.T
    return values[int(np.argmin(np.linalg.norm(values, axis=1)))]


def load_json(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON root must be a mapping: {path}")
    return cast(JsonObject, value)


def mapping(value: JsonValue, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a mapping")
    return value


def list_values(value: JsonValue, label: str) -> list[JsonObject]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise TypeError(f"{label} must be a list of mappings")
    return cast(list[JsonObject], value)


def vector3(value: JsonValue, label: str) -> tuple[float, float, float]:
    if not isinstance(value, list) or len(value) != 3:
        raise TypeError(f"{label} must contain three numbers")
    return (
        numeric_value(value[0], label),
        numeric_value(value[1], label),
        numeric_value(value[2], label),
    )


def numeric_value(value: JsonValue, label: str) -> float:
    if type(value) not in {int, float}:
        raise TypeError(f"{label} must be numeric")
    return float(cast(int | float, value))


def string_value(value: JsonValue, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    return value


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


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("S40 development result already exists")
    result = DevelopmentComparator().execute()
    OUTPUT.write_bytes(TypedJsonMappingSerializer().serialize(result))


if __name__ == "__main__":
    main()
