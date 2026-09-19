r"""Software verification of ``FiniteDomainEffectsCaseEnumerator``.

Evidence profile: routine

Bounded artifact scope: deterministic execution-free enumeration of adopted defect-2D
finite-domain cases.

Facet and represented meaning

The ActionObject de-duplicates shared isotropic geometries and emits orientation
comparison records, each representing three future operator evaluations.

Intrinsic and cross-object scope

The adopted 9x9 mesh, nine isotropic geometries, two defects, and two orientation pairs
are included.

VVUQ and scientific exclusions

Enumeration does not construct operators, read accepted-parent results, execute a
campaign, establish numerical or scientific validation, UQ, or human acceptance.
"""

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainChannel,
    FiniteDomainEffectsCaseEnumerator,
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainEffectsCaseEnumerator


class TestFiniteDomainEffectsCaseEnumerator:
    """Own software evidence for deterministic case enumeration."""

    def test_method__execute__matches_adopted_inventory_and_order(self) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-FINITE-DOMAIN-ENUMERATION-001

        Requirement: Enumeration emits 1,458 unique isotropic evaluations and 324
        orientation comparisons, totaling 2,430 proposed operator evaluations.

        Acceptance: Counts, first-case order, shared 12x12 memberships, and swapped
        orientation twist components match the adopted design.
        """
        area = (
            FiniteLatticeShape(LatticeDimension.TWO, (6, 6)),
            FiniteLatticeShape(LatticeDimension.TWO, (8, 8)),
            FiniteLatticeShape(LatticeDimension.TWO, (10, 10)),
            FiniteLatticeShape(LatticeDimension.TWO, (12, 12)),
            FiniteLatticeShape(LatticeDimension.TWO, (16, 16)),
        )
        shape = (
            FiniteLatticeShape(LatticeDimension.TWO, (8, 18)),
            FiniteLatticeShape(LatticeDimension.TWO, (9, 16)),
            FiniteLatticeShape(LatticeDimension.TWO, (12, 12)),
            FiniteLatticeShape(LatticeDimension.TWO, (16, 9)),
            FiniteLatticeShape(LatticeDimension.TWO, (18, 8)),
        )
        definition = FiniteDomainEffectsStudyDefinition(
            identifier="finite_domain_v1",
            area_shapes=area,
            shape_shapes=shape,
            orientation_shape_pairs=((shape[0], shape[4]), (shape[1], shape[3])),
            defect_identifiers=(
                "directional_nearest_neighbor",
                "finite_range_diagonal_nonlocal",
            ),
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (9, 9)),
            isotropic_parent_identifier="isotropic",
            orientation_source_parent_identifier="anisotropic_source",
            orientation_swapped_parent_identifier="anisotropic_swapped",
        )

        inventory = FiniteDomainEffectsCaseEnumerator().execute(definition)

        assert len(inventory.isotropic_cases) == 1458
        assert len(inventory.orientation_cases) == 324
        assert inventory.operator_evaluation_count == 2430
        assert inventory.isotropic_cases[0].identifier.endswith("twist-000")
        shared_offset = definition.isotropic_shapes.index(shape[2]) * 2 * 81
        assert inventory.isotropic_cases[shared_offset].channel_memberships == (
            FiniteDomainChannel.AREA,
            FiniteDomainChannel.SHAPE,
            FiniteDomainChannel.BOUNDARY_PHASE,
        )
        orientation = inventory.orientation_cases[1]
        assert orientation.source_twist.turns == (0.0, 1.0 / 9.0)
        assert orientation.target_twist.turns == (1.0 / 9.0, 0.0)
        assert orientation.operator_evaluation_count == 3
