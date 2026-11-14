Interpolation
=============

Interpolation evaluates an admitted represented field between construction samples and
retains interpolation-only error diagnostics. It is separate from Fourier analysis,
hopping-locality measurement, and support truncation; a study may compose those stages
without making any one stage intrinsic to the others.

Shared periodic roles
---------------------

.. currentmodule:: ksdft2effmass.interpolation

.. autoclass:: Interpolation
.. autoclass:: InterpolationAnalysisRequest
.. autoclass:: InterpolationAnalysis
.. autoclass:: InterpolationAnalyzer
.. autoclass:: PeriodicInterpolation
.. autoclass:: PeriodicInterpolationAnalysisRequest
.. autoclass:: PeriodicInterpolationAnalysis
.. autoclass:: PeriodicInterpolationAnalyzer
.. autoclass:: PeriodicRankNInterpolationCapability
   :members:

Dimensional finite-rank roles
-----------------------------

Periodic-1D, periodic-2D, and periodic-3D roles are sibling refinements. Coordinate
selection, mesh topology, periodic sewing, and dimensional interpolation policy remain
owned by the concrete dimensional action.

.. currentmodule:: ksdft2effmass.periodic1d.rankN.interpolation

.. autoclass:: Periodic1DRankNInterpolationCapability
   :members:
.. autoclass:: Periodic1DRankNInterpolationAnalysisRequestRole
.. autoclass:: Periodic1DRankNInterpolationAnalysisRole
.. autoclass:: Periodic1DRankNInterpolationAnalyzerRole
.. autoclass:: Periodic1DRankNInterpolationAnalysisRequest
   :members:
.. autoclass:: Periodic1DRankNInterpolationAnalysis
   :members:
.. autoclass:: Periodic1DRankNInterpolationAnalyzer
   :members:

.. currentmodule:: ksdft2effmass.periodic2d.rankN.interpolation

.. autoclass:: Periodic2DRankNInterpolationCapability
   :members:
.. autoclass:: Periodic2DRankNInterpolationAnalysisRequestRole
.. autoclass:: Periodic2DRankNInterpolationAnalysisRole
.. autoclass:: Periodic2DRankNInterpolationAnalyzerRole

.. currentmodule:: ksdft2effmass.periodic3d.rankN.interpolation

.. autoclass:: Periodic3DRankNInterpolationCapability
   :members:
.. autoclass:: Periodic3DRankNInterpolationAnalysisRequestRole
.. autoclass:: Periodic3DRankNInterpolationAnalysisRole
.. autoclass:: Periodic3DRankNInterpolationAnalyzerRole
