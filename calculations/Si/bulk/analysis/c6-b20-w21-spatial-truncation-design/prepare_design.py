from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

from ksdft2effmass.serialization import TypedJsonMappingSerializer

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
PROTOCOL = BULK / "research-protocol/controlled-reduction-protocol.tex"
S30_ROOT = BULK / "analysis/c6-b20-w21-untruncated-characterization"
S30_IMPLEMENTATION = S30_ROOT / "run_analysis.py"
S30_RESULT = S30_ROOT / "characterization-result.json"
S40_ROOT = BULK / "analysis/c6-b20-w21-revealed-408-development"
S40_CORRECTION = S40_ROOT / "hidden-oracle-role-correction.md"
S40_RESULT = S40_ROOT / "development-result.json"
OUTPUT = ROOT / "truncation-design.json"
EXPECTED = {
    PROTOCOL: "80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380",
    S30_IMPLEMENTATION: (
        "985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e"
    ),
    S30_RESULT: ("37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18"),
    S40_CORRECTION: (
        "29e58f90c40ec428e12d087b4d6b6b70bfcd18d9c539bdcd9f17aa3dd36f333d"
    ),
    S40_RESULT: ("bb1a6d0fab5d08fecaa0d86cbfe00e8670e7f089e289c6fabc59c32c6f76991d"),
}
EXPECTED_OPERATOR_IDENTITIES = {
    "eligible_hr": "24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55",
    "eligible_wsvec": (
        "f40fa7f81afaa9bcf9614c6e3c53c14db0db6b0b429b84bfd10f2e40474de1a0"
    ),
    "eligible_u": "41758b721b79cae233689b4fb9fa359e750b82da8ed5bcd13b1d5faf3c5d8bf3",
    "eligible_u_dis": (
        "3c1d3574f3bf783cf7b54d8e9fd00fa5811ef05a56240850d46f43a2c95b7ace"
    ),
}


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


def mapping_list(value: JsonValue, label: str) -> list[JsonObject]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise TypeError(f"{label} must be a list of mappings")
    return cast(list[JsonObject], value)


