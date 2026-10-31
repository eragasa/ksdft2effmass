from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from projectkoios.physkit import units as _physkit_units
from projectkoios.physkit.periodic.lattice import (
    DirectLattice3D,
    ReciprocalLattice3D,
)

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (  # type: ignore[attr-defined]
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER
    )

from ksdft2effmass.serialization import (  # noqa: E402
    TypedJsonMappingSerializer,
)

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
STRUCTURE = (
    BULK / "simulations/structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
VALIDATION = (
    BULK / "simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-"
    "withheld-parent-nscf-408-david/result/validation-result.json"
)
FIRST_HOLDOUT = (
    BULK / "analysis/withheld-parent-validation-preflight/withheld-kpoint-manifest.json"
)
ELIGIBLE_WIN = (
    BULK / "simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-"
    "wannier90-localization-lower-energy-frozen-dis2000-eligible/input/silicon.win"
)
PROTOCOL = BULK / "research-protocol/research-protocol.tex"
OUTPUT_MESHES = ROOT / "construction-mesh-candidates.json"
OUTPUT_HOLDOUT = ROOT / "successor-confirmation-holdout.json"
OUTPUT_RECOMMENDATION = ROOT / "recommendation.json"
OUTPUT_AUTHORIZATION = ROOT / "authorization-boundary.json"


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Bind one exact recommendation source."""

    label: str
    path: Path
    byte_size: int
    sha256: str


class ArtifactAuthenticator:
    """Authenticate every recommendation source before deriving coordinates."""

    __slots__ = ()

    def execute(self, identity: ArtifactIdentity) -> JsonObject:
        payload = identity.path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if len(payload) != identity.byte_size or digest != identity.sha256:
            raise RuntimeError(f"{identity.label} identity mismatch")
        return {
            "path": str(identity.path.relative_to(BULK)),
            "byte_size": len(payload),
            "sha256": digest,
        }


@dataclass(frozen=True, slots=True)
class SiliconLattice:
    """Bind accepted S1 direct and reciprocal bases."""

    direct: DirectLattice3D
    reciprocal: ReciprocalLattice3D
    lattice_parameter_angstrom: float

    @classmethod
    def from_structure(cls, path: Path) -> SiliconLattice:
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
        return cls(
            direct=direct,
            reciprocal=ReciprocalLattice3D.from_direct_lattice(direct),
            lattice_parameter_angstrom=lattice_parameter,
        )


class ConstructionMeshDesigner:
    """Generate exact ordered Gamma-origin candidate meshes."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        return {
            "schema_version": 1,
            "status": "recommended-not-preflighted",
            "ordering": "lexicographic i,j,k with k fastest",
            "coordinate_convention": "fractional primitive reciprocal coordinates",
            "candidates": [
                self._candidate("C6", 6, "first-successor"),
                self._candidate("C8", 8, "conditional-not-automatic"),
                self._candidate("C12", 12, "bounded-upper-diagnostic"),
            ],
        }

    @staticmethod
    def _candidate(label: str, size: int, disposition: str) -> JsonObject:
        count = size**3
        points = [
            {
                "fractional_reciprocal_coordinates": [
                    i / size,
                    j / size,
                    k / size,
                ],
                "qe_crystal_weight": 1.0 / count,
            }
            for i in range(size)
            for j in range(size)
            for k in range(size)
        ]
        return {
            "label": label,
            "grid": [size, size, size],
            "offset": [0, 0, 0],
            "point_count": count,
            "disposition": disposition,
            "points": points,
        }


@dataclass(frozen=True, slots=True)
class HoldoutRole:
    """Describe one parent-informed successor-confirmation coordinate."""

    valley_label: str
    kind: str
    step_inverse_angstrom: float | None
    rotated_axes_zero_based: tuple[int, ...]
    signs: tuple[int, ...]

    def to_json(self) -> JsonObject:
        return {
            "valley_label": self.valley_label,
            "kind": self.kind,
            "step_inverse_angstrom": self.step_inverse_angstrom,
            "rotated_axes_zero_based": list(self.rotated_axes_zero_based),
            "signs": list(self.signs),
        }


