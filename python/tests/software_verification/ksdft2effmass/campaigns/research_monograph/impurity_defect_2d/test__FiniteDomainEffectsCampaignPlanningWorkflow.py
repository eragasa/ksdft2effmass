r"""Software verification of ``FiniteDomainEffectsCampaignPlanningWorkflow``.

Evidence profile: routine

Bounded artifact scope: execution-free composition of finite-domain definition
validation, deterministic enumeration, and canonical plan serialization.

Facet and represented meaning

The Workflow returns an authenticated proposed-work plan and performs no operator,
eigensolver, accepted-parent, or campaign evaluation.

Intrinsic and cross-object scope

A compact definition verifies inventory counts and canonical byte reconstruction.

VVUQ and scientific exclusions

This is software verification of planning only. It establishes no numerical result,
scientific validation, UQ, protected execution authority, or human acceptance.
"""

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCampaignPlanningWorkflow,
    FiniteDomainEffectsCaseInventoryJsonSerializer,
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainEffectsCampaignPlanningWorkflow


class TestFiniteDomainEffectsCampaignPlanningWorkflow:
    """Own software evidence for execution-free campaign planning."""

    def test_method__execute__returns_authenticated_nonexecuted_plan(self) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-PLAN-001

        Requirement: The Workflow composes only deterministic planning actions and
        binds the resulting inventory to canonical version-one bytes.

        Acceptance: The compact study yields 16 isotropic cases, four orientation
        comparisons, 28 future evaluations, and byte-exact reconstruction.
        """
        result = FiniteDomainEffectsCampaignPlanningWorkflow().execute(
            self.definition()
        )

        assert len(result.inventory.isotropic_cases) == 16
        assert len(result.inventory.orientation_cases) == 4
        assert result.inventory.operator_evaluation_count == 28
        assert b'"execution_status": "not_executed"' in result.serialized_plan
        assert (
            FiniteDomainEffectsCaseInventoryJsonSerializer().deserialize(
                result.serialized_plan
            )
            == result.inventory
        )

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
