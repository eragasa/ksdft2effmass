# Band-equivalence and hopping-locality dimensional extension

## Purpose

This sequence extends one controlled rank-two scientific question across periodic
dimension without turning dimensional realizations into versions of one experiment.

1. The maintained 1-D family supplies the analytic and implemented predecessor.
2. The square-lattice 2-D family introduces complete square displacement orbits and a
   two-line cyclic Nyquist boundary.
3. The separate graphene-inspired 2-D family introduces a triangular non-orthogonal
   metric, two-site honeycomb basis, dependent Bravais control orbit, metric-complete
   shells, basis-aware distances, and primitive-basis covariance.
4. The simple-cubic 3-D family introduces complete cubic displacement orbits, a
   three-plane cyclic Nyquist boundary, and explicit resource scaling.
5. The separate silicon-inspired 3-D family combines an FCC non-orthogonal metric,
   two-site diamond basis, dependent Bravais control orbit, metric-complete shells,
   basis-aware distances, primitive-basis covariance, and the 3-D resource boundary.

There is no distinct 1-D non-orthogonal geometry: a one-vector primitive basis has no
inter-vector angle. The 1-D family instead supplies specialization fixtures for shared
behavior.

## Family identities

```text
ksdft2effmass.campaign.model-adequacy.periodic1d.band-equivalence-versus-hopping-locality
ksdft2effmass.campaign.model-adequacy.periodic2d.band-equivalence-versus-hopping-locality
ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal.band-equivalence-versus-hopping-locality
ksdft2effmass.campaign.model-adequacy.periodic3d.band-equivalence-versus-hopping-locality
ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal.band-equivalence-versus-hopping-locality
```

Each family owns an independent protocol, version sequence, run identity, evidence
package, thresholds, convergence result, and interpretation. A publication may compare
them without becoming their identity owner.

## Shared analytic structure

For dimension `d`, the prospective hypercubic children use

```math
K_\rho^{(d)}(\mathbf q)=T_0+\frac{\rho}{d}
\sum_{\alpha=1}^{d}
\left(e^{2\pi iq_\alpha}T_+ + e^{-2\pi iq_\alpha}T_-\right),
```

and

```math
U_a^{(d)}(\mathbf q)=R\!\left(
\frac a d\sum_{\alpha=1}^{d}\sin(2\pi q_\alpha)
\right).
```

At the flat endpoint,

```math
\mu_{\max}^{(d)}(a)=J_0(2a/d)^d.
```

At $d=1$, these equations reduce exactly to the maintained 1-D parent homotopy and sine
rotation. The onsite and directed hopping matrices, $\rho$ and $a$ meanings, retained
rank, continuous global $SO(2)$ restriction, spectral channels, and error decomposition
remain unchanged. Reconstructed-Hamiltonian maximum/RMS channels now exist in the 1-D
development implementation but remain subject to dimension-general contract review.
Only lattice dimension, periodic-frame construction, Fourier indexing, Nyquist boundary,
support geometry, mesh scaling, and resource policy change.

The exact rank-two common-curvature geometry and Parseval residual/locality theorem are
dimension independent. The higher-dimensional protocols additionally expose the
finite-space factorization

```math
\mathcal H_{p,N}^{(d)}=(\mathbb C^N)^{\otimes d}\otimes\mathbb C^4,
```

construct lattice translations with Kronecker products, and use the centered tensor
Fourier transform to relate the cell--orbital, complete Bloch, spectral-eigensystem,
retained-frame, and Wannier/TB representations. The orbital fiber remains four-
dimensional. Hamiltonian subtraction requires an explicit frame, projector lift, or
gauge alignment; eigenvalue arrays and matrices on unequal spaces are never directly
subtracted. Numerical controls and retained evidence are not shared, and cross-
dimensional values are not treated as directly subtractable.

## Coherence contract

