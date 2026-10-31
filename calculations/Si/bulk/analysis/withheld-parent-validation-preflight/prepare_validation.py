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
    TypedJsonMappingDeserializer,
    TypedJsonMappingSerializer,
)

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
STRUCTURE = (
    BULK
    / "simulations"
    / "structures"
    / "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
QUALIFICATION_RESULT = (
    BULK
    / "analysis"
    / "provider-eligible-operator-qualification"
    / "qualification-result.json"
)
OUTPUT_MANIFEST = ROOT / "withheld-kpoint-manifest.json"
OUTPUT_CRITERIA = ROOT / "validation-criteria.json"
OUTPUT_INPUT = ROOT / "pw.in"
OUTPUT_REQUEST = ROOT / "authorization-request.json"


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Declare exact bytes consumed by this preparation."""

    label: str
    path: Path
    byte_size: int
    sha256: str


class ArtifactAuthenticator:
    """Verify exact local bytes before deriving a validation inventory."""

    __slots__ = ()

    def execute(self, identity: ArtifactIdentity) -> JsonObject:
        payload = identity.path.read_bytes()
        observed_size = len(payload)
        observed_sha256 = hashlib.sha256(payload).hexdigest()
        if observed_size != identity.byte_size:
            raise RuntimeError(f"{identity.label} byte-size mismatch")
        if observed_sha256 != identity.sha256:
            raise RuntimeError(f"{identity.label} SHA-256 mismatch")
        return {
            "path": str(identity.path.relative_to(BULK)),
            "byte_size": observed_size,
            "sha256": observed_sha256,
        }


@dataclass(frozen=True, slots=True)
class SiliconLattice:
    """Bind accepted physical scales to PhysKit lattice primitives."""

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


@dataclass(frozen=True, slots=True)
class PointRole:
    """Describe why one candidate-conditioned point is withheld."""

    valley_label: str
    kind: str
    step_inverse_angstrom: float | None
    cartesian_axes: tuple[int, ...]
    signs: tuple[int, ...]

    def to_json(self) -> JsonObject:
        return {
            "valley_label": self.valley_label,
            "kind": self.kind,
            "step_inverse_angstrom": self.step_inverse_angstrom,
            "cartesian_axes_zero_based": list(self.cartesian_axes),
            "signs": list(self.signs),
        }


@dataclass(frozen=True, slots=True)
class WithheldPoint:
    """Retain one unique fractional point and all roles selecting it."""

    point_id: str
    fractional: tuple[float, float, float]
    roles: tuple[PointRole, ...]

    def to_json(self, weight: float) -> JsonObject:
        return {
            "point_id": self.point_id,
            "fractional_reciprocal_coordinates": list(self.fractional),
            "qe_crystal_weight": weight,
            "roles": [role.to_json() for role in self.roles],
        }


class CandidateValleyReader:
    """Read the frozen candidate valley predictions through generic serialization."""

    __slots__ = ()

    def execute(self, path: Path) -> tuple[tuple[str, RealArray, RealArray], ...]:
        record = TypedJsonMappingDeserializer().deserialize(path.read_bytes())
        results = record["results"]
        if not isinstance(results, dict):
            raise TypeError("qualification results must be a mapping")
        valley_family = results["valley_family"]
        if not isinstance(valley_family, dict):
            raise TypeError("valley-family result must be a mapping")
        raw_valleys = valley_family["valleys"]
        if not isinstance(raw_valleys, list) or len(raw_valleys) != 6:
            raise ValueError("exactly six candidate valleys are required")
        valleys: list[tuple[str, RealArray, RealArray]] = []
        for raw in raw_valleys:
            if not isinstance(raw, dict):
                raise TypeError("valley records must be mappings")
            label = raw["label"]
            fractional = raw["fractional_reciprocal_coordinates"]
            cartesian = raw["cartesian_inverse_angstrom"]
            if type(label) is not str:
                raise TypeError("valley label must be a string")
            fractional_array = np.asarray(fractional, dtype=np.float64)
            cartesian_array = np.asarray(cartesian, dtype=np.float64)
            if fractional_array.shape != (3,) or cartesian_array.shape != (3,):
                raise ValueError("valley coordinates must have three components")
            valleys.append((label, fractional_array, cartesian_array))
        labels = tuple(item[0] for item in valleys)
        if labels != ("-x", "+x", "-y", "+y", "-z", "+z"):
            raise ValueError("candidate valley labels have unexpected ordering")
        return tuple(valleys)


class WithheldKPointDesigner:
    """Construct a candidate-conditioned local validation inventory."""

    __slots__ = ("_lattice",)

    HESSIAN_STEPS = (0.002, 0.005, 0.010)
    CAPTURE_STEPS = (0.020, 0.040)

    def __init__(self, lattice: SiliconLattice) -> None:
        self._lattice = lattice

    def execute(
        self, valleys: tuple[tuple[str, RealArray, RealArray], ...]
    ) -> tuple[WithheldPoint, ...]:
        selected: dict[tuple[float, float, float], list[PointRole]] = {}
        for label, center, _ in valleys:
            self._add(
                selected,
                center,
                PointRole(label, "candidate-center", None, (), ()),
            )
            for step in self.HESSIAN_STEPS:
                for axis in range(3):
                    for sign in (-1, 1):
                        delta = np.zeros(3, dtype=np.float64)
                        delta[axis] = sign * step
                        self._add(
                            selected,
                            self._shift(center, delta),
                            PointRole(
                                label,
                                "hessian-axial",
                                step,
                                (axis,),
                                (sign,),
                            ),
                        )
                for first_axis in range(3):
                    for second_axis in range(first_axis + 1, 3):
                        for first_sign in (-1, 1):
                            for second_sign in (-1, 1):
                                delta = np.zeros(3, dtype=np.float64)
                                delta[first_axis] = first_sign * step
                                delta[second_axis] = second_sign * step
                                self._add(
                                    selected,
                                    self._shift(center, delta),
                                    PointRole(
                                        label,
                                        "hessian-mixed",
                                        step,
                                        (first_axis, second_axis),
                                        (first_sign, second_sign),
                                    ),
                                )
            for step in self.CAPTURE_STEPS:
                for axis in range(3):
                    for sign in (-1, 1):
                        delta = np.zeros(3, dtype=np.float64)
                        delta[axis] = sign * step
                        self._add(
                            selected,
                            self._shift(center, delta),
                            PointRole(
                                label,
                                "capture-axial",
                                step,
                                (axis,),
                                (sign,),
                            ),
                        )
        mean_radius = float(
            np.mean(tuple(np.linalg.norm(cartesian) for _, _, cartesian in valleys))
        )
        inverse_reciprocal = np.linalg.inv(
            self._lattice.reciprocal.primitive_basis_matrix
        )
        for axis in range(3):
            for sign in (-1, 1):
                cartesian = np.zeros(3, dtype=np.float64)
                cartesian[axis] = sign * mean_radius
                fractional = (inverse_reciprocal @ cartesian) % 1.0
                label = f"{('-' if sign < 0 else '+')}{'xyz'[axis]}"
                self._add(
                    selected,
                    fractional,
                    PointRole(label, "symmetry-anchor", None, (axis,), (sign,)),
                )
        points: list[WithheldPoint] = []
        for index, key in enumerate(sorted(selected), start=1):
            points.append(
                WithheldPoint(
                    point_id=f"W{index:04d}",
                    fractional=key,
                    roles=tuple(selected[key]),
                )
            )
        self._verify_disjoint_from_construction(tuple(points))
        if len(points) != 408:
            raise RuntimeError(
                f"expected 408 unique withheld points, got {len(points)}"
            )
        return tuple(points)

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
        selected: dict[tuple[float, float, float], list[PointRole]],
        fractional: RealArray,
        role: PointRole,
    ) -> None:
        key = self._key(np.asarray(fractional, dtype=np.float64))
        selected.setdefault(key, []).append(role)

    @staticmethod
    def _verify_disjoint_from_construction(points: tuple[WithheldPoint, ...]) -> None:
        values = np.arange(4, dtype=np.float64) / 4.0
        construction = np.asarray(
            [(i, j, k) for i in values for j in values for k in values],
            dtype=np.float64,
        )
        for point in points:
            fractional = np.asarray(point.fractional, dtype=np.float64)
            difference = np.abs(construction - fractional[np.newaxis, :])
            torus_difference = np.minimum(difference, 1.0 - difference)
            if np.any(np.max(torus_difference, axis=1) <= 1.0e-12):
                raise RuntimeError(
                    f"withheld point {point.point_id} overlaps construction mesh"
                )


class WithheldManifestBuilder:
    """Build the compact point inventory and role-separation declaration."""

    __slots__ = ("_lattice",)

    def __init__(self, lattice: SiliconLattice) -> None:
        self._lattice = lattice

    def execute(
        self,
        points: tuple[WithheldPoint, ...],
        sources: JsonObject,
    ) -> JsonObject:
        weight = 1.0 / len(points)
        role_counts: dict[str, int] = {}
        for point in points:
            for role in point.roles:
                role_counts[role.kind] = role_counts.get(role.kind, 0) + 1
        return {
            "schema_version": 1,
            "status": "prepared-not-executed",
            "calculator_invocations": 0,
            "selection_role": (
                "candidate-conditioned and construction-disjoint parent-evaluation "
                "coordinates; no parent eigenvalues were observed during selection"
            ),
            "sources": sources,
            "coordinate_convention": {
                "fractional_basis": "accepted relaxed primitive reciprocal basis",
                "reciprocal_convention": "two-pi dual",
                "qe_card": "K_POINTS crystal",
                "wrapping_interval": "[0, 1)",
                "direct_basis_columns_angstrom": (
                    self._lattice.direct.primitive_basis_matrix.tolist()
                ),
                "reciprocal_basis_columns_inverse_angstrom": (
                    self._lattice.reciprocal.primitive_basis_matrix.tolist()
                ),
                "qe_parent_execution_basis_columns_angstrom": (
                    np.round(
                        self._lattice.direct.primitive_basis_matrix, decimals=8
                    ).tolist()
                ),
                "maximum_selection_to_execution_basis_difference_angstrom": float(
                    np.max(
                        np.abs(
                            self._lattice.direct.primitive_basis_matrix
                            - np.round(
                                self._lattice.direct.primitive_basis_matrix, decimals=8
                            )
                        )
                    )
                ),
                "execution_basis_reason": (
                    "reuse the exact eight-decimal cell text that produced the "
                    "accepted parent saved state"
                ),
            },
            "design": {
                "candidate_valley_count": 6,
                "hessian_steps_inverse_angstrom": list(
                    WithheldKPointDesigner.HESSIAN_STEPS
                ),
                "capture_axial_steps_inverse_angstrom": list(
                    WithheldKPointDesigner.CAPTURE_STEPS
                ),
                "symmetry_anchor_rule": (
                    "six Cartesian axis points at the mean candidate-valley radius"
                ),
                "unique_point_count": len(points),
                "role_record_counts": role_counts,
                "construction_mesh": "Gamma-origin 4 x 4 x 4",
                "construction_overlap_count": 0,
            },
            "points": [point.to_json(weight) for point in points],
            "scientific_disposition": (
                "coordinates frozen for a separately authorized direct-parent NSCF; "
                "no acceptance threshold or calculator authorization is implied"
            ),
        }


class ValidationCriteriaBuilder:
    """Bind intended-use criteria already declared by the publication program."""

    __slots__ = ("_lattice",)

    def __init__(self, lattice: SiliconLattice) -> None:
        self._lattice = lattice

    def execute(self) -> JsonObject:
        gamma_x_distance = 2.0 * np.pi / self._lattice.lattice_parameter_angstrom
        return {
            "schema_version": 1,
            "status": "prospective-before-parent-observation",
            "intended_use": (
                "non-SOC bulk-silicon pilot and subsequent sp3s-star reduction"
            ),
            "frozen_candidate_prediction_source": {
                "path": (
                    "analysis/provider-eligible-operator-qualification/"
                    "qualification-result.json"
                ),
                "sha256": (
                    "e82995489fd5e5084008c0a7d8bf6bc42c6c219838b073f0b0d9a56d24e04c53"
                ),
                "contains": (
                    "six candidate locations and energies plus curvature and "
                    "effective-mass diagnostics at the declared scales"
                ),
            },
            "authority": {
                "required_observables": (
                    "specification/ksdft2Effmass.physical-specification.v1.md"
                ),
                "adopted_target_source": (
                    "docs/publications/conferences/ICMSEP2026/"
                    "ksdft2effmass.ICMEP2026.abstract.md"
                ),
                "source_targets": {
                    "indirect_gap_relative": 0.05,
                    "valley_position_fraction_of_gamma_x": 0.03,
                    "each_electron_effective_mass_relative": 0.08,
                },
                "transfer_to_this_pilot": (
                    "necessary intended-use screen, not an additive error-budget "
                    "allocation; any later reduction is compared directly with its "
                    "parent under separately bound criteria"
                ),
                "method_scope_warning": (
                    "the target source anticipates the final PseudoDojo branch; this "
                    "occurrence is the separately identified SSSP pilot and cannot "
                    "satisfy that pseudopotential or independent-toolchain gate"
                ),
            },
            "gating_comparisons": {
                "indirect_gap": {
                    "metric": "abs(candidate - parent) / abs(parent)",
                    "maximum": 0.05,
                    "zero_denominator_disposition": "inconclusive",
                },
                "valley_position": {
                    "metric": (
                        "Euclidean Cartesian reciprocal displacement between matched "
                        "candidate and direct-parent minima"
                    ),
                    "gamma_x_distance_inverse_angstrom": gamma_x_distance,
                    "maximum_fraction_of_gamma_x": 0.03,
                    "maximum_inverse_angstrom": 0.03 * gamma_x_distance,
                },
                "longitudinal_effective_mass": {
                    "metric": (
                        "abs(candidate - parent) / abs(parent) for every matched valley"
                    ),
                    "maximum": 0.08,
                },
                "transverse_effective_masses": {
                    "metric": (
                        "abs(candidate - parent) / abs(parent) for both transverse "
                        "principal masses at every matched valley"
                    ),
                    "maximum": 0.08,
                },
            },
            "observable_conventions": {
                "tracked_band": (
                    "lowest conduction state, tracked continuously within each "
                    "candidate-conditioned valley neighborhood"
                ),
                "local_coordinates": (
                    "Cartesian reciprocal displacement in inverse angstrom"
                ),
                "valley_fit": (
                    "direct-parent minimum from the joint three-dimensional quadratic "
                    "fit over points no farther than 0.010 inverse angstrom from the "
                    "frozen candidate center"
                ),
                "gating_hessian": (
                    "parent and candidate three-dimensional quadratic fits on the "
                    "identical 0.002 inverse-angstrom stencil, matching the frozen "
                    "candidate characterization's declared primary scale"
                ),
                "sensitivity_hessians": (
                    "separate fits at 0.005 and 0.010 inverse angstrom are reported "
                    "but do not replace the prospective primary-scale comparison"
                ),
                "mass_tensor": (
                    "full Cartesian inverse-mass tensor from the fitted energy "
                    "Hessian, reported in free-electron-mass units"
                ),
                "principal_mass_labels": (
                    "longitudinal is the principal direction with maximum absolute "
                    "overlap with the matched signed cubic valley axis; the other two "
                    "direction-matched principal values are transverse"
                ),
                "spectral_residual": (
                    "gauge-invariant optimal injective matching of the rank-10 "
                    "candidate spectrum into the 12 direct-parent eigenvalues; the "
                    "matching is reported and no operator subtraction is performed"
                ),
            },
            "reported_non_gating_comparisons": [
                (
                    "injectively matched spectral maximum, RMS, and 95th-percentile "
                    "error"
                ),
                "candidate and parent valley-energy spreads",
                "opposite-valley energy splittings",
                "local gradients at candidate minima",
                "Hessian and mass sensitivity across declared stencil scales",
                "quadratic-fit residuals and condition numbers",
            ],
            "energy_reference": {
                "gap_and_curvature": "shift invariant",
                "parent_gamma_vbm": {
                    "role": (
                        "authenticated construction-point support datum; only the "
                        "conduction-valley side of the gap is withheld"
                    ),
                    "qexsd_sha256": (
                        "cc389a14d6b9f809eab69ba30b86129a01951788a3fdbc290589ef8f5f69adb0"
                    ),
                },
                "pointwise_spectral_residuals": (
                    "common accepted-S1 parent native QE reference; no fitted scalar "
                    "shift"
                ),
            },
            "inconclusive_conditions": [
                (
                    "a matched parent minimum lies outside the sampled 0.04 "
                    "inverse-angstrom capture radius"
                ),
                (
                    "the local fit is rank deficient or fails its recorded "
                    "conditioning check"
                ),
                (
                    "the direct-parent conduction band cannot be tracked through the "
                    "local sample"
                ),
                (
                    "required eigenvalues are nonfinite or carry unconverged-"
                    "eigenvalue diagnostics"
                ),
                "a comparison denominator required by a relative metric is zero",
            ],
            "scope_note": (
                "failure means inadequate for this declared intended use under the "
                "adopted targets; it does not mean the finite operator is "
                "intrinsically invalid"
            ),
        }


class QeWithheldInputRenderer:
    """Render the exact proposed QE NSCF input without filesystem side effects."""

    __slots__ = ("_lattice",)

    def __init__(self, lattice: SiliconLattice) -> None:
        self._lattice = lattice

    def render(self, points: tuple[WithheldPoint, ...]) -> str:
        matrix = self._lattice.direct.primitive_basis_matrix
        lines = [
            "&CONTROL",
            "    calculation = 'nscf'",
            "    prefix = 'system'",
            "    pseudo_dir = './'",
            "    outdir = './tmp/'",
            "    iprint = 2",
            "    verbosity = 'high'",
            "/",
            "&SYSTEM",
            "    ibrav = 0",
            "    nat = 2",
            "    ntyp = 1",
            "    nbnd = 12",
            "    ecutwfc = 42.0000000000",
            "    ecutrho = 336.0000000000",
            "    occupations = 'fixed'",
            "    nosym = .true.",
            "    noinv = .true.",
            "/",
            "&ELECTRONS",
            "    conv_thr = 1.0000000000e-12",
            "    diagonalization = 'david'",
            "    diago_full_acc = .true.",
            "/",
            "ATOMIC_SPECIES",
            " Si 28.086 Si.pbe-n-rrkjus_psl.1.0.0.UPF",
            "CELL_PARAMETERS (angstrom)",
        ]
        for column in range(3):
            lines.append(" " + " ".join(f"{value:.8f}" for value in matrix[:, column]))
        lines.extend(
            [
                "ATOMIC_POSITIONS (crystal)",
                " Si 0.000000000000 0.000000000000 0.000000000000",
                " Si 0.250000000000 0.250000000000 0.250000000000",
                "K_POINTS crystal",
                f" {len(points)}",
            ]
        )
        weight = 1.0 / len(points)
        for point in points:
            coordinate_text = " ".join(f"{value:.14f}" for value in point.fractional)
            lines.append(f" {coordinate_text} {weight:.16f}")
        return "\n".join(lines) + "\n"


class AuthorizationRequestBuilder:
    """Bind the exact proposed occurrence while leaving authorization absent."""

    __slots__ = ()

    def execute(
        self,
        input_identity: JsonObject,
        manifest_identity: JsonObject,
        criteria_identity: JsonObject,
        point_count: int,
    ) -> JsonObject:
        prior_point_count = 64
        prior_saved_state_bytes = 18_799_008
        workload_ratio = point_count / prior_point_count
        return {
            "schema_version": 1,
            "status": "authorization-required",
            "authorization_granted": False,
            "requested_invocation_count": 1,
            "retry_count_authorized": 0,
            "proposed_working_root": (
                "/Users/eugene/projects/ksdft2effmass/"
                "si-accepted-s1-withheld-parent-nscf-v1"
            ),
            "command": [
                "/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x",
                "-in",
                "pw.in",
            ],
            "executable": {
                "sha256": (
                    "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"
                ),
                "application": "Quantum ESPRESSO pw.x 7.5",
            },
            "input": input_identity,
            "withheld_manifest": manifest_identity,
            "validation_criteria": criteria_identity,
            "pseudopotential": {
                "filename": "Si.pbe-n-rrkjus_psl.1.0.0.UPF",
                "byte_size": 1_299_382,
                "sha256": (
                    "ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b"
                ),
            },
            "parent_saved_state": {
                "source_root": (
                    "/Users/eugene/projects/ksdft2effmass/"
                    "si-accepted-s1-parent-scf-gamma-k10-c42-20261031T070321Z/"
                    "run/tmp"
                ),
                "copy_required": True,
                "mutate_source": False,
                "manifest_byte_size": 10_763,
                "manifest_sha256": (
                    "2b80acf2bc53dcbc5c667d50c4747036704a640c86cdf5902a98e998e21aefb9"
                ),
                "producing_input": {
                    "byte_size": 606,
                    "sha256": (
                        "47138c7325cb854a6411fcb59babfda4bb102ed33aacd44ea62fb97d0c310bd6"
                    ),
                    "cell_text_reused": True,
                },
            },
            "scientific_scale": {
                "kpoint_count": point_count,
                "band_count": 12,
                "ecutwfc_ry": 42.0,
                "ecutrho_ry": 336.0,
                "diagonalization": "david",
                "full_accuracy_diagonalization": True,
            },
            "resource_report": {
                "reference_occurrence_kpoint_count": prior_point_count,
                "nominal_kpoint_workload_ratio": workload_ratio,
                "runtime_estimate": (
                    "unknown; nominal independent-k-point work is 6.375 times the "
                    "prior 64-point Davidson NSCF before fixed overhead"
                ),
                "linear_saved_state_extrapolation_bytes": int(
                    round(prior_saved_state_bytes * workload_ratio)
                ),
                "maximum_retained_bytes": 2_147_483_648,
                "execution_mode": "one local process",
            },
            "required_outputs": [
                "execution.json",
                "pw.out",
                "pw.err",
                "tmp/system.save/data-file-schema.xml",
                "nscf-saved-state-manifest.json",
                "artifact-manifest.json",
            ],
            "warning_and_stop_policy": {
                "unconverged_eigenvalue_warning": "block scientific handoff",
                "nonfinite_or_corrupt_output": "block scientific handoff",
                "timeout": "block scientific handoff; no automatic retry",
                "retry": "requires a new bounded authorization",
            },
            "authorization_boundary": (
                "approval of the recommendation and preparation does not authorize "
                "pw.x execution, parent-state copying, or artifact acquisition"
            ),
        }


class WithheldValidationPreparation:
    """Prepare exact coordinates, input, and an unauthorized execution request."""

    __slots__ = ()

    def execute(self) -> None:
        authenticator = ArtifactAuthenticator()
        structure_source = authenticator.execute(ARTIFACTS["structure"])
        qualification_source = authenticator.execute(ARTIFACTS["qualification"])
        lattice = SiliconLattice.from_structure(STRUCTURE)
        valleys = CandidateValleyReader().execute(QUALIFICATION_RESULT)
        points = WithheldKPointDesigner(lattice).execute(valleys)
        sources: JsonObject = {
            "structure": structure_source,
            "candidate_characterization": qualification_source,
        }
        manifest = WithheldManifestBuilder(lattice).execute(points, sources)
        serializer = TypedJsonMappingSerializer()
        manifest_wire = serializer.serialize(manifest)
        OUTPUT_MANIFEST.write_bytes(manifest_wire)
        criteria = ValidationCriteriaBuilder(lattice).execute()
        OUTPUT_CRITERIA.write_bytes(serializer.serialize(criteria))
        rendered_input = QeWithheldInputRenderer(lattice).render(points)
        OUTPUT_INPUT.write_text(rendered_input, encoding="utf-8")
        manifest_identity = self._identity(OUTPUT_MANIFEST)
        criteria_identity = self._identity(OUTPUT_CRITERIA)
        input_identity = self._identity(OUTPUT_INPUT)
        request = AuthorizationRequestBuilder().execute(
            input_identity, manifest_identity, criteria_identity, len(points)
        )
        OUTPUT_REQUEST.write_bytes(serializer.serialize(request))

    @staticmethod
    def _identity(path: Path) -> JsonObject:
        payload = path.read_bytes()
        return {
            "path": path.name,
            "byte_size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }


ARTIFACTS = {
    "structure": ArtifactIdentity(
        "structure",
        STRUCTURE,
        758,
        "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
    ),
    "qualification": ArtifactIdentity(
        "candidate characterization",
        QUALIFICATION_RESULT,
        48_404,
        "e82995489fd5e5084008c0a7d8bf6bc42c6c219838b073f0b0d9a56d24e04c53",
    ),
}


def main() -> None:
    WithheldValidationPreparation().execute()


if __name__ == "__main__":
    main()
