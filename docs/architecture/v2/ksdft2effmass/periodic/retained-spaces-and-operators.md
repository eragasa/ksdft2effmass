# Scientific retention: spaces, operators, and representations

## Status, scope, and evidence boundary

This page defines the software architecture for scientific retention in periodic
models. It distinguishes the modeled subject, mathematical objects, numerical
representations, and Python owners used to record them. It does not change the
mathematics in the applicable specification, prove that a chosen subspace is
physically adequate, report a new calculation, or validate an effective model.

In the research monograph, **retained** identifies state-space and operator content
kept by a declared projection, band selection, disentanglement, or related reduction.
It does not mean merely that a file was saved. The governing mathematical distinctions
are developed in:

- [Chapter 1, model adequacy](../../../../publications/research-monograph/chapters/01-model-adequacy.tex);
- [Appendix A, notation and status](../../../../publications/research-monograph/appendices/A-notation-and-status.tex);
- [Appendix C, operator spaces, compression, and alignment](../../../../publications/research-monograph/appendices/C-operator-spaces-compression-alignment.tex);
- [Appendix G, one-dimensional reduction](../../../../publications/research-monograph/appendices/G-one-dimensional-reduction.tex);
- [state-space assumptions](../../../../research/proofs/ksdft2effmass/foundations/state-space-assumptions.md);
  and
- [representation and reduction maps](../../../../research/proofs/ksdft2effmass/foundations/representation-maps.md).

The monograph is explanatory narrative, and the proof-foundation pages are proposed
proof material. Applicable versioned files under `specification/` remain authoritative
for accepted physical and mathematical definitions. The present page owns the software
separation and the phase-4 public contract.

## Four layers that must not collapse

The retention path has four distinct layers:

| Layer | Meaning | Phase-4 owner |
|---|---|---|
| Modeled subject | The periodic physical or mathematical system under study. | `PeriodicModel` and its dimensional branch. |
| Mathematical object | A parent operator, retained subspace, or exact operator restricted to that subspace. | Stable operator reference, `PeriodicRetainedSubspace`, and `PeriodicRetainedOperator`. |
| Numerical representation | Coordinates of a retained operator in a finite ordered basis, including geometry, unit, energy zero, and gauge metadata. | `PeriodicRepresentedRetainedOperator` composed with `OperatorRecord`. |
| Software implementation | Immutable records and explicit construction Actions that validate and bind the preceding meanings. | Classes in `ksdft2effmass.periodic.retention`. |

The scientific dependency is:

```text
PeriodicModel
     |
     v
stable parent-operator reference
     |
     +-- retention definition
     v
PeriodicRetainedSubspace
     |
     +-- exact restriction or compression
     v
PeriodicRetainedOperator
     |
     +-- declared representation map
     v
PeriodicRepresentedRetainedOperator
     |
     +-- truncation, fitting, or projection into a model class
     v
EffectivePeriodicModel (later phase)
```

The arrows denote explicit constructions or identifications, not inheritance. A
retained operator is not a `PeriodicModel`, and a matrix is not an abstract operator.
An effective model is approximate even when its matrix dimension or spectrum agrees
with an exact retained representation.

## Mathematical contract

### Parent space and retention definition

Let the parent operator be

$$
\hat H:\mathcal D(\hat H)\subseteq\mathcal H\longrightarrow\mathcal H.
$$

A retention definition records what is selected from the parent and how that selection
is identified. Phase 4 supports the closed construction classifications:

- **spectral restriction**, selecting an invariant spectral sector;
- **selected bands**, selecting an ordered band family over a reciprocal domain; and
- **disentangled subspace**, selecting a fixed-rank subspace from a larger candidate
  manifold by a separately identified construction.

The classification is metadata, not the construction itself. A complete definition
also records stable parent-model and parent-operator identities, the ambient state
space, retained-space identity, rank, ordered retained-state labels, reciprocal-domain
identity, construction-record identity, assumptions, and provenance.
`Periodic1DSelectedBandRetentionDefinition` and
`Periodic2DSelectedBandRetentionDefinition` compose `ContiguousBandSelection` for the
demonstrated dimensions. Each requires exact parent dimension, selected-band kind, and
rank agreement without treating the interval as a projector or retained space. Later
phase-specific definitions may compose another closed selection record without widening
this foundation into an arbitrary parameter map.

### Retained subspace

For an orthogonal projector

$$
\hat P:\mathcal H\longrightarrow\mathcal H,
\qquad
\hat P^2=\hat P,
\qquad
\hat P^\dagger=\hat P,
$$

the retained space is

$$
\mathcal H^{(P)}=\operatorname{im}\hat P.
$$

A finite orthonormal frame may instead be written as an isometry

$$
\hat F:\mathbb C^r\longrightarrow\mathcal H,
\qquad
\hat F^\dagger\hat F=I_r,
\qquad
\hat P=\hat F\hat F^\dagger,
$$

where $r=\operatorname{rank}\hat P$. The projector identifies the subspace; the
columns of $\hat F$ identify one frame for it. For $G\in U(r)$,

$$
\hat F' = \hat F G
\quad\Longrightarrow\quad
\hat F'\hat F'^\dagger=\hat P.
$$

Thus a unitary frame change does not create a different retained subspace. The frame,
its ordering, and its gauge remain representation data needed to interpret matrix
coordinates.

`PeriodicRetainedSubspace` records the scientific identity of
$\mathcal H^{(P)}$. Its accepted target records the ambient dimension, retained rank,
ordered retained labels, reciprocal-boundary convention, spin and internal-degree
conventions, and provenance. When represented frame coordinates exist, a separate
typed frame binding owns their orthogonality, gauge, sewing, and content identity.
Digest-only projector evidence remains with its campaign result and does not become a
represented projector or mathematical retained-space field.

The implemented
[band-frame ownership decision](band-frame-ownership-decision.md) leaves the generic
mathematical retained space free of projector/frame witness fields. The exact isolated
frame digest is owned and reauthenticated by its typed frame binding. The composite
projector digest remains with its exact source campaign result because the corresponding
projector coordinates are unavailable; it is not promoted to a represented projector
binding or copied into retained-space identity.

Equal rank is necessary for some unitary identifications but is not sufficient for
retained-space compatibility. Parentage, reciprocal domain, geometry, spin, internal
degrees of freedom, and construction remain relevant.

### Exact retained operator

The exact retained operator is

$$
\hat H^{(P)}
=
\left.\hat P\hat H\hat P\right|_{\mathcal H^{(P)}}:
\mathcal H^{(P)}\longrightarrow\mathcal H^{(P)}.
$$

This must not be conflated with the ambient compression
$\hat P\hat H\hat P:\mathcal H\to\mathcal H$, which has a different declared domain
and codomain and acts as zero on the orthogonal complement. It must also remain
distinct from an energy-dependent downfolded operator containing eliminated-space
resolvents.

`PeriodicRetainedOperator` identifies the parent operator, retained domain and
codomain, restriction-or-compression construction, energy unit and scalar energy-zero
convention, Hermiticity declaration status, and provenance. The Hermiticity field is a
declaration status, not a tolerance-based numerical assessment. A represented
Hermiticity analyzer remains a separate ActionObject.

### Numerical compression evidence

For a finite real matrix $H\in\mathbb R^{N\times N}$ and an orthonormal column
embedding $Q\in\mathbb R^{N\times K}$, `OperatorCompression` constructs

$$
H_{\mathrm{coord}}=Q^T H Q,
\qquad
P=QQ^T,
\qquad
H_{\mathrm{ambient}}=PHP=QH_{\mathrm{coord}}Q^T.
$$

`OperatorCompressionResult` retains the input represented matrix, numerical subspace,
$K\times K$ coordinate matrix, and $N\times N$ ambient embedding. Its intrinsic
contract correlates their dimensions and requires both output units to equal the input
operator unit. The Action owns evaluation of the matrix products; the DataObject does
not become a second compression engine.

This numerical result is not itself a `PeriodicRetainedOperator`. It has no stable
parent-model, parent-operator, ambient-state-space, retained-space, basis, gauge,
energy-zero, invariance-result, or construction-provenance identity. Those fields must
be attached by a separate scientific construction when demonstrated. Equal dimensions
or a known compression route cannot supply them by inference.

When $[H,P]=0$, the coordinate matrix represents the exact restriction of this finite
operator to an invariant subspace. Otherwise it represents a projected compression,
and its eigenvalues are Ritz values. Neither case is the energy-dependent downfolded
operator containing discarded-space resolvent corrections. The present software
result does not calculate or classify the commutator and therefore does not decide
between those cases.

### Finite representation

For an ordered orthonormal basis or frame
$\mathcal B=(|b_0\rangle,\ldots,|b_{r-1}\rangle)$ of the retained space, the represented
matrix is

$$
H^{(P)}_{ij}
=
\langle b_i|\hat H^{(P)}|b_j\rangle,
\qquad
\mathbf H^{(P)}\in\mathbb C^{r\times r}.
$$

A unitary frame change gives

$$
\mathbf H^{(P)\prime}=G^\dagger\mathbf H^{(P)}G.
$$

The coordinates are gauge covariant; the underlying exact retained operator need not
change. Consequently, entrywise equality or subtraction is meaningful only after the
applicable basis and gauge relation is established.

`PeriodicRepresentedRetainedOperator` composes the exact retained-operator owner with
an `OperatorRecord`. The aggregate records the representation-map identity, gauge
identity, and binding provenance. Its intrinsic contract requires:

1. the `OperatorRecord` state-space identity to equal the retained-space identity;
2. matrix, state-space, basis-ordering, and retained-rank dimensions to agree;
3. basis ordering to equal the retained definition's ordered state labels; and
4. represented energy unit and energy zero to agree exactly with the exact retained
   operator metadata.

`OperatorRecord` continues to own the finite matrix, basis, geometry, energy reference,
and represented provenance. Phase 4 does not copy those fields into a second record.
Exact textual equality here is a binding precondition, not unit conversion, scalar
energy alignment, gauge alignment, or physical equivalence.

## Stable parent references

Phase 4 references a parent model and operator by stable immutable identity through
`PeriodicOperatorReference`; it does not embed an arbitrary concrete `PeriodicModel`
implementation. The reference records:

- `model_id`;
- `operator_id`;
- `state_space_id`; and
- exact spatial dimension.

This choice keeps scientific records immutable, serializable in a future explicit wire
contract, and independent of mutable implementation objects. It also prevents a record
from silently acquiring calculator, campaign, filesystem, or execution behavior.
Resolution from these identities to a concrete model or artifact is a separate future
Action and is intentionally absent in phase 4. A stable identity is not a filesystem
path, repository root, remote URL, or proof that the referenced object exists.

## Construction ownership

Construction is explicit and composition based:

| ActionObject | Input meaning | Output | Required checks |
|---|---|---|---|
| `PeriodicRetainedSubspaceConstructor` | One retention definition plus ambient-space, boundary, spin, internal-degree, and provenance metadata. Numerical projector/frame witnesses are excluded; available frame payloads and content identities belong to typed frame bindings, while digest-only projector evidence remains with its campaign result until projector coordinates exist. | `PeriodicRetainedSubspace` | Exact semantic types, nonempty identities, rank and ordered-label agreement, ambient-space identity and dimension. |
| `PeriodicRetainedOperatorConstructor` | One parent reference, retained subspace, construction kind, energy reference, declaration status, and provenance. | `PeriodicRetainedOperator` | Parent identity and retained domain/codomain agreement. |
| `PeriodicRepresentedRetainedOperatorConstructor` | One exact retained operator, one finite `OperatorRecord`, representation-map identity, gauge identity, and provenance. | `PeriodicRepresentedRetainedOperator` | State-space, dimension, basis ordering, energy unit, and energy-zero agreement. |

The constructors do not select eigenvectors, compute a projector, compress a numerical
matrix, choose a gauge, transform coordinates, truncate hoppings, fit parameters,
perform I/O, or execute a scientific campaign. Existing numerical owners such as
`OrthogonalSpectralSubspace`, `ReciprocalBandFramePath1D`,
`ReciprocalOperatorSamples1D`, and `OperatorCompressionResult` remain distinct. Phase 5
may compose them with these scientific identities through specialized Actions.

DataObject constructors enforce intrinsic aggregate invariants so invalid public state
cannot be created directly. ActionObjects own the explicit scientific binding step and
provide the supported construction route. No module-level scientific constructor or
validator is introduced.

## Failure conditions

Construction fails rather than guessing when:

- an identity or convention is empty or has the wrong semantic type;
- a Boolean, numeric string, or NumPy scalar is supplied as a rank or spatial
  dimension;
- retained labels are duplicated or their count differs from the declared rank;
- retained rank exceeds the ambient finite dimension;
- the retained definition and subspace name different ambient spaces;
- a retained operator names a different parent from its retained subspace;
- domain and codomain would not be the same retained space;
- a represented state-space identity or dimension differs;
- represented basis ordering differs from retained ordering; or
- represented and exact energy metadata differ.

The software does not repair these failures by reordering, truncating, padding,
converting units, shifting energies, inferring a gauge, or choosing an alignment.

## Boundaries to later operations

Phase 4 deliberately excludes:

- **alignment:** independently constructed retained spaces require an explicit
  directional unitary or partial-isometry result;
- **energy alignment:** a scalar offset is not hidden in a basis map;
- **subtraction:** pristine and defect operators are not differenced before alignment;
- **truncation:** dropping real-space blocks constructs an approximation;
- **fitting:** parameter estimation constructs a model instance in a prescribed class;
- **continuum embedding:** continuum and atomistic operators require an explicit map;
- **serialization:** no phase-4 wire format or generic document wrapper is defined; and
- **resolution or I/O:** stable references do not load files or access a repository.

A complete Fourier transform can provide another exact representation on its declared
finite mesh. Truncation or fitting is a separate approximation even if it reuses the
same coefficient container.

## Error and evidence accounting

Retention does not erase the distinction among:

1. **parent-model error**, concerning adequacy of the parent physical model;
2. **numerical or discretization error**, concerning approximation of the stated
   mathematics; and
3. **model-reduction error**, concerning replacement of the exact retained operator by
   a restricted effective-model class.

Phase-4 constructor tests are software verification only. They establish type,
identity, and dimension behavior of the Python contract. They do not numerically verify
a projector, establish gauge equivariance, validate a material model, quantify
uncertainty, or show that the selected retained space is suitable for an intended use.

## Evidence retention is a different meaning

The repository also retains files, payloads, checksums, reports, and results as
historical evidence. That preservation meaning must be qualified as **retained
evidence**, **retained artifact**, **retained result**, or **encoded campaign
document**. It must not classify a byte container as a scientific retained space or
operator.

Campaign-specific `...EncodedDocuments` classes are exact-byte aggregates. They are
not implementations of `PeriodicRetainedSubspace`, `PeriodicRetainedOperator`, or
`PeriodicModel`, regardless of historical names or directory locations.

## Implementation map

The supported phase-4 public route is `ksdft2effmass.periodic`:

| Public owner | Implementation location |
|---|---|
| Retention and operator enums | `python/src/ksdft2effmass/periodic/retention.py` |
| `PeriodicOperatorReference` | same module |
| `PeriodicRetentionDefinition` | same module |
| `PeriodicRetainedSubspace` and constructor | same module |
| `PeriodicRetainedOperator` and constructor | same module |
| `PeriodicRepresentedRetainedOperator` and constructor | same module |

The implementation remains campaign independent. Concrete one-dimensional adoption,
numerical projector/frame composition, effective-model classes, and defect alignment
belong to later migration phases.
