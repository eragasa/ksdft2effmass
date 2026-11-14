# Hopping-locality implementation inventory

## Scope of this inventory

This page records the maintained source that exists now. It separates installed nominal
ownership and concrete cell-block diagnostics from the prospective orbital- and
MLWF-resolved extensions. It does not claim that every installed analyzer has been used
in a retained scientific execution.

## Installed nominal hierarchy

The domain owner is implemented in
`python/src/ksdft2effmass/hopping_locality/base.py`:

```text
HoppingLocality
├── HoppingLocalityAnalysisRequest
├── HoppingLocalityAnalysis
├── HoppingLocalityAnalyzer
└── PeriodicHoppingLocality
    ├── PeriodicHoppingLocalityAnalysisRequest
    ├── PeriodicHoppingLocalityAnalysis
    └── PeriodicHoppingLocalityAnalyzer
```

The generic analyzer contract binds one exact immutable request, exposes it through
`request`, and executes without changing coefficient support. The nominal base owns no
lattice primitive, transform backend, tolerance, acceptance policy, or wire format.

Dimension-specific nominal roles are implemented under:

- `periodic1d/hopping_locality/base.py`;
- `periodic2d/hopping_locality/base.py`; and
- `periodic3d/hopping_locality/base.py`.

Rank-specific capabilities, request roles, analysis roles, analyzer roles, and applicable
standalone value roles are implemented for:

| Dimension | Installed rank leaves |
|---|---|
| periodic 1D | rank one, rank two, and rank $N$ |
| periodic 2D | rank two and rank $N$ |
| periodic 3D | rank two and rank $N$ |

Rank two and rank $N$ are siblings. Rank-$N$ request owners require rank at least three;
a rank-four calculation remains rank $N$ rather than gaining a separate namespace.
Truthful rank-bearing values expose `band_subspace_rank` through their rank owner.

## Installed concrete diagnostics

All currently installed concrete diagnostics are cell-block or scalar-coefficient
locality. None associates an individual matrix-element power with an embedded orbital or
MLWF center.

| Owner | Bound input | Installed result | Resolution and limitations |
|---|---|---|---|
| `Periodic1DRank1HoppingLocalityAnalyzer` | one retained scalar Fourier-locality calculation, one exact source mesh, and explicit 1D lattice geometry | one `Periodic1DRank1HoppingTailResult` for each stored symmetric range | scalar coefficient-tail $L^2$ norm; adapts an existing retained calculation rather than accepting a block model |
| `Periodic1DRank2HoppingLocalityAnalyzer` | one frozen composite-band-alignment channel and unchanged ordinary `BlockHoppingModel1D` | omitted block Frobenius $L^2$ norm for every configured symmetric range | cell-block tail diagnostic; unitless frozen study contract remains maintained until this study passes explicit model migration, parity, replay, and provenance gates |
| `Periodic1DRankNHoppingLocalityAnalyzer` | one exact gauge-alignment request and correlated Fourier analysis | squared Frobenius weight, Frobenius $L^2$ norm, block $L^1$ norm, normalized forms, and consecutive-range monotonicity | cell-block tail diagnostics over an odd ordinary Fourier inventory; no support removal |
| `Periodic2DRank2HoppingLocalityAnalyzer` | one exact `Periodic2DRank2BlockHoppingModel`, positional metric-shell labels, and PhysKit raw-power analyzer | retained-rank-normalized Frobenius power per displacement and shell | cell-block locality; dense provider representation required by this numerical route |
| `Periodic3DRank2HoppingLocalityAnalyzer` | one exact `Periodic3DRank2BlockHoppingModel`, positional metric-shell labels, and PhysKit raw-power analyzer | retained-rank-normalized Frobenius power per displacement and shell | cell-block locality; dense provider representation required by this numerical route |
| `Periodic2DRankNHoppingLocalityAnalyzer` | one finite Fourier matrix series, rank, basis and energy-reference strings, positional shell labels, and PhysKit raw-power analyzer | retained-rank-normalized Frobenius power per displacement and shell | representation-level cell-block locality; does not admit an exact KSD scientific model |
| `Periodic3DRankNHoppingLocalityAnalyzer` | one finite Fourier matrix series, rank, basis and energy-reference strings, positional shell labels, and PhysKit raw-power analyzer | retained-rank-normalized Frobenius power per displacement and shell | representation-level cell-block locality; does not admit an exact KSD scientific model |

