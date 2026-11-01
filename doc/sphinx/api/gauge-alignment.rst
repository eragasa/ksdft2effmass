Gauge alignment
===============

The gauge-alignment API identifies retained-space transformation groups, action and
inner-product conventions, and the common request--analysis--analyzer roles.  Group
family and inner-product convention are separate: a future metric-unitary formulation
would remain unitary while supplying a different metric contract and numerical
objective.

Shared scientific identities
----------------------------

.. currentmodule:: ksdft2effmass.gauge_alignment

.. autoclass:: GaugeAlignment
.. autoclass:: GaugeAlignmentGroupFamily
   :members:
.. autoclass:: GaugeAlignmentGroupIdentity
   :members:
.. autoclass:: GaugeAlignmentActionConvention
   :members:
.. autoclass:: GaugeAlignmentInnerProductConvention
   :members:
.. autoclass:: GaugeAlignmentAnalysisIdentity
   :members:

Analysis roles
--------------

.. autoclass:: GaugeAlignmentAnalysisRequest
   :members:
.. autoclass:: GaugeAlignmentAnalysis
   :members:
.. autoclass:: GaugeAlignmentAnalyzer
   :members:

Periodic one-dimensional roles
------------------------------

.. currentmodule:: ksdft2effmass.periodic1d.gauge_alignment

.. autoclass:: Periodic1DGaugeAlignment
.. autoclass:: Periodic1DGaugeAlignmentAnalysisRequest
   :members:
.. autoclass:: Periodic1DGaugeAlignmentAnalysis
   :members:
.. autoclass:: Periodic1DGaugeAlignmentAnalyzer
   :members:

Rank-one applicability
----------------------

Rank one retains the same typed unitary-group identity at represented dimension one,
but scalar operator conjugation is trivial.  The capability therefore reports an
applicability boundary rather than manufacturing numerical alignment channels.

.. currentmodule:: ksdft2effmass.periodic1d.rank1.alignment

.. autoclass:: Periodic1DRank1AlignmentApplicability
   :members:
.. autoclass:: Periodic1DRank1AlignmentApplicabilityAnalyzer
   :members:
.. autoclass:: Periodic1DRank1AlignmentApplicabilityResult
   :members:
