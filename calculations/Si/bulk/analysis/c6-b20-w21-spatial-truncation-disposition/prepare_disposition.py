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
REPOSITORY = BULK.parents[2]
PROTOCOL = BULK / "research-protocol/controlled-reduction-protocol.tex"
S90_DESIGN = (
    BULK / "analysis/c6-b20-w21-spatial-truncation-design/truncation-design.json"
)
S100_IMPLEMENTATION = (
    BULK / "analysis/c6-b20-w21-spatial-truncation-evaluation/run_evaluation.py"
)
S100_INITIAL_RESULT = (
    BULK / "analysis/c6-b20-w21-spatial-truncation-evaluation/"
    "truncation-evaluation-initial-incomplete-diagnostics.json"
)
S100_CORRECTION = (
    BULK / "analysis/c6-b20-w21-spatial-truncation-evaluation/"
    "diagnostic-completeness-correction.md"
)
S100_RESULT = (
    BULK / "analysis/c6-b20-w21-spatial-truncation-evaluation/"
    "truncation-evaluation.json"
)
LOCALITY_NUMERICS = (
    REPOSITORY / "docs/computational/Si-bulk/wannier-component-locality/numerics.md"
)
NUMERICAL_SPECIFICATION = (
    REPOSITORY / "specification/ksdft2Effmass.numerical-specification.v1.md"
)
OUTPUT = ROOT / "spatial-truncation-disposition.json"
EXPECTED = {
    PROTOCOL: "80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380",
    S90_DESIGN: "6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531",
    S100_IMPLEMENTATION: (
        "5e2779945974c4c9cbdf702236d3686d937964be3bb4ff480fe7c476d582436f"
    ),
    S100_INITIAL_RESULT: (
        "4a2e18d889ffc682acc2dc04cf37760aa1d662ac945d0ea8452eae814eb186de"
    ),
    S100_CORRECTION: (
        "ba371d967dcc623002657709f75280a46e86c51305fe3ecb8c7df00185c1c4dc"
    ),
    S100_RESULT: ("1ac8bb59137e8dc7217df52f89c18a84e8599bcf82ec59f40a361929d4322a52"),
    LOCALITY_NUMERICS: (
        "0eaadb70e16813045595b63a96133e27feffe2d4cfff5a30e46ed582ca49ca60"
    ),
    NUMERICAL_SPECIFICATION: (
        "095cfb8fbb376873be3994d22198f9f13263e24f99bcfd04c6b192eee0eac06c"
    ),
}


class SpatialTruncationDisposition:
    """Retain full support without post-observation threshold creation."""

    __slots__ = ()

    def execute(self) -> JsonObject:
        for path, expected in EXPECTED.items():
            if not path.is_file() or path.is_symlink() or sha256(path) != expected:
                raise RuntimeError(f"source identity mismatch: {path}")
        design = load_json(S90_DESIGN)
        evaluation = load_json(S100_RESULT)
        self._verify_boundaries(design, evaluation)
        shells = mapping_list(
            mapping(evaluation["evaluation"], "S100 evaluation")["shells"],
            "S100 shells",
        )
        selected = shells[-1]
        smaller = shells[:-1]
        if any(
            number(
                mapping(
                    mapping(shell["direct_operator"], "direct operator")[
                        "spectral_norm"
                    ],
                    "spectral norm",
                )["maximum_ev"],
                "direct operator maximum",
            )
            <= 0.0
            for shell in smaller
        ):
            raise RuntimeError("a non-full shell unexpectedly has zero operator error")
        self._verify_full_support(selected)
        shell_15 = shells[15]
        shell_16 = shells[16]
        nonmonotone = self._nonmonotone_observables(shell_15, shell_16)
        return {
            "schema_version": 1,
            "stage_id": "S105-spatial-truncation-disposition",
            "status": "complete-full-support-retained-S110-definition-ready",
            "calculator_invocations": 0,
            "bound_inputs": {
                "current_protocol": identity(PROTOCOL),
                "S90_frozen_design": identity(S90_DESIGN),
                "S100_final_implementation": identity(S100_IMPLEMENTATION),
                "S100_initial_incomplete_result": identity(S100_INITIAL_RESULT),
                "S100_diagnostic_correction": identity(S100_CORRECTION),
                "S100_complete_family_evaluation": identity(S100_RESULT),
                "locality_numerics": identity(LOCALITY_NUMERICS),
                "numerical_specification": identity(NUMERICAL_SPECIFICATION),
            },
            "disposition": {
                "outcome": "retain-full-support-no-spatial-truncation",
                "selected_shell_id": selected["shell_id"],
                "selected_shell_index_zero_based": selected["shell_index_zero_based"],
                "selected_radius_angstrom": selected["radius_angstrom"],
                "selected_representative_count": selected[
                    "included_representative_count"
                ],
                "excluded_representative_count": selected[
                    "excluded_representative_count"
                ],
                "spatial_truncation_applied": False,
                "H_T_equals_H_W": True,
                "basis_gauge_energy_reference_and_state_space_unchanged": True,
            },
            "decision_rule": {
                "rule": (
                    "retain full support when no nontrivial spatial-error acceptance "
                    "threshold was frozen before inspecting S100; do not create a "
                    "post-observation threshold to accept an attractive shell"
                ),
                "S90_selected_a_radius": False,
                "S90_froze_a_numeric_operator_acceptance_threshold": False,
                "existing_numerical_convergence_tolerances_repurposed": False,
                "reason_not_repurposed": (
                    "the numerical-specification tolerances govern the parent "
                    "numerical-convergence channel, not spatial model reduction"
                ),
                "only_exact_shell_is_full_support": True,
                "nontrivial_shell_count_retained_as_descriptive_evidence": len(smaller),
            },
            "full_support_checks": {
                "tail_spectral_triangle_bound_ev": nested_number(
                    selected, ("tail", "spectral_triangle_bound_ev")
                ),
                "direct_operator_maximum_spectral_norm_ev": nested_number(
                    selected,
                    ("direct_operator", "spectral_norm", "maximum_ev"),
                ),
                "ordered_spectrum_maximum_absolute_ev": nested_number(
                    selected,
                    ("ordered_spectrum", "all_bands", "maximum_absolute_ev"),
                ),
                "indirect_gap_change_ev": nested_number(
                    selected,
                    ("full_source_observable_changes", "gap_change_ev"),
                ),
                "maximum_valley_displacement_inverse_angstrom": nested_number(
                    selected,
                    (
                        "full_source_observable_changes",
                        "maximum_valley_displacement_inverse_angstrom",
                    ),
                ),
                "maximum_primary_mass_absolute_relative_change": nested_number(
                    selected,
                    (
                        "full_source_observable_changes",
                        "maximum_primary_mass_absolute_relative_change",
                    ),
                ),
            },
            "nonmonotone_observation": nonmonotone,
            "error_channel_disposition": {
                "selected_spatial_truncation_error_H_W_minus_H_T": (
                    "identically zero because H_T is defined to equal H_W"
                ),
                "future_parameterization_error": "H_T minus H_SK",
                "future_parent_to_reduction_error": "H_KS minus H_SK",
                "rule_for_future_SK_range_restriction": (
                    "unless a new separately frozen H_T is authorized, any support "
                    "restriction introduced by H_SK belongs to parameterization error"
                ),
            },
            "oracle_boundary": {
                "revealed_408_parent_values_consumed": False,
                "confirmation_402_parent_values_observed": False,
                "confirmation_402_parent_values_consumed": False,
                "parent_oracle_used_for_disposition": False,
            },
            "next_stage": {
                "stage_id": "S110-slater-koster-definition-fit",
                "status": "ready-separate-no-calculator-stage",
                "authorization_inferred": False,
                "required_source": (
                    "the full-support H_T identical to the authenticated S30 H_W"
                ),
            },
            "nonclaims": [
                "No nontrivial truncation radius is accepted.",
                "No Slater-Koster basis, parameter map, fit, or optimizer is selected.",
                "No parent-fidelity limitation is repaired or reclassified.",
                "No physical validation or uncertainty bound is established.",
                "No later-stage execution, commit, or publication is authorized.",
            ],
        }

    def _verify_boundaries(self, design: JsonObject, evaluation: JsonObject) -> None:
        selection = mapping(
            design["selection_and_freeze_policy"], "S90 selection policy"
        )
        if selection["S90_accepts_a_radius"] is not False:
            raise RuntimeError("S90 unexpectedly accepted a radius")
        if selection["future_radius_selection_requires_separate_record"] is not True:
            raise RuntimeError("S90 separate-disposition rule changed")
        if evaluation["status"] != "complete-family-evaluated-no-radius-selected":
            raise RuntimeError("S100 status changed")
        evaluated = mapping(evaluation["evaluation"], "S100 evaluation")
        if evaluated["radius_selected"] is not False:
            raise RuntimeError("S100 unexpectedly selected a radius")
        oracle = mapping(evaluation["oracle_boundary"], "S100 oracle boundary")
        for key in (
            "revealed_408_parent_values_consumed",
            "confirmation_402_parent_values_observed",
            "confirmation_402_parent_values_consumed",
        ):
            if oracle[key] is not False:
                raise RuntimeError(f"S100 oracle boundary changed: {key}")

    def _verify_full_support(self, shell: JsonObject) -> None:
        if integer(shell["included_representative_count"], "included count") != 383:
            raise RuntimeError("full-support representative count changed")
        if integer(shell["excluded_representative_count"], "excluded count") != 0:
            raise RuntimeError("full-support shell excludes representatives")
        zero_paths = (
            ("tail", "spectral_triangle_bound_ev"),
            ("direct_operator", "spectral_norm", "maximum_ev"),
            ("ordered_spectrum", "all_bands", "maximum_absolute_ev"),
            ("full_source_observable_changes", "gap_change_ev"),
            (
                "full_source_observable_changes",
                "maximum_valley_displacement_inverse_angstrom",
            ),
            (
                "full_source_observable_changes",
                "maximum_primary_mass_absolute_relative_change",
            ),
        )
        if any(nested_number(shell, path) != 0.0 for path in zero_paths):
            raise RuntimeError("full-support equality control changed")

    def _nonmonotone_observables(
        self, smaller: JsonObject, larger: JsonObject
    ) -> JsonObject:
        smaller_gap = abs(
            nested_number(smaller, ("full_source_observable_changes", "gap_change_ev"))
        )
        larger_gap = abs(
            nested_number(larger, ("full_source_observable_changes", "gap_change_ev"))
        )
        smaller_mass = nested_number(
            smaller,
            (
                "full_source_observable_changes",
                "maximum_primary_mass_absolute_relative_change",
            ),
        )
        larger_mass = nested_number(
            larger,
            (
                "full_source_observable_changes",
                "maximum_primary_mass_absolute_relative_change",
            ),
        )
        smaller_direct = nested_number(
            smaller, ("direct_operator", "spectral_norm", "maximum_ev")
        )
        larger_direct = nested_number(
            larger, ("direct_operator", "spectral_norm", "maximum_ev")
        )
        detected = (
            smaller_gap < larger_gap
            and smaller_mass < larger_mass
            and smaller_direct > larger_direct
        )
        if not detected:
            raise RuntimeError("expected S100 nonmonotone observation changed")
        return {
            "detected": True,
            "smaller_shell_id": smaller["shell_id"],
            "larger_shell_id": larger["shell_id"],
            "smaller_shell_gap_absolute_change_ev": smaller_gap,
            "larger_shell_gap_absolute_change_ev": larger_gap,
            "smaller_shell_primary_mass_absolute_relative_change": smaller_mass,
            "larger_shell_primary_mass_absolute_relative_change": larger_mass,
            "smaller_shell_direct_operator_maximum_ev": smaller_direct,
            "larger_shell_direct_operator_maximum_ev": larger_direct,
            "interpretation": (
                "the smaller shell has more favorable gap and mass changes while the "
                "larger shell has the smaller direct operator error; no isolated "
                "observable supplies an unambiguous nontrivial choice"
            ),
        }


def nested_number(record: JsonObject, path: tuple[str, ...]) -> float:
    value: JsonValue = record
    for key in path:
        value = mapping(value, "nested value")[key]
    return number(value, "nested value")


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


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("S105 disposition already exists")
    result = SpatialTruncationDisposition().execute()
    OUTPUT.write_bytes(TypedJsonMappingSerializer().serialize(result))


if __name__ == "__main__":
    main()
