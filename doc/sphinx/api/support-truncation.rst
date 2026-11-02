Support truncation
==================

Support truncation irreversibly removes coefficients outside an explicitly declared
representation support. It is distinct from hopping-locality diagnostics, which inspect
an unchanged Fourier representation.

Domain and periodic roles
-------------------------

.. currentmodule:: ksdft2effmass.support_truncation.base

.. autoclass:: SupportTruncation
.. autoclass:: SupportTruncationAnalysisRequest
.. autoclass:: SupportTruncationAnalysis
.. autoclass:: SupportTruncationAnalyzer

.. currentmodule:: ksdft2effmass.real_space_support_truncation.base

.. autoclass:: RealSpaceSupportTruncation
.. autoclass:: RealSpaceSupportTruncationAnalysisRequest
.. autoclass:: RealSpaceSupportTruncationAnalysis
.. autoclass:: RealSpaceSupportTruncationAnalyzer
.. autoclass:: PeriodicRealSpaceSupportTruncation
.. autoclass:: PeriodicRealSpaceSupportTruncationAnalysisRequest
.. autoclass:: PeriodicRealSpaceSupportTruncationAnalysis
.. autoclass:: PeriodicRealSpaceSupportTruncationAnalyzer

Dimensional roles
-----------------

.. currentmodule:: ksdft2effmass.periodic1d.support_truncation.base

.. autoclass:: Periodic1DSupportTruncation
.. autoclass:: Periodic1DSupportTruncationAnalysisRequest
.. autoclass:: Periodic1DSupportTruncationAnalysis
.. autoclass:: Periodic1DSupportTruncationAnalyzer

.. currentmodule:: ksdft2effmass.periodic2d.support_truncation.base

.. autoclass:: Periodic2DSupportTruncation
.. autoclass:: Periodic2DSupportTruncationAnalysisRequest
.. autoclass:: Periodic2DSupportTruncationAnalysis
.. autoclass:: Periodic2DSupportTruncationAnalyzer

.. currentmodule:: ksdft2effmass.periodic3d.support_truncation.base

.. autoclass:: Periodic3DSupportTruncation
.. autoclass:: Periodic3DSupportTruncationAnalysisRequest
.. autoclass:: Periodic3DSupportTruncationAnalysis
.. autoclass:: Periodic3DSupportTruncationAnalyzer

Rank ownership
--------------

Implemented rank-one, rank-two, and arbitrary-rank leaves expose
``band_subspace_rank`` through sibling rank owners. Rank four is a rank-N value, not a
separate namespace. Standalone support policies, removed-support consequences, family
analyses, and support-selection references inherit their truthful rank owner when they
belong to a rank-specific study.