`Periodic1DRank2HoppingPower` is also installed as an authoritative standalone value for
reference and comparison normalized squared Frobenius block power at one integer
displacement. It does not retain basis-pair attribution.

## Shared numerical collaborators in their current locations

PhysKit `BlockHoppingPowerAnalyzer` owns raw unit-aware squared Frobenius powers for
individual provider blocks. KSD currently owns retained-rank normalization and shell
aggregation through `MetricShellHoppingPowerAnalyzer` and
`MetricShellHoppingPowerResult` in
`band_equivalence_hopping_locality/shell_power.py`.

The periodic-2D/3D rank-two analyzers consume that shared KSD numerical behavior from its
current historical package location. The periodic-2D/3D rank-$N$ analyzers additionally
consume `BandEquivalenceHoppingLocalityFourierShellPowerAnalyzer`, which projects a
finite Fourier matrix series into a PhysKit block-hopping representation before applying
the same shell-power calculation.

This location is an implementation fact, not a scientific ownership reassignment.
General hopping-locality owns the nominal operation. Moving the shared shell-power
mechanics would require a separately reviewed behavior-preserving extraction and import
migration; no such move is made by the current documentation.

## Installed geometry-related diagnostic

`band_equivalence_hopping_locality.geometry.basis_distance_range()` maps every supplied
cell displacement and every ordered source/target `basis_offsets` pair through a direct
lattice metric, then returns only the minimum and maximum distances. It:

- includes same-basis onsite zero vectors;
- returns `(None, None)` when no basis offsets are supplied;
- does not retain state identifiers;
- does not correlate a distance with
  $\lvert T_{\alpha\beta}(\mathbf n)\rvert^2$; and
- does not retain MLWF localization or gauge provenance.

It is therefore a basis-pair geometry diagnostic, not an orbital-resolved locality
analyzer.

## Public surfaces and evidence

`ksdft2effmass.hopping_locality` deliberately re-exports the domain request, analysis,
and analyzer bases. Periodic and rank-specific values remain available from their exact
owning packages. Sphinx documents the nominal domain, periodic, dimensional, and rank
ownership in `doc/sphinx/api/hopping-locality.rst`.

Maintained tests cover nominal inheritance, rank-sibling ownership, separation from
support truncation, exact request correlation, rank normalization, dimensional
admission, shell-power behavior, hopping-tail behavior, and selected monotonicity
contracts. These tests establish software behavior only. They do not establish physical
locality, material validation, or convergence.

## Missing capabilities

The following are not implemented:

- `PeriodicOrbitalBasisEmbedding` or an equivalent ordered embedded-basis value;
- `PeriodicMlwfBasisEmbedding` or an equivalent MLWF identity/provenance value;
- a reusable direct-lattice coordinate value for intracell centers;
- orbital-resolved element-power requests, analyses, or analyzers;
- center-attributed MLWF-pair locality requests, analyses, or analyzers;
- state-correlation or MLWF-alignment results for comparing two constructions;
- directed-versus-pair-symmetric element counting records;
- spread-aware or full wavefunction-shape locality observables; and
- retained scientific evidence from an MLWF-resolved locality calculation.

The initial proposed extension remains center-attributed MLWF-pair coefficient locality,
with spreads retained as peer metadata rather than implicit weights.

## Incremental extension boundary

An implementation should proceed without replacing current results:

1. add immutable ordered basis-embedding and MLWF-provenance values;
2. add peer orbital- and MLWF-resolved requests, analyses, and analyzers under the
   existing nominal hierarchy;
3. reconcile element powers with cell-block Frobenius power independently;
4. keep support truncation as a separate operation;
5. preserve historical cell-block results and retained bytes; and
6. add a calculation-owned composition only after the model, embedding, gauge, units,
   energy reference, and provenance are explicitly correlated.

No current analyzer should infer an embedding from `basis_identifier`, `basis_offsets`,
matrix order, or nearest-center matching.

The periodic-1D rank-two legacy-input migration is a separate transition within the
cell-block resolution. It must use the existing `BlockHoppingModel1D`, existing
cyclic-to-ordinary result, approved PhysKit representation values, and existing
`Periodic1DRank2BlockHoppingModel`. No new class is approved by this inventory. Each
study continues to accept its established legacy input until its complete consumer and
retained-result migration passes; another dimensional analyzer's model input does not by
itself establish that migration.
