r"""Software verification of ``FiniteDomainEffectsCampaignPlanResult``.

Evidence profile: routine

Bounded artifact scope: immutable correlation of one enumerated finite-domain
inventory with its canonical execution-free plan bytes.

Facet and represented meaning

The ResultObject rejects bytes that do not authenticate and reconstruct the exact
retained inventory.

Intrinsic and cross-object scope

A valid compact plan and one valid-JSON definition-identity alteration are included.

VVUQ and scientific exclusions

This is software verification of planning data only. It establishes no numerical or
scientific result, UQ, protected execution authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCampaignPlanningWorkflow,
    FiniteDomainEffectsCampaignPlanResult,
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainEffectsCampaignPlanResult


class TestFiniteDomainEffectsCampaignPlanResult:
    """Own software evidence for plan-result correlation."""

    def test_constructor__serialized_plan__must_authenticate_exact_inventory(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-PLAN-002

        Requirement: Plan bytes cannot be edited independently of the retained
        deterministic case inventory.

        Acceptance: Changing the serialized definition identifier while retaining
        valid JSON raises ``ValueError`` during ResultObject construction.
        """
        result = FiniteDomainEffectsCampaignPlanningWorkflow().execute(
            self.definition()
        )
        tampered = result.serialized_plan.replace(
            b"workflow_contract_v1", b"workflow_contract_v2"
        )

        with pytest.raises(ValueError):
            replace(result, serialized_plan=tampered)

    @staticmethod
    def definition() -> FiniteDomainEffectsStudyDefinition:
        """Return a compact immutable planning definition."""
        area = (
            FiniteLatticeShape(LatticeDimension.TWO, (2, 2)),
            FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
        )
        shape = (
            FiniteLatticeShape(LatticeDimension.TWO, (2, 3)),
            FiniteLatticeShape(LatticeDimension.TWO, (3, 2)),
        )
        return FiniteDomainEffectsStudyDefinition(
            identifier="workflow_contract_v1",
            area_shapes=area,
            shape_shapes=shape,
            orientation_shape_pairs=((shape[0], shape[1]),),
            defect_identifiers=("synthetic_defect",),
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (2, 2)),
            isotropic_parent_identifier="isotropic",
            orientation_source_parent_identifier="orientation_source",
            orientation_swapped_parent_identifier="orientation_swapped",
        )
