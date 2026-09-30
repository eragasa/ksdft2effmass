# ruff: noqa: E501
r"""Numerical verification for ``BlindAlignmentInferenceEvaluator``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns post hoc map, energy-shift, extraction, model-class, and active-sector
spectral diagnostics for successful blind inference.

Intrinsic and cross-object scope
--------------------------------
The test composes authenticated construction and inference, then compares evaluator
channels with retained exact-case values. It is integration evidence and uses explicit
absolute tolerances rather than matrix digests as cross-platform numerical acceptance.

VVUQ and scientific exclusions
------------------------------
A pass is bounded numerical verification on synthetic finite matrices. It does not
validate silicon, electronic-structure alignment, transferability, or uncertainty
quantification.
"""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d import (
    Periodic1DJsonValue,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.baseline import (
    BlindAlignmentBaselineData,
    BlindAlignmentBaselineLoader,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.construction import (
    BlindAlignmentObservationConstructionRequest,
    BlindAlignmentObservationConstructor,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.evaluation import (
    BlindAlignmentEvaluationRequest,
    BlindAlignmentInferenceEvaluator,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.inference import (
    BlindAlignmentInferenceActionizer,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.input_records import (
    BlindAlignmentCampaignInput,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.records import (
    BlindAlignmentInferenceRequest,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.serialization import (
    BlindAlignmentInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]
SUT = BlindAlignmentInferenceEvaluator


class TestBlindAlignmentInferenceEvaluator:
    """Own post hoc blind-inference numerical evaluation evidence."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing immutable campaign artifacts."""
        return Path(__file__).resolve().parents[8]

    def campaign_state(
        self,
    ) -> tuple[
        BlindAlignmentCampaignInput,
        BlindAlignmentBaselineData,
        tuple[dict[str, Periodic1DJsonValue], ...],
    ]:
        """Load typed controls, authenticated baseline, and retained exact records."""
        root = self.repository_root()
        directory = root / (
            "calculations/research-monograph/impurity-defect-1d-blind-alignment"
        )
        specification = BlindAlignmentInputDeserializer().execute(
            (directory / "input.json").read_bytes()
        )
        baseline = BlindAlignmentBaselineLoader().execute(specification, root)
        retained = cast(
            dict[str, Periodic1DJsonValue],
            json.loads((directory / "result.json").read_text(encoding="utf-8")),
        )
        records = cast(
            list[dict[str, Periodic1DJsonValue]], retained["exact_full_rank_cases"]
        )
        return specification, baseline, tuple(records)

    @pytest.mark.parametrize(
        "case_index",
        (
            pytest.param(0, id="spinless_full_rank"),
            pytest.param(1, id="spinor_full_rank"),
        ),
    )
    def test_method__execute__reproduces_retained_exact_case_diagnostics(
        self, case_index: int
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-001.

        Requirement: Independent post hoc evaluation must reproduce every retained
        scalar diagnostic for both exact full-rank cases.

        Method: Construct and infer each exact case through maintained Actionizers,
        evaluate against separately retained hidden truth, and compare with the
        immutable retained result.

        Oracle: Retained synthetic numerical-verification scalar channels generated
        under the accepted version-one protocol.

        Acceptance: Integer and optional-value channels agree exactly; every floating
        channel agrees with absolute tolerance ``1e-10`` and zero relative tolerance.

        Interpretation: A pass establishes maintained exact-case evaluation agreement
        while keeping correlation and matrix identity separate.

        Limitations: Platform-dependent matrix SHA-256 values are not numerical
        acceptance criteria, and no material-validation claim is made.
        """
        specification, baseline, retained_records = self.campaign_state()
        case = specification.exact_cases[case_index]
        constructed = BlindAlignmentObservationConstructor().execute(
            BlindAlignmentObservationConstructionRequest(
                baseline=baseline,
                identifier=case.identifier,
                defect_id=case.defect_id,
                spin_count=case.spin_count,
                minimum_anchor_singular_value=(case.minimum_anchor_singular_value),
                unitary_noise_radians=0.0,
                generator_seed=0,
                core_radius_cells=specification.core_radius_cells,
            )
        )
        inference = BlindAlignmentInferenceActionizer().execute(
            BlindAlignmentInferenceRequest(
                constructed.observation, specification.policy
            )
        )
        result = SUT().execute(
            BlindAlignmentEvaluationRequest(
                identifier=case.identifier,
                inference=inference,
                hidden_truth=constructed.hidden_truth,
                cell_count=baseline.cell_count,
                eigenvalue_degeneracy_tolerance=specification.algebraic_tolerance,
            )
        )
        retained = retained_records[case_index]

        assert result.identifier == retained["id"]
        assert (
            result.active_lowest_eigenspace_dimension
            == retained["active_lowest_eigenspace_dimension"]
        )
        assert result.active_lowest_state_fidelity == pytest.approx(
            cast(float, retained["active_lowest_state_fidelity"]),
            rel=0.0,
            abs=1e-10,
        )
        scalar_fields = (
            "phase_quotiented_alignment_frobenius_defect",
            "energy_shift_error",
            "extraction_frobenius_defect",
            "extraction_relative_frobenius_defect",
            "planted_onsite_model_class_residual",
            "extracted_onsite_model_class_residual",
            "active_spectral_maximum_absolute_defect",
            "active_lowest_eigenspace_projector_defect",
        )
        for field in scalar_fields:
            assert getattr(result, field) == pytest.approx(
                cast(float, retained[field]), rel=0.0, abs=1e-10
            )