@dataclass(frozen=True, slots=True)
class HoldoutPoint:
    """Retain one unique successor-confirmation point and its role."""

    point_id: str
    fractional: tuple[float, float, float]
    roles: tuple[HoldoutRole, ...]

    def to_json(self, weight: float) -> JsonObject:
        return {
            "point_id": self.point_id,
            "fractional_reciprocal_coordinates": list(self.fractional),
            "qe_crystal_weight": weight,
            "roles": [role.to_json() for role in self.roles],
        }


class SuccessorHoldoutDesigner:
    """Generate the protocol's rotated, parent-value-unobserved 402-point set."""

    __slots__ = ("_lattice", "_revealed_points")

    HESSIAN_STEPS = (0.002, 0.006, 0.012)
    CAPTURE_STEPS = (0.024, 0.048)
    EXPECTED_MEAN_RADIUS = 0.9629174643168844
    ROTATION = np.asarray(
        [
            [1.0 / np.sqrt(3.0), 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(6.0)],
            [1.0 / np.sqrt(3.0), -1.0 / np.sqrt(2.0), 1.0 / np.sqrt(6.0)],
            [1.0 / np.sqrt(3.0), 0.0, -2.0 / np.sqrt(6.0)],
        ],
        dtype=np.float64,
    )

    def __init__(self, lattice: SiliconLattice, revealed_points: RealArray) -> None:
        self._lattice = lattice
        self._revealed_points = revealed_points

    def execute(self, validation: JsonObject) -> JsonObject:
        mean_radius = self._mean_parent_radius(validation)
        if not np.isclose(
            mean_radius,
            self.EXPECTED_MEAN_RADIUS,
            atol=1.0e-14,
            rtol=0.0,
        ):
            raise RuntimeError("revealed parent-valley mean radius changed")
        if (
            not np.allclose(
                self.ROTATION.T @ self.ROTATION,
                np.eye(3),
                atol=1.0e-15,
                rtol=0.0,
            )
            or np.linalg.det(self.ROTATION) <= 0.0
        ):
            raise RuntimeError("rotated holdout basis must be right-handed orthonormal")
        selected: dict[tuple[float, float, float], list[HoldoutRole]] = {}
        inverse_reciprocal = np.linalg.inv(
            self._lattice.reciprocal.primitive_basis_matrix
        )
        labels = ("-x", "+x", "-y", "+y", "-z", "+z")
        for label in labels:
            axis = "xyz".index(label[-1])
            sign = -1 if label[0] == "-" else 1
            center_cartesian = np.zeros(3, dtype=np.float64)
            center_cartesian[axis] = sign * mean_radius
            center = (inverse_reciprocal @ center_cartesian) % 1.0
            self._add(
                selected,
                center,
                HoldoutRole(label, "parent-informed-center", None, (), ()),
            )
            for step in self.HESSIAN_STEPS:
                for rotated_axis in range(3):
                    for offset_sign in (-1, 1):
                        delta = offset_sign * step * self.ROTATION[:, rotated_axis]
                        self._add(
                            selected,
                            self._shift(center, delta),
                            HoldoutRole(
                                label,
                                "rotated-hessian-axial",
                                step,
                                (rotated_axis,),
                                (offset_sign,),
                            ),
                        )
                for first_axis in range(3):
                    for second_axis in range(first_axis + 1, 3):
                        for first_sign in (-1, 1):
                            for second_sign in (-1, 1):
                                delta = step * (
                                    first_sign * self.ROTATION[:, first_axis]
                                    + second_sign * self.ROTATION[:, second_axis]
                                )
                                self._add(
                                    selected,
                                    self._shift(center, delta),
                                    HoldoutRole(
                                        label,
                                        "rotated-hessian-mixed",
                                        step,
                                        (first_axis, second_axis),
                                        (first_sign, second_sign),
                                    ),
                                )
            for step in self.CAPTURE_STEPS:
                for rotated_axis in range(3):
                    for offset_sign in (-1, 1):
                        delta = offset_sign * step * self.ROTATION[:, rotated_axis]
                        self._add(
                            selected,
                            self._shift(center, delta),
                            HoldoutRole(
                                label,
                                "rotated-capture-axial",
                                step,
                                (rotated_axis,),
                                (offset_sign,),
                            ),
                        )
        points = tuple(
            HoldoutPoint(
                point_id=f"S{index:04d}",
                fractional=key,
                roles=tuple(selected[key]),
            )
            for index, key in enumerate(sorted(selected), start=1)
        )
        if len(points) != 402:
            raise RuntimeError(f"expected 402 unique holdout points, got {len(points)}")
        separation = self._separation_checks(points)
        weight = 1.0 / len(points)
        gamma_x = 2.0 * np.pi / self._lattice.lattice_parameter_angstrom
        return {
            "schema_version": 1,
            "status": "coordinates-frozen-parent-values-unobserved",
            "selection_role": (
                "parent-informed confirmation geometry; direct parent values at these "
                "coordinates have not been observed"
            ),
            "center_rule": {
                "mean_revealed_parent_valley_radius_inverse_angstrom": mean_radius,
                "fraction_of_gamma_x": mean_radius / gamma_x,
                "signed_cartesian_axes": list(labels),
            },
            "rotated_basis_cartesian_columns": self.ROTATION.tolist(),
            "hessian_steps_inverse_angstrom": list(self.HESSIAN_STEPS),
            "capture_steps_inverse_angstrom": list(self.CAPTURE_STEPS),
            "unique_point_count": len(points),
            "qe_crystal_weight_sum": sum(weight for _ in points),
            "separation": separation,
            "points": [point.to_json(weight) for point in points],
            "use_boundary": (
                "freeze one successor candidate's predictions and fitting conventions "
                "before any direct-parent calculation at these points"
            ),
        }

    def _mean_parent_radius(self, validation: JsonObject) -> float:
        valleys = validation["valleys"]
        if not isinstance(valleys, list) or len(valleys) != 6:
            raise ValueError("validation result must contain six valleys")
        shifts = np.asarray(
            [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)],
            dtype=np.float64,
        )
        radii: list[float] = []
        reciprocal = self._lattice.reciprocal.primitive_basis_matrix
        for valley in valleys:
            if not isinstance(valley, dict):
                raise TypeError("valley result must be a mapping")
            fractional = np.asarray(
                valley["parent_minimum_fractional"], dtype=np.float64
            )
            candidates = (fractional[np.newaxis, :] + shifts) @ reciprocal.T
            cartesian = candidates[int(np.argmin(np.linalg.norm(candidates, axis=1)))]
            radii.append(float(np.linalg.norm(cartesian)))
        return float(np.mean(radii))

    def _shift(self, center: RealArray, cartesian_delta: RealArray) -> RealArray:
        inverse_reciprocal = np.linalg.inv(
            self._lattice.reciprocal.primitive_basis_matrix
        )
        return (center + inverse_reciprocal @ cartesian_delta) % 1.0

    @staticmethod
    def _key(fractional: RealArray) -> tuple[float, float, float]:
        wrapped = np.mod(fractional, 1.0)
        wrapped[np.isclose(wrapped, 1.0, atol=1.0e-14, rtol=0.0)] = 0.0
        return tuple(float(value) for value in np.round(wrapped, decimals=14))

    def _add(
        self,
        selected: dict[tuple[float, float, float], list[HoldoutRole]],
        fractional: RealArray,
        role: HoldoutRole,
    ) -> None:
        selected.setdefault(self._key(fractional), []).append(role)

    def _separation_checks(self, points: tuple[HoldoutPoint, ...]) -> JsonObject:
        fractional = np.asarray([point.fractional for point in points])
        grids = {
            f"Gamma-origin-{size}x{size}x{size}": np.asarray(
                [
                    (i / size, j / size, k / size)
                    for i in range(size)
                    for j in range(size)
                    for k in range(size)
                ],
                dtype=np.float64,
            )
            for size in (4, 6, 8, 10, 12)
        }
        results: JsonObject = {}
        for label, other in (
            *grids.items(),
            ("revealed-408-point-set", self._revealed_points),
        ):
            overlap, minimum = self._torus_separation(fractional, other)
            results[label] = {
                "overlap_count": overlap,
                "minimum_fractional_torus_infinity_distance": minimum,
            }
            if overlap != 0:
                raise RuntimeError(f"successor holdout overlaps {label}")
        return results

    @staticmethod
    def _torus_separation(first: RealArray, second: RealArray) -> tuple[int, float]:
        minimum = np.inf
        overlaps = 0
        for point in first:
            difference = np.abs(second - point[np.newaxis, :])
            torus = np.minimum(difference, 1.0 - difference)
            distances = np.max(torus, axis=1)
            point_minimum = float(np.min(distances))
            minimum = min(minimum, point_minimum)
            if point_minimum <= 1.0e-12:
                overlaps += 1
        return overlaps, float(minimum)