| Scientific element | Preserved from 1-D | Dimension-specific extension |
|---|---|---|
| Parent | Same `T0`, `T+`, `T-`, and bounded `rho` homotopy | Equal `1/d` hopping contribution and Kronecker lattice translation on every axis |
| Representation bridge | Same complete Bloch field and finite Fourier signs | Explicit tensor lattice space, complete eigensystem map, projector lift, and Wannier/TB operator |
| Retained model | Lowest rank-two projector and qualified periodic frame | Torus traversal, boundary sewing, and path/plaquette consistency |
| Gauge | Same sine rotation, maximum angle `a`, and continuous global `SO(2)` restriction | Normalized sum over axes |
| Exact theory | Same common-curvature loss and Parseval residual/locality identity | Flat correlation `J_0(2a/d)^d` |
| Fourier evidence | Same finite-interpolant semantics and Parseval check | Vector indices and Nyquist boundary hyperplanes |
| Truncation | Same explicit conjugate-closed retained-model identity | Complete square/cubic support shells and block counts |
| Accuracy | Separate parent reconstruction, covariant representation, restricted alignment, conversion, interpolation, truncation, and total channels | Dimension-qualified operator normalizations and disjoint tensor meshes |
| Decisions | Same pointwise primary claim and `converged`/`unresolved` outcomes | Dimension-qualified mesh, shell, and resource caps |
| Verification | Independent reconstruction, not producer reuse | Independent orbit, boundary, frame, and cutoff reconstruction |

Shared implementation factors only behavior demonstrated to be dimension and geometry
independent. `geometry.py` consumes PhysKit-owned direct-lattice metrics, Cartesian
mapping, exact integral operations, and lattice-displacement transformation. Alignment
consumes Optimization's batched unitary Procrustes owner, while centered uniform-mesh
matrix transforms, bounded or tensor-product Fourier evaluation, Parseval arithmetic,
and twisted/ordinary Hermiticity diagnostics come directly from Numerics. KSD retains
shell scaling and complete physical-metric support selection, selected covariance
probes, state-space meaning, positive splitting-scale policy, retained-rank and energy
normalization, path/plaquette inventory, scientific thresholds, and evidence
disposition. Immutable family controls are owned by `definitions.py`; plain calculated
scientific values are owned by `analysis.py` and `results/`; and retained wire
projections are owned by `result.py` and `records/`. `fourier.py` retains only the KSD
error channels and complete-shell composition over owner evaluation contracts. The
analysis recorder binds completed scientific results to exact canonical requests.
Plotting consumes plain analysis values, while lifecycle verification and rendering
consume retained typed records without moving scientific calculations into wire or
rendering code. Software-verification tests enforce these boundaries while the package
root preserves only deliberate public imports.

All experiment packages retain separate definitions, controls, schemas, versions, runs,
and evidence packages. Their required comparable software-test layers
and diagnostic categories are defined in the
[test and diagnostic parity contract](band-equivalence-test-and-diagnostic-parity.md).

## Cross-protocol comparison composition

The publication-independent source root
[`experiments/model-adequacy/band-equivalence-dimensional-comparison/`](../../../../../experiments/model-adequacy/band-equivalence-dimensional-comparison/)
composes typed diagnostics from the four Paper 2 family requests. It may calculate
componentwise cross-family display envelopes and render comparison figures, but it does
not own family geometry, scientific parameters, thresholds, convergence dispositions,
canonical artifacts, runs, or evidence. Its current tolerance-requirement map deliberately
omits an acceptance region until each family has justified and frozen its scientific
limits.

## Stage gates

The 2-D family must review and freeze its finite spaces, basis order, Fourier convention,
projector lift, aligned-subtraction contract, parent gaps, field covariance, support-orbit
inventory, Nyquist conversion, sample roles, shell caps, tolerances, schemas, and
verifier before implementation. The 3-D family is sequenced after that review and must additionally
freeze resource bounds and a cubic 48-operation support inventory.

The existing isotropic/anisotropic hopping-support ladder is a separate scalar model-
adequacy sequence. Its reviewed lattice and orbit capabilities may be reused directly
from their owners, but its experiment identities and scientific results are not
inherited.

## Bounded interpretation

The sequence studies synthetic representation cost after truncation. It does not
establish physical inequivalence of complete gauge-related Hamiltonians, validate a
square or cubic material, or transfer thresholds to silicon or another material system.
