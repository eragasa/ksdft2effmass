"""Software verification for retained-subspace identity construction.

Evidence profile: routine

Bounded artifact scope: ``PeriodicRetainedSubspaceConstructor`` identity, dimension,
and immutability contract.

Facet and represented meaning
-----------------------------
The module verifies the public construction route from a stable parent-operator
reference and retention definition to an immutable retained mathematical space.

Intrinsic and cross-object scope
--------------------------------
Exact identity, tuple ordering, rank, ambient dimension, and parent-space agreement
are checked against the documented public contract.

VVUQ and scientific exclusions
------------------------------
These synthetic tests establish software behavior only. They do not verify a
projector, validate a selected subspace, or establish gauge smoothness or physical
adequacy.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetainedSubspace,
    PeriodicRetainedSubspaceConstructor,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicRetainedSubspaceConstructor:
    """Verify exact parent-qualified retained-space construction."""

    @staticmethod
    def make_parent() -> PeriodicOperatorReference:
        """Return one synthetic one-dimensional parent reference."""
        return PeriodicOperatorReference(
            model_id="test.periodic.parent",
            operator_id="test.periodic.parent.hamiltonian",
            state_space_id="test.periodic.parent.space",
            spatial_dimension=1,
        )

    @classmethod
    def make_definition(cls) -> PeriodicRetentionDefinition:
        """Return one synthetic rank-two selected-band definition."""
        return PeriodicRetentionDefinition(
            retention_id="test.retention.selected-bands",
            parent_operator=cls.make_parent(),
            retained_space_id="test.retained.space",
            kind=PeriodicRetentionKind.SELECTED_BANDS,
            rank=2,
            ordered_state_labels=("band-0", "band-1"),
            reciprocal_domain_id="test.reciprocal.mesh",
            construction_record_id="test.band-selection",
            assumption_ids=("test.assumption.isolation",),
            provenance_id="test.provenance.retention-definition",
        )

    @classmethod
    def construct(cls) -> PeriodicRetainedSubspace:
        """Construct the valid synthetic retained space through its ActionObject."""
        return PeriodicRetainedSubspaceConstructor().execute(
            definition=cls.make_definition(),
            ambient_state_space_id="test.periodic.parent.space",
            ambient_dimension=4,
            spin_convention="spinless",
            internal_degree_convention="ordered bands",
            reciprocal_boundary_convention="periodic sewing",
            provenance_id="test.provenance.retained-space",
        )

    def test_method__execute__propagates_exact_identity_and_rank(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-SUBSPACE-001

        Requirement: Retained-space construction preserves exact parent, space, rank,
        ordering, and dimension identity.

        Acceptance: Every inspected field equals the independently declared input.
        """
        subspace = self.construct()

        assert subspace.retained_space_id == "test.retained.space"
        assert subspace.rank == 2
        assert subspace.spatial_dimension == 1
        assert subspace.ambient_dimension == 4
        assert subspace.definition.parent_operator == self.make_parent()
        assert subspace.definition.ordered_state_labels == ("band-0", "band-1")

    def test_construction__definition__rejects_boolean_rank(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-SUBSPACE-002

        Requirement: Retained rank requires an exact built-in integer.

        Acceptance: Boolean rank construction raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="rank must be a built-in int"):
            PeriodicRetentionDefinition(
                retention_id="test.retention.invalid-rank",
                parent_operator=self.make_parent(),
                retained_space_id="test.retained.space",
                kind=PeriodicRetentionKind.SELECTED_BANDS,
                rank=True,
                ordered_state_labels=("band-0",),
                reciprocal_domain_id="test.reciprocal.mesh",
                construction_record_id="test.band-selection",
                assumption_ids=(),
                provenance_id="test.provenance",
            )

    def test_construction__definition__rejects_rank_label_disagreement(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-SUBSPACE-003

        Requirement: Ordered retained labels supply exactly one identity per rank.

        Acceptance: A label-count mismatch raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="length must equal rank"):
            PeriodicRetentionDefinition(
                retention_id="test.retention.invalid-label-count",
                parent_operator=self.make_parent(),
                retained_space_id="test.retained.space",
                kind=PeriodicRetentionKind.SELECTED_BANDS,
                rank=2,
                ordered_state_labels=("band-0",),
                reciprocal_domain_id="test.reciprocal.mesh",
                construction_record_id="test.band-selection",
                assumption_ids=(),
                provenance_id="test.provenance",
            )

    def test_method__execute__rejects_mismatched_ambient_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-SUBSPACE-004

        Requirement: Retained and parent ambient state-space identities agree exactly.

        Acceptance: A different ambient identity raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="identity must match parent"):
            PeriodicRetainedSubspaceConstructor().execute(
                definition=self.make_definition(),
                ambient_state_space_id="test.different.space",
                ambient_dimension=4,
                spin_convention="spinless",
                internal_degree_convention="ordered bands",
                reciprocal_boundary_convention="periodic sewing",
                provenance_id="test.provenance.retained-space",
            )

    def test_method__execute__rejects_rank_larger_than_ambient_space(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-SUBSPACE-005

        Requirement: Retained rank cannot exceed represented ambient dimension.

        Acceptance: Rank larger than ambient dimension raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="must not exceed ambient dimension"):
            PeriodicRetainedSubspaceConstructor().execute(
                definition=self.make_definition(),
                ambient_state_space_id="test.periodic.parent.space",
                ambient_dimension=1,
                spin_convention="spinless",
                internal_degree_convention="ordered bands",
                reciprocal_boundary_convention="periodic sewing",
                provenance_id="test.provenance.retained-space",
            )

    def test_construction__result__is_frozen(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-SUBSPACE-006

        Requirement: Constructed retained-space state is operationally immutable.

        Acceptance: Public field assignment raises ``FrozenInstanceError``.
        """
        subspace = self.construct()

        with pytest.raises(FrozenInstanceError):
            subspace.ambient_dimension = 8  # type: ignore[misc]
