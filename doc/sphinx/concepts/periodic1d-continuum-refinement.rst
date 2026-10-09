Periodic-1D continuum-refinement numerics
==========================================

Scientific scope
----------------

The separated continuum-refinement campaign is a controlled synthetic comparison of a
finite scalar lattice parent and its parabolic band-edge comparator.  It asks whether a
*declared finite sequence* satisfies frozen numerical criteria after continuum
resolution, finite domain, periodic images, represented lattice scale, and defect
profile are varied independently.

The authoritative calculation contract is
``calculations/research-monograph/impurity-defect-1d-continuum-refinement/protocol.md``.
The retained result and its interpretation are ``result.json`` and ``report.md`` in the
same directory.  This page explains their numerical logic; it does not replace them or
turn their finite observations into an asymptotic theorem.

The campaign is synthetic numerical-verification evidence.  It is not a silicon donor
model, a DFT or Wannier90 calculation, scientific validation, transferability evidence,
uncertainty quantification, or an acceptance decision.

Parent dispersion and the scale parameter
-----------------------------------------

The accepted scalar hoppings :math:`t_R` define

.. math::

   E_{\mathrm{lat}}(k)=\sum_R t_R\exp(2\pi i kR),

with lower edge and quadratic coefficient

.. math::

   E_0=\sum_R t_R,
   \qquad
   \alpha=-\frac12\sum_R(2\pi R)^2t_R.

On a periodic physical domain of length :math:`L`, centered Fourier mode :math:`m` has
physical reduced wave number :math:`q_m=m/L`.  The continuum comparator is

.. math::

   E_{\mathrm{cont}}(q_m)=E_0+\alpha q_m^2.

At represented lattice spacing :math:`a`, the scaled lattice parent is

.. math::

   E_a(q_m)=E_0+
   \frac{E_{\mathrm{lat}}(a q_m)-E_0}{a^2}.

Subtracting the common edge and dividing by :math:`a^2` preserve the physical
band-edge curvature while the represented lattice spacing changes.  This is the
campaign's changing-scale operation.  Broadening a defect while keeping
:math:`a=a_{\mathrm{ref}}` is a different operation and is not called lattice
refinement.

Energies are expressed in :math:`E_G`, lengths in :math:`a_{\mathrm{ref}}`, and both
routes use the same centered Fourier-mode ordering and energy reference before any
matrix subtraction.  The retained coefficient is
:math:`\alpha=0.6519378386943853 E_Ga_{\mathrm{ref}}^2`; it belongs to the frozen
synthetic parent rather than to a claimed material.

Defect normalization families
-----------------------------

For fixed integrated magnitude :math:`g=0.30E_Ga_{\mathrm{ref}}`, the periodized
Gaussian has analytical Fourier coefficients

.. math::

   V_\ell=-\frac{g}{L}
   \exp\!\left[-2\pi^2\sigma^2\left(\frac{\ell}{L}\right)^2\right].

The fixed-peak family instead holds :math:`V_0=0.12E_G` constant, so its integrated
magnitude is :math:`V_0\sqrt{2\pi}\sigma`.  Increasing width therefore has different
scientific meaning in the two families:

* fixed-integrated broadening redistributes a constant integrated strength; and
* fixed-peak broadening increases integrated strength and can create additional shallow
  levels.

The continuum route uses analytical Fourier coefficients.  The lattice route samples
the periodized profile at lattice sites, builds a site-diagonal potential, and
transforms it to the declared Fourier coordinates.  The routes are not assumed equal by
construction; they are compared only after explicit finite-space alignment.

Separated refinement axes
-------------------------

The campaign keeps five operations distinct.

``continuum mesh``
   Mode counts 64, 96, 128, 192, and 256 vary at fixed
   :math:`L=64a_{\mathrm{ref}}`, :math:`\sigma=2a_{\mathrm{ref}}`, and
   fixed-integrated normalization.  This targets finite Fourier truncation.

``continuum domain``
   :math:`L/a_{\mathrm{ref}}=32,48,64,96,128` varies while the spectral spacing
   :math:`L/M=0.25a_{\mathrm{ref}}` and profile remain fixed.  This targets finite
   domain and boundary-localization effects without coarsening the represented spacing.

``lattice supercell``
   Site counts 32, 48, 64, 96, and 128 vary at fixed
   :math:`a=a_{\mathrm{ref}}` and fixed profile.  This targets periodic-image and
   finite-supercell effects, not the lattice-spacing limit.

``lattice scale``
   :math:`a/a_{\mathrm{ref}}=1,1/2,1/4,1/8` varies at fixed physical domain and
   profile.  The represented dimension changes so the physical domain does not.  This
   is the bounded changing-scale comparison.

``profile width``
   :math:`\sigma/a_{\mathrm{ref}}=0.5,1,2,4,8,12` varies at fixed original lattice
   spacing and :math:`L=128a_{\mathrm{ref}}`.  Fixed-integrated and fixed-peak families
   are evaluated separately.

No axis substitutes for another.  In particular, mesh refinement is not an
infinite-domain limit, supercell enlargement is not lattice-spacing refinement, and
profile broadening is not a continuum limit.

Finite operators and dense eigensolves
--------------------------------------

For each finite mode set, the continuum Hamiltonian is the diagonal parabolic parent
plus the convolution matrix of the analytical profile.  The lattice Hamiltonian is the
scaled lattice dispersion plus the Fourier-transformed sampled site potential.  Both
matrices must be finite and Hermitian.

The workflow uses dense Hermitian eigensolves.  A represented dimension :math:`M`
requires :math:`O(M^2)` matrix storage and conventionally :math:`O(M^3)` dense
eigensolver work.  Completion of this finite computation establishes neither
convergence nor physical adequacy.

The signed represented difference is fixed as

.. math::

   D=H_a-H_{\mathrm{cont}}.

The common basis ordering, domain, energy unit, and energy reference are checked before
forming :math:`D`; dimensions or spectra alone are not accepted as state-space
identity.

Spectral and state diagnostics
------------------------------

The campaign retains the lowest energy, its binding relative to :math:`E_0`, and the
number of eigenvalues below the edge by more than the declared margin.  Count agreement
is separate because a small lowest-state energy error can coexist with a different
finite bound-state spectrum.

A discrete inverse Fourier transform supplies a periodic coordinate-space state.
Boundary probability is the weight at coordinate distances at least :math:`L/4` from
the profile center.  It diagnoses finite-domain localization for this represented
problem; it is not an infinite-volume decay theorem.

Direct subtraction of eigenvectors would depend on their arbitrary global phases.
For compatible lowest states :math:`\psi_a` and :math:`\psi_c`, the campaign therefore
uses fidelity

.. math::

   F=\frac{|\langle\psi_a,\psi_c\rangle|^2}
   {\langle\psi_a,\psi_a\rangle\langle\psi_c,\psi_c\rangle}

and rank-one projector distance

.. math::

   \lVert |\psi_a\rangle\langle\psi_a|
   -|\psi_c\rangle\langle\psi_c|\rVert_F=\sqrt{2(1-F)}.

Roundoff-level excursions of :math:`F` are clipped to :math:`[0,1]`.  This removes a
global phase ambiguity but does not define matching for a degenerate multiplet.  The
retained state claim is limited to the lowest nondegenerate state.

Operator and momentum-sector diagnostics
----------------------------------------

Let :math:`P` select the physical low-momentum sector
:math:`|q|\le0.25/a_{\mathrm{ref}}`.  The campaign reports separately

.. math::

   \lVert PDP\rVert_2,
   \qquad
   \lVert PD(I-P)\rVert_2.

The compressed norm measures the parent-plus-defect discrepancy within the declared
low sector.  The cross norm measures cross-sector coupling between that sector and its
represented complement.  As written, :math:`PD(I-P)` maps complement inputs into
low-sector outputs.  Because :math:`D` is Hermitian, its adjoint
:math:`(I-P)DP` maps in the opposite direction and has the same spectral norm.  The
compressed norm is computed from the largest absolute Hermitian eigenvalue; the cross
norm from the largest singular value of the rectangular cross block.

The outer-Brillouin state weight is

.. math::

   \sum_{|aq_m|\ge0.25}|\psi_a(m)|^2.

Binding error, bound-state count, projector defect, compressed residual, cross
residual, and Brillouin-edge weight are not interchangeable.  A state may have small
binding and projector errors while the represented low-sector operators still differ
beyond the frozen criterion.

Frozen decision rules
---------------------

Supporting continuum-mesh evidence requires final binding change no larger than
:math:`10^{-10}E_G` and final projector defect no larger than :math:`10^{-6}`.
Continuum-domain and lattice-supercell support each require final binding change no
larger than :math:`10^{-8}E_G` and boundary probability no larger than
:math:`10^{-8}`.

A lattice/continuum point passes only when all six criteria hold:

* relative binding error no larger than :math:`10^{-3}`;
* projector defect no larger than :math:`10^{-2}`;
* compressed residual no larger than :math:`10^{-3}E_G`;
* cross residual no larger than :math:`10^{-3}E_G`;
* outer-Brillouin weight no larger than :math:`10^{-4}`; and
* exact agreement of below-edge bound-state counts.

The lattice-scale boundary is the largest tested spacing whose point and every finer
point pass.  A profile crossover is the smallest tested width whose point and every
broader point pass.  This persistent-tail rule prevents an isolated passing point from
being promoted to a boundary.  The thresholds were frozen before evaluation and are
campaign decisions, not universal physical tolerances.

Retained finite result
----------------------

The retained result reports passing continuum-mesh, continuum-domain, and
lattice-supercell support axes.  At fixed physical profile, every comparison criterion
passes from :math:`a=0.5a_{\mathrm{ref}}` through the finest tested spacing
:math:`0.125a_{\mathrm{ref}}`.  This supports a persistent pass over that finite tested
sequence, not a proof as :math:`a\to0`.

At the original spacing, neither profile family defines a crossover over the tested
widths.  Spectral and projector diagnostics improve for broad profiles, but the
compressed parent-dispersion residual remains
:math:`3.78\times10^{-3}E_G`, above the frozen :math:`10^{-3}E_G` criterion.  The
fixed-peak family can also change the number of shallow levels because its integrated
strength grows with width.

The reasoning consequence is important: state-level agreement for a selected bound
state does not imply operator-level agreement, and profile broadening does not replace a
changing-lattice-scale study.

Independent reconstruction
--------------------------

The verifier does not import the maintained runner.  Whereas the runner constructs the
lattice matrix directly in Fourier coordinates, the verifier assembles hopping and the
sampled defect in site coordinates and Fourier-transforms the complete matrix.  It
reconstructs the continuum matrix entry by entry, then repeats all eigensolves,
projector comparisons, operator partitions, criteria, boundary decisions, and content
digests.

Canonical matrix digests round real and imaginary coordinates to
:math:`10^{-9}E_G` only to stabilize byte identity across independently ordered
floating-point operations.  All numerical comparisons use unrounded matrices.  Digest
agreement is quantized content identity; it is not exact arithmetic, execution
provenance, validation, or acceptance.

This is implementation independence inside one declared synthetic model.  It is not
independent experimental or material evidence.

Error-accounting discipline
---------------------------

The campaign keeps these channels separate:

* continuum discretization -- mode-count refinement;
* finite domain -- domain refinement at fixed spectral spacing;
* periodic images -- supercell enlargement at fixed lattice spacing;
* represented lattice scale -- fixed-profile spacing sequence;
* profile model -- separate normalization families;
* operator approximation -- compressed and cross residuals;
* spectral behavior -- binding and count;
* state behavior -- rank-one projector and edge weight; and
* floating-point reproducibility -- independent reconstruction and quantized digests.

None establishes scientific adequacy.  The calculation performs no material
validation, transferability assessment, or uncertainty quantification.

Literature and claim boundaries
-------------------------------

Koster and Slater (1954) provide historical finite-rank impurity context.  Hoefer and
Weinstein (2011) and Duchêne, Vukićević, and Weinstein (2015) motivate explicit weak,
slow, near-edge scaling.  Nakamura and Tadano (2021) motivate explicit changing-space
and lattice-spacing control.  König, Lee, and Hammer (2011) motivate keeping
finite-volume effects separate.  Kohn and Luttinger (1955) and Gamble *et al.* (2015)
mark the multivalley and central-cell boundary for semiconductor donor models.

Those works motivate the campaign's distinctions; their theorem hypotheses and
material conclusions are not asserted for this finite scalar parent.  Exact
bibliographic identities, access classifications, and supported claim fragments are
retained under ``docs/research/literature-reviews/impurity-defect-1d``.

Software ownership boundary
---------------------------

``ContinuumRefinementEncodedDocuments`` stores exact input and retained-result bytes.
``ContinuumRefinementCampaignResultDocument`` separately stores one exact result wire
and derives SHA-256 directly from it.  Neither owns the operators, scales, diagnostics,
criteria, provenance, or scientific interpretation described above.  Retained
correlation receives an explicit
repository root at execution, while independent verification owns one in
``ContinuumRefinementVerificationRequest``.  Neither a path nor a SHA-256 digest is
used to infer scientific meaning.

See :doc:`periodic-1d-defect-extraction` for the wider defect-campaign sequence and
:ref:`continuum-refinement-api` for the public encoded-document and campaign routes.
