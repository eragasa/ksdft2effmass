Periodic2d controlled reduction
===============================

The isolated periodic2d campaign integrates the retained scalar controlled exercise
without changing its version-one input or result. Its current public DataObject owns
exact input and result bytes, correlation reproduces the canonical retained document,
and an independent route reconstructs represented operators and diagnostics. This is
partial coverage rather than parity with periodic1d: typed stress controls, reusable
gauge and hopping-route Actions, granular result records, and complete serializers
remain required by the periodic2d parity gate.

Represented toy model
---------------------

``Periodic2DCosinePotentialToyModel`` owns the reusable spinless dimensionless
potential

.. math::

   V(x,y) = \lambda_x\cos x + \lambda_y\cos y
            + \lambda_{xy}\cos x\cos y

on the square cell of period :math:`2\pi`. The model exposes PhysKit
``DirectLattice2D`` and ``ReciprocalLattice2D`` objects. Their primitive vectors are
columns of :math:`A` and :math:`B`, with

.. math::

   B = 2\pi A^{-\mathsf T},
   \qquad
   A^{\mathsf T}B = 2\pi I.

For this fixed model, :math:`A=2\pi I` and :math:`B=I`. A reduced momentum
:math:`\boldsymbol\kappa` and reciprocal index :math:`\mathbf n=(p,q)` therefore
produce the kinetic diagonal
:math:`\lVert B(\boldsymbol\kappa+\mathbf n)\rVert^2`; the familiar
:math:`(\kappa_x+p)^2+(\kappa_y+q)^2` is its square-cell specialization.

The campaign plane-wave adapter delegates matrix construction to the reusable
``PlaneWaveBlochHamiltonian2DConstructor`` documented in
:doc:`../api/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves`. That
Action owns the general finite Fourier inventory, PhysKit lattice duality check,
reduced-to-Cartesian reciprocal map, and represented operator result; the campaign
retains only its cosine coefficients and provenance policy.

``CenteredUniformReciprocalMesh2D`` and the neighbor records now make half-open
reciprocal sampling, positive-direction wrapping, and integer boundary translations
explicit. ``PlaneWaveReciprocalSewing2DConstructor`` maps a wrapped momentum fiber by
shifting reciprocal coefficients without wrapping the finite basis itself: coefficients
leaving the retained cutoff are discarded. See
:doc:`../api/ksdft2effmass/analysis/model_systems/periodic2d/reciprocal_mesh`.
This distinction separates periodic mesh topology from finite-basis truncation.

``Periodic2DCommonSpaceOperatorComparator`` now samples the retained plane waves on
the coordinate grid and evaluates
:math:`T^\dagger H_{\mathrm{FD}}T-H_{\mathrm{PW}}` only after checking model,
momentum, geometry, energy, spin, ordering, and alias preconditions. It returns the
isometry defect and operator norms without an acceptance threshold; see
:doc:`../api/ksdft2effmass/campaigns/periodic2d/common_space`.

Separate Actionizers construct finite plane-wave and centered Bloch finite-difference
Hamiltonians. ``Periodic2DPlaneWaveBasis`` owns reciprocal pairs ``(p,q)`` in
``p``-outer, ``q``-inner order, while ``Periodic2DUniformCellGrid`` owns period,
spacing, and ``x``-outer, ``y``-inner site order. The requests combine those finite basis identities
with the model and momentum fiber; the finite-difference request additionally exposes
positive Bloch seam phases. Each represented result retains the exact request
that identifies its model, momentum fiber, ordering, and finite dimension. The
plane-wave result also retains the maximum direct--reciprocal duality residual. Public
momenta and sizes accept only their documented built-in ``float`` and ``int`` types;
booleans, numeric strings, and NumPy scalar substitutes are rejected rather than
coerced. The model owns no retained paths, acceptance thresholds, provenance, or
material interpretation.

Campaign boundary
-----------------

``Periodic2DIsolatedBandCampaign`` composes the exact retained-wire model with separate
correlation and verification Actionizers. Correlation establishes semantic and byte
identity only. Verification separately authenticates the retained input and historical
runner identities and reconstructs the plane-wave cutoff sequence, finite-difference
sequence, separable Kronecker identities, degenerate projectors, coupling sequence,
sewn-link topology, hopping shells, effective-mass tensors, and anisotropy control.
The independent verifier imports neither the maintained calculation Workflow nor the
reusable toy-model constructors.

Composite projected-gauge campaign
----------------------------------

``Periodic2DCompositeCampaign`` applies the same retained DataObject, correlation, and
independent-verification structure to the isolated lowest-three-band group. It keeps
the smooth projected gauge and deterministic rough internal gauge separate while
comparing gauge-invariant spectra, Chern sums, and Wilson eigenphase sets. Localization
spreads and matrix-valued hopping locality remain gauge-dependent diagnostics rather
than invariants. The independent verifier reconstructs polar projection, reciprocal
links, hopping blocks, and finite-supercell density moments without importing the
maintained calculation or toy-model constructor.

Topological benchmark campaign
------------------------------

``Periodic2DTopologicalCampaign`` retains Qi--Wu--Zhang, flux-one-third
Hofstadter, and Haldane benchmarks as three separate represented state spaces.
Each model includes a nonzero-Chern case, a trivial control, finite-mesh
refinement, Wilson-loop winding, a gauge attack, and source authentication. The
campaign does not combine errors between models or identify any benchmark with
the scalar cosine parent. Nonzero Chern and Wilson diagnostics are bounded
numerical obstruction evidence, not a general mathematical proof or material
validation.

Topological parameter sweeps
----------------------------

``Periodic2DTopologicalPhaseSweepCampaign`` keeps the Qi--Wu--Zhang mass,
Hofstadter superlattice-amplitude, and Haldane sublattice-mass axes separate.
Every retained sample records the represented gap and band Chern diagnostics;
the independent route reconstructs them with projector Bargmann loops. Analytic
sector expectations are applied only to the declared Qi--Wu--Zhang and Haldane
boundaries, while the Hofstadter transition remains a sampled numerical bracket.
The results are not combined into a material phase diagram or exact transition
theorem.

Portable Wannier90 comparison
------------------------------

``Periodic2DWannier90BalancedCampaign`` verifies the compact repository-retained
representation of one completed rank-three Wannier90 comparison. The independent
route authenticates the extractor source and reconstructs the plane-wave parent,
polar projected frame, represented operators, bounded alignment search, hopping
blocks, shell tails, and finite-supercell localization diagnostics without accessing
native external-run files. ``Periodic2DWannier90StudyCampaign`` applies the same portable reconstruction to
six retained mesh, plane-wave-cutoff, and auxiliary-embedding cases. The axes remain
separate and preserve the calculated nonmonotone sensitivity and alternate-basin
evidence. Portable verification does not rerun Wannier90, authenticate absent native
files, establish mesh, cutoff, or embedding convergence, or support a material claim.

Optimizer-basin outcomes
------------------------

``Periodic2DOptimizerBasinCampaign`` verifies the repository-retained nine-
configuration, eight-start study without reading its external execution directory. It
requires every completed endpoint, partitions all 51 converged outcomes into the
retained observed basins, preserves all 21 iteration-bound stops, and reconstructs the
failed repeated-basin and finest-pair convergence disposition. An observed basin is a
finite endpoint classification, not proof of a distinct local minimum or a global
optimizer result.

``Periodic2DOptimizerReanalysisCampaign`` separately checks the native invariant
spread :math:`\Omega_I`, gauge-dependent spread
:math:`\widetilde{\Omega}=\Omega_D+\Omega_{OD}`, post-hoc terminal-trace classes,
:math:`D_4`-quotiented observed basins, and four retained common-estimator grid
refinements. The portable verifier authenticates estimator inputs but does not replay
the unavailable native Wannier90 traces or wavefunctions. The reanalysis remains
descriptive and preserves the negative convergence conclusion.

``Periodic2DOptimizerStandaloneCampaign`` extends the retained endpoint accounting to
256 initial localizations and 120 exact-checkpoint continuations. It preserves all
60 final nonconverged outcomes, density-aware :math:`D_4` basin partitions, post-hoc
exact-equivalence controls, density-threshold sensitivity, and the missing
pre-execution tolerance control as a protocol deviation. The campaign verifies the
retained transition and classification arithmetic without reading native run roots.

``Periodic2DOptimizerRegressionCampaign`` retains all 60 nonconverged endpoints as
right-censored observations in an exploratory log-normal model. Its independent
route reconstructs the likelihood, score, start-clustered covariance, adjusted time
ratios, model intervals, and finite-iteration probability curves. These intervals
summarize retained synthetic trajectories; they are not causal effects, population
sampling intervals, physical uncertainty, or predictions of DFT behavior.

The retained scalar family is a controlled synthetic, topologically trivial example.
Passing checks establish only the documented finite software and numerical contracts.
They do not establish a continuum limit, a two-dimensional material model, silicon
behavior, production Wannier localization, scientific validation, transferability, or
uncertainty quantification. Composite gauges, topological benchmark models, external
Wannier90 evidence, optimizer-basin studies, and impurity-defect stages remain separate
capabilities rather than being folded into this isolated campaign.

Direct references
-----------------

- Bloch, F., “Über die Quantenmechanik der Elektronen in Kristallgittern,”
  *Z. Phys.* **52**, 555–600 (1929). DOI: ``10.1007/BF01339455``.
- Chelikowsky, J. R., Troullier, N. and Saad, Y.,
  “Finite-Difference-Pseudopotential Method: Electronic Structure Calculations
  without a Basis,” *Phys. Rev. Lett.* **72**, 1240–1243 (1994).
  DOI: ``10.1103/PhysRevLett.72.1240``.
- Marzari, N. and Vanderbilt, D., “Maximally Localized Generalized Wannier
  Functions for Composite Energy Bands,” *Phys. Rev. B* **56**, 12847–12865
  (1997). DOI: ``10.1103/PhysRevB.56.12847``.
- Fukui, T., Hatsugai, Y. and Suzuki, H., “Chern Numbers in Discretized
  Brillouin Zone: Efficient Method of Computing (Spin) Hall Conductances,”
  *J. Phys. Soc. Jpn.* **74**, 1674–1677 (2005).
  DOI: ``10.1143/JPSJ.74.1674``.
- Yates, J. R., Wang, X., Vanderbilt, D. and Souza, I., “Spectral and Fermi
  Surface Properties from Wannier Interpolation,” *Phys. Rev. B* **75**,
  195121 (2007). DOI: ``10.1103/PhysRevB.75.195121``.
- Soluyanov, A. A. and Vanderbilt, D., “Computing Topological Invariants
  without Inversion Symmetry,” *Phys. Rev. B* **83**, 235401 (2011).
  DOI: ``10.1103/PhysRevB.83.235401``.
