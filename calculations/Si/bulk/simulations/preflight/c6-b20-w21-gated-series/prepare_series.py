from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ksdft2effmass.serialization import TypedJsonMappingSerializer

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[2]
SIMULATIONS = BULK / "simulations"
S90_THROUGH_S110_PROTOCOL = BULK / "research-protocol/controlled-reduction-protocol.tex"
CURRENT_PROTOCOL = (
    BULK / "research-protocol/controlled-reduction-protocol-post-s110.tex"
)
LOCALIZATION_PREFLIGHT = (
    SIMULATIONS
    / "preflight/accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise"
)
LOCALIZATION_REQUEST = LOCALIZATION_PREFLIGHT / "authorization-request.json"
LOCALIZATION_CAMPAIGN = LOCALIZATION_PREFLIGHT / "campaign-preflight.json"
LOCALIZATION_OCCURRENCE = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1"
)
LOCALIZATION_RESULT = LOCALIZATION_OCCURRENCE / "campaign-result.json"
LOCALIZATION_FAILURE = LOCALIZATION_OCCURRENCE / "failure-summary.json"
LOCALIZATION_DIAGNOSTIC = LOCALIZATION_OCCURRENCE / "structural-diagnostic.json"
LOCALIZATION_REVERIFICATION = (
    LOCALIZATION_OCCURRENCE / "provider-reverification-result.json"
)
LOCALIZATION_ELIGIBILITY = (
    LOCALIZATION_OCCURRENCE / "reconciled-eligibility-summary.json"
)
S30_ROOT = BULK / "analysis/c6-b20-w21-untruncated-characterization"
S30_IMPLEMENTATION = S30_ROOT / "run_analysis.py"
S30_INITIAL_RESULT = S30_ROOT / "characterization-result-initial-fixed-gate.json"
S30_CORRECTION = S30_ROOT / "serialization-bound-correction.md"
S30_RESULT = S30_ROOT / "characterization-result.json"
S40_ROOT = BULK / "analysis/c6-b20-w21-revealed-408-development"
S40_IMPLEMENTATION = S40_ROOT / "run_analysis.py"
S40_INITIAL_RESULT = (
    S40_ROOT / "development-result-initial-linear-gate-disposition.json"
)
S40_CORRECTION = S40_ROOT / "hidden-oracle-role-correction.md"
S40_RESULT = S40_ROOT / "development-result.json"
S90_ROOT = BULK / "analysis/c6-b20-w21-spatial-truncation-design"
S90_IMPLEMENTATION = S90_ROOT / "prepare_design.py"
S90_DESIGN = S90_ROOT / "truncation-design.json"
S100_ROOT = BULK / "analysis/c6-b20-w21-spatial-truncation-evaluation"
S100_IMPLEMENTATION = S100_ROOT / "run_evaluation.py"
S100_LAUNCH_FAILURE = S100_ROOT / "initial-analysis-failure.md"
S100_INITIAL_RESULT = (
    S100_ROOT / "truncation-evaluation-initial-incomplete-diagnostics.json"
)
S100_CORRECTION = S100_ROOT / "diagnostic-completeness-correction.md"
S100_RESULT = S100_ROOT / "truncation-evaluation.json"
S105_ROOT = BULK / "analysis/c6-b20-w21-spatial-truncation-disposition"
S105_IMPLEMENTATION = S105_ROOT / "prepare_disposition.py"
S105_RESULT = S105_ROOT / "spatial-truncation-disposition.json"
S110_ROOT = BULK / "analysis/c6-b20-w21-slater-koster-definition-fit"
S110_IMPLEMENTATION = S110_ROOT / "run_definition_fit.py"
S110_RESULT = S110_ROOT / "slater-koster-definition-fit-result.json"
PREPROCESSING_RESULT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise-v1/"
    "preprocessing-result.json"
)
CONVERTER_RESULT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1/converter-result.json"
)
DEVELOPMENT_PARENT_CAMPAIGN = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-withheld-parent-nscf-v1/campaign-result.json"
)
DEVELOPMENT_PARENT_RESULT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-withheld-parent-nscf-v1/nscf-result.json"
)
CONFIRMATION_GEOMETRY = (
    BULK / "analysis/construction-mesh-adequacy-recommendation/"
    "successor-confirmation-holdout.json"
)
TARGET_DECISION = SIMULATIONS / "c6-b20-w21-outer-window-decision.md"
CONVERGENCE_DECISION = SIMULATIONS / "aiida-precise-convergence-adaptation-decision.md"
EXPECTED = {
    S90_THROUGH_S110_PROTOCOL: (
        "80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380"
    ),
    CURRENT_PROTOCOL: (
        "3ec2902a94ebe78eba1e223a0ee4ef99075f4bd86238398b67d370fa88224653"
    ),
    LOCALIZATION_REQUEST: (
        "02375507dbe487f1ad5dee2569151faf04c2e5a5fa3aadd9b0007d977bc26aa7"
    ),
    LOCALIZATION_CAMPAIGN: (
        "b7e6b150e28e4ae79eadffbc8799eb593554ccd4f9792347fbd6852ca9a1977d"
    ),
    LOCALIZATION_RESULT: (
        "5727bb294590868e28a1fb57e0b847863c6b02b7ab669a8d71ac2a12bd5b9d3c"
    ),
    LOCALIZATION_FAILURE: (
        "79fc6306e55581ae4b3fa90647d8f0c0b206f1339bdec332e064fd8c445dd135"
    ),
    LOCALIZATION_DIAGNOSTIC: (
        "95553e74ffe50177f859b5ec56627ffafeadc0b5c02a8e1745e9852938030618"
    ),
    LOCALIZATION_REVERIFICATION: (
        "23a0a6fe182abd0b5d2f7dcd142f27f81d6d6cca4fe9852be1950b5b622548b6"
    ),
    LOCALIZATION_ELIGIBILITY: (
        "0b2a0e6bab52574c353d780f562afe11d07bb1400bf149fa1178ddb5e8504e4c"
    ),
    S30_IMPLEMENTATION: (
        "985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e"
    ),
    S30_INITIAL_RESULT: (
        "f038459542ab2d7801ce83630274fd27db60275c6694b53fbcb904980a22ef89"
    ),
    S30_CORRECTION: (
        "680cf0aeaa25c85915e8315ce06d1a821c9172333b43e5046dc8f75ba06a3ef9"
    ),
    S30_RESULT: ("37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18"),
    S40_IMPLEMENTATION: (
        "c555f690fb0d6a7517bd61bcc3abee5acc30fc337e0bd3add358593f9b8f2952"
    ),
    S40_INITIAL_RESULT: (
        "fbd9ab474328323f43d03754d01a0a9be115ea30739c1a4ac65ca47767d99459"
    ),
    S40_CORRECTION: (
        "29e58f90c40ec428e12d087b4d6b6b70bfcd18d9c539bdcd9f17aa3dd36f333d"
    ),
    S40_RESULT: ("bb1a6d0fab5d08fecaa0d86cbfe00e8670e7f089e289c6fabc59c32c6f76991d"),
    S90_IMPLEMENTATION: (
        "687ed568e392ea1c3ac333c543313cc57206d5a92903b7e3e015b5103224cc1d"
    ),
    S90_DESIGN: ("6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531"),
    S100_IMPLEMENTATION: (
        "5e2779945974c4c9cbdf702236d3686d937964be3bb4ff480fe7c476d582436f"
    ),
    S100_LAUNCH_FAILURE: (
        "ba85289c91f189a3d1ebd6982029f1a951c70d410d3bbeea28cea896d8c5d65c"
    ),
    S100_INITIAL_RESULT: (
        "4a2e18d889ffc682acc2dc04cf37760aa1d662ac945d0ea8452eae814eb186de"
    ),
    S100_CORRECTION: (
        "ba371d967dcc623002657709f75280a46e86c51305fe3ecb8c7df00185c1c4dc"
    ),
    S100_RESULT: ("1ac8bb59137e8dc7217df52f89c18a84e8599bcf82ec59f40a361929d4322a52"),
    S105_IMPLEMENTATION: (
        "6613d234b7e084baede6d9cfef9d34be7e14360b23ccc296e6adacfe24f422e0"
    ),
    S105_RESULT: ("519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68"),
    S110_IMPLEMENTATION: (
        "64459edf6f03161d30c6b6beec3361fa5ad7085417ab2a038d4f6c7c632925b3"
    ),
    S110_RESULT: ("b9b8403dfc8b24df01e1671f582697440e1a211d60e0e70c9b0f621dfa086e98"),
    PREPROCESSING_RESULT: (
        "ca73c8e0384e5f8b3bccffbe1ab1b2e58d636876f802b380a06eec74f8c50e93"
    ),
    CONVERTER_RESULT: (
        "b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a"
    ),
    DEVELOPMENT_PARENT_CAMPAIGN: (
        "babd24f429f4eb51082235c2d7f6afaeccf193160a139cd295f14916b1cbb7cd"
    ),
    DEVELOPMENT_PARENT_RESULT: (
        "29d3c50f70b9faa0eed24acf5f0673d43eb666d1216327fdf74e53cdd6176b51"
    ),
    CONFIRMATION_GEOMETRY: (
        "51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8"
    ),
    TARGET_DECISION: (
        "526b0a265b306c13f9ae54ce34c57030277f15704a4a571295da43330005db59"
    ),
    CONVERGENCE_DECISION: (
        "9d2e8269d1f2351d1c3b3228c24f4b2baad6505c1c1039da8889412b3cba6238"
    ),
}
SERIALIZER = TypedJsonMappingSerializer()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def stage(
    *,
    stage_id: str,
    title: str,
    kind: str,
    status: str,
    prerequisites: list[str],
    gate: str,
    success: str,
    failure: str,
    execution_authorized: bool,
    exact_artifact_binding_available: bool,
) -> dict[str, object]:
    return {
        "stage_id": stage_id,
        "title": title,
        "kind": kind,
        "status": status,
        "prerequisites": prerequisites,
        "entry_gate": gate,
        "on_success": success,
        "on_failure": failure,
        "execution_authorized": execution_authorized,
        "exact_artifact_binding_available": exact_artifact_binding_available,
    }


