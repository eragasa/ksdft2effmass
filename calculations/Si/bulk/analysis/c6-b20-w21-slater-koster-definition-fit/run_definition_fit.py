from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import projectkoios
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.serialization import TypedJsonMappingSerializer

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
REPOSITORY = BULK.parents[2]
PROTOCOL = BULK / "research-protocol/controlled-reduction-protocol.tex"
S105_RESULT = (
    BULK / "analysis/c6-b20-w21-spatial-truncation-disposition/"
    "spatial-truncation-disposition.json"
)
REDUCTION_SPECIFICATION = REPOSITORY / "docs/research/ksdft2effmass.05.md"
ALIGNMENT_PROOF = (
    REPOSITORY / "docs/research/proofs/ksdft2effmass/operator-alignment/"
    "tb-anchored-identification.md"
)
PROJECTKOIOS_PACKAGE = Path(
    "/Users/eugene/worktrees/"
    "projectkoios-simulations-pw-dft-wannierization-tranche-1/"
    "src/python/projectkoios"
)
PROJECTKOIOS_WANNIER90 = PROJECTKOIOS_PACKAGE / "integrations/wannier90"
PROJECTKOIOS_SOURCES = {
    PROJECTKOIOS_WANNIER90 / "__init__.py": (
        "26f568e7446d2721983ec0e0a3e7131ba8c2e6442c88b91d92d81c4b296a36ad"
    ),
    PROJECTKOIOS_WANNIER90 / "_parsing.py": (
        "07de9ab225fbc7cfd5317f1592b5dcd0105d5eaec982d814980272cdd578439a"
    ),
    PROJECTKOIOS_WANNIER90 / "_matrix_conventions.py": (
        "95d7d19b520548cc860d6c56d53b0cec477b078a307c3e4bcb2feddbc8f2ee65"
    ),
    PROJECTKOIOS_WANNIER90 / "interface_data.py": (
        "5b4033f5b99373eca5bd7ce1b492f52f3d16cad43945e0e2ddf845121193b078"
    ),
    PROJECTKOIOS_WANNIER90 / "unitary_matrices.py": (
        "33ebad1a82f887f0dd59787c066bded1989b6dd9b7220c3e551b0c5cb798e75f"
    ),
    PROJECTKOIOS_WANNIER90 / "disentanglement_matrices.py": (
        "64ede7d0e45b9d1b200026322f48d832fe7587b5b99c7eb292bfae2d7390fdd7"
    ),
}
CONVERTER_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1"
)
LOCALIZATION_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1"
)
PREPROCESSING_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise-v1"
)
AMN = CONVERTER_ROOT / "run/silicon.amn"
CONVERTER_RESULT = CONVERTER_ROOT / "converter-result.json"
GAUGE = LOCALIZATION_ROOT / "run/silicon_u.mat"
DISENTANGLEMENT = LOCALIZATION_ROOT / "run/silicon_u_dis.mat"
ELIGIBILITY = LOCALIZATION_ROOT / "reconciled-eligibility-summary.json"
WIN = PREPROCESSING_ROOT / "input/silicon.win"
NNKP = PREPROCESSING_ROOT / "run/silicon.nnkp"
WANNIER90_PROJECTION_GUIDE = Path(
    "/Users/eugene/projects/wannier90-3.1.0/doc/user_guide/projections.tex"
)
OUTPUT = ROOT / "slater-koster-definition-fit-result.json"
EXPECTED = {
    PROTOCOL: "80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380",
    S105_RESULT: "519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68",
    REDUCTION_SPECIFICATION: (
        "694aeab14b067e54a26b8d746a4e5cf24fb55c0a43427b2acdfa8473b3725df2"
    ),
    ALIGNMENT_PROOF: (
        "42ae19c9ac076d8617da7cef35d4bd6b12a5d446f6620ffb0c863196abe6e59b"
    ),
    AMN: "9186cd5b8802bede18f81b96188f0a2035eb97565c2f811f5ca7769f2ebefece",
    CONVERTER_RESULT: (
        "b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a"
    ),
    GAUGE: "41758b721b79cae233689b4fb9fa359e750b82da8ed5bcd13b1d5faf3c5d8bf3",
    DISENTANGLEMENT: (
        "3c1d3574f3bf783cf7b54d8e9fd00fa5811ef05a56240850d46f43a2c95b7ace"
    ),
    ELIGIBILITY: ("0b2a0e6bab52574c353d780f562afe11d07bb1400bf149fa1178ddb5e8504e4c"),
    WIN: "b48069e4f8ecd7209a318c47c77691de063bd0575658eb88a1e662a359d3dcc8",
    NNKP: "608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575",
    WANNIER90_PROJECTION_GUIDE: (
        "c4b56f2d92bc98d0d86d629ad66ff3fe6433200c89ae4902728c552e3aded090"
    ),
    **PROJECTKOIOS_SOURCES,
}


