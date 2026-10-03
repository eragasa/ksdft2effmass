"""Software verification of ``Periodic1DSelectedBandRetentionDefinition``.

Evidence profile: routine

Bounded artifact scope: one-dimensional parent-qualified composition of one reusable
contiguous parent-band selection.

Facet and represented meaning
-----------------------------
The DataObject binds ordered parent-band indices to the general scientific-retention
definition without constructing a retained subspace.

Intrinsic and cross-object scope
--------------------------------
Exact public imports, one-dimensional parentage, selected-band kind, rank agreement,
and retained ordering are covered.

VVUQ and scientific exclusions
------------------------------
Inputs are synthetic test data. These tests do not establish band isolation, numerical
projection, physical adequacy, scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

import pytest

import ksdft2effmass.periodic1d as periodic1d_api
from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import Periodic1DSelectedBandRetentionDefinition

pytestmark = pytest.mark.software_verification


class TestPeriodic1DSelectedBandRetentionDefinition:
    """Own software evidence for parent-qualified contiguous-band retention."""

    @staticmethod
    def make_retention(
        *,
        spatial_dimension: int = 1,
        kind: PeriodicRetentionKind = PeriodicRetentionKind.SELECTED_BANDS,
        rank: int = 2,
    ) -> PeriodicRetentionDefinition:
        """Return one synthetic general retention definition for consuming cases."""
        return PeriodicRetentionDefinition(
            retention_id="test.periodic1d.valence-group",
            parent_operator=PeriodicOperatorReference(
                model_id="test.periodic1d.parent",
                operator_id="test.periodic1d.parent.hamiltonian",
                state_space_id="test.periodic1d.parent.bloch-space",
                spatial_dimension=spatial_dimension,  # type: ignore[arg-type]
            ),
            retained_space_id="test.periodic1d.valence-space",
            kind=kind,
            rank=rank,
            ordered_state_labels=tuple(f"valence-{index}" for index in range(rank)),
            reciprocal_domain_id="test.periodic1d.centered-mesh",
            construction_record_id="test.periodic1d.band-selection",
            assumption_ids=("test.periodic1d.band-ordering",),
            provenance_id="test.periodic1d.retention-provenance",
        )

    def test_construction__fields__binds_parent_selection_and_order(self) -> None:
        """Evidence ID: SV-PERIODIC1D-RETENTION-001

        Requirement: The one-dimensional definition preserves the general retention
        owner and contiguous band selection in ascending retained-state order.

        Acceptance: Exact fields are retained and indices equal ``(2, 3)``.
        """
        retention = self.make_retention()
        selection = ContiguousBandSelection(2, 3)

        definition = Periodic1DSelectedBandRetentionDefinition(retention, selection)

        assert definition.retention is retention
        assert definition.selection is selection
        assert definition.band_indices == (2, 3)
        assert tuple(
            zip(
                definition.band_indices,
                definition.retention.ordered_state_labels,
                strict=True,
            )
        ) == ((2, "valence-0"), (3, "valence-1"))

    def test_construction__parent__rejects_non_one_dimensional_reference(self) -> None:
        """Evidence ID: SV-PERIODIC1D-RETENTION-002

        Requirement: The specialized retention definition accepts only a 1D parent.

        Acceptance: A dimension-two parent raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="parent must be one-dimensional"):
            Periodic1DSelectedBandRetentionDefinition(
                self.make_retention(spatial_dimension=2),
                ContiguousBandSelection(2, 3),
            )

    def test_construction__kind__rejects_non_band_retention(self) -> None:
        """Evidence ID: SV-PERIODIC1D-RETENTION-003

        Requirement: The aggregate represents selected-band retention only.

        Acceptance: A spectral-restriction kind raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="kind must be selected bands"):
            Periodic1DSelectedBandRetentionDefinition(
                self.make_retention(kind=PeriodicRetentionKind.SPECTRAL_RESTRICTION),
                ContiguousBandSelection(2, 3),
            )

    def test_construction__rank__rejects_selection_count_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC1D-RETENTION-004

        Requirement: General retained rank equals contiguous selected-band count.

        Acceptance: Rank two with a three-band interval raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="rank must equal selected band count"):
            Periodic1DSelectedBandRetentionDefinition(
                self.make_retention(rank=2),
                ContiguousBandSelection(2, 4),
            )

    def test_public_api__package__exports_only_supported_definition(self) -> None:
        """Evidence ID: SV-PERIODIC1D-RETENTION-005

        Requirement: The canonical periodic1d route exposes the accepted scientific
        models, finite parent representation, and selected-band retention definitions.

        Acceptance: ``__all__`` and the retained-definition binding equal the declared
        inventory.
        """
        assert periodic1d_api.__all__ == [
            "Periodic1DBandFrameRetainedSubspace",
            "Periodic1DCompleteHoppingRepresentationResult",
            "Periodic1DFiniteHoppingToyModel",
            "Periodic1DFittedHoppingEffectiveModelResult",
            "Periodic1DFourierHamiltonianToyModel",
            "Periodic1DHoppingBlock",
            "Periodic1DOrthogonalSpectralRetainedSubspace",
            "Periodic1DPlaneWaveParentRepresentation",
            "Periodic1DPlaneWaveParentRepresentationConstructor",
            "Periodic1DRetainedBandGroupDefinition",
            "Periodic1DSelectedBandRetentionDefinition",
            "Periodic1DTruncatedHoppingEffectiveModelResult",
        ]
        assert (
            periodic1d_api.Periodic1DSelectedBandRetentionDefinition
            is Periodic1DSelectedBandRetentionDefinition
        )
