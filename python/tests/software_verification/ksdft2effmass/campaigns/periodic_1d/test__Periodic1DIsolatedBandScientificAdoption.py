r"""Software verification of periodic-1D isolated-band replay adoption.

Evidence profile: claim_bearing

Bounded artifact scope: the authorized deterministic replay sidecar, typed scientific
hierarchy, and complete, truncated, and fitted coefficient routes.

Scientific exclusions: passing establishes source authentication and software/numerical
reproducibility only. It does not establish material relevance, scientific validation,
uncertainty quantification, or acceptance of the effective models.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic_1d import (
    PERIODIC_1D_ISOLATED_BAND_DEFAULT_ABSOLUTE_TOLERANCE,
    Periodic1DIsolatedBandCampaignJsonSerializer,
    Periodic1DIsolatedBandReplayArtifactDecoder,
    Periodic1DIsolatedBandResultJsonSerializer,
    Periodic1DIsolatedBandScientificAdoption,
    Periodic1DIsolatedBandScientificAdoptionRequest,
    Periodic1DIsolatedBandScientificAdoptionResult,
)
from ksdft2effmass.periodic import PeriodicModelRole, PeriodicRetentionKind

pytestmark = pytest.mark.software_verification


class TestPeriodic1DIsolatedBandScientificAdoption:
    """Own typed replay-adoption and route-separation evidence."""

    @staticmethod
    def adopt() -> tuple[
        Periodic1DIsolatedBandScientificAdoptionRequest,
        Periodic1DIsolatedBandScientificAdoptionResult,
    ]:
        """Decode authenticated repository sources and execute scientific adoption."""
        repository_root = Path(__file__).resolve().parents[6]
        calculation_root = repository_root / (
            "calculations/research-monograph/periodic-1d"
        )
        input_payload = calculation_root.joinpath("input.json").read_bytes()
        result_payload = calculation_root.joinpath("result.json").read_bytes()
        definition = Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(
            input_payload
        )
        result = Periodic1DIsolatedBandResultJsonSerializer().deserialize(
            result_payload
        )
        replay = Periodic1DIsolatedBandReplayArtifactDecoder().execute(
            calculation_root.joinpath(
                "replay/isolated-band-v1/artifacts.json"
            ).read_bytes(),
            definition=definition,
            result=result,
            input_payload=input_payload,
            reference_result_payload=result_payload,
            producer_script_payload=calculation_root.joinpath(
                "run_experiment.py"
            ).read_bytes(),
            replay_script_payload=calculation_root.joinpath(
                "replay_isolated_band.py"
            ).read_bytes(),
        )
        request = Periodic1DIsolatedBandScientificAdoptionRequest(
            definition=definition,
            result=result,
            replay=replay,
        )
        return request, Periodic1DIsolatedBandScientificAdoption().execute(request)

    def test_method__execute__authenticates_replay_and_constructs_hierarchy(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-001.

        Requirement: The replay sidecar must authenticate its immutable sources and
        supply a typed frame representation for the selected lowest-band space.

        Acceptance: Exact retained-result replay is recorded; source, frame, and
        projector identities match the retained evidence; and parent, retention,
        subspace, and exact-operator identities remain distinct.
        """
        request, adoption = self.adopt()

        assert request.absolute_tolerance == (
            PERIODIC_1D_ISOLATED_BAND_DEFAULT_ABSOLUTE_TOLERANCE
        )
        assert request.replay.source_payload_sha256 == (
            "e02eaaeb6d93f31648294beb5b9f2288264fae4c86866f655b3d6b72669a01cb"
        )
        assert request.replay.source_correlation.exact_result_bytes_match
        assert request.replay.frame_content_sha256 == (
            "dc73eccef0c2761649b85a89a97c3adeff1e37c70ab0301691960934ea6b0215"
        )
        assert request.replay.projector_path_content_sha256 == (
            "331608c22b9de43d09e06adb9da9974319c5b4d2a89395c77dcec48ab761f74a"
        )
        assert adoption.parent_model.model_role is PeriodicModelRole.TOY
        assert adoption.selected_bands.retention.kind is (
            PeriodicRetentionKind.SELECTED_BANDS
        )
        assert adoption.represented_subspace.frame_path.rank == 1
        assert adoption.represented_subspace.frame_path.ambient_dimension == 23
        assert adoption.retained_operator.domain_id == (
            adoption.retained_operator.codomain_id
        )
        assert adoption.represented_zone_center_operator.retained_operator is (
            adoption.retained_operator
        )

    def test_method__execute__keeps_complete_truncated_and_fitted_routes_separate(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-002.

        Requirement: Complete representation, coefficient truncation, and direct
        least-squares fitting are separate numerical routes bound to one exact retained
        operator.

        Acceptance: The complete transform reconstructs the source under the documented
        default tolerance; every requested range is present; both approximate routes
        bind the same exact operator; and at range zero their coefficients differ.
        """
        request, adoption = self.adopt()

        assert adoption.complete_hopping.transform.reconstruction_passes
        assert (
            tuple(value.hopping_range_cells for value in adoption.effective_models)
            == request.definition.hopping_ranges
        )
        assert all(
            value.truncated.retained_operator is adoption.retained_operator
            and value.fitted.retained_operator is adoption.retained_operator
            for value in adoption.effective_models
        )
        first = adoption.effective_models[0]
        truncated = first.truncated.model.hopping_blocks[0].magnitude
        fitted = first.fitted.model.hopping_blocks[0].magnitude
        assert not np.array_equal(truncated, fitted)

    def test_method__execute__rejects_tampered_replay_source_correlation(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-003.

        Requirement: Replay artifacts cannot be adopted against different source bytes.

        Acceptance: One changed input byte is rejected before constructing scientific
        adoption results.
        """
        repository_root = Path(__file__).resolve().parents[6]
        calculation_root = repository_root / (
            "calculations/research-monograph/periodic-1d"
        )
        input_payload = calculation_root.joinpath("input.json").read_bytes()
        result_payload = calculation_root.joinpath("result.json").read_bytes()
        definition = Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(
            input_payload
        )
        result = Periodic1DIsolatedBandResultJsonSerializer().deserialize(
            result_payload
        )

        with pytest.raises(ValueError, match="input_sha256"):
            Periodic1DIsolatedBandReplayArtifactDecoder().execute(
                calculation_root.joinpath(
                    "replay/isolated-band-v1/artifacts.json"
                ).read_bytes(),
                definition=definition,
                result=result,
                input_payload=input_payload + b" ",
                reference_result_payload=result_payload,
                producer_script_payload=calculation_root.joinpath(
                    "run_experiment.py"
                ).read_bytes(),
                replay_script_payload=calculation_root.joinpath(
                    "replay_isolated_band.py"
                ).read_bytes(),
            )
