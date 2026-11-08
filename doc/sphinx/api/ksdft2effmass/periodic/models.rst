Periodic scientific-model hierarchy
===================================

The nominal hierarchy proceeds from KSD scientific identity to periodic dimension and
then, where applicable, retained band-subspace rank. These classes identify scientific
models rather than campaign executions. The block-hopping family composes exact PhysKit
representations; the hierarchy owns no calculator, serializer, tolerance, provenance,
or acceptance behavior.

A concrete model implements a stable nonempty ``model_id`` and, for periodic models, an
exact ``PeriodicModelRole``. The role is an explicitly wire-mapped enum value, not a
role-specific package or model subclass. Dimension-specific bases provide exact built-in integer
dimensions and reject subclass attempts to override them. Finite-rank dimensional bases
require a positive retained rank and an exact dimensional structured basis identity.
Fixed-rank bases refine those contracts; the rank-two bases fix the inherited rank to
two while retaining the explicit two-coordinate basis requirement.

The hierarchy identifies scientific models, not retained subspaces, retained operators,
or finite matrix representations. Those are separate scientific objects connected to a
model by explicit selection, restriction, representation, and alignment operations.
Likewise, a campaign record containing preserved encoded bytes is not a model merely
because historical code names it ``...CampaignModel``.

Dimension-neutral models
------------------------

.. currentmodule:: ksdft2effmass.models

.. autoclass:: Model
   :members:

Periodic root
-------------

.. currentmodule:: ksdft2effmass.periodic.models

.. autodata:: SpatialDimension

.. autoclass:: PeriodicModelRole
   :members:

.. autoclass:: PeriodicModel
   :members:

Block-hopping hierarchy
-----------------------

.. autoclass:: PeriodicBlockHoppingModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic1d.rank2.models

.. autoclass:: Periodic1DRank2BlockHoppingModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic2d.rank2.models

.. autoclass:: Periodic2DRank2BlockHoppingModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic3d.rank2.models

.. autoclass:: Periodic3DRank2BlockHoppingModel
   :members:

Dimension owners
----------------

.. currentmodule:: ksdft2effmass.periodic.periodic1d.models

.. autoclass:: Periodic1DModel
   :members:

.. autoclass:: Periodic1DDefectModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic2d.models

.. autoclass:: Periodic2DModel
   :members:

.. autoclass:: Periodic2DDefectModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic3d.models

.. autoclass:: Periodic3DModel
   :members:

.. autoclass:: Periodic3DDefectModel
   :members:

Rank owners
-----------

.. currentmodule:: ksdft2effmass.periodic1d.rank1.models

.. autoclass:: Periodic1DRank1Model
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic1d.rankN.models

.. autoclass:: Periodic1DRankNModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic1d.rank2.models

.. autoclass:: Periodic1DRank2Model
   :members:

.. currentmodule:: ksdft2effmass.periodic2d.rank1.models

.. autoclass:: Periodic2DRank1Model
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic2d.rankN.models

.. autoclass:: Periodic2DRankNModel
   :members:

.. autoclass:: Periodic2DRankNAnalyticParentModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic2d.rank2.models

.. autoclass:: Periodic2DRank2Model
   :members:

.. currentmodule:: ksdft2effmass.periodic3d.rank1.models

.. autoclass:: Periodic3DRank1Model
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic3d.rankN.models

.. autoclass:: Periodic3DRankNModel
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic3d.rank2.models

.. autoclass:: Periodic3DRank2Model
   :members:
