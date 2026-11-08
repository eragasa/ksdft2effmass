# Periodic basis embedding and reciprocal-shift sewing

## Status

**Structured basis identity implemented; embedding and reciprocal-shift sewing remain
prospective.**

`ksdft2effmass.periodic.operators.basis.PeriodicBasisIdentity` now owns the exact ordered
coordinate inventory and deterministic version-1 wire selected by the
[`basis-identity audit`](basis-identity-audit.md). Supported families are labeled
components, plane-wave reciprocal indices, qualified native Wannier orbitals, and
Slater--Koster site orbitals. Display identifiers are descriptive and do not determine
compatibility.

This page continues to define prospective ownership boundaries required before periodic
rank-two calculations can make Wilson-loop claims. `PeriodicBasisEmbedding`, Bloch-basis
conventions, reciprocal-shift sewing, provider admission adapters, and reusable Wilson
analysis are not implemented or authorized by the basis-identity decision.

## Scientific purpose

A periodic block-hopping model identifies coefficient blocks by integer lattice
translation and matrix index. That information is sufficient for Bloch-Hamiltonian
construction and cell-block hopping-locality analysis, but it does not identify where
represented basis states are embedded inside a primitive cell.

Wilson-loop closure under a reciprocal-lattice shift additionally requires:

1. a basis embedding aligned with matrix order;
2. an explicit Bloch-sum phase convention;
3. an explicit reciprocal-loop orientation and closing shift; and
4. an actual linear sewing map between the represented fibers at the two reciprocal
   endpoints.

None of these values may be inferred from crystal labels such as square, hexagonal,
FCC, BCT, diamond, or simple cubic.

## Proposed class hierarchy

```text
PeriodicBasisEmbedding
├── Periodic1DBasisEmbedding
├── Periodic2DBasisEmbedding
└── Periodic3DBasisEmbedding
```

`PeriodicBasisEmbedding` owns the dimension-neutral basis and embedding correlation.
The dimensional classes own exact coordinate tuple lengths. Structure identity remains
data in the geometry and embedding values; no structure-specific embedding subclass is
introduced.

The proposed immutable fields are:

```python
embedding_id: str
basis_identity: PeriodicBasisIdentity
fractional_positions: tuple[tuple[float, ...], ...]
```

The concrete dimensional classes narrow `fractional_positions` to one-, two-, or
three-component tuples.

### Ordering contract

Tuple position is the matrix-index correlation:

```text
fractional_positions[j] ↔ block-matrix row and column j
```

Ordering is therefore an invariant, not part of the class name. The class is named
`PeriodicBasisEmbedding`, not `OrderedPeriodicBasisEmbedding`.

No per-state identifier tuple is proposed for the first contract. Matrix index already
distinguishes basis states, including multiple orbitals or spin states at the same
fractional position. If retained provenance later requires names for individual basis
states, that inventory must be designed as a separate basis contract rather than added
implicitly to the embedding.

### Fractional-position contract

Fractional positions are coefficients in the ordered primitive direct-lattice basis.
They are dimensionless built-in finite floats. The embedding does not replace the
physical lattice geometry and does not attach a length unit to fractional coordinates.

Positions remain as supplied. Construction does not automatically reduce coordinates
into `[0, 1)`, choose a home cell, or erase an integer lattice lift. Such operations can
change represented gauge and provenance conventions even when positions are physically
equivalent modulo lattice translation.

Duplicate positions are valid. They may represent multiple orbitals, spin states, or
other basis states embedded at the same point.

## Resolved structured basis-identity gate

The former provisional `basis_identifier: str` contract is superseded for new periodic
basis identity by `PeriodicBasisIdentity`. Its equality uses the concrete family and
ordered coordinate values; its display identifier is descriptive only. The exact
coordinate keys and first wire are recorded in the
[`basis-identity audit`](basis-identity-audit.md).

The baseline inventory remains relevant to migration of current producers and consumers,
including:

- KSD periodic scientific models;
- PhysKit block-hopping representations;
- Fourier-series conversion results;
- retained `BlockHoppingModel1D` evidence;
- Wannier90 orbital and MLWF inventories;
- plane-wave and finite-basis frame paths;
- serialization and retained-result records; and
- calculation-owned reference and candidate composition.

Migration remains explicit and fail-closed:

- calculations not yet migrated continue to pass through their already-owned strings;
- code may not synthesize compatibility from joined labels;
- no enum of project-specific basis names is approved;
- no lowercasing, trimming, aliasing, or fallback is approved; and
- no sewing or Wilson result may claim cross-record basis compatibility solely because
  two historical strings compare equal.

`StrWireEnum` is used only for closed coordinate-family and Slater--Koster orbital
vocabularies. The scientific basis inventory itself remains open and
calculation-specific through immutable ordered coordinate values.

## Bloch basis convention

The proposed closed wire vocabulary is:

```python
class BlochBasisConvention(StrWireEnum):
    positive_cell_phase = "positive_cell_phase"
    positive_position_phase = "positive_position_phase"
```

The conventions distinguish the Bloch sums

\[
|\alpha,\mathbf q\rangle_{\mathrm{cell}}
=
\sum_{\mathbf n}
\exp\!\left(2\pi i\,\mathbf q\!\cdot\!\mathbf n\right)
|\mathbf n,\alpha\rangle
\]

and

\[
|\alpha,\mathbf q\rangle_{\mathrm{position}}
=
\sum_{\mathbf n}
\exp\!\left(2\pi i\,\mathbf q\!\cdot
(\mathbf n+\mathbf s_\alpha)\right)
|\mathbf n,\alpha\rangle .
\]

The sign and placement of the phase are part of the enum definition. A calculation may
not infer the convention from matrix values, embedding positions, or a basis-identifier
spelling.

## Reciprocal-shift sewing map

The proposed value is named `ReciprocalShiftSewingMap` because it represents an actual
linear map

\[
S_{\mathbf m}:\mathcal H_{\mathbf q}^{(\mathcal B)}
\longrightarrow
\mathcal H_{\mathbf q+\mathbf m}^{(\mathcal B)},
\qquad \mathbf m\in\mathbb Z^d.
\]

Its proposed fields are:

```python
basis_identity: PeriodicBasisIdentity
reciprocal_shift: LatticeDisplacement
transformation: ComplexMatrixQuantity
convention: BlochBasisConvention
```

The source and target fibers use the same represented basis identity. Separate
`SourceBasisEnum` and `TargetBasisEnum` values are not proposed. If source and target
basis identities differ, the operation is a basis transformation or gauge bridge, not
reciprocal sewing.

`ReciprocalShiftSewingMap` must validate:

- exact displacement dimension;
- matrix shape equal to embedding rank;
- unitless matrix values;
- correlation with one admitted basis identity and Bloch convention; and
- the convention-specific expected transformation when constructed from an embedding.

The corresponding action is `ReciprocalShiftSewingMapConstructor`. Construction does
not select a reciprocal loop, band subspace, tolerance, or Wilson interpretation.

For a periodic cell-phase basis, the sewing matrix may be the identity. For a
position-phase basis, it generally contains embedding-dependent diagonal phases. An
identity result remains explicit rather than inferred.

A finite-cutoff plane-wave coefficient shift can be nonunitary because reciprocal-index
states leave the truncated inventory. Such a map is valid evidence of a represented
finite-basis shift, but it must not be silently promoted to an exact unitary Wilson-loop
sewing map.

## Reciprocal-loop ownership

A later reciprocal-loop value must retain:

```python
loop_id: str
reduced_coordinates: tuple[tuple[float, ...], ...]
closing_shift: LatticeDisplacement
```

The coordinates are ordered and half-open. Point order defines loop orientation. The
closing shift explicitly identifies the reciprocal-lattice displacement used to map the
starting fiber to the endpoint fiber. Geometry does not own loop ordering, sampling,
sewing, or band selection.

Dimension-specific loop classes should enforce coordinate tuple length without
introducing structure-specific subclasses.

## Wilson-loop use

A Wilson-loop analyzer may consume the basis embedding, Bloch convention, reciprocal
loop, sewing map, model, and explicit selected band indices. It must not construct any
of those scientific identities implicitly.

The closure link has the represented form

\[
F_{\mathrm{end}}^{\dagger}
S_{\mathbf m}
F_{\mathrm{start}}.
\]

The sewing map is therefore a peer input used by frame transport, band equivalence,
gauge alignment, and Wilson-loop construction. It is not owned by a class named
`WilsonSewing`.

A complete rank-two subspace inside a `2 x 2` model spans the entire represented state
space. Its Wilson result may be an embedding- or convention-dependent full-space
holonomy and must not automatically be interpreted as nontrivial topology,
polarization, or retained-subspace fidelity. A nontrivial interpretation requires an
explicit isolated subspace, a retained subspace of a larger parent, or another
scientifically defined state-space restriction.

## Complete sewing problem inventory

The following sewing categories are intentionally distinct and are owned by
`ksdft2effmass.sewing`. Identity reciprocal sewing now has a concrete ambient-space
value; the other six categories remain abstract until their own scientific contracts
are selected.

| Sewing owner | Problem represented | Current boundary |
|---|---|---|
| `IdentityReciprocalSewing` | Explicitly identify reciprocal endpoints when the admitted ordered ambient basis and Bloch convention are identical. | Constructs a named ambient identity map; it does not infer basis identity or define `basis_identifier`. |
| `EmbeddedPositionReciprocalSewing` | Account for reciprocal endpoint phases caused by fractional basis positions. | Must wait for embedding and Bloch-phase conventions. |
| `PermutationPhaseReciprocalSewing` | Reconcile a legitimate endpoint permutation and phase convention for the same represented basis. | Must not infer correspondence or repair accidental ordering. |
| `PlaneWaveIndexSewing` | Review finite plane-wave reciprocal-index shifts for possible Wilson use. | Does not replace the implemented finite-cutoff plane-wave shift constructor; completeness and unitarity admission remain unresolved. |
| `ProjectedSubspaceSewing` | Project an admitted ambient sewing map into explicitly selected endpoint band frames. | Must not select bands or infer occupied subspaces. |
| `SymmetrySewing` | Relate fibers at momenta connected by a declared spatial or antiunitary symmetry. | Ordinary reciprocal closure, unitary symmetry, and antiunitary symmetry must not be conflated. |
| `FiniteBoundarySewing` | Correlate real-space periodic seam identification with retained twist fibers and gauge bridges. | Does not duplicate existing boundary-twist or gauge-bridge behavior. |

The seven categories are not aliases and are not interchangeable inputs to a Wilson-loop
analyzer. `ReciprocalEndpointSewingMap` and
`ReciprocalEndpointSewingInventory` provide the implemented reciprocal-endpoint values;
identity remains one construction of those values rather than a generic sewing base.

### Preservation rule

The six reserved abstract classes must not be deleted merely because they have no
concrete implementation. Their source comments, NumPy-style docstrings, abstract status,
this architecture page, and focused tests jointly record distinct scientific boundaries
rather than dead code. Removal requires a reviewed ownership decision showing that the
represented problem has either been implemented under its named owner or explicitly
retired.

The reserved category classes intentionally add no scientific fields or constructor
parameters yet. Adding those values before map direction, dimensional ownership, and
wire behavior are frozen would create a false public API. No shared source type, target
type, or map method is inferred across the seven problems.

## Relationship to studies and calculations

The reusable `Periodic*DRank2Study` values continue to retain only study identity, one
exact model, and `PeriodicStudyModelRole.reference` or
`PeriodicStudyModelRole.candidate`.

A named calculation owns composition of peer analyses:

```text
study correlation
├── hopping-locality analysis
├── reciprocal-loop frame construction
├── Wilson-loop analysis
└── reference/candidate comparison
```

The generic study constructor does not receive embedding inventories, loop meshes,
sewing maps, Wilson tolerances, or locality thresholds.

## Implementation gates

Implementation order is:

1. **Complete:** implement and document the structured `PeriodicBasisIdentity` wire;
2. design and review new operator correlation and provider admission without projecting
   structured coordinates through legacy string labels;
3. implement and test dimensional `PeriodicBasisEmbedding` values;
4. implement the closed `BlochBasisConvention` vocabulary;
5. implement `ReciprocalShiftSewingMap` and its constructor;
6. implement dimensional reciprocal-loop values;
7. implement frame construction and Wilson-loop analysis over explicitly selected
   subspaces;
8. integrate those peer analyses into named calculations; and
9. add independent numerical verification before retaining or interpreting results.

No step in this architecture page authorizes production electronic-structure execution,
rewriting retained evidence, or making a scientific Wilson-loop claim.
