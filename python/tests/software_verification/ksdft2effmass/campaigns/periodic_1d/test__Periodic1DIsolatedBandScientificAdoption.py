r"""Software verification of periodic-1D isolated-band replay adoption.

Evidence profile: claim_bearing

Bounded artifact scope: the authorized deterministic replay sidecar, typed scientific
hierarchy, and complete, truncated, and fitted coefficient routes.

Scientific exclusions: passing establishes source authentication and software/numerical
reproducibility only. It does not establish material relevance, scientific validation,
uncertainty quantification, or acceptance of the effective models.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic_1d import (
    Periodic1DIsolatedBandCampaignJsonSerializer,
    Periodic1DIsolatedBandReplayArtifactDecoder,
    Periodic1DIsolatedBandResultJsonSerializer,
    Periodic1DIsolatedBandScientificAdoption,
    Periodic1DIsolatedBandScientificAdoptionRequest,
    Periodic1DIsolatedBandScientificAdoptionResult,
)
from ksdft2effmass.operators import ScalarQuantity
from ksdft2effmass.periodic import PeriodicModelRole, PeriodicRetentionKind

pytestmark = pytest.mark.software_verification

REPRESENTED_PLANE_WAVE_CUTOFF = 11
REPRESENTED_AMBIENT_DIMENSION = 23
REPRESENTED_RECIPROCAL_MESH_SIZE = 64
REFERENCE_PLANE_WAVE_CUTOFF = 15
COMPARED_PARENT_BAND_COUNT = 3
RETAINED_CUTOFF_OBSERVATION = 2.954581024283698e-14


class TestPeriodic1DIsolatedBandScientificAdoption:
    """Own typed replay-adoption and route-separation evidence."""

    @staticmethod
    def adopt(
        absolute_tolerance: float | None = None,
    ) -> tuple[
        Periodic1DIsolatedBandScientificAdoptionRequest,
        Periodic1DIsolatedBandScientificAdoptionResult,
    ]:
        """Decode authenticated sources and execute scientific adoption."""
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
            absolute_tolerance=absolute_tolerance,
        )
        return request, Periodic1DIsolatedBandScientificAdoption().execute(request)

    def test_method__execute__authenticates_replay_and_constructs_hierarchy(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-001.

        Requirement: The replay sidecar must authenticate its immutable sources and
        supply a typed frame representation for the selected lowest-band space.

        Acceptance: Exact retained-result replay is recorded; source, frame, and
        projector identities match the retained evidence; and untruncated parent,
        finite parent representation, retained space, and finite-parent retained
        operator identities remain distinct.
        """
        request, adoption = self.adopt()

        assert request.absolute_tolerance is None
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
        assert adoption.parent_representation.parent_model is adoption.parent_model
        assert request.definition.plane_wave_cutoffs[-1] == (
            REPRESENTED_PLANE_WAVE_CUTOFF
        )
        assert adoption.parent_representation.cutoff == REPRESENTED_PLANE_WAVE_CUTOFF
        assert adoption.parent_representation.ambient_dimension == (
            REPRESENTED_AMBIENT_DIMENSION
        )
        assert adoption.parent_representation.reciprocal_mesh.point_count == (
            REPRESENTED_RECIPROCAL_MESH_SIZE
        )
        assert adoption.parent_model.state_space_id != (
            adoption.parent_representation.represented_operator.state_space_id
        )
        assert adoption.parent_discretization.representation is (
            adoption.parent_representation
        )
        assert request.definition.plane_wave_reference_cutoff == (
            REFERENCE_PLANE_WAVE_CUTOFF
        )
        assert adoption.parent_discretization.reference_basis.cutoff == (
            REFERENCE_PLANE_WAVE_CUTOFF
        )
        assert adoption.parent_discretization.compared_band_count == (
            COMPARED_PARENT_BAND_COUNT
        )
        assert np.array_equal(
            adoption.parent_discretization.comparison_momenta.magnitude,
            request.definition.parent_sample_momenta.magnitude,
        )
        assert (
            adoption.parent_discretization.cutoff_observation
            == (request.result.parent_verification.plane_wave_cutoff_study[-1])
        )
        assert (
            adoption.parent_discretization.cutoff_observation.maximum_first_bands_absolute_error
            == RETAINED_CUTOFF_OBSERVATION
        )
        assert adoption.selected_bands.retention.kind is (
            PeriodicRetentionKind.SELECTED_BANDS
        )
        assert adoption.selected_bands.retention.parent_operator is (
            adoption.parent_representation.represented_operator
        )
        assert adoption.represented_subspace.frame_path.rank == 1
        assert adoption.represented_subspace.frame_path.ambient_dimension == (
            REPRESENTED_AMBIENT_DIMENSION
        )
        assert adoption.retained_subspace.ambient_state_space_id == (
            adoption.parent_representation.represented_operator.state_space_id
        )
        assert adoption.retained_subspace.ambient_dimension == (
            REPRESENTED_AMBIENT_DIMENSION
        )
        assert adoption.retained_operator.parent_operator is (
            adoption.parent_representation.represented_operator
        )
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

        Acceptance: The complete transform reconstructs the source under a retained
        calculated tolerance; every requested range is present; both approximate
        routes bind the same exact operator; and at range zero their coefficients
        differ.
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

    def test_init__rejects_contradictory_effective_model_ranges(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-008.

        Requirement: Each effective-model adoption must correlate its declared range
        with both numerical routes, and the aggregate must retain unique increasing
        ranges.

        Acceptance: Independent contradictions in truncation range, truncated
        representatives, fitted representatives, duplicate ranges, and range order
        each raise ``ValueError``.
        """
        _, adoption = self.adopt()
        range_zero = adoption.effective_models[0]
        range_one = adoption.effective_models[1]

        with pytest.raises(ValueError, match="maximum_range must match"):
            replace(range_zero, hopping_range_cells=1)

        asymmetric_source = range_zero.truncated.model
        asymmetric_truncation = replace(
            range_zero.truncated.truncation,
            source=asymmetric_source,
            maximum_range=1,
            truncated=asymmetric_source,
            omitted_block_l2_norm=0.0,
        )
        with pytest.raises(ValueError, match="truncated representatives must match"):
            replace(
                range_zero,
                hopping_range_cells=1,
                truncated=replace(
                    range_zero.truncated,
                    truncation=asymmetric_truncation,
                ),
            )

        with pytest.raises(ValueError, match="fitted representatives must match"):
            replace(range_one, fitted=range_zero.fitted)
        with pytest.raises(ValueError, match="unique and increasing"):
            replace(adoption, effective_models=(range_zero, range_zero))
        with pytest.raises(ValueError, match="unique and increasing"):
            replace(
                adoption, effective_models=tuple(reversed(adoption.effective_models))
            )

    def test_method__execute__calculates_and_retains_distinct_route_tolerances(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-003.

        Requirement: ``None`` must calculate coordinate- and energy-valued allowances
        independently and retain every allowance with its route comparison.

        Acceptance: Each allowance equals binary64 epsilon times its comparison
        dimension times the greater of one and the applicable reference norm.
        """
        request, adoption = self.adopt()
        samples = request.result.reduction.reciprocal_samples
        epsilon = np.finfo(np.float64).eps
        coordinate_scale = max(
            1.0,
            abs(samples.reciprocal_period.magnitude),
            float(np.max(np.abs(samples.coordinates.magnitude))),
        )
        reconstruction_scale = max(
            float(np.linalg.norm(value.magnitude)) for value in samples.matrices
        )

        assert adoption.complete_hopping.transform.coordinate_absolute_tolerance == (
            epsilon * samples.coordinates.magnitude.size * coordinate_scale
        )
        assert (
            adoption.complete_hopping.transform.reconstruction_absolute_tolerance
            == epsilon * len(samples.matrices) * max(1.0, reconstruction_scale)
        )
        complete_scale = float(
            np.sqrt(
                sum(
                    np.linalg.norm(block.magnitude) ** 2
                    for block in request.replay.complete_hopping_model.hopping_blocks
                )
            )
        )
        assert adoption.complete_coefficient_absolute_tolerance == (
            epsilon
            * len(request.replay.complete_hopping_model.hopping_blocks)
            * max(1.0, complete_scale)
        )
        assert adoption.complete_replay_comparison.candidate is (
            adoption.complete_hopping.transform.hopping_model
        )
        for adopted, replayed in zip(
            adoption.effective_models,
            request.replay.range_artifacts,
            strict=True,
        ):
            for tolerance, comparison, model, candidate in (
                (
                    adopted.truncation_coefficient_absolute_tolerance,
                    adopted.truncation_replay_comparison,
                    replayed.truncated_model,
                    adopted.truncated.model,
                ),
                (
                    adopted.fitting_coefficient_absolute_tolerance,
                    adopted.fitting_replay_comparison,
                    replayed.fitted_model,
                    adopted.fitted.model,
                ),
            ):
                scale = float(
                    np.sqrt(
                        sum(
                            np.linalg.norm(block.magnitude) ** 2
                            for block in model.hopping_blocks
                        )
                    )
                )
                assert tolerance == (
                    epsilon * len(model.hopping_blocks) * max(1.0, scale)
                )
                assert comparison.candidate is candidate
                assert comparison.coefficient_l2_frobenius_defect.magnitude <= (
                    tolerance
                )

    def test_method__execute__honors_explicit_energy_tolerance_only(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-004.

        Requirement: A caller-supplied tolerance applies to energy-valued comparisons
        without replacing the independently calculated coordinate allowance.

        Acceptance: Reconstruction and every coefficient route retain the supplied
        value while the coordinate allowance remains dimension-scaled binary64.
        """
        requested = 1.0e-10
        _, adoption = self.adopt(requested)

        assert (
            adoption.complete_hopping.transform.reconstruction_absolute_tolerance
            == requested
        )
        assert adoption.complete_coefficient_absolute_tolerance == requested
        assert all(
            value.truncation_coefficient_absolute_tolerance == requested
            and value.fitting_coefficient_absolute_tolerance == requested
            for value in adoption.effective_models
        )
        assert (
            adoption.complete_hopping.transform.coordinate_absolute_tolerance
            != requested
        )

    def test_init__rejects_invalid_optional_absolute_tolerances(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-005.

        Requirement: The public optional scalar contract rejects booleans, integers,
        numeric strings, nonfinite values, and negative values.

        Acceptance: Wrong scalar types raise ``TypeError`` and invalid built-in floats
        raise ``ValueError`` before adoption executes.
        """
        request, _ = self.adopt()

        for invalid_type in (True, 1, "1e-10"):
            with pytest.raises(TypeError, match="built-in float or None"):
                Periodic1DIsolatedBandScientificAdoptionRequest(
                    definition=request.definition,
                    result=request.result,
                    replay=request.replay,
                    absolute_tolerance=invalid_type,  # type: ignore[arg-type]
                )
        for invalid_value in (-1.0, float("inf"), float("nan")):
            with pytest.raises(ValueError, match="finite and nonnegative"):
                Periodic1DIsolatedBandScientificAdoptionRequest(
                    definition=request.definition,
                    result=request.result,
                    replay=request.replay,
                    absolute_tolerance=invalid_value,
                )

    def test_init__rejects_same_identifier_source_substitution(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-006.

        Requirement: Adoption must reuse the exact immutable definition and result
        objects authenticated by the replay decoder, not replacements that merely
        share the experiment identifier.

        Acceptance: A changed same-identifier definition and a newly constructed
        same-identifier result are both rejected before adoption executes.
        """
        request, _ = self.adopt()
        replacement_definition = replace(
            request.definition,
            potential_strength=ScalarQuantity(
                request.definition.potential_strength.magnitude + 0.1,
                request.definition.potential_strength.unit,
            ),
        )
        replacement_result = replace(request.result)

        with pytest.raises(ValueError, match="replay-authenticated object"):
            replace(request, definition=replacement_definition)
        with pytest.raises(ValueError, match="replay-authenticated object"):
            replace(request, result=replacement_result)

    def test_method__execute__rejects_tampered_replay_source_correlation(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-REPLAY-007.

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
