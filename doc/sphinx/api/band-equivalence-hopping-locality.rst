Band-equivalence and hopping-locality aggregate
===============================================

``band_equivalence_hopping_locality`` coordinates separately owned scientific
operations. Its ownership hierarchy is founded on band equivalence; aggregate
membership does not make a request, analysis, or action a reusable hopping-locality,
gauge-alignment, frame-transport, or support-truncation owner.

Domain and periodic roles
-------------------------

.. currentmodule:: ksdft2effmass.band_equivalence_hopping_locality.base

.. autoclass:: BandEquivalenceHoppingLocality
.. autoclass:: BandEquivalenceHoppingLocalityRequest
.. autoclass:: BandEquivalenceHoppingLocalityAnalysis
.. autoclass:: BandEquivalenceHoppingLocalityAnalyzer
.. autoclass:: BandEquivalenceHoppingLocalityValue
.. autoclass:: BandEquivalenceHoppingLocalityAction
.. autoclass:: PeriodicBandEquivalenceHoppingLocality
.. autoclass:: PeriodicBandEquivalenceHoppingLocalityRequest
.. autoclass:: PeriodicBandEquivalenceHoppingLocalityAnalysis
.. autoclass:: PeriodicBandEquivalenceHoppingLocalityAnalyzer

Dimensional roles
-----------------

.. currentmodule:: ksdft2effmass.periodic1d.band_equivalence_hopping_locality.base

.. autoclass:: Periodic1DBandEquivalenceHoppingLocality
.. autoclass:: Periodic1DBandEquivalenceHoppingLocalityRequest
.. autoclass:: Periodic1DBandEquivalenceHoppingLocalityAnalysis
.. autoclass:: Periodic1DBandEquivalenceHoppingLocalityAnalyzer

.. currentmodule:: ksdft2effmass.periodic2d.band_equivalence_hopping_locality.base

.. autoclass:: Periodic2DBandEquivalenceHoppingLocality
.. autoclass:: Periodic2DBandEquivalenceHoppingLocalityRequest
.. autoclass:: Periodic2DBandEquivalenceHoppingLocalityAnalysis
.. autoclass:: Periodic2DBandEquivalenceHoppingLocalityAnalyzer

.. currentmodule:: ksdft2effmass.periodic3d.band_equivalence_hopping_locality.base

.. autoclass:: Periodic3DBandEquivalenceHoppingLocality
.. autoclass:: Periodic3DBandEquivalenceHoppingLocalityRequest
.. autoclass:: Periodic3DBandEquivalenceHoppingLocalityAnalysis
.. autoclass:: Periodic3DBandEquivalenceHoppingLocalityAnalyzer

Periodic-3D rank-N represented-field boundary
----------------------------------------------

The sampled-field value separates analysis operands from the producer that supplied
them. The synthetic-case sampler and the in-memory Wannier-field producer are separate
adapters to the same immutable boundary; neither becomes a block-hopping model. The
construction inventory is the regular transform mesh, while evaluation coordinates may
be either a tensor product or an arbitrary ordered reciprocal-point inventory.
The selected synthetic parent is constructed as the existing PhysKit
``DenseBlockHoppingModel`` rather than as a competing KSD model hierarchy.

.. currentmodule:: ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality

.. autoclass:: Periodic3DRankNLatticeControlEnum
   :members:
.. autoclass:: Periodic3DRankNBlockHoppingParentBuilder
   :members:
.. autoclass:: Periodic3DRankNBandEquivalenceFieldSamples
   :members:
.. autoclass:: Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry
   :members:
.. autoclass:: Periodic3DRankNBandEquivalenceHoppingLocalityPolicy
   :members:
.. autoclass:: Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer
   :members:
.. autoclass:: Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalysis
   :members:
.. autoclass:: Periodic3DRankNWannierFieldSource
   :members:
.. autoclass:: Periodic3DRankNWannierFieldProducer
   :members:
.. autoclass:: Periodic3DRankNAnalyticCaseFieldSampler
   :members:

Rank ownership
--------------

Top-level rank-two studies and the concrete Periodic1D rank-N rank/depth calculation
expose ``band_subspace_rank``. Periodic2D/3D rank-N family requests, analyses,
analyzers, case expanders, and family actions expose ``band_subspace_ranks``. Their
concrete case analyses, independent references, and case actions instead expose singular
``band_subspace_rank``. Rank-two and rank-N remain sibling specializations.

Serialized wire-owner records remain serialization objects. Recorders, verifiers,
independent scientific references, and authenticated visualization inputs receive
aggregate action or value ownership only when they can report the applicable rank
truthfully without changing canonical bytes.
