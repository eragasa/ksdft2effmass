"""Software verification of ``Periodic2DSelectedBandRetentionDefinition``.

Evidence profile: routine

Bounded artifact scope: two-dimensional parent-qualified composition of one reusable
contiguous parent-band selection.

Facet and represented meaning
-----------------------------
The immutable DataObject binds ordered parent-band indices to the general scientific-
retention definition without constructing a retained subspace or operator.

Intrinsic and cross-object scope
--------------------------------
Exact public types, two-dimensional parentage, selected-band construction kind, rank
agreement, retained ordering, immutability, and deliberate public export are covered.

VVUQ and scientific exclusions
------------------------------
Inputs are synthetic test data. These tests do not establish band isolation, numerical
projection, physical adequacy, scientific validation, uncertainty quantification, or
relationships among parent-model, discretization, and model-reduction errors.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

import ksdft2effmass.periodic2d as periodic2d_api
from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic2d import Periodic2DSelectedBandRetentionDefinition

pytestmark = pytest.mark.software_verification


class TestPeriodic2DSelectedBandRetentionDefinition:
    """Own software evidence for parent-qualified 2D band retention."""

    @staticmethod
    def make_retention(
        *,
        spatial_dimension: int = 2,
        kind: PeriodicRetentionKind = PeriodicRetentionKind.SELECTED_BANDS,
        rank: int = 2,
    ) -> PeriodicRetentionDefinition:
        """Return one synthetic general retention definition for consuming cases."""
        return PeriodicRetentionDefinition(
            retention_id="test.periodic2d.valence-group",
            parent_operator=PeriodicOperatorReference(
                model_id="test.periodic2d.parent",
                operator_id="test.periodic2d.parent.hamiltonian",
                state_space_id="test.periodic2d.parent.bloch-space",
                spatial_dimension=spatial_dimension,  # type: ignore[arg-type]
            ),
            retained_space_id="test.periodic2d.valence-space",
            kind=kind,
            rank=rank,
            ordered_state_labels=tuple(f"valence-{index}" for index in range(rank)),
            reciprocal_domain_id="test.periodic2d.centered-mesh",
            construction_record_id="test.periodic2d.band-selection",
            assumption_ids=("test.periodic2d.band-ordering",),
            provenance_id="test.periodic2d.retention-provenance",
        )

    def test_construction__fields__binds_parent_selection_and_order(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-001.

        Requirement: The definition preserves its general retention owner and
        contiguous selection in ascending retained-state order.

        Acceptance: Exact fields are retained and indices equal ``(2, 3)``.
        """
        retention = self.make_retention()
        selection = ContiguousBandSelection(2, 3)

        definition = Periodic2DSelectedBandRetentionDefinition(retention, selection)

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

    def test_construction__types__rejects_semantic_substitutes(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-002.

        Requirement: Only exact public DataObject types cross this boundary.

        Acceptance: String and tuple substitutes raise ``TypeError``.
        """
        with pytest.raises(
            TypeError, match="retention must be PeriodicRetentionDefinition"
        ):
            Periodic2DSelectedBandRetentionDefinition(
                "not-retention",  # type: ignore[arg-type]
                ContiguousBandSelection(2, 3),
            )
        with pytest.raises(
            TypeError, match="selection must be ContiguousBandSelection"
        ):
            Periodic2DSelectedBandRetentionDefinition(
                self.make_retention(),
                (2, 3),  # type: ignore[arg-type]
            )

    def test_construction__parent__rejects_non_two_dimensional_reference(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-003.

        Requirement: The specialized retention definition accepts only a 2D parent.

        Acceptance: A dimension-one parent raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="parent must be two-dimensional"):
            Periodic2DSelectedBandRetentionDefinition(
                self.make_retention(spatial_dimension=1),
                ContiguousBandSelection(2, 3),
            )

    def test_construction__kind__rejects_non_band_retention(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-004.

        Requirement: The aggregate represents selected-band retention only.

        Acceptance: A spectral-restriction kind raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="kind must be selected bands"):
            Periodic2DSelectedBandRetentionDefinition(
                self.make_retention(kind=PeriodicRetentionKind.SPECTRAL_RESTRICTION),
                ContiguousBandSelection(2, 3),
            )

    def test_construction__rank__rejects_selection_count_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-005.

        Requirement: General retained rank equals contiguous selected-band count.

        Acceptance: Rank two with a three-band interval raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="rank must equal selected band count"):
            Periodic2DSelectedBandRetentionDefinition(
                self.make_retention(rank=2),
                ContiguousBandSelection(2, 4),
            )

    def test_data_object__mutation__is_rejected(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-006.

        Requirement: Maintained scientific definitions are operationally immutable.

        Acceptance: Field reassignment raises ``FrozenInstanceError``.
        """
        definition = Periodic2DSelectedBandRetentionDefinition(
            self.make_retention(), ContiguousBandSelection(2, 3)
        )

        with pytest.raises(FrozenInstanceError):
            definition.selection = ContiguousBandSelection(0, 1)  # type: ignore[misc]

    def test_public_api__package__exports_supported_definition(self) -> None:
        """Evidence ID: SV-PERIODIC2D-RETENTION-007.

        Requirement: The canonical periodic2d route deliberately exports the accepted
        selected-band retention definition.

        Acceptance: ``__all__`` contains the name and the binding is exact.
        """
        assert "Periodic2DSelectedBandRetentionDefinition" in periodic2d_api.__all__
        assert (
            periodic2d_api.Periodic2DSelectedBandRetentionDefinition
            is Periodic2DSelectedBandRetentionDefinition
        )
