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

The retained scalar family is a controlled synthetic, topologically trivial example.
Passing checks establish only the documented finite software and numerical contracts.
They do not establish a continuum limit, a two-dimensional material model, silicon
behavior, production Wannier localization, scientific validation, transferability, or
uncertainty quantification. Composite gauges, topological benchmark models, external
Wannier90 evidence, optimizer-basin studies, and impurity-defect stages remain separate
capabilities rather than being folded into this isolated campaign.
