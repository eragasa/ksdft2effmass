Two-dimensional selected-band retention
=======================================

.. currentmodule:: ksdft2effmass.periodic2d

:class:`Periodic2DSelectedBandRetentionDefinition` composes a reusable
:class:`~ksdft2effmass.analysis.periodic_bands.ContiguousBandSelection` with the
general parent-qualified
:class:`~ksdft2effmass.periodic.PeriodicRetentionDefinition`.

For inclusive zero-based bounds ``lower_index`` and ``upper_index``, the ordered
selection is

.. math::

   \mathcal I = (\ell,\ell+1,\ldots,u).

The entry at position :math:`i` corresponds to
``retention.ordered_state_labels[i]``.  The interval supplies band indices only.  The
general definition separately supplies stable parent-model, parent-operator, ambient
state-space, retained-space, reciprocal-domain, construction-record, assumption, and
provenance identities.

Construction requires:

* an exact :class:`~ksdft2effmass.periodic.PeriodicRetentionDefinition`;
* an exact
  :class:`~ksdft2effmass.analysis.periodic_bands.ContiguousBandSelection`;
* parent spatial dimension two;
* :attr:`~ksdft2effmass.periodic.PeriodicRetentionKind.SELECTED_BANDS`; and
* retained rank equal to the inclusive selected-band count.

The object is a scientific retention *definition*, not a retained subspace.  It stores
no projector, frame, gauge, represented operator, or finite matrix.  It does not
establish band isolation, choose between projection and disentanglement, transform a
basis, truncate hopping coefficients, or construct an effective model.

Consequently, this contract does not yet bind the preserved periodic2d isolated-band or
composite result documents to
:class:`~ksdft2effmass.periodic.PeriodicRetainedSubspace` or
:class:`~ksdft2effmass.periodic.PeriodicRetainedOperator`.  Those historical documents
do not contain authenticated frame or projector coordinates sufficient for such a
claim.  Parent-model, numerical or discretization, and model-reduction errors remain
separate.

Synthetic tests establish only software type, identity, dimensional, ordering, rank,
immutability, and export behavior.  They do not establish numerical verification,
physical adequacy, scientific validation, or uncertainty quantification.

.. autoclass:: Periodic2DSelectedBandRetentionDefinition
   :members:

Mappings
--------

* Source:
  ``python/src/ksdft2effmass/periodic2d/retention.py``
* Software verification:
  ``python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py``
* General retention concept: :doc:`../../../concepts/scientific-retention`