class RecommendationBuilder:
    """Bind the staged C6-first decision without granting execution."""

    __slots__ = ()

    def execute(
        self,
        sources: JsonObject,
        meshes_identity: JsonObject,
        holdout_identity: JsonObject,
    ) -> tuple[JsonObject, JsonObject]:
        recommendation: JsonObject = {
            "schema_version": 1,
            "status": "recommendation-prepared-no-calculator-authorized",
            "sources": sources,
            "first_successor": {
                "label": "C6",
                "changed_scientific_coordinate": (
                    "Gamma-origin construction mesh from 4x4x4 to 6x6x6"
                ),
                "held_fixed": {
                    "accepted_structure": "Si.PrimitiveUnitCell.RightHanded.RelaxedS1",
                    "parent": "accepted S1 Gamma-K10 42/336 Ry SCF",
                    "occupations": "fixed",
                    "nosym": True,
                    "noinv": True,
                    "conv_thr_rydberg": 1.0e-12,
                    "diagonalization": "david",
                    "diago_full_acc": True,
                    "nscf_band_count": 12,
                    "wannier_rank": 10,
                    "spinors": False,
                    "outer_window_ev": [-5.85, 19.02],
                    "frozen_window_ev": [-5.85, 8.0],
                    "projections": ["Si:sp3", "Si:l=0:r=2"],
                    "dis_num_iter": 2000,
                    "dis_conv_tol": 1.0e-10,
                    "dis_conv_window": 3,
                    "dis_mix_ratio": 0.2,
                    "num_iter": 4000,
                    "conv_tol_angstrom_squared": 2.0e-9,
                    "conv_window": 6,
                    "precond": True,
                    "num_cg_steps": 200,
                    "trial_step": 2.0,
                    "trial_step_source": "native-default",
                    "fixed_step": None,
                    "guiding_centres": False,
                },
                "required_distinct_occurrences": [
                    "QE NSCF",
                    "Wannier90 preprocessing",
                    "pw2wannier90 conversion",
                    "Wannier90 localization",
                ],
            },
            "development_evaluation": {
                "revealed_parent_set": "prior 408-point validation set",
                "criteria": {
                    "indirect_gap_relative_maximum": 0.05,
                    "valley_position_fraction_gamma_x_maximum": 0.03,
                    "each_effective_mass_relative_maximum": 0.08,
                },
                "interpretation": (
                    "development/model-selection evidence for successors, not a new "
                    "withheld confirmation"
                ),
            },
            "conditional_C8": {
                "automatic": False,
                "grid": [8, 8, 8],
                "decision": (
                    "requires separate operator review after channel-resolved C4-to-C6 "
                    "changes; stop mesh escalation if they do not support the mesh "
                    "density hypothesis"
                ),
            },
            "conditional_C12": {
                "automatic": False,
                "grid": [12, 12, 12],
                "point_count": 1728,
                "relative_to_C4_point_count": 27.0,
                "decision": (
                    "bounded upper mesh diagnostic eligible for separate review only "
                    "after C8 still supports the mesh-density hypothesis"
                ),
                "finite_model_nonclaim": (
                    "passing at C12 establishes intended-use adequacy of the finite "
                    "operator, not an infinite-mesh convergence result"
                ),
            },
            "successor_confirmation": {
                "manifest": holdout_identity,
                "criteria_unchanged": True,
                "candidate_predictions_must_be_frozen_first": True,
                "direct_parent_values_observed": False,
                "geometry_blind": False,
                "geometry_description": (
                    "parent-informed symmetry-projected centers with rotated stencils"
                ),
            },
            "construction_mesh_manifest": meshes_identity,
            "scientific_stop": (
                "component-operator and Slater-Koster work remain blocked until a "
                "successor full Wannier operator passes development and confirmation"
            ),
        }
        authorization: JsonObject = {
            "schema_version": 1,
            "status": "no-calculator-authorized",
            "recommendation_authorized": True,
            "calculator_execution_authorized": False,
            "artifact_acquisition_authorized": False,
            "C6": {
                "qe_nscf_authorized": False,
                "wannier90_preprocessing_authorized": False,
                "pw2wannier90_authorized": False,
                "wannier90_localization_authorized": False,
                "automatic_retries": 0,
            },
            "C8": {
                "scientifically_selected": False,
                "calculator_execution_authorized": False,
            },
            "C12": {
                "scientifically_selected": False,
                "calculator_execution_authorized": False,
            },
            "successor_confirmation_parent": {
                "calculator_execution_authorized": False,
            },
            "boundary": (
                "the operator authorized writing and preparing this recommendation, "
                "not any QE or Wannier90 invocation"
            ),
        }
        return recommendation, authorization


