Periodic-2D controlled reduction
================================

The isolated periodic-2D campaign integrates the retained scalar controlled exercise
without changing its version-one input or result. Its public DataObject mirrors the
periodic-1D campaign structure: an immutable model owns exact input and result bytes,
a correlator reproduces the canonical retained document, and an independent verifier
reconstructs the represented operators and diagnostics.

Represented toy model
---------------------

``Periodic2DCosinePotentialToyModel`` owns the reusable spinless dimensionless
potential

.. math::

   V(x,y) = \lambda_x\cos x + \lambda_y\cos y
            + \lambda_{xy}\cos x\cos y

on the square cell of period :math:`2\pi`. Separate Actionizers construct finite
plane-wave and centered Bloch finite-difference Hamiltonians. Plane-wave ordering is
``p`` outer and ``q`` inner. Finite-difference ordering is ``x`` outer and ``y`` inner.
The model owns no retained paths, acceptance thresholds, provenance, or material
interpretation.

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

The retained scalar family is a controlled synthetic, topologically trivial example.
Passing checks establish only the documented finite software and numerical contracts.
They do not establish a continuum limit, a two-dimensional material model, silicon
behavior, production Wannier localization, scientific validation, transferability, or
uncertainty quantification. Composite gauges, topological benchmark models, external
Wannier90 evidence, optimizer-basin studies, and impurity-defect stages remain separate
capabilities rather than being folded into this isolated campaign.
