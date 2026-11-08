Gauge alignment
===============

The gauge-alignment API identifies retained-space transformation groups, action and
inner-product conventions, and the common request--analysis--analyzer roles.  Group
family and inner-product convention are separate: a future metric-unitary formulation
would remain unitary while supplying a different metric contract and numerical
objective. Frame orthonormality is validated by concrete frame and request types; it is
not encoded into the Euclidean inner-product label.

Shared scientific identities
----------------------------

.. currentmodule:: ksdft2effmass.gauge_alignment

.. autoclass:: GaugeAlignment
.. autoclass:: PeriodicGaugeAlignment
.. autoclass:: PeriodicRankNGaugeAlignmentCapability
   :members:
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

Finite-rank gauge transformations
---------------------------------

Generic Givens-circuit mechanics own only the ordered rotation structure, supplied
angle samples, and explicit right actions. Periodic one-dimensional Fourier angle
fields supply coefficients independently of any validation-study inventory.

.. currentmodule:: ksdft2effmass.gauge_transformation

.. autoclass:: FiniteRankGivensRotation
   :members:
.. autoclass:: FiniteRankGivensLayer
   :members:
.. autoclass:: FiniteRankGivensCircuit
   :members:
.. autoclass:: FiniteRankGivensCircuitTransformationConstructor
   :members:
.. autoclass:: SampledFiniteRankGaugeTransformation
   :members:

.. currentmodule:: ksdft2effmass.periodic1d.gauge_transformation

.. autoclass:: Periodic1DFourierGivensGaugeTransformation
   :members:

Analysis roles
--------------

.. currentmodule:: ksdft2effmass.gauge_alignment

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

Rank-first Periodic1D study dispatch
------------------------------------

.. currentmodule:: ksdft2effmass.periodic1d.gauge_alignment.factory

.. autoclass:: Periodic1DRank1AlignmentStudySpecification
   :members:
.. autoclass:: Periodic1DRank2AlignmentStudySpecification
   :members:
.. autoclass:: Periodic1DRankNAlignmentStudySpecification
   :members:
.. autoclass:: Periodic1DAlignmentStudyFactory
   :members:
.. autoclass:: Periodic1DRank2AlignmentStudyAnalyzer
   :members:
.. autoclass:: Periodic1DRankNAlignmentStudyAnalyzer
   :members:

Periodic three-dimensional rank-N synthetic transformation
-----------------------------------------------------------

The synthetic gauge transformation is independent of the parent Hamiltonian. It can
act on any admitted periodic-3D frame and represented-operator fields with matching
reciprocal sample shape and retained rank.

.. currentmodule:: ksdft2effmass.periodic3d.rankN.gauge_alignment

.. autoclass:: Periodic3DRankNGaugeNormalizationEnum
   :members:
.. autoclass:: Periodic3DRankNGivensGaugeTransformation
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
