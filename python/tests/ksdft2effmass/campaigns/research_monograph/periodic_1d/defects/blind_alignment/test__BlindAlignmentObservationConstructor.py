# ruff: noqa: E501
r"""Software verification for ``BlindAlignmentObservationConstructor``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns construction of inference-visible synthetic observations separately
from authored post hoc truth.

Intrinsic and cross-object scope
--------------------------------
The test uses the authenticated retained baseline, so it is integration evidence. Its
oracle is direct finite-matrix conjugation with the separately returned hidden record;
it does not invoke the inference Actionizer or historical runner.

VVUQ and scientific exclusions
------------------------------
A pass establishes the declared synthetic construction and information boundary. It
does not validate an electronic-structure overlap, silicon, transferability, or
uncertainty quantification.
"""

from dataclasses import fields
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.baseline import (
    BlindAlignmentBaselineData,
    BlindAlignmentBaselineLoader,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.construction import (
    BlindAlignmentObservationConstructionRequest,
    BlindAlignmentObservationConstructor,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.input_records import (
    BlindAlignmentCampaignInput,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.serialization import (
    BlindAlignmentInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = BlindAlignmentObservationConstructor


class TestBlindAlignmentObservationConstructor:
    """Own synthetic observation-construction integration evidence."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing immutable campaign artifacts."""
        return Path(__file__).resolve().parents[8]

    def campaign_state(
        self,
    ) -> tuple[
        BlindAlignmentCampaignInput,
        BlindAlignmentBaselineData,
    ]:
        """Decode input and authenticate the matched-extraction baseline."""
        root = self.repository_root()
        path = root / (
            "calculations/research-monograph/"
            "impurity-defect-1d-blind-alignment/input.json"
        )
        specification = BlindAlignmentInputDeserializer().execute(path.read_bytes())
        baseline = BlindAlignmentBaselineLoader().execute(specification, root)
        return specification, baseline

    @pytest.mark.parametrize(
        "case_index",
        (
            pytest.param(0, id="spinless_full_rank"),
            pytest.param(1, id="spinor_full_rank"),
        ),
    )
    def test_method__execute__separates_observation_from_hidden_truth(
        self, case_index: int
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-014.

        Requirement: Exact campaign construction must expose only declared matrices
        to inference while retaining the authored map, perturbation, and shift in a
        separate post hoc record.

        Method: Construct each retained exact case from authenticated baseline data
        and recompute the candidate Hamiltonian directly from hidden truth.

        Oracle: Direct unitary conjugation and scalar-identity addition in the finite
        represented space.

        Acceptance: Candidate reconstruction and map unitarity agree within absolute
        tolerance ``1e-12``; dimensions, spin metadata, exterior rank, and immutable
        storage agree with the authored case.

        Interpretation: A pass establishes the synthetic observation formula and
        typed information separation for both spin factors.

        Limitations: The authored covariance is synthetic rather than an independently
        calculated electronic-structure overlap.
        """
        specification, baseline = self.campaign_state()
        case = specification.exact_cases[case_index]
        result = SUT().execute(
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
        observation = result.observation
        truth = result.hidden_truth
        expected_candidate = truth.candidate_to_reference.conj().T @ (
            observation.reference_operator.matrix + truth.planted_defect
        ) @ truth.candidate_to_reference + truth.energy_shift * np.eye(
            observation.candidate_operator.basis.dimension
        )

        assert observation.reference_operator.basis.spin_count == case.spin_count
        assert observation.candidate_operator.basis.spin_count == case.spin_count
        np.testing.assert_allclose(
            observation.candidate_operator.matrix,
            expected_candidate,
            rtol=0.0,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            truth.candidate_to_reference @ truth.candidate_to_reference.conj().T,
            np.eye(truth.candidate_to_reference.shape[0]),
            rtol=0.0,
            atol=1e-12,
        )
        exterior_rank = np.linalg.matrix_rank(
            observation.exterior_energy_anchor,
            tol=specification.policy.anchor_rank_tolerance,
        )
        assert exterior_rank >= specification.policy.minimum_energy_anchor_rank
        assert not observation.anchor_cross_covariance.flags.writeable
        assert not truth.candidate_to_reference.flags.writeable
        assert not truth.planted_defect.flags.writeable
        observation_fields = tuple(value.name for value in fields(observation))
        assert "candidate_to_reference" not in observation_fields
        assert "planted_defect" not in observation_fields
        assert "energy_shift" not in observation_fields
