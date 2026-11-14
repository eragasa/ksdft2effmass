Hopping locality
================

Hopping locality diagnoses the distribution of an unchanged Fourier hopping
representation. It does not remove coefficients or construct a finite-support model;
those actions belong to support truncation.

Domain and periodic roles
-------------------------

.. currentmodule:: ksdft2effmass.hopping_locality.base

.. autoclass:: HoppingLocality
.. autoclass:: HoppingLocalityAnalysisRequest
.. autoclass:: HoppingLocalityAnalysis
.. autoclass:: HoppingLocalityAnalyzer
.. autoclass:: PeriodicHoppingLocality
.. autoclass:: PeriodicRankNHoppingLocalityCapability
   :members:
.. autoclass:: PeriodicHoppingLocalityAnalysisRequest
.. autoclass:: PeriodicHoppingLocalityAnalysis
.. autoclass:: PeriodicHoppingLocalityAnalyzer

Dimensional roles
-----------------

.. currentmodule:: ksdft2effmass.periodic1d.hopping_locality.base

.. autoclass:: Periodic1DHoppingLocality
.. autoclass:: Periodic1DHoppingLocalityAnalysisRequest
.. autoclass:: Periodic1DHoppingLocalityAnalysis
.. autoclass:: Periodic1DHoppingLocalityAnalyzer

.. currentmodule:: ksdft2effmass.periodic2d.hopping_locality.base

.. autoclass:: Periodic2DHoppingLocality
.. autoclass:: Periodic2DHoppingLocalityAnalysisRequest
.. autoclass:: Periodic2DHoppingLocalityAnalysis
.. autoclass:: Periodic2DHoppingLocalityAnalyzer

.. currentmodule:: ksdft2effmass.periodic3d.hopping_locality.base

.. autoclass:: Periodic3DHoppingLocality
.. autoclass:: Periodic3DHoppingLocalityAnalysisRequest
.. autoclass:: Periodic3DHoppingLocalityAnalysis
.. autoclass:: Periodic3DHoppingLocalityAnalyzer

Rank ownership
--------------

Implemented rank-one, rank-two, and arbitrary-rank leaves expose
``band_subspace_rank``. Rank-two owners refine the applicable dimensional finite-rank
owner, while rank one remains a separate specialization. Rank four is a rank-N value
rather than a separate namespace. Standalone hopping-power and tail values inherit their
truthful rank owner without becoming support-truncation results.