def integer(value: JsonValue, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an integer")
    return value


def number(value: JsonValue, label: str) -> float:
    if type(value) not in {int, float}:
        raise TypeError(f"{label} must be numeric")
    return float(cast(int | float, value))


def boolean(value: JsonValue, label: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{label} must be boolean")
    return value


class SpatialTruncationDesignPreparer:
    """Freeze an outcome-independent complete-shell truncation design."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        for path, expected in EXPECTED.items():
            if not path.is_file() or path.is_symlink() or sha256(path) != expected:
                raise RuntimeError(f"source identity mismatch: {path}")
        s30 = load_json(S30_RESULT)
        self._verify_s30_source(s30)
        shells = self._shell_family(s30)
        lattice = mapping(s30["lattice"], "S30 lattice")
        return {
            "schema_version": 1,
            "stage_id": "S90-spatial-truncation-design",
            "status": "complete-design-frozen-S100-ready",
            "calculator_invocations": 0,
            "authorization_scope": (
                "prepare the controlled spatial-truncation design only; do not run "
                "S100, fit a Slater-Koster model, or observe 402-point parent values"
            ),
            "bound_inputs": {
                "current_protocol": identity(PROTOCOL),
                "S30_implementation": identity(S30_IMPLEMENTATION),
                "S30_full_operator_characterization": identity(S30_RESULT),
                "S40_hidden_oracle_role_correction": identity(S40_CORRECTION),
                "S40_corrected_development_result": identity(S40_RESULT),
            },
            "fixed_reduction_source": {
                "route": "C6-B20-W21-aiida-precise",
                "operator": "full untruncated rank-10 Wannier Hamiltonian H_W",
                "basis": "localized Wannier90 basis from the authenticated u and u_dis",
                "energy_unit": "electron_volt",
                "energy_reference": (
                    "native Quantum ESPRESSO reference retained by EIG/HR"
                ),
                "direct_basis_columns_angstrom": lattice[
                    "direct_basis_columns_angstrom"
                ],
                "reciprocal_basis_columns_inverse_angstrom": lattice[
                    "reciprocal_basis_columns_inverse_angstrom"
                ],
                "operator_artifacts": self._operator_artifacts(s30),
                "wannier_rank": 10,
                "effective_representative_count": 383,
                "structural_eligibility": (
                    "native convergence, provider eligibility, pair closure, "
                    "Hermiticity, and source reconstruction verified by S20/S30"
                ),
                "physical_fidelity_disposition": (
                    "revealed parent discrepancies limit physical claims but do not "
                    "change controlled-reduction source eligibility"
                ),
            },
            "truncation_family": {
                "operator_scope": "H_W only",
                "mask_rule": (
                    "include every effective representative whose Cartesian physical "
                    "radius belongs to a complete shell at or below the indexed shell"
                ),
                "shell_grouping_rule": (
                    "reproduce the authenticated S30 rule: round Cartesian radii to "
                    "nine decimal places in angstrom before grouping"
                ),
                "pair_rule": (
                    "every mask must preserve complete R and -R representative pairs; "
                    "a closure failure rejects that truncation occurrence"
                ),
                "nested": True,
                "outcome_selected_radius": False,
                "complete_family_required": True,
                "shell_count": len(shells),
                "full_support_control_shell_index_zero_based": len(shells) - 1,
                "shells": shells,
                "design_rationale": (
                    "retain all authenticated shells, including onsite-only and full-"
                    "support controls, because S30 descriptive locality values were "
                    "already observed and must not be used to prune the family"
                ),
            },
            "S100_evaluation_domains": {
                "source_mesh": {
                    "role": "finite-transform reconstruction control",
                    "point_count": 216,
                },
                "uniform_reciprocal_grid": {
                    "kind": "Gamma-origin fractional primitive grid",
                    "points_per_axis": 21,
                    "point_count": 9261,
                    "role": "primary direct finite-representation compression domain",
                },
                "dense_valley_grid": {
                    "kind": "Gamma-origin fractional primitive grid",
                    "points_per_axis": 41,
                    "point_count": 68921,
                    "role": "valley-family initialization and identity control",
                },
                "curvature_stencils": {
                    "coordinate_basis": "Cartesian reciprocal axes",
                    "steps_inverse_angstrom": [0.001, 0.002, 0.005, 0.01],
                    "primary_step_inverse_angstrom": 0.002,
                    "role": (
                        "within-source valley curvature and stencil-stability "
                        "diagnostics"
                    ),
                },
                "conduction_band_index_zero_based": 4,
                "edge_window_ev": 0.5,
            },
            "operational_diagnostics": {
                "structural": [
                    "included and excluded representative counts",
                    "negative-representative closure",
                    "maximum pair-Hermiticity residual in electron_volt",
                    "full-support reconstruction equality",
                ],
                "tail": {
                    "spectral_triangle_bound": (
                        "B_H(s) = sum over excluded representatives of the block "
                        "spectral norm; a uniform operator-error upper bound"
                    ),
                    "frobenius_tail": (
                        "F_H(s) = square root of the sum of excluded squared block "
                        "Frobenius norms; an RMS/Parseval measure, not a uniform bound"
                    ),
                    "maximum_excluded_block_spectral_norm": True,
                },
                "direct_full_to_truncated": {
                    "operator_metrics": [
                        "maximum spectral norm on the 21^3 grid",
                        "RMS Frobenius norm on the 21^3 grid",
                        "95th-percentile spectral norm on the 21^3 grid",
                    ],
                    "ordered_spectrum_metrics": [
                        "maximum absolute error over all ten bands",
                        "RMS and 95th-percentile absolute error over all ten bands",
                        "lowest-conduction-band errors over the full grid",
                        (
                            "lowest-conduction-band errors within 0.5 eV of the "
                            "full-source edge"
                        ),
                    ],
                    "monotone_envelope_rule": (
                        "for every direct metric report the supremum over all retained "
                        "larger-shell truncations; do not select an isolated favorable "
                        "shell"
                    ),
                },
                "full_source_observable_changes": [
                    "indirect-gap change",
                    "six signed Delta-family valley identity and location changes",
                    "valley-energy splitting and spread changes",
                    "principal-curvature and direction-matched effective-mass changes",
                    "curvature-stencil stability across every declared step",
                ],
                "interpretation": (
                    "all differences are H_W-to-H_truncated controlled-reduction "
                    "diagnostics; none is a direct-parent physical error"
                ),
            },
            "selection_and_freeze_policy": {
                "S90_accepts_a_radius": False,
                "S100_must_report_every_shell": True,
                "S100_may_refit_or_change_masks": False,
                "future_radius_selection_requires_separate_record": True,
                "future_selection_inputs": (
                    "only the frozen operational diagnostics and declared construction "
                    "data; never 402-point parent values"
                ),
                "before_402_parent_reveal": [
                    "selected truncation candidates",
                    "all operational diagnostic rules",
                    (
                        "any diagnostic-to-error calibration using revealed 408 "
                        "development data"
                    ),
                    (
                        "Slater-Koster basis, shells, parameter map, fit and "
                        "validation roles"
                    ),
                    "predicted hidden-parent errors and evaluation criteria",
                ],
            },
            "oracle_boundary": {
                "revealed_408_role": (
                    "development-oracle labels only; not consumed to define this "
                    "shell family"
                ),
                "confirmation_402_geometry_known": True,
                "confirmation_402_parent_values_observed": False,
                "confirmation_402_values_consumed_by_S90": False,
                "parent_fidelity_is_an_operational_truncation_gate": False,
            },
            "nonclaims": [
                "No spatial truncation was evaluated or accepted by S90.",
                (
                    "No Slater-Koster basis, parameterization, fit, or validation was "
                    "performed."
                ),
                "No direct-parent error is available as an operational diagnostic.",
                (
                    "No physical fidelity, uncertainty bound, or material validation "
                    "is established."
                ),
                "No calculator invocation or later-stage authorization is implied.",
            ],
            "next_stage": (
                "S100 may evaluate the complete frozen shell family in one separately "
                "authorized no-calculator analysis; it may not select or fit a model"
            ),
        }

    def _verify_s30_source(self, s30: JsonObject) -> None:
        if not boolean(
            s30["structural_reconstruction_verified"],
            "S30 structural reconstruction status",
        ):
            raise RuntimeError("S30 operator is not structurally verified")
        inventory = mapping(s30["operator_inventory"], "S30 operator inventory")
        if boolean(inventory["spatial_truncation_applied"], "S30 truncation status"):
            raise RuntimeError("S30 source must be untruncated")
        if integer(inventory["wannier_rank"], "S30 rank") != 10:
            raise RuntimeError("S30 rank changed")
        if (
            integer(
                inventory["effective_ws_representative_count"],
                "S30 representative count",
            )
            != 383
        ):
            raise RuntimeError("S30 representative count changed")
        sources = mapping(s30["sources"], "S30 sources")
        for label, expected in EXPECTED_OPERATOR_IDENTITIES.items():
            artifact = mapping(sources[label], f"S30 source {label}")
            if artifact.get("sha256") != expected:
                raise RuntimeError(f"S30 source identity changed: {label}")

    def _operator_artifacts(self, s30: JsonObject) -> JsonObject:
        sources = mapping(s30["sources"], "S30 sources")
        return {
            label: mapping(sources[label], f"S30 source {label}")
            for label in EXPECTED_OPERATOR_IDENTITIES
        }

    def _shell_family(self, s30: JsonObject) -> list[JsonValue]:
        results = mapping(s30["results"], "S30 results")
        locality = mapping(results["locality"], "S30 locality")
        source_shells = mapping_list(locality["shells"], "S30 locality shells")
        if len(source_shells) != 18:
            raise RuntimeError("S30 shell inventory changed")
        records: list[JsonValue] = []
        previous_included = 0
        for index, shell in enumerate(source_shells):
            shell_count = integer(
                shell["shell_representative_count"], "shell representative count"
            )
            included = integer(
                shell["included_representative_count"], "included representative count"
            )
            excluded = integer(
                shell["excluded_representative_count"], "excluded representative count"
            )
            if included != previous_included + shell_count:
                raise RuntimeError("S30 shell counts are not cumulative")
            if included + excluded != 383:
                raise RuntimeError("S30 shell does not partition the representation")
            records.append(
                {
                    "shell_index_zero_based": index,
                    "shell_id": f"H-shell-{index:02d}",
                    "display_radius_angstrom": number(
                        shell["radius_angstrom"], "shell radius"
                    ),
                    "shell_representative_count": shell_count,
                    "included_representative_count": included,
                    "excluded_representative_count": excluded,
                    "onsite_only_control": index == 0,
                    "full_support_control": excluded == 0,
                }
            )
            previous_included = included
        if previous_included != 383:
            raise RuntimeError("S30 full shell does not recover every representative")
        return records


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("S90 truncation design already exists")
    design = SpatialTruncationDesignPreparer().execute()
    OUTPUT.write_bytes(TypedJsonMappingSerializer().serialize(design))


if __name__ == "__main__":
    main()
