Periodic scientific-model hierarchy
===================================

.. currentmodule:: ksdft2effmass.periodic

The periodic scientific hierarchy provides nominal runtime membership for models with
one, two, or three periodic spatial directions. It identifies scientific models rather
than campaign executions. These classes own no numerical construction, represented
operator, serializer, tolerance, provenance, or acceptance behavior.

A concrete model must implement a stable nonempty ``model_id`` and an exact
:class:`PeriodicModelRole`. The dimension-specific bases provide exact built-in integer
dimensions and reject subclass attempts to override them. Defect bases additionally
require a stable pristine-parent identity; concrete defect records remain responsible
for their geometry, basis, gauge, energy-reference, unit, and alignment prerequisites.

The hierarchy identifies scientific models, not retained subspaces, retained operators,
or finite matrix representations. Those are separate scientific objects connected to a
model by explicit selection, restriction, representation, and alignment operations.
Likewise, a campaign record containing preserved encoded bytes is not a model merely
because historical code names it ``...CampaignModel``. The implemented scientific-
retention API is documented in :doc:`retention`.

``MATERIAL_REFERENCE`` means that a model represents an explicitly specified material.
It does not establish physical completeness or scientific validation. Graphene and
bulk-silicon model classes are proposed work and are not supplied by this foundation.

.. autodata:: SpatialDimension

.. autoclass:: PeriodicModelRole
   :members:

.. autoclass:: PeriodicModel
   :members:

.. autoclass:: Periodic1DModel
   :members:

.. autoclass:: Periodic2DModel
   :members:

.. autoclass:: Periodic3DModel
   :members:

.. autoclass:: Periodic1DDefectModel
   :members:

.. autoclass:: Periodic2DDefectModel
   :members:

.. autoclass:: Periodic3DDefectModel
   :members:
