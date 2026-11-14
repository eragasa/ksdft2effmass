# `ksdft2effmass.hopping_locality`

## Status

The nominal scientific owner is implemented in
`python/src/ksdft2effmass/hopping_locality/`. Its current bases identify diagnostics on
unchanged hopping coefficients and require concrete owners to declare coefficient index
space, support geometry, basis, gauge, normalization, and range inventory.

The three-resolution architecture below is prospective. Installed concrete locality
paths currently implement cell-block power or hopping-tail diagnostics. Orbital-resolved
and MLWF-resolved analyzers, basis-embedding records, and corresponding public imports
are not yet implemented. This document does not report a new calculation or authorize
Wannier90 execution.

## Responsibility

Hopping locality interprets the real-space coefficients of one already identified
periodic block-hopping model. It does not construct the model, choose its gauge, infer
basis-state positions, perform Wannier localization, or decide scientific acceptance.

For an ordered primitive basis matrix $A$, integer displacement
$\mathbf n\in\mathbb Z^d$, and block coefficient
$T(\mathbf n)\in\mathbb C^{r\times r}$, locality has three distinct resolutions:

| Resolution | Elementary quantity | Required identity |
|---|---|---|
| cell block | $\lVert T(\mathbf n)\rVert_F^2$ | model geometry and ordered retained basis |
| orbital resolved | $\lvert T_{\alpha\beta}(\mathbf n)\rvert^2$ | ordered basis embedding in the primitive cell |
| MLWF resolved | $\lvert T_{ab}(\mathbf n)\rvert^2$ attributed to correlated MLWF identities and centers | ordered MLWF embedding plus localization and gauge provenance |

The three analyzers are peers. A specialized analyzer does not invoke a sibling analyzer
or silently replace its result. A calculation may compose several peer results when its
scientific question requires comparison across resolutions.

## Current implementation summary

The installed hierarchy reaches periodic 1D rank one, rank two, and rank $N$; periodic
2D rank two and rank $N$; and periodic 3D rank two and rank $N$. Concrete analyzers
currently provide scalar or block coefficient tails in one dimension and normalized
cell-block Frobenius powers by metric shell in two and three dimensions.

Periodic-2D/3D rank-two requests consume exact dimensional KSD block-hopping models. The
corresponding rank-$N$ requests still consume finite Fourier matrix series plus declared
basis and energy-reference strings; they are representation-level analyses and do not
promote those series to exact KSD scientific models. The complete source inventory and
known gaps are recorded in [Implementation inventory](implementation.md).

## Cell-block locality

Cell-block locality is the current baseline. It assigns one power to each integer
lattice displacement,

\[
P_{\mathrm{block}}(\mathbf n)=\lVert T(\mathbf n)\rVert_F^2,
\]

and may aggregate those powers by a declared shell policy. It is independent of any
intracell position assigned to an individual retained basis state. The existing
`MetricShellHoppingPowerAnalyzer` additionally divides by the declared retained rank for
its historical normalized scalar result.

Cell-block locality remains the primary basis-aggregate diagnostic because it does not
pretend that retained matrix indices have atomic-orbital or MLWF meaning. Neither an
orbital-resolved nor an MLWF-resolved implementation may remove this baseline.

## Ordered basis embedding

Orbital-resolved locality requires an immutable `PeriodicOrbitalBasisEmbedding`-like
scientific value owned outside geometry. It correlates:

- one exact periodic geometry;
- one nonempty `basis_identifier` matching the model;
- the exact ordered retained-state inventory;
- one stable state identifier per matrix index; and
- one finite fractional direct-basis center $\mathbf s_\alpha$ per state.

The term *orbital* identifies an embedded retained basis state. It does not imply an
atomic orbital, chemical site, Slater--Koster channel, or uniquely physical object.
Geometry owns the primitive lattice; the embedding owner correlates internal basis
indices with intracell centers. Until a separately reviewed reusable
`DirectLatticeCoordinate` value is adopted, these centers remain exact-dimensional
finite coefficient tuples on the embedding record rather than new geometry values.

For source index $\alpha$, target index $\beta$, and integer displacement $\mathbf n$,
the directed physical element displacement is

\[
\mathbf d_{\alpha\beta\mathbf n}
 = A\left(\mathbf n+\mathbf s_\beta-\mathbf s_\alpha\right).
\]

Therefore a cell displacement $A\mathbf n$ is not generally an orbital-resolved hopping
displacement. A same-cell off-diagonal element can have nonzero physical separation, and
a nonzero cell displacement can be shortened by the intracell offset difference.

## MLWF embedding and initial scope

MLWF-resolved locality is a specialization of basis-attributed interpretation, not a new
kernel representation. Its initial supported scientific scope should be **center-attributed
MLWF-pair hopping locality**:

\[
P^{\mathrm{MLWF}}_{ab}(\mathbf n)=\lvert T_{ab}(\mathbf n)\rvert^2,
\qquad
\mathbf d^{\mathrm{MLWF}}_{ab\mathbf n}
 = A\left(\mathbf n+\mathbf s_b-\mathbf s_a\right).
\]

A prospective `PeriodicMlwfBasisEmbedding` composes the ordered basis embedding with
explicit MLWF and localization provenance. It must retain enough identity to establish
that matrix row and column $a$ refer to the same ordered MLWF as center $\mathbf s_a$.
A generic `basis_identifier` alone is insufficient.

Wannier spreads may be retained as provenance and diagnostic metadata. They do not
modify the center-attributed displacement or power in the initial capability. A
spread-weighted distance, overlap-weighted locality, or full wavefunction-shape
observable would answer a different question and requires a separately specified
scientific definition.

## Gauge and interpretation boundary

MLWF-resolved locality is gauge conditioned. Individual MLWF identities, centers, and
matrix elements can change with disentanglement windows, projections, localization
settings, local minima, permutations, lattice-image choices, and admissible unitary
mixing. It must not be reported as an intrinsic material observable or as a unique
atomic-orbital decomposition.

Comparisons between MLWF-resolved results require an explicit correlation or alignment
of ordered MLWF identities. Matching only by nearest center is not sufficient in a
degenerate or symmetry-related manifold. Cell-block locality remains available when no
scientifically justified state-by-state correlation exists.

## Ownership boundary

- PhysKit owns reusable block-hopping storage, integer lattice displacements, physical
  quantities, and raw block-power mechanics.
- KSD periodic models own scientific model, geometry, basis, gauge, energy-reference,
  and role identity.
- KSD hopping-locality owners define resolution, attribution, normalization, directed or
  pair-symmetric counting, shell aggregation, and result meaning.
- Wannier90 owns localization. Project Koios Simulations owns reusable Wannier90
  execution, parsing, artifact, and provenance mechanics.
- Campaigns and calculations own selected settings, correlations, thresholds, retained
  evidence, and scientific interpretation.

The periodic model binds geometry and ordered internal-basis identity but does not select
one locality resolution. Basis embeddings and MLWF provenance are explicit analyzer
inputs, not inferred model properties.

## Detailed documents

- [Implementation inventory](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Installed band-equivalence locality owner](../band_equivalence_hopping_locality/index.md)
- [Prospective periodic geometry](../geometry/periodic/index.md)
- [Finite-rank block-hopping model capability](../periodic/models/PeriodicBlockHoppingModel/index.md)
