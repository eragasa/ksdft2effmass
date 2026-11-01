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