class SlaterKosterDefinitionFit:
    """Apply the mandatory orbital-alignment gate before any SK fit."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        for path, expected in EXPECTED.items():
            if not path.is_file() or path.is_symlink() or sha256(path) != expected:
                raise RuntimeError(f"source identity mismatch: {path}")
        disposition = load_json(S105_RESULT)
        self._verify_disposition(disposition)
        source_package = str(PROJECTKOIOS_PACKAGE)
        if source_package not in projectkoios.__path__:
            projectkoios.__path__.append(source_package)
        from projectkoios.integrations.wannier90 import (  # type: ignore[import-untyped] # noqa: PLC0415
            Wannier90DisentanglementMatrixParser,
            Wannier90ProjectionParser,
            Wannier90UnitaryMatrixParser,
        )

        projections = Wannier90ProjectionParser().execute(AMN.read_bytes())
        gauge = Wannier90UnitaryMatrixParser().execute(GAUGE.read_bytes())
        disentanglement = Wannier90DisentanglementMatrixParser().execute(
            DISENTANGLEMENT.read_bytes()
        )
        if (
            projections.kpoint_count != 216
            or projections.band_count != 20
            or projections.projection_count != 10
            or gauge.kpoint_count != 216
            or gauge.wannier_count != 10
            or disentanglement.kpoint_count != 216
            or disentanglement.band_count != 20
            or disentanglement.wannier_count != 10
        ):
            raise RuntimeError("alignment artifact dimensions changed")
        kpoints = np.asarray(gauge.fractional_kpoints.magnitude, dtype=np.float64)
        dis_kpoints = np.asarray(
            disentanglement.fractional_kpoints.magnitude, dtype=np.float64
        )
        expected_grid = gamma_grid(6)
        if not np.allclose(kpoints, dis_kpoints, atol=1.0e-12, rtol=0.0):
            raise RuntimeError("gauge and disentanglement k-point orders disagree")
        if not np.allclose(kpoints, expected_grid, atol=1.0e-10, rtol=0.0):
            raise RuntimeError("alignment artifacts do not use the canonical C6 order")
        hybrid_transform = atomic_to_projection_transform()
        projection_unitarity = float(
            np.max(np.abs(hybrid_transform.conj().T @ hybrid_transform - np.eye(10)))
        )
        if projection_unitarity != 0.0:
            raise RuntimeError("declared sp3-to-atomic transformation is not unitary")
        amn_matrices = tuple(
            np.asarray(value.magnitude, dtype=np.complex128)
            for value in projections.matrices
        )
        maximum_amn = max(float(np.max(np.abs(value))) for value in amn_matrices)
        native_bound = alignment_singular_value_bound(maximum_amn)
        records: list[JsonValue] = []
        deficient: list[JsonValue] = []
        gamma_null_weights: JsonObject | None = None
        for index in range(216):
            u_dis = np.asarray(
                disentanglement.matrices[index].magnitude, dtype=np.complex128
            )
            u_matrix = np.asarray(gauge.matrices[index].magnitude, dtype=np.complex128)
            final_frame = u_dis @ u_matrix
            projection_in_final_frame = (
                final_frame.conj().T @ amn_matrices[index] @ hybrid_transform.conj().T
            )
            _left, singular_values, right_adjoint = np.linalg.svd(
                projection_in_final_frame
            )
            minimum = float(singular_values[-1])
            rank = int(np.count_nonzero(singular_values > native_bound))
            condition = float(singular_values[0] / singular_values[-1])
            record: JsonObject = {
                "ordered_kpoint_index_zero_based": index,
                "fractional_reciprocal_coordinates": kpoints[index].tolist(),
                "resolved_rank_at_native_bound": rank,
                "maximum_singular_value": float(singular_values[0]),
                "next_to_minimum_singular_value": float(singular_values[-2]),
                "minimum_singular_value": minimum,
                "condition_number": condition,
                "full_rank_gate_passed": rank == 10,
            }
            records.append(record)
            if rank != 10:
                deficient.append(record)
            if index == 0:
                null_vector = right_adjoint[-1].conj()
                labels = atomic_orbital_labels()
                gamma_null_weights = {
                    label: float(abs(value) ** 2)
                    for label, value in zip(labels, null_vector, strict=True)
                }
        if gamma_null_weights is None:
            raise RuntimeError("Gamma alignment diagnostic was not constructed")
        passed = not deficient
        if passed:
            raise RuntimeError(
                "alignment unexpectedly passed; the retained stop disposition must be "
                "reviewed before enabling fitting"
            )
        fit_indices, validation_indices = fit_validation_split()
        return {
            "schema_version": 1,
            "stage_id": "S110-slater-koster-definition-fit",
            "status": "blocked-orbital-alignment-rank-deficient-no-fit",
            "calculator_invocations": 0,
            "fit_invocations": 0,
            "bound_inputs": {
                "current_protocol": identity(PROTOCOL),
                "S105_full_support_disposition": identity(S105_RESULT),
                "reduction_specification": identity(REDUCTION_SPECIFICATION),
                "alignment_proof_material": identity(ALIGNMENT_PROOF),
                "AMN": identity(AMN),
                "converter_result": identity(CONVERTER_RESULT),
                "gauge": identity(GAUGE),
                "disentanglement": identity(DISENTANGLEMENT),
                "localization_eligibility": identity(ELIGIBILITY),
                "canonical_WIN": identity(WIN),
                "NNKP": identity(NNKP),
                "Wannier90_projection_guide": identity(WANNIER90_PROJECTION_GUIDE),
                "ProjectKoios_parser_sources": [
                    identity(path) for path in PROJECTKOIOS_SOURCES
                ],
            },
            "fixed_source": {
                "H_T_equals_H_W": True,
                "rank": 10,
                "spin_convention": "spinless scalar-relativistic non-SOC",
                "energy_reference": "unchanged native S30 Wannier reference in eV",
                "basis_for_fit": (
                    "two Si sites, each ordered (s, px, py, pz, s-star), after "
                    "TB-anchored projection and Lowdin orthonormalization"
                ),
            },
            "provisional_model_definition": {
                "activated_for_fit": False,
                "M1": {
                    "description": "orthogonal nearest-neighbor homopolar sp3s-star",
                    "real_parameters": [
                        "E_s",
                        "E_p",
                        "E_s_star",
                        "V1_ss_sigma",
                        "V1_sp_sigma",
                        "V1_pp_sigma",
                        "V1_pp_pi",
                        "V1_s_star_p_sigma",
                    ],
                },
                "M2": {
                    "description": (
                        "M1 plus symmetry-shared second-neighbor two-center channels"
                    ),
                    "additional_real_parameters": [
                        "V2_ss_sigma",
                        "V2_sp_sigma",
                        "V2_pp_sigma",
                        "V2_pp_pi",
                        "V2_s_star_p_sigma",
                        "V2_s_s_star_sigma",
                        "V2_s_star_s_star_sigma",
                    ],
                },
                "parameter_domain": "real and unbounded for the direct linear fit",
                "first_neighbor_s_s_star_and_s_star_s_star": "fixed to zero in M1",
                "orbital_order": list(atomic_orbital_labels()),
                "projection_file_order": [
                    "A:sp3-1",
                    "A:sp3-2",
                    "A:sp3-3",
                    "A:sp3-4",
                    "B:sp3-1",
                    "B:sp3-2",
                    "B:sp3-3",
                    "B:sp3-4",
                    "A:s-star",
                    "B:s-star",
                ],
            },
            "frozen_fit_plan_not_executed": {
                "fit_source_grid": "canonical Gamma-origin 6x6x6 C6 grid",
                "fit_indices_zero_based": fit_indices,
                "validation_indices_zero_based": validation_indices,
                "split_rule": (
                    "fit when (i+j+k) modulo 2 is zero; validate otherwise in "
                    "lexicographic C6 order"
                ),
                "operator_objective": (
                    "uniform real-and-imaginary Frobenius least squares after "
                    "TB-anchored unitary alignment"
                ),
                "optimizer": (
                    "deterministic real linear SVD least squares with no random start"
                ),
                "validation": (
                    "disjoint operator and ordered-spectrum residuals; full-source "
                    "valley, gap, curvature, and effective-mass changes"
                ),
                "acceptance_tolerances_defined": False,
                "interpretation": (
                    "even a successful future fit would be descriptive until separate "
                    "operator and spectral acceptance tolerances are frozen"
                ),
            },
            "alignment_gate": {
                "formula": (
                    "B(k) = [U_dis(k) U(k)]^dagger A(k) T^dagger; a unitary "
                    "TB-to-Wannier identification requires all ten singular values "
                    "to be resolved"
                ),
                "AMN_native_decimal_places": 12,
                "gauge_native_decimal_places": 10,
                "disentanglement_native_decimal_places": 10,
                "maximum_native_AMN_absolute_value": maximum_amn,
                "singular_value_native_uncertainty_bound": native_bound,
                "required_rank": 10,
                "all_kpoints_full_rank": False,
                "deficient_kpoint_count": len(deficient),
                "deficient_kpoints": deficient,
                "gamma_null_direction_atomic_orbital_weights": gamma_null_weights,
                "kpoint_diagnostics": records,
                "gate_passed": False,
            },
            "failure_disposition": {
                "reason": (
                    "the projected ten-orbital sp3s-star trial frame is not full rank "
                    "inside the retained rank-10 Wannier subspace at every source "
                    "k point; Lowdin orthonormalization and a unitary common-space "
                    "operator residual are therefore undefined"
                ),
                "fit_started": False,
                "parameter_vector_produced": False,
                "Slater_Koster_model_accepted": False,
                "dependent_S50_prediction_freeze_ready": False,
            },
            "oracle_boundary": {
                "revealed_408_parent_values_consumed": False,
                "confirmation_402_parent_values_observed": False,
                "confirmation_402_parent_values_consumed": False,
            },
            "next_action": {
                "status": "human-scientific-decision-required",
                "automatic_retry_allowed": False,
                "options_requiring_separate_authority": [
                    (
                        "retain no Slater-Koster reduction from this source and stop "
                        "the branch"
                    ),
                    (
                        "define a lower-rank or nonunitary common-space comparison, "
                        "explicitly changing the operator question"
                    ),
                    (
                        "authorize a new target-space/projection/localization route; "
                        "this requires new calculator authorizations"
                    ),
                    (
                        "authorize a spectral-only fit that cannot satisfy the S110 "
                        "aligned-operator contract"
                    ),
                ],
            },
            "nonclaims": [
                "No Slater-Koster parameters were fit.",
                "No model-class adequacy or identifiability was established.",
                "No spectral-only result is substituted for operator alignment.",
                "No target space, projection, gauge, or source operator was changed.",
                "No parent-oracle value was used.",
                "No retry or later stage is authorized.",
            ],
        }

    def _verify_disposition(self, disposition: JsonObject) -> None:
        if disposition["status"] != (
            "complete-full-support-retained-S110-definition-ready"
        ):
            raise RuntimeError("S105 status changed")
        selected = mapping(disposition["disposition"], "S105 disposition")
        if (
            selected["H_T_equals_H_W"] is not True
            or selected["spatial_truncation_applied"] is not False
            or selected["selected_representative_count"] != 383
        ):
            raise RuntimeError("S105 full-support disposition changed")
        oracle = mapping(disposition["oracle_boundary"], "S105 oracle boundary")
        if any(value is not False for value in oracle.values()):
            raise RuntimeError("S105 oracle boundary changed")


def atomic_to_projection_transform() -> Complex128Array:
    """Map atomic sp3s-star coordinates to native projection-file columns."""
    transform = np.zeros((10, 10), dtype=np.complex128)
    hybrids = 0.5 * np.asarray(
        (
            (1.0, 1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0, -1.0),
            (1.0, -1.0, 1.0, -1.0),
            (1.0, -1.0, -1.0, 1.0),
        ),
        dtype=np.complex128,
    )
    transform[0:4, 0:4] = hybrids
    transform[5:9, 4:8] = hybrids
    transform[4, 8] = 1.0
    transform[9, 9] = 1.0
    transform.setflags(write=False)
    return transform


def atomic_orbital_labels() -> tuple[str, ...]:
    return (
        "A:s",
        "A:px",
        "A:py",
        "A:pz",
        "A:s-star",
        "B:s",
        "B:px",
        "B:py",
        "B:pz",
        "B:s-star",
    )


def alignment_singular_value_bound(maximum_amn: float) -> float:
    """Derive a conservative spectral bound from native decimal precision."""
    gauge_rounding = 0.5e-10
    amn_rounding = 0.5e-12
    composite_element_bound = 10.0 * (2.0 * gauge_rounding + gauge_rounding**2)
    projected_element_bound = 20.0 * (
        maximum_amn * composite_element_bound
        + amn_rounding * (1.0 + composite_element_bound)
    )
    return 10.0 * projected_element_bound


def gamma_grid(size: int) -> Float64Array:
    values = np.arange(size, dtype=np.float64) / size
    return np.asarray(
        tuple((i, j, k) for i in values for j in values for k in values),
        dtype=np.float64,
    )


def fit_validation_split() -> tuple[list[JsonValue], list[JsonValue]]:
    fit: list[JsonValue] = []
    validation: list[JsonValue] = []
    index = 0
    for i in range(6):
        for j in range(6):
            for k in range(6):
                destination = fit if (i + j + k) % 2 == 0 else validation
                destination.append(index)
                index += 1
    if len(fit) != 108 or len(validation) != 108:
        raise RuntimeError("fit/validation split is not balanced")
    return fit, validation


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


def load_json(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON root must be a mapping: {path}")
    return cast(JsonObject, value)


def mapping(value: JsonValue, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a mapping")
    return value


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("S110 result already exists")
    result = SlaterKosterDefinitionFit().execute()
    OUTPUT.write_bytes(TypedJsonMappingSerializer().serialize(result))


if __name__ == "__main__":
    main()
