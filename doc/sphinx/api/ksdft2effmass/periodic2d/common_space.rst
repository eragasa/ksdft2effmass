Periodic2d plane-wave/finite-difference common space
====================================================

Purpose and comparison boundary
-------------------------------

``Periodic2DCommonSpaceOperatorComparator`` transports a dimensionless square-cell
finite-difference operator into the explicitly retained plane-wave basis before matrix
subtraction.  It prevents direct subtraction of operators acting on different finite
state spaces and records the transport, transported matrix, difference, and diagnostic
norms.  It applies no tolerance and returns no acceptance status.

This is ksdft-specific comparison policy around the current periodic2d cosine model.
PhysKit owns the primitive lattice geometry used by the plane-wave model, while the
campaign owns its finite-difference convention, represented-space compatibility rules,
and diagnostic interpretation.  The authoritative finite comparison definition is
``specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md``.

Mathematical and physical setting
---------------------------------

Both routes represent the same controlled dimensionless spinless scalar toy parent

.. math::

   H=-\partial_x^2-\partial_y^2
     +\lambda_x\cos x+\lambda_y\cos y
     +\lambda_{xy}\cos x\cos y

on the period-:math:`2\pi` square cell and at the same reduced Bloch momentum.  This
parent is not a material Hamiltonian.  Agreement between its finite representations
cannot establish physical adequacy; disagreement is not parent-model error because the
parent law is shared.

For :math:`N` grid points per direction on the period-:math:`2\pi` cell,
:math:`x_i=2\pi i/N`, reduced Bloch momentum
:math:`\boldsymbol\kappa=(\kappa_x,\kappa_y)`, and reciprocal indices
:math:`-M\leq p,q\leq M`, define

.. math::
   :label: periodic2d-plane-wave-grid-map

   T_{(i,j),(p,q)}
   = \frac{1}{N}
     \exp\!\left(i\left[(\kappa_x+p)x_i
                         +(\kappa_y+q)x_j\right]\right).

Both domains use first-index-outer, second-index-inner order.  When
:math:`2M+1\leq N`, the retained reciprocal indices are distinct modulo the grid and

.. math::
   :label: periodic2d-plane-wave-grid-isometry

   T^\dagger T = I

up to binary64 evaluation error.  When :math:`N>2M+1`, the map is a proper
rectangular semiunitary embedding and :math:`TT^\dagger\ne I`.  At the allowed
boundary :math:`N=2M+1`, :math:`T` is square unitary in exact arithmetic and
:math:`TT^\dagger=I` as well.  The transported finite-difference operator and
common-space difference are

.. math::
   :label: periodic2d-common-space-difference

   \widetilde H_{\mathrm{FD}}=T^\dagger H_{\mathrm{FD}}T,
   \qquad
   \Delta H=\widetilde H_{\mathrm{FD}}-H_{\mathrm{PW}}.

For :math:`N>2M+1`, :math:`\widetilde H_{\mathrm{FD}}` is a proper-subspace
compression of the grid operator, not a similarity transform of the full grid matrix.
For :math:`N=2M+1`, it is a full-space unitary similarity transform.  Neither case
identifies a physical retained space or establishes scientific adequacy.

For spacing :math:`h=2\pi/N`, the finite-difference kinetic dispersion on a sampled
mode is

.. math::

   \epsilon^{\mathrm{FD}}_{pq}
   =\frac{4}{h^2}\left[
      \sin^2\frac{(\kappa_x+p)h}{2}
      +\sin^2\frac{(\kappa_y+q)h}{2}
     \right],

whereas the plane-wave matrix uses
:math:`\epsilon^{\mathrm{PW}}_{pq}=(\kappa_x+p)^2+(\kappa_y+q)^2`.
The fixed-mode kinetic difference is second order in :math:`h`, but the comparator
performs no extrapolation.  Pointwise potential sampling follows discrete Fourier
arithmetic modulo :math:`N`; the isometry condition does not by itself prevent every
pairwise potential-transfer alias for every permitted cutoff/grid pair.

The result reports :math:`\lVert T^\dagger T-I\rVert_{\mathrm F}`,
:math:`\lVert\Delta H\rVert_{\mathrm F}`, and
:math:`\max_{ij}|\Delta H_{ij}|`.  These are representation-disagreement diagnostics,
not estimates of parent-model error or scientific validation.  The Frobenius norm is
not normalized by rank, so cross-cutoff comparisons require a separately declared
protocol.

Compatibility prerequisites
---------------------------

The request rejects comparison unless both represented results have:

* the same exact ``Periodic2DCosinePotentialToyModel`` values;
* the same reduced Bloch momentum;
* the same dimensionless period-:math:`2\pi` geometry, energy scale, fixed energy zero,
  and spinless scalar convention supplied by those concrete result types;
* declared ``p``-outer, ``q``-inner and ``x``-outer, ``y``-inner orderings; and
* a finite-difference point count satisfying :math:`2M+1\leq N`.

Equal matrix sizes alone are neither required nor sufficient.  The comparison map is
rectangular when :math:`N>2M+1` and square at equality; in both cases the two matrices
become subtractable only after the declared map places them in the plane-wave common
space.

Algorithm and data flow
-----------------------

#. Validate the two complete represented results and comparison identity.
#. Build one normalized one-dimensional sampling matrix for each reciprocal direction.
#. Form their Kronecker product in the declared two-dimensional order.
#. Transport the coordinate-grid operator by :math:`T^\dagger H_{\mathrm{FD}}T`.
#. Subtract the plane-wave operator and compute threshold-free diagnostics.
#. Store all arrays in immutable ``complex128`` quantity records and retain the exact
   request.
#. Validate in the Result that the retained transported matrix equals
   :math:`T^\dagger H_{\mathrm{FD}}T`, that the signed difference is correlated, and
   that every diagnostic is recomputed from retained values.

The Action owns construction of the request-dependent sampling map.  Result validation
does not reconstruct that map or establish that the Action produced a manually
constructed Result.  It does repeat the dense congruence product from retained
:math:`T` and :math:`H_{\mathrm{FD}}` so a forged transport cannot be hidden behind
consistent downstream values.  Manual construction proves only intrinsic structure
and algebra, not execution provenance or scientific evidence.

Units, types, and numerical behavior
------------------------------------

The current toy-model operators and all comparison outputs are dimensionless.  Public
inputs require exact represented-result classes and a nonempty string identity; no
array or scalar coercion is performed at this boundary.  The matrix products use
binary64 complex arithmetic.  Transport, subtraction, or diagnostic overflow raises
``OverflowError`` rather than retaining nonfinite output.  With
:math:`G=N^2` and :math:`P=(2M+1)^2`, the map stores :math:`GP` complex values and one
implemented congruence costs :math:`O(PG^2+P^2G)`.  Result correlation repeats that
congruence once.  Dense workspaces can exhaust memory; no sparse fallback or hidden
size cap is applied.

No diagnostic threshold, monotonic-convergence expectation, or pass/fail classification
is embedded.  Callers that compare a sequence of grids own any trend analysis and must
keep discretization error distinct from parent-model and model-reduction error.

Implementation and evidence mapping
-----------------------------------

* Specification:
  ``specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md``
* Source:
  ``python/src/ksdft2effmass/periodic2d/compare/common_space.py``
* Software verification:
  ``python/tests/software_verification/ksdft2effmass/periodic2d/compare/``
* Numerical verification:
  ``python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/``
* Represented operators:
  :doc:`/api/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves`

The equality-boundary oracle uses :math:`M=2,N=5` and checks both
:math:`T^\dagger T=I` and :math:`TT^\dagger=I` to distinguish the supported square
unitary case from proper rectangular compression.  The remaining numerical oracle
independently evaluates the centered-difference dispersion

.. math::

   \epsilon^{\mathrm{FD}}_{pq}
   = \frac{4}{h^2}\left[
       \sin^2\!\frac{(\kappa_x+p)h}{2}
       +\sin^2\!\frac{(\kappa_y+q)h}{2}
     \right]

for free and cosine-potential cases.  The cosine test checks that resolved potential
Fourier blocks agree after transport, leaving only the analytical diagonal kinetic
discretization error.  This is numerical verification of the declared finite
mathematics, not material validation.

Reference and provenance
------------------------

* Bloch, F., “Über die Quantenmechanik der Elektronen in Kristallgittern,”
  *Z. Phys.* **52**, 555–600 (1929). DOI: ``10.1007/BF01339455``.
* Cooley, J. W. and Tukey, J. W., “An Algorithm for the Machine Calculation of
  Complex Fourier Series,” *Math. Comp.* **19**, 297–301 (1965). DOI:
  ``10.1090/S0025-5718-1965-0178586-1``.
* The Bloch citation supplies historical context for Bloch-form states; it does not
  validate this toy parent, finite representations, or scientific use.
* The Cooley--Tukey citation supplies historical discrete-Fourier context.  This
  implementation evaluates phases and dense products directly and does not implement a
  Cooley--Tukey FFT; the citation does not validate its rounding, aliasing, complexity,
  or correctness.
* The sampling-map orientation, finite-difference pullback/compression direction,
  square-boundary behavior, compatibility checks, sign, diagnostics, and threshold-free Result contract are
  repository-derived conventions documented in the project specification.

Limitations
-----------

The comparator currently supports only the campaign's square period-:math:`2\pi`
cosine model, equal grid counts in both directions, one symmetric square plane-wave
cutoff, and full dense operators.  It does not align unrelated models, repair gauge or
energy-reference differences, interpolate eigenvectors, compare selected subspaces,
construct Wilson loops, serialize results, or establish convergence.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d

.. autoclass:: Periodic2DCommonSpaceComparisonRequest
   :members:

.. autoclass:: Periodic2DCommonSpaceComparisonResult
   :members:

.. autoclass:: Periodic2DCommonSpaceOperatorComparator
   :members:
