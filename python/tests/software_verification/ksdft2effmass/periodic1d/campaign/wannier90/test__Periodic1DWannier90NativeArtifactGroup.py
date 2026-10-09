r"""Class-owned software verification of explicit Wannier90 artifact groups.

Evidence profile: routine

Bounded scope
-------------
The intrinsic field, ordering, member-type, unique-name, and immutability contract of
``Periodic1DWannier90NativeArtifactGroup`` using synthetic named byte payloads only.

Ownership and scientific exclusions
-----------------------------------
The SUT owns an explicit correlation key and caller-supplied native artifact records. It
owns no encoded campaign document, repository path, parser result, retained operator,
or scientific disposition. These tests perform no filesystem discovery, invoke no
calculator, and establish no retained native-file identity, execution provenance,
localization convergence, scientific validity, uncertainty quantification, or
acceptance.
"""

from dataclasses import FrozenInstanceError, fields
from typing import get_type_hints

import pytest

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact
from ksdft2effmass.periodic1d.campaign.wannier90.native_artifacts import (
    Periodic1DWannier90NativeArtifactGroup,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90NativeArtifactGroup


class TestPeriodic1DWannier90NativeArtifactGroup:
    """Own intrinsic row-040 native-artifact-group contract evidence."""

    def test_contract__owns_group_identity_and_ordered_artifacts(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-NATIVE-001.

        Requirement: The group owns exactly one explicit string key and one ordered,
        nonempty tuple of exact native-artifact values.

        Method: Inspect dataclass fields and construct a group from two distinct
        synthetic native records, including one valid empty payload.

        Oracle: The documented field inventory, defining module, tuple order, and Python
        object identity.

        Acceptance: Names, field order, defining owner, tuple order, and retained member
        identities match exactly.

        Interpretation: A pass establishes the intrinsic native side of the row-040
        ownership split.

        Limitations: Synthetic names and bytes establish no retained-file identity,
        parser compatibility, result correlation, or provenance.
        """
        first = Wannier90NativeArtifact("synthetic.win", b"")
        second = Wannier90NativeArtifact("synthetic.eig", b"synthetic eigenvalues")
        artifacts = (first, second)
        group = SUT("synthetic-group", artifacts)

        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.wannier90.native_artifacts"
        )
        type_hints = get_type_hints(SUT)
        assert [(field.name, type_hints[field.name]) for field in fields(SUT)] == [
            ("group_id", str),
            ("artifacts", tuple[Wannier90NativeArtifact, ...]),
        ]
        assert group.group_id == "synthetic-group"
        assert group.artifacts is artifacts
        assert group.artifacts[0] is first
        assert group.artifacts[1] is second

    def test_construction__rejects_invalid_identity_inventory_and_names(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-NATIVE-002.

        Requirement: Group identity is a nonempty exact string; artifacts form a
        nonempty tuple of exact native records with unique logical names.

        Method: Exercise wrong, subtype, and empty identities; wrong and empty
        inventories; a wrong member type and exact-record subtype; and duplicate
        logical names.

        Oracle: The documented group and inventory exception contract.

        Acceptance: Identity and duplicate-name failures raise ``ValueError``;
        inventory-representation and member-type failures raise ``TypeError``.

        Interpretation: A pass establishes fail-closed, unambiguous native inventory
        construction.

        Limitations: Unique logical names do not prove completeness or agreement with a
        retained result's expected artifact identities.
        """

        class GroupIdSubclass(str):
            """Provide a string subtype that violates the exact key contract."""

        class NativeArtifactSubclass(Wannier90NativeArtifact):
            """Provide a native-record subtype that violates exact membership."""

        artifact = Wannier90NativeArtifact("synthetic.win", b"")
        with pytest.raises(ValueError, match="group_id must be"):
            SUT(1, (artifact,))  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="group_id must be"):
            SUT(GroupIdSubclass("group"), (artifact,))
        with pytest.raises(ValueError, match="group_id must be"):
            SUT("", (artifact,))
        with pytest.raises(TypeError, match="artifacts must be"):
            SUT("group", [artifact])  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="artifacts must be"):
            SUT("group", ())
        with pytest.raises(TypeError, match="artifacts must be"):
            SUT("group", (b"not an artifact",))  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="artifacts must be"):
            SUT("group", (NativeArtifactSubclass("synthetic.win", b""),))
        duplicate = Wannier90NativeArtifact("synthetic.win", b"other bytes")
        with pytest.raises(ValueError, match="native artifact names must be unique"):
            SUT("group", (artifact, duplicate))

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-NATIVE-003.

        Requirement: A native group is operationally immutable and cannot acquire
        undeclared encoded-document or path state.

        Method: Attempt to replace the group key and add a repository-root attribute.

        Oracle: Frozen and slotted dataclass semantics.

        Acceptance: Both mutations fail and the original key remains unchanged.

        Interpretation: A pass establishes immutable explicit integration state.

        Limitations: Immutability does not authenticate the supplied bytes.
        """
        artifact = Wannier90NativeArtifact("synthetic.win", b"")
        group = SUT("group", (artifact,))

        with pytest.raises(FrozenInstanceError):
            group.group_id = "changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            group.repository_root = "/tmp"  # type: ignore[attr-defined]
        assert group.group_id == "group"
        assert not hasattr(group, "repository_root")
