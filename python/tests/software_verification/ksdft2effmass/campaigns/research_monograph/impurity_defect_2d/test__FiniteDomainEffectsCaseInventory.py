r"""Software verification of ``FiniteDomainEffectsCaseInventory``.

Evidence profile: routine

Bounded artifact scope: immutable correlation of one definition with isotropic and
orientation case inventories.

Facet and represented meaning

The ResultObject distinguishes unique isotropic evaluations from three-evaluation
orientation comparisons and enforces definition-derived counts.

Intrinsic and cross-object scope

A minimal correlated definition, complete inventory, and omitted-case attack are
included.

VVUQ and scientific exclusions

This is software inventory evidence only; it does not execute a campaign or establish
numerical validation, scientific validation, UQ, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCaseEnumerator,
    FiniteDomainEffectsCaseInventory,
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainEffectsCaseInventory


class TestFiniteDomainEffectsCaseInventory:
    """Own software evidence for definition-derived inventory integrity."""

    def test_constructor__case_counts__rejects_missing_cases(self) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-INVENTORY-001

        Requirement: A retained inventory cannot silently omit a defined case.

        Acceptance: A minimal enumerated inventory contains three isotropic cases and
        one orientation comparison; removing one isotropic case raises ``ValueError``.
        """
        area_shape = FiniteLatticeShape(LatticeDimension.TWO, (2, 2))
        source_shape = FiniteLatticeShape(LatticeDimension.TWO, (2, 3))
        target_shape = FiniteLatticeShape(LatticeDimension.TWO, (3, 2))
        definition = FiniteDomainEffectsStudyDefinition(
            identifier="minimal",
            area_shapes=(area_shape,),
            shape_shapes=(source_shape, target_shape),
            orientation_shape_pairs=((source_shape, target_shape),),
            defect_identifiers=("defect",),
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (1, 1)),
            isotropic_parent_identifier="isotropic",
            orientation_source_parent_identifier="anisotropic_source",
            orientation_swapped_parent_identifier="anisotropic_swapped",
        )
        inventory = FiniteDomainEffectsCaseEnumerator().execute(definition)

        assert len(inventory.isotropic_cases) == 3
        assert len(inventory.orientation_cases) == 1
        assert inventory.operator_evaluation_count == 6
        with pytest.raises(ValueError, match="isotropic case count"):
            replace(inventory, isotropic_cases=inventory.isotropic_cases[:-1])
