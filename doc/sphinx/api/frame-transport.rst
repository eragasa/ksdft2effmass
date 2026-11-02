Frame transport
===============

Frame transport owns the ordered propagation of represented frames along explicit
periodic routes. It is distinct from pointwise gauge alignment, band equivalence,
hopping locality, and support truncation. Concrete studies retain their route,
closure or sewing, action, inner-product, rank, and numerical-policy contracts.

Domain and periodic roles
-------------------------

.. currentmodule:: ksdft2effmass.frame_transport.base

.. autoclass:: FrameTransport
.. autoclass:: FrameTransportAnalysisRequest
   :members:
.. autoclass:: FrameTransportAnalysis
   :members:
.. autoclass:: FrameTransportAnalyzer
   :members:
.. autoclass:: PeriodicFrameTransport
.. autoclass:: PeriodicFrameTransportAnalysisRequest
   :members:
.. autoclass:: PeriodicFrameTransportAnalysis
   :members:
.. autoclass:: PeriodicFrameTransportAnalyzer
   :members:

Dimensional specializations
---------------------------

.. currentmodule:: ksdft2effmass.periodic1d.frame_transport.base

.. autoclass:: Periodic1DFrameTransport
.. autoclass:: Periodic1DFrameTransportAnalysisRequest
.. autoclass:: Periodic1DFrameTransportAnalysis
.. autoclass:: Periodic1DFrameTransportAnalyzer

.. currentmodule:: ksdft2effmass.periodic2d.frame_transport.base

.. autoclass:: Periodic2DFrameTransport
.. autoclass:: Periodic2DFrameTransportAnalysisRequest
.. autoclass:: Periodic2DFrameTransportAnalysis
.. autoclass:: Periodic2DFrameTransportAnalyzer

.. currentmodule:: ksdft2effmass.periodic3d.frame_transport.base

.. autoclass:: Periodic3DFrameTransport
.. autoclass:: Periodic3DFrameTransportAnalysisRequest
.. autoclass:: Periodic3DFrameTransportAnalysis
.. autoclass:: Periodic3DFrameTransportAnalyzer

Rank specializations
--------------------

Rank two and arbitrary rank are sibling specializations. A rank-four transport is a
rank-N value, not a separate rank-four namespace. No Periodic2D or Periodic3D rank-one
transport capability is claimed.
