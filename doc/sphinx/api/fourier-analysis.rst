Fourier analysis
================

Fourier analysis transforms one represented periodic matrix field into finite-periodic
coefficient data and retains transform-consistency diagnostics. It is independently
composable: gauge alignment may produce a represented field, while hopping locality may
consume Fourier coefficients, but neither operation owns Fourier analysis.

Shared periodic roles
---------------------

.. currentmodule:: ksdft2effmass.fourier_analysis

.. autoclass:: FourierAnalysis
.. autoclass:: FourierAnalysisRequest
.. autoclass:: FourierAnalysisResult
.. autoclass:: FourierAnalyzer
.. autoclass:: PeriodicFourierAnalysis
.. autoclass:: PeriodicFourierAnalysisRequest
.. autoclass:: PeriodicFourierAnalysisResult
.. autoclass:: PeriodicFourierAnalyzer
.. autoclass:: PeriodicRankNFourierAnalysisCapability
   :members:

Dimensional finite-rank roles
-----------------------------

Periodic-1D, periodic-2D, and periodic-3D roles are sibling refinements. Mesh topology,
translation representatives, Nyquist policy, sewing, and tensor shape remain owned by
the dimensional implementation.

.. currentmodule:: ksdft2effmass.periodic1d.rankN.fourier_analysis

.. autoclass:: Periodic1DRankNFourierAnalysisCapability
   :members:
.. autoclass:: Periodic1DRankNFourierAnalysisRequestRole
.. autoclass:: Periodic1DRankNFourierAnalysisRole
.. autoclass:: Periodic1DRankNFourierAnalyzerRole
.. autoclass:: Periodic1DRankNFourierAnalysisRequest
   :members:
.. autoclass:: Periodic1DRankNFourierAnalysis
   :members:
.. autoclass:: Periodic1DRankNFourierAnalyzer
   :members:

.. currentmodule:: ksdft2effmass.periodic2d.rankN.fourier_analysis

.. autoclass:: Periodic2DRankNFourierAnalysisCapability
   :members:
.. autoclass:: Periodic2DRankNFourierAnalysisRequestRole
.. autoclass:: Periodic2DRankNFourierAnalysisRole
.. autoclass:: Periodic2DRankNFourierAnalyzerRole

.. currentmodule:: ksdft2effmass.periodic3d.rankN.fourier_analysis

.. autoclass:: Periodic3DRankNFourierAnalysisCapability
   :members:
.. autoclass:: Periodic3DRankNFourierAnalysisRequestRole
.. autoclass:: Periodic3DRankNFourierAnalysisRole
.. autoclass:: Periodic3DRankNFourierAnalyzerRole
