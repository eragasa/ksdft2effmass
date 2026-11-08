Rank-N periodic-1D band alignment
=================================

This API defines a reusable parent-model contract, independent gauge transformations,
represented fields, reciprocal-space meshes, four alignment families, strict
numerical-rank tests, periodic-frame transport, finite-periodic Fourier analysis,
interpolation, and calculation records for the higher-rank study.

The producer evaluates one explicitly requested rank/depth case over all three odd
construction meshes.  It selects the global unitary only at ``M = 2049``, reuses it
without refitting, applies pointwise and known-inverse transformations separately,
and evaluates interpolation and symmetric-range truncation on the shifted 8191-point
mesh.  Energies are dimensionless in this analytic study.  Frame residuals use
``||R||_F / sqrt(r)`` and operator residuals use
``||R||_F / (sqrt(r) E_ref)`` with the recorded positive ``E_ref = 1``.

Public integer inputs reject booleans and numeric strings.  Their finite protocol
inventories prevent application-level overflow.  The maintained calculation owns its
concrete immutable ``PeriodicBasisInventory``; reusable source requires the selected
structured basis explicitly and does not generate it from rank or retained-basis
strings. Public floating inputs require
built-in finite binary64 values; nonfinite values and alternative frozen tolerances
are rejected.  NumPy arrays require exact ``float64``, ``int64``, or ``complex128``
dtypes as documented by their records.

The calculation result is producer output, not independently verified scientific
evidence.  One bounded reference analyzer directly reconstructs analytic-model and
gauge-transformation core invariants.  A second uses direct NumPy sums to reconstruct
all four Fourier controls on all three construction meshes, including shifted
interpolation and support
tails for every alignment and exact-support comparisons for the oracle.  A third
reconstructs the global polar factor by Hermitian eigendecomposition and
all pointwise right unitaries directly from the analytic gauge transformation, then
compares rank, residual, integrity, and selected-unitary evidence.  A fourth directly
reconstructs the
constant-frame closed route, link rank evidence, and identity closure actions on all
three meshes.  These paths do not invoke the corresponding producer scientific actions
or own the result bytes.  ``Producer-independent`` means direct NumPy reconstruction,
not a separate numerical-library stack: NumPy/LAPACK and typed quantity/comparison
infrastructure remain shared.  Complete locality error channels, refinement, complete
independent recalculation, byte-owning verification, authenticated figures,
retained execution, material validation, and publication remain unimplemented and are
not implied by these software paths.

Parent contract, transformation, and represented fields
---------------------------------------------------------

.. automodule:: ksdft2effmass.periodic.periodic1d.rankN.models.base
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.gauge_transformation
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

The reusable API owns only the parent-model contract and generic transformation
mechanics.  Exact analytic parent formulas and parent/transformation study composition
are calculation- or verification-support-owned.

.. automodule:: ksdft2effmass.periodic1d.rankN.represented_fields
   :members:
   :undoc-members:
   :show-inheritance:

Fourier analysis and interpolation
----------------------------------

The independently composable finite-rank stages are documented in
:doc:`../../fourier-analysis` and :doc:`../../interpolation`.

Frame-transport capability
--------------------------

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.request
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.analysis
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.failure
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.link
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.result
   :members:
   :undoc-members:
   :show-inheritance:

Band-alignment calculation records
----------------------------------

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.gauge_case_result
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.construction_mesh_result
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.evaluation_result
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_alignment.refinement_result
   :members:
   :undoc-members:
   :show-inheritance:

Composite calculation actions
-----------------------------

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.analysis
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.construction_mesh
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.gauge_case
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.evaluation
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.refinement
   :members:
   :undoc-members:
   :show-inheritance:

Purpose-specific independent reference analysis
------------------------------------------------

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.reference
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.fourier_reference
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.procrustes_reference
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.transport_reference
   :members:
   :undoc-members:
   :show-inheritance:
