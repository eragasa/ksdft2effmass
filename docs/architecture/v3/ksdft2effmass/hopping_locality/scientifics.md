# Hopping-locality scientific interpretation

## Locality is representation dependent

Hopping locality describes coefficients after a retained space, ordered basis, gauge,
energy convention, and lattice geometry have been fixed. It is not an intrinsic property
of an energy spectrum alone. Momentum-dependent gauge changes can redistribute power
among real-space displacements while preserving complete represented bands.

The three resolutions answer different questions:

- **cell-block locality** asks where the total matrix-block power lies across lattice
  cells;
- **orbital-resolved locality** asks which ordered embedded basis-state pairs carry that
  power; and
- **MLWF-resolved locality** asks the same pair question for one explicitly correlated
  Wannier-localized gauge and its retained provenance.

None is a substitute for the others.

## Why MLWF-resolved locality is useful

Center-attributed MLWF-pair locality can identify whether a long-range block tail is
spread across many matrix elements or dominated by a small number of Wannier pairs. It
can support:

- channel-specific truncation diagnostics;
- interpretation of long-range hopping tails;
- comparison of explicitly aligned Wannier constructions;
- investigation of projection, disentanglement, or localization choices; and
- attribution of a block-level truncation consequence to its coefficient channels.

These are scientifically meaningful diagnostics when the exact MLWF construction and
state correlation are retained.

## Gauge-conditioned nonclaims

An MLWF-resolved result is gauge conditioned. It must not be described as:

- a unique material observable;
- a unique decomposition into physical atomic orbitals;
- proof that an MLWF belongs to one atom or bond;
- a gauge-invariant ranking of individual hopping channels;
- evidence that the selected Wannier construction is globally optimal; or
- evidence that small spreads guarantee short-ranged Hamiltonian coefficients.

Individual MLWFs can be permuted, translated by lattice vectors, rephased, or mixed
within an admissible subspace. Disentanglement windows, initial projections,
localization settings, convergence behavior, and local minima can change both centers
and coefficient attribution. A state-by-state comparison therefore requires an explicit
correlation or alignment result. Similar centers alone do not establish equivalent
wavefunctions.

## Centers, spreads, and shapes

A center locates the first moment used for coefficient attribution. It does not encode
an MLWF's spatial shape. A quadratic spread adds a second-moment localization diagnostic
but still does not determine overlap, directional tails, nodal structure, or the
Hamiltonian matrix element between two functions.

Accordingly, the initial MLWF-resolved capability is deliberately limited to
**center-attributed coefficient locality**. Spreads are retained as metadata and peer
diagnostics. Spread-aware or full-shape observables remain separate prospective
scientific definitions rather than optional modes hidden inside one analyzer.

## Relation to orbital-resolved locality

MLWF-resolved locality uses the same matrix-element decomposition as orbital-resolved
locality, but it carries stronger identity and provenance requirements. A generic
embedded retained basis can be synthetic or conventionally labeled. An MLWF embedding
must establish that every ordered matrix index is correlated with one retained Wannier
function, center representative, localization result, and gauge construction.

The word *orbital* in the generic capability means a retained basis state. It does not
supply atomic-orbital semantics. Those semantics require an additional scientific model
and an independently qualified common-space correlation.

## Comparison policy

Two MLWF-resolved locality results are directly comparable only when their comparison
definition states:

- common physical geometry and units;
- common retained state space and energy reference;
- each ordered basis and gauge identity;
- the MLWF correlation or alignment between the two ordered inventories;
- center representative and lattice-image conventions;
- common coefficient support and counting convention; and
- common normalization.

If state-by-state correlation is unresolved, comparison may remain at the cell-block
level. The absence of a justified MLWF alignment is an inapplicability condition, not a
reason to infer correspondence from index order.

## Evidence boundary

A future result must retain or reference authenticated provenance for the Wannier
construction, including applicable projections, windows, localization and
disentanglement settings, executable/version identity, convergence status, ordered
centers, spreads when used, and the coefficient artifact correlated with those values.
Large wavefunctions or checkpoints may remain external under complete manifests.

Artifact digests establish byte identity, not scientific validity. Successful Wannier90
execution, parser tests, small spreads, or block-sum reconciliation do not establish
material validation, convergence, transferability, or publication acceptance.
