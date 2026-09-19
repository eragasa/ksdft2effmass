r"""Software verification of ``FiniteDomainEffectsCaseInventoryJsonSerializer``.

Evidence profile: routine

Bounded artifact scope: canonical version-one JSON for deterministic execution-free
finite-domain definitions and case inventories.

Facet and represented meaning

The serializer retains exact geometry, mesh, parent, defect, channel, ordering, count,
and full deterministic inventory-content identity contracts without calculation data.

Intrinsic and cross-object scope

Canonical round-trip reconstruction and content-digest tamper rejection are included.

VVUQ and scientific exclusions

The payload records proposed work only. It does not read accepted-parent results,
execute operators or campaigns, establish numerical or scientific validation, perform
UQ, or provide human acceptance.
"""

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCaseEnumerator,
    FiniteDomainEffectsCaseInventoryJsonSerializer,
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainEffectsCaseInventoryJsonSerializer


class TestFiniteDomainEffectsCaseInventoryJsonSerializer:
    """Own software evidence for the finite-domain inventory wire contract."""

    def test_method__serialize__emits_round_trip_canonical_inventory(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-WIRE-001

        Requirement: Version-one bytes retain the exact execution-free definition and
        authenticate its deterministic complete case inventory.

        Acceptance: Deserialization reproduces the source inventory and reserialization
        yields byte-identical canonical JSON ending in one newline.
        """
        inventory = FiniteDomainEffectsCaseEnumerator().execute(self.definition())
        serializer = FiniteDomainEffectsCaseInventoryJsonSerializer()

        payload = serializer.serialize(inventory)
        reconstructed = serializer.deserialize(payload)

        assert reconstructed == inventory
        assert serializer.serialize(reconstructed) == payload
        assert payload.endswith(b"\n")
        assert b'"execution_status": "not_executed"' in payload

    def test_method__deserialize__rejects_inventory_digest_tampering(self) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-WIRE-002

        Requirement: Retained summary identity must authenticate all reconstructed case
        content rather than counts alone.

        Acceptance: Changing one hexadecimal content-identity digit while preserving
        valid JSON raises ``ValueError``.
        """
        serializer = FiniteDomainEffectsCaseInventoryJsonSerializer()
        payload = serializer.serialize(
            FiniteDomainEffectsCaseEnumerator().execute(self.definition())
        )
        marker = b'"content_sha256": "'
        start = payload.index(marker) + len(marker)
        replacement = b"0" if payload[start : start + 1] != b"0" else b"1"
        tampered = payload[:start] + replacement + payload[start + 1 :]

        with pytest.raises(ValueError, match="SHA-256"):
            serializer.deserialize(tampered)

    @staticmethod
    def definition() -> FiniteDomainEffectsStudyDefinition:
        """Return a compact execution-free definition for wire-contract evidence."""
        area = (
            FiniteLatticeShape(LatticeDimension.TWO, (2, 2)),
            FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
        )
        shape = (
            FiniteLatticeShape(LatticeDimension.TWO, (2, 3)),
            FiniteLatticeShape(LatticeDimension.TWO, (3, 2)),
        )
        return FiniteDomainEffectsStudyDefinition(
            identifier="wire_contract_v1",
            area_shapes=area,
            shape_shapes=shape,
            orientation_shape_pairs=((shape[0], shape[1]),),
            defect_identifiers=("synthetic_defect",),
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (2, 2)),
            isotropic_parent_identifier="isotropic",
            orientation_source_parent_identifier="orientation_source",
            orientation_swapped_parent_identifier="orientation_swapped",
        )
