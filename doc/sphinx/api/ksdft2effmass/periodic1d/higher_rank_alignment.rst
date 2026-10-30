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
evidence.  A bounded reference analyzer directly reconstructs analytic-model and
attack core invariants without invoking the producer or its scientific actions.  It
does not reconstruct transport, Procrustes, Fourier, locality, or refinement values
and does not own the result bytes.  Complete independent recalculation, byte-owning
verification, authenticated figures, retained execution, material validation, and
publication remain unimplemented and are not implied by either software path.

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