def main() -> None:
    for path, expected in EXPECTED.items():
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"identity mismatch: {path}")
    request = json.loads(LOCALIZATION_REQUEST.read_text(encoding="utf-8"))
    if request["authorization_granted"] is not False:
        raise RuntimeError("localization request must remain ungranted")
    holdout = json.loads(CONFIRMATION_GEOMETRY.read_text(encoding="utf-8"))
    if (
        holdout["status"] != "coordinates-frozen-parent-values-unobserved"
        or holdout["unique_point_count"] != 402
        or len(holdout["points"]) != 402
    ):
        raise RuntimeError("confirmation geometry or blinding status changed")

    plan = {
        "schema_version": 1,
        "series_id": "Si-bulk-C6-B20-W21-full-operator-to-reduction-v1",
        "candidate_id": "C6-B20-W21",
        "status": (
            "blocked-S110-orbital-alignment-rank-deficient-human-decision-required"
        ),
        "automation_policy": {
            "automatic_execution": False,
            "automatic_stage_advance": False,
            "blanket_authorization": False,
            "calculator_authorization_rule": (
                "every calculator occurrence requires a new exact bounded human "
                "authorization after its artifact-bound request exists"
            ),
            "failure_rule": (
                "failure stops the dependent branch at an operational gate; no retry, "
                "budget extension, target-space change, mesh escalation, truncation, "
                "or reduction is automatic; parent-oracle criteria limit physical "
                "claims but do not gate controlled reduction"
            ),
        },
        "fixed_scientific_coordinates": {
            "structure": "accepted relaxed S1",
            "parent": "accepted PBE SSSP 1.3.0 efficiency SCF",
            "construction_mesh": "Gamma-origin 6x6x6 ordered mesh",
            "parent_band_count": 20,
            "wannier_rank": 10,
            "outer_window_ev": [-6.0, 21.0],
            "frozen_window_ev": [-5.85, 8.0],
            "projections": ["Si:sp3", "Si:l=0:r=2"],
            "num_iter": 40000,
            "dis_num_iter": 40000,
            "conv_tol_angstrom_squared": 2e-9,
            "dis_conv_tol_dimensionless": 2e-9,
            "conv_window": 6,
            "num_cg_steps": 200,
        },
        "bound_inputs": {
            "S90_through_S110_controlled_reduction_protocol": identity(
                S90_THROUGH_S110_PROTOCOL
            ),
            "current_post_S110_controlled_reduction_protocol": identity(
                CURRENT_PROTOCOL
            ),
            "target_space_decision": identity(TARGET_DECISION),
            "convergence_adaptation_decision": identity(CONVERGENCE_DECISION),
            "preprocessing_result": identity(PREPROCESSING_RESULT),
            "converter_result": identity(CONVERTER_RESULT),
            "localization_preflight": identity(LOCALIZATION_CAMPAIGN),
            "localization_authorization_request": identity(LOCALIZATION_REQUEST),
            "localization_result": identity(LOCALIZATION_RESULT),
            "localization_failure": identity(LOCALIZATION_FAILURE),
            "localization_structural_diagnostic": identity(LOCALIZATION_DIAGNOSTIC),
            "localization_provider_reverification": identity(
                LOCALIZATION_REVERIFICATION
            ),
            "localization_reconciled_eligibility": identity(LOCALIZATION_ELIGIBILITY),
            "S30_implementation": identity(S30_IMPLEMENTATION),
            "S30_initial_fixed_gate_result": identity(S30_INITIAL_RESULT),
            "S30_serialization_bound_correction": identity(S30_CORRECTION),
            "S30_characterization_result": identity(S30_RESULT),
            "S40_corrected_implementation": identity(S40_IMPLEMENTATION),
            "S40_initial_linear_gate_disposition": identity(S40_INITIAL_RESULT),
            "S40_hidden_oracle_role_correction": identity(S40_CORRECTION),
            "S40_corrected_development_result": identity(S40_RESULT),
            "S90_design_implementation": identity(S90_IMPLEMENTATION),
            "S90_frozen_truncation_design": identity(S90_DESIGN),
            "S100_evaluation_implementation": identity(S100_IMPLEMENTATION),
            "S100_initial_launch_failure": identity(S100_LAUNCH_FAILURE),
            "S100_initial_incomplete_diagnostic_result": identity(S100_INITIAL_RESULT),
            "S100_diagnostic_completeness_correction": identity(S100_CORRECTION),
            "S100_complete_family_evaluation": identity(S100_RESULT),
            "S105_disposition_implementation": identity(S105_IMPLEMENTATION),
            "S105_spatial_truncation_disposition": identity(S105_RESULT),
            "S110_definition_fit_implementation": identity(S110_IMPLEMENTATION),
            "S110_blocked_alignment_result": identity(S110_RESULT),
            "revealed_408_parent_campaign": identity(DEVELOPMENT_PARENT_CAMPAIGN),
            "revealed_408_parent_result": identity(DEVELOPMENT_PARENT_RESULT),
            "confirmation_402_geometry": identity(CONFIRMATION_GEOMETRY),
        },
        "development_targets": {
            "role": (
                "revealed-parent oracle-evaluation criteria, not operational "
                "reduction gates"
            ),
            "indirect_gap_relative_maximum": 0.05,
            "valley_position_fraction_of_gamma_x_maximum": 0.03,
            "each_effective_mass_relative_maximum": 0.08,
            "gamma_x_distance_inverse_angstrom": 1.1488345422775257,
            "valley_position_maximum_inverse_angstrom": 0.03446503626832577,
        },
        "hidden_oracle_policy": {
            "fixed_reduction_source": "S30 full untruncated Wannier operator",
            "revealed_408_role": "development-oracle labels and calibration only",
            "unobserved_402_role": "prospective confirmation oracle",
            "operational_diagnostics_exclude_withheld_parent_values": True,
            "parent_fidelity_does_not_gate_controlled_reduction": True,
            "freeze_before_402_reveal": [
                "spatial truncations",
                "Slater-Koster parameterizations",
                "diagnostic rules and calibration",
                "fitting conventions",
                "oracle-error predictions",
                "evaluation criteria",
            ],
        },
        "stages": [
            stage(
                stage_id="S00-interface",
                title="Authenticated 20-band preprocessing and conversion",
                kind="retained-evidence",
                status="complete",
                prerequisites=[],
                gate="authenticated NNKP and finite shape-correct AMN/MMN/EIG",
                success="S10-localization",
                failure="closed; upstream reconstruction requires a new decision",
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S10-localization",
                title="Fresh precise-profile localization",
                kind="calculator",
                status="complete-native-convergence",
                prerequisites=["S00-interface"],
                gate="exact authorization request 02375507...b26aa7",
                success="S20-provider-eligibility",
                failure="stop for target-space and trajectory review",
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S20-provider-eligibility",
                title="Native and represented-operator eligibility",
                kind="no-calculator-verification",
                status="complete-provider-eligible-after-reference-correction",
                prerequisites=["S10-localization"],
                gate=(
                    "passed without tolerance change: canonical-WIN gauge and "
                    "disentanglement k-point residuals 3.300004713935323e-11 are "
                    "below the declared 1e-10 fractional tolerance"
                ),
                success="S30-untruncated-characterization",
                failure="stop; failed outputs remain diagnostic only",
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S30-untruncated-characterization",
                title="Full untruncated Wannier-operator characterization",
                kind="no-calculator-analysis",
                status="complete-structurally-verified-scientifically-unassessed",
                prerequisites=["S20-provider-eligibility"],
                gate=(
                    "bind exact eligible HR/u/u_dis identities; verify source-mesh "
                    "reconstruction, spectra, valleys, curvatures, masses, and locality"
                ),
                success="S40-development-408",
                failure="stop; no spatial truncation or reduction",
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S40-development-408",
                title="Revealed 408-point direct-parent development comparison",
                kind="no-calculator-analysis",
                status="complete-development-oracle-labels-recorded",
                prerequisites=["S30-untruncated-characterization"],
                gate=(
                    "apply the frozen 5%, 3%, and 8% oracle-evaluation criteria "
                    "without treating them as deployable diagnostics"
                ),
                success="S90-spatial-truncation-design",
                failure=(
                    "limit parent-fidelity claims without blocking controlled reduction"
                ),
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S50-prediction-freeze",
                title="Freeze operator identity, predictions, fits, and conventions",
                kind="no-calculator-record",
                status="blocked-by-S110",
                prerequisites=["S110-slater-koster-definition-fit"],
                gate=(
                    "reductions, operational diagnostics, calibration, fitting "
                    "conventions, oracle-error predictions, and criteria are immutable"
                ),
                success="S60-confirmation-parent-402",
                failure="stop; no confirmation-parent calculation",
                execution_authorized=False,
                exact_artifact_binding_available=False,
            ),
            stage(
                stage_id="S60-confirmation-parent-402",
                title="Blinded 402-point direct-parent confirmation calculation",
                kind="calculator",
                status="blocked-by-S50",
                prerequisites=["S50-prediction-freeze"],
                gate=(
                    "frozen prediction record plus separately rendered exact QE input "
                    "and a new bounded human authorization"
                ),
                success="S70-confirmation-comparison",
                failure="stop; do not alter frozen predictions",
                execution_authorized=False,
                exact_artifact_binding_available=False,
            ),
            stage(
                stage_id="S70-confirmation-comparison",
                title="Prospective 402-point confirmation comparison",
                kind="no-calculator-analysis",
                status="blocked-by-S60",
                prerequisites=["S60-confirmation-parent-402"],
                gate=(
                    "test frozen diagnostic-to-hidden-error predictions without "
                    "refitting"
                ),
                success="S120-slater-koster-validation",
                failure=(
                    "record diagnostic non-prediction without erasing the controlled "
                    "reduction"
                ),
                execution_authorized=False,
                exact_artifact_binding_available=False,
            ),
            stage(
                stage_id="S80-full-operator-acceptance",
                title="Optional physical-fidelity disposition for the full operator",
                kind="scientific-disposition",
                status="not-required-for-controlled-reduction",
                prerequisites=["S40-development-408"],
                gate=(
                    "parent-oracle criteria control physical claims, not reduction "
                    "eligibility"
                ),
                success=(
                    "physical-fidelity claim only; no effect on reduction eligibility"
                ),
                failure=(
                    "retain source-fidelity limitations and continue controlled "
                    "reduction"
                ),
                execution_authorized=False,
                exact_artifact_binding_available=False,
            ),
            stage(
                stage_id="S90-spatial-truncation-design",
                title="Declare spatial-truncation coordinates and tail criteria",
                kind="scientific-decision",
                status="complete-design-frozen-S100-ready",
                prerequisites=[
                    "S30-untruncated-characterization",
                    "S40-development-408",
                ],
                gate=(
                    "freeze the full operator as the reduction source and separately "
                    "declare hopping geometry, retained shells or radii, operational "
                    "tail diagnostics, tolerances, and state-space alignment"
                ),
                success="S100-spatial-truncation-evaluation",
                failure=(
                    "retain the structurally eligible full operator without truncation "
                    "claims"
                ),
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S100-spatial-truncation-evaluation",
                title="Evaluate each declared truncation against the full operator",
                kind="no-calculator-analysis",
                status="complete-family-evaluated-no-radius-selected",
                prerequisites=["S90-spatial-truncation-design"],
                gate="separate spectral, valley, curvature, mass, and locality errors",
                success="S105-spatial-truncation-disposition",
                failure=("retain the full operator without accepting a truncation"),
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S105-spatial-truncation-disposition",
                title="Accept one declared shell or retain full support",
                kind="scientific-decision",
                status="complete-full-support-retained-S110-definition-ready",
                prerequisites=["S100-spatial-truncation-evaluation"],
                gate=(
                    "use only frozen construction requirements and S90/S100 "
                    "operational diagnostics; do not use parent-oracle values"
                ),
                success="S110-slater-koster-definition-fit",
                failure="retain the full untruncated operator as the only source",
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S110-slater-koster-definition-fit",
                title="Declare and fit the Slater-Koster reduction",
                kind="no-calculator-model-reduction",
                status="blocked-orbital-alignment-rank-deficient-no-fit",
                prerequisites=["S105-spatial-truncation-disposition"],
                gate=(
                    "explicit basis, gauge, energy reference, shells, parameter map, "
                    "fit set, validation set, and optimizer declaration"
                ),
                success="S50-prediction-freeze",
                failure="no Slater-Koster model is accepted",
                execution_authorized=False,
                exact_artifact_binding_available=True,
            ),
            stage(
                stage_id="S120-slater-koster-validation",
                title=(
                    "Validate the reduction separately from parent and "
                    "truncation errors"
                ),
                kind="no-calculator-analysis",
                status="blocked-by-S70",
                prerequisites=[
                    "S110-slater-koster-definition-fit",
                    "S70-confirmation-comparison",
                ],
                gate=(
                    "disjoint hidden-parent confirmation data and separate parent-"
                    "model, mesh, spectral-truncation, spatial-truncation, and "
                    "parameterization errors"
                ),
                success="final reviewed reduction disposition",
                failure=(
                    "reject the reduction without changing the accepted full operator"
                ),
                execution_authorized=False,
                exact_artifact_binding_available=False,
            ),
        ],
        "confirmation_blinding": {
            "geometry_status": holdout["status"],
            "point_count": holdout["unique_point_count"],
            "parent_values_present_in_plan": False,
            "unblinding_allowed_after_stage": "S50-prediction-freeze",
        },
        "current_next_action": (
            "choose the default stop after the failed S110 common-space gate or "
            "separately authorize Level 1 reusable Slater-Koster foundations under "
            "the post-S110 protocol; spectral-only, global-unitary, rank-nine, and "
            "new-source levels each require a later separate decision"
        ),
    }
    (ROOT / "series-plan.json").write_bytes(SERIALIZER.serialize(plan))


if __name__ == "__main__":
    main()
