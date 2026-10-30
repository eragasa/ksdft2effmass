Higher-rank periodic-1D alignment
=================================

This API defines the analytic parent Hamiltonians, synthetic frame attacks, ranks,
circuit depths, reciprocal-space meshes, four alignment families, strict
numerical-rank test, periodic-frame transport, finite-periodic Fourier transforms,
and calculation records for the higher-rank study.

The producer evaluates one explicitly requested rank/depth case over all three odd
construction meshes.  It selects the global unitary only at ``M = 2049``, reuses it
without refitting, applies pointwise and known-inverse transformations separately,
and evaluates interpolation and symmetric-range truncation on the shifted 8191-point
mesh.  Energies are dimensionless in this analytic study.  Frame residuals use
``||R||_F / sqrt(r)`` and operator residuals use
``||R||_F / (sqrt(r) E_ref)`` with the recorded positive ``E_ref = 1``.

Public integer inputs reject booleans and numeric strings.  Their finite protocol
inventories prevent application-level overflow.  Public floating inputs require
built-in finite binary64 values; nonfinite values and alternative frozen tolerances
are rejected.  NumPy arrays require exact ``float64``, ``int64``, or ``complex128``
dtypes as documented by their records.

The calculation result is producer output, not independently verified scientific
evidence.  One bounded reference analyzer directly reconstructs analytic-model and
attack core invariants.  A second uses direct NumPy sums to reconstruct all four Fourier
controls on all three construction meshes, including shifted interpolation and support
tails for every alignment and exact-support comparisons for the oracle.  A third
reconstructs the global polar factor by Hermitian eigendecomposition and
all pointwise right unitaries directly from the analytic attack, then compares rank,
residual, integrity, and selected-unitary evidence.  A fourth directly reconstructs the
constant-frame closed route, link rank evidence, and identity closure actions on all
three meshes.  These paths do not invoke the corresponding producer scientific actions
or own the result bytes.  ``Producer-independent`` means direct NumPy reconstruction,
not a separate numerical-library stack: NumPy/LAPACK and typed quantity/comparison
infrastructure remain shared.  Complete locality error channels, refinement, complete
independent recalculation, byte-owning verification, authenticated figures,
retained execution, material validation, and publication remain unimplemented and are
not implied by these software paths.

.. automodule:: ksdft2effmass.periodic1d.higher_rank_alignment
   :members:
   :undoc-members:
   :show-inheritance:

Purpose-specific independent reference analysis
------------------------------------------------

.. automodule:: ksdft2effmass.periodic1d.higher_rank_alignment.reference
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.higher_rank_alignment.fourier_reference
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.higher_rank_alignment.procrustes_reference
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.higher_rank_alignment.transport_reference
   :members:
   :undoc-members:
   :show-inheritance:
