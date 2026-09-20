r"""Software verification of ``FiniteDomainEffectsStudyDefinition``.

Evidence profile: routine

Bounded artifact scope: execution-free geometry, defect, twist, and parent inventories
for finite-domain case enumeration.

Facet and represented meaning

The DataObject retains ordered area and fixed-area shape channels, orientation pairs,
and a complete 2D twist mesh without authorizing evaluation.

Intrinsic and cross-object scope

The adopted geometry inventory and an unequal-area adverse definition are included.

VVUQ and scientific exclusions

This is software verification of authored synthetic inputs, not calculation execution,
numerical validation, scientific validation, UQ, or human acceptance.
"""

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainEffectsStudyDefinition


class TestFiniteDomainEffectsStudyDefinition:
    """Own software evidence for the finite-domain study definition."""

    def test_constructor__channel_geometries__preserves_shared_shape_once(self) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-DEFINITION-001

        Requirement: Area and shape inventories remain separate while their shared
        geometry is exposed once for operator evaluation.

        Acceptance: The adopted five-plus-five lists yield nine isotropic geometries;
        changing one fixed-area shape to area 143 raises ``ValueError``.
        """
        area_shapes = (
            FiniteLatticeShape(LatticeDimension.TWO, (6, 6)),
            FiniteLatticeShape(LatticeDimension.TWO, (8, 8)),
            FiniteLatticeShape(LatticeDimension.TWO, (10, 10)),
            FiniteLatticeShape(LatticeDimension.TWO, (12, 12)),
            FiniteLatticeShape(LatticeDimension.TWO, (16, 16)),
        )
        shape_shapes = (
            FiniteLatticeShape(LatticeDimension.TWO, (8, 18)),
            FiniteLatticeShape(LatticeDimension.TWO, (9, 16)),
            FiniteLatticeShape(LatticeDimension.TWO, (12, 12)),
            FiniteLatticeShape(LatticeDimension.TWO, (16, 9)),
            FiniteLatticeShape(LatticeDimension.TWO, (18, 8)),
        )
        definition = FiniteDomainEffectsStudyDefinition(
            identifier="finite_domain_v1",
            area_shapes=area_shapes,
            shape_shapes=shape_shapes,
            orientation_shape_pairs=(
                (shape_shapes[0], shape_shapes[4]),
                (shape_shapes[1], shape_shapes[3]),
            ),
            defect_identifiers=(
                "directional_nearest_neighbor",
                "finite_range_diagonal_nonlocal",
            ),
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (9, 9)),
            isotropic_parent_identifier="isotropic",
            orientation_source_parent_identifier="anisotropic_source",
            orientation_swapped_parent_identifier="anisotropic_swapped",
        )

        assert len(definition.isotropic_shapes) == 9
        assert definition.isotropic_shapes.count(shape_shapes[2]) == 1
        with pytest.raises(ValueError, match="fixed cell count"):
            FiniteDomainEffectsStudyDefinition(
                identifier="bad",
                area_shapes=area_shapes,
                shape_shapes=(
                    shape_shapes[0],
                    FiniteLatticeShape(LatticeDimension.TWO, (11, 13)),
                ),
                orientation_shape_pairs=((shape_shapes[0], shape_shapes[4]),),
                defect_identifiers=("defect",),
                twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (9, 9)),
                isotropic_parent_identifier="isotropic",
                orientation_source_parent_identifier="anisotropic_source",
                orientation_swapped_parent_identifier="anisotropic_swapped",
            )