class ConstructionAdequacyPreparation:
    """Orchestrate a deterministic no-calculator recommendation preparation."""

    __slots__ = ()

    def execute(self) -> None:
        authenticator = ArtifactAuthenticator()
        sources: JsonObject = {
            key: authenticator.execute(identity) for key, identity in ARTIFACTS.items()
        }
        lattice = SiliconLattice.from_structure(STRUCTURE)
        validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
        first_holdout = json.loads(FIRST_HOLDOUT.read_text(encoding="utf-8"))
        revealed_points = np.asarray(
            [
                item["fractional_reciprocal_coordinates"]
                for item in first_holdout["points"]
            ],
            dtype=np.float64,
        )
        serializer = TypedJsonMappingSerializer()
        meshes = ConstructionMeshDesigner().execute()
        OUTPUT_MESHES.write_bytes(serializer.serialize(meshes))
        holdout = SuccessorHoldoutDesigner(lattice, revealed_points).execute(validation)
        OUTPUT_HOLDOUT.write_bytes(serializer.serialize(holdout))
        meshes_identity = self._identity(OUTPUT_MESHES)
        holdout_identity = self._identity(OUTPUT_HOLDOUT)
        recommendation, authorization = RecommendationBuilder().execute(
            sources, meshes_identity, holdout_identity
        )
        OUTPUT_RECOMMENDATION.write_bytes(serializer.serialize(recommendation))
        OUTPUT_AUTHORIZATION.write_bytes(serializer.serialize(authorization))

    @staticmethod
    def _identity(path: Path) -> JsonObject:
        payload = path.read_bytes()
        return {
            "path": path.name,
            "byte_size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }


ARTIFACTS = {
    "accepted_structure": ArtifactIdentity(
        "accepted structure",
        STRUCTURE,
        758,
        "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
    ),
    "failed_candidate_validation": ArtifactIdentity(
        "failed candidate validation",
        VALIDATION,
        227_328,
        "46f3716e20037187989863fccad9181402a7dc4f4b89e3c143527b10353c7aa6",
    ),
    "revealed_point_manifest": ArtifactIdentity(
        "revealed point manifest",
        FIRST_HOLDOUT,
        208_847,
        "754bce5030ef0e34eb092406b27d9094287b4f749e358ef36404040f44b8d2b4",
    ),
    "eligible_localization_input": ArtifactIdentity(
        "eligible localization input",
        ELIGIBLE_WIN,
        3_638,
        "33a73bc040883929657e20e6cb4ce2b3fd60ede9e185e276e595143bb9809d4d",
    ),
    "research_protocol": ArtifactIdentity(
        "research protocol",
        PROTOCOL,
        14_928,
        "7822d6365e05e5bb479f318d5235717d60b29368f049078defe9d991cd6fac04",
    ),
}


def main() -> None:
    ConstructionAdequacyPreparation().execute()


if __name__ == "__main__":
    main()
