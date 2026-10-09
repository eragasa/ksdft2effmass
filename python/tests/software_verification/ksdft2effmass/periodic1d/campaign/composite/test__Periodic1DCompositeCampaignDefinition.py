r"""Intrinsic software verification of the composite campaign definition.

Evidence profile: routine

The tests use synthetic schema-one bytes and exercise immutable definition invariants.
They read no retained artifact and establish no numerical or scientific claim.
"""

import json
from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeCampaignDefinition


class TestPeriodic1DCompositeCampaignDefinition:
    """Own intrinsic representation and finite-parent executability evidence."""

    @staticmethod
    def _definition() -> Periodic1DCompositeCampaignDefinition:
        """Decode a compact synthetic schema-one definition."""
        payload = {
            "schema_version": 1,
            "experiment_id": "synthetic.composite.v1",
            "evidence_status": "illustrative numerical verification",
            "period": 1.0,
            "potential_strength_over_recoil": 0.25,
            "plane_wave_cutoff": 2,
            "reciprocal_mesh_size": 8,
            "withheld_mesh_size": 9,
            "retained_band_groups": [{"id": "pair", "band_indices": [0, 1]}],
            "hopping_ranges_cells": [1, 2],
            "external_gap_threshold": 0.01,
            "direct_route_range_cells": 1,
            "controlled_gauge_amplitude": 0.1,
            "rough_gauge_amplitude": 0.2,
        }
        wire = (json.dumps(payload, separators=(",", ":")) + "\n").encode()
        return Periodic1DCompositeCampaignJsonSerializer().deserialize(wire)

    def test_contract__canonical_owner_and_no_forwarding_methods(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-001.

        Requirement: The definition and serializer have canonical composite ownership,
        and the serializer exposes only the reviewed ``serialize``/``deserialize``
        contract rather than compatibility forwarding methods.

        Acceptance: Defining modules are canonical and ``encode``/``decode`` are absent.

        Limitations: Import ownership does not establish retained-wire provenance or
        decoded scientific correctness.
        """
        serializer = Periodic1DCompositeCampaignJsonSerializer()

        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.composite.definition"
        )
        assert type(serializer).__module__ == SUT.__module__
        assert not hasattr(serializer, "encode")
        assert not hasattr(serializer, "decode")

    def test_construction__separates_wrong_identity_type_from_empty_value(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-002.

        Requirement: Exact representation failures and invalid identity values use
        distinct exception categories without coercion.

        Acceptance: A numeric identity raises ``TypeError`` and an empty identity raises
        ``ValueError``.

        Limitations: This intrinsic test does not authenticate a historical experiment.
        """
        definition = self._definition()

        with pytest.raises(TypeError, match="experiment_id must be a built-in str"):
            replace(definition, experiment_id=1)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="experiment_id must be nonempty"):
            replace(definition, experiment_id="")

    @pytest.mark.parametrize("reciprocal_mesh_size", [1, 3])
    def test_construction__mesh_must_support_canonical_adoption(
        self, reciprocal_mesh_size: int
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-003.

        Requirement: Every intrinsically valid composite definition supplies the
        nontrivial even reciprocal mesh required by canonical scientific adoption.

        Acceptance: One-point and odd reciprocal meshes fail during definition
        construction rather than at the later adoption boundary.

        Limitations: Mesh executability does not establish sampling convergence or
        scientific adequacy.
        """
        with pytest.raises(ValueError, match="must be an even integer"):
            replace(self._definition(), reciprocal_mesh_size=reciprocal_mesh_size)

    def test_construction__retained_groups_must_match_declared_parent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-005.

        Requirement: Each retained-band group explicitly references the definition's
        declared untruncated parent operator and reciprocal domain.

        Acceptance: A foreign parent-operator identity and a foreign reciprocal-domain
        identity are rejected before execution or adoption.

        Limitations: Identity agreement does not prove projector coordinates, retained
        space adequacy, parent convergence, or scientific validation.
        """
        definition = self._definition()
        group = definition.retained_band_groups[0]
        retention = group.retained_bands.retention
        foreign_parent = replace(
            group,
            retained_bands=replace(
                group.retained_bands,
                retention=replace(
                    retention,
                    parent_operator=replace(
                        retention.parent_operator,
                        model_id="foreign.parent",
                    ),
                ),
            ),
        )
        with pytest.raises(ValueError, match="declared untruncated parent operator"):
            replace(definition, retained_band_groups=(foreign_parent,))

        foreign_domain = replace(
            group,
            retained_bands=replace(
                group.retained_bands,
                retention=replace(
                    retention,
                    reciprocal_domain_id="foreign.reciprocal-domain",
                ),
            ),
        )
        with pytest.raises(ValueError, match="declared parent reciprocal domain"):
            replace(definition, retained_band_groups=(foreign_domain,))

    def test_construction__retained_indices_must_fit_finite_parent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-006.

        Requirement: Every retained band selected by a valid campaign definition fits
        the declared finite plane-wave parent representation.

        Acceptance: Reducing cutoff one below the represented band inventory fails
        before campaign execution or scientific adoption.

        Limitations: Passing the dimension check does not establish parent convergence,
        isolation, retention adequacy, or scientific validation.
        """
        definition = self._definition()
        high_group = replace(
            definition.retained_band_groups[0],
            retained_bands=replace(
                definition.retained_band_groups[0].retained_bands,
                selection=replace(
                    definition.retained_band_groups[0].retained_bands.selection,
                    lower_index=2,
                    upper_index=3,
                ),
            ),
        )

        with pytest.raises(
            ValueError, match="retained band indices must fit the finite parent"
        ):
            replace(
                definition,
                plane_wave_cutoff=1,
                retained_band_groups=(high_group,),
            )
