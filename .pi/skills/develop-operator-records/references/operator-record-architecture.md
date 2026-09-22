# Represented Finite-Operator Architecture

## Domain boundary

This reference applies to finite matrix representations of mathematical
operators and the metadata required to interpret them. It does not define a
general linear-algebra framework, perform basis or gauge alignment, validate a
physical model, or authorize a future reduction workflow.

The applicable specification and supported public imports remain authoritative
for exact fields and object names. This reference owns reusable domain
relationships rather than a source-tree, test-file, or command inventory.

## Represented meaning

For an abstract operator $\hat O$ acting on an identified finite-dimensional
space and an ordered basis $\{|b_i\rangle\}_{i=0}^{N-1}$, its matrix coordinates
are

$$
O_{ij}=\langle b_i|\hat O|b_j\rangle,
\qquad O\in\mathbb C^{N\times N}.
$$

The numbers $O_{ij}$ are not a complete operator record when interpretation also
depends on:

- state-space identity and dimension;
- basis identity, convention, and ordering;
- units and normalization;
- geometry, boundary, and coordinate conventions;
- energy-zero reference for energy-valued operators;
- spin representation;
- gauge, phase, or other alignment conventions; and
- serialization version and field vocabulary.

Store every comparison-critical convention explicitly or declare it outside the
supported representation. Provenance can identify an input calculation but does
not prove that the represented metadata or physical model is correct.

## Operator-specific object ownership

Use `design-data-action-objects` for the general architecture. Its
operator-domain application is:

| Responsibility | Owner |
|---|---|
| Matrix and intrinsic representation metadata | Operator-record DataObject |
| Intrinsic state-space, basis, geometry, or energy-reference invariants | DataObject that owns those fields |
| Hermiticity evaluation and tolerance | Hermiticity analyzer ActionObject |
| Representation compatibility | Compatibility ActionObject |
| Signed represented difference | Difference ActionObject |
| Residual norms and numerical policy | Residual-analysis ActionObject |
| Wire-format conversion | Serializer ActionObject |
| Structured operation outcome | Immutable ResultObject |
| Reusable comparison composition | Workflow, only when genuinely multi-step |

An operator record must not acquire analyzer tolerances, unit conversion,
comparison policy, residual computation, serialization methods, or scientific
acceptance state. ResultObjects record outcomes without performing their
operations and need no nominal DataObject inheritance.

## Compatibility before arithmetic

Subtraction and residuals are meaningful only after the applicable represented
conventions agree or have been explicitly aligned. A compatibility operation
should check, as applicable:

- state-space identity and represented dimension;
- matrix dimensions;
- exact basis ordering and basis convention;
- units and normalization;
- geometry and coordinate convention;
- energy reference;
- spin convention; and
- gauge or phase alignment.

Equal shape, dtype, eigenvalues, or provenance does not replace these checks.
Compatibility of stored representations is a software precondition; it is not
physical equivalence or scientific validation.

A difference ActionObject must define its operand order. For example,

$$
\Delta O = O_{\mathrm{candidate}}-O_{\mathrm{reference}}
$$

has the opposite sign from the reversed convention. A represented difference is
not automatically an impurity operator, perturbation, error operator, or
physical observable.

## Basis, gauge, and coordinates

Under a unitary basis transformation $U$,

$$
O' = U^\dagger O U.
$$

This changes matrix coordinates without necessarily changing the underlying
operator. Consequently:

- entrywise differences are coordinate dependent;
- basis labels alone do not establish alignment;
- an alignment map must state its direction and convention;
- invariant comparisons must identify the invariant being used; and
- equal spectra do not establish gauge equivalence or provide an alignment.

Do not interpret a residual physically until coordinate compatibility,
alignment, or a justified invariant comparison has been established. Full gauge-
equivariant reduction and approximate physical alignment remain outside this
skill.

## Hermiticity

For a represented matrix, one possible Hermiticity residual is the absolute
entrywise maximum

$$
\varepsilon_{\mathrm H}
=
\max_{i,j}|O_{ij}-O_{ji}^{*}|.
$$

The owning analyzer contract must state the chosen residual, its units, any scale
or normalization, and an inclusive or exclusive tolerance rule. Keep distinct:

1. exact stored matrix values;
2. the computed residual;
3. normalization or scale;
4. tolerance policy;
5. the immutable structured result; and
6. scientific interpretation.

A residual below a software tolerance establishes only the analyzer's documented
criterion under its recorded representation. It does not prove that the source
calculation, modeled operator, basis, units, or physical interpretation is
correct. Hermiticity status may be invariant under an exact unitary basis change
even when a nonzero entrywise residual magnitude is basis dependent.

## Residuals and numerical robustness

Each residual or norm must define its mathematical quantity. Common examples are

$$
\varepsilon_{\max}=\max_{i,j}|\Delta O_{ij}|,
\qquad
\varepsilon_{\mathrm F}=\|\Delta O\|_{\mathrm F},
\qquad
\varepsilon_2=\|\Delta O\|_2.
$$

State whether each result is absolute or normalized and identify its units.
Normalization must define the reference scale and explicitly handle a zero scale;
it must not hide an undefined ratio behind zero, infinity, or NaN.

Numerical implementations must:

- reject or report nonfinite represented inputs and intermediates;
- use scale-safe norm or residual computation where direct arithmetic can
  overflow or underflow materially;
- distinguish roundoff handling from scientific tolerance;
- make any canonicalization bound explicit and owned by the analyzer; and
- return or raise structured numerical failures instead of silently emitting
  `inf` or `nan`.

Do not combine parent-model error, discretization or numerical error, and
model-reduction error unless an owning scientific contract defines their
relationship.

## Serialization

An operator serializer owns the versioned wire representation. Its contract must
keep field and enum vocabularies explicit, preserve all represented metadata
required for interpretation, and make unsupported versions or ambiguous values
fail explicitly. Schema validation and runtime construction must agree while
remaining distinct layers: a schema can check wire shape, whereas runtime logic
may own cross-field dimensions, finiteness, canonicalization, and error taxonomy.

A successful round trip should preserve the exact represented state promised by
the wire contract. It does not establish basis alignment, gauge equivalence,
physical validity, provenance truth, numerical verification, or scientific
validation. Cross-language compatibility is required only when an accepted shared
wire contract or authorized implementation task requires it.

## Evidence boundary

- Construction, intrinsic invariants, compatibility codes, serialization shape,
  round trips, and public imports are software-verification subjects.
- Independently derived analytical residuals or norms may provide numerical
  verification of stated mathematics.
- Comparison against a physical system or trusted independent scientific
  reference is scientific validation for a declared use.
- Sensitivity analysis or propagation of declared uncertainty sources is UQ.

One class does not imply another. Detailed test ownership, naming, documentation,
parameterization, and evidence identifiers belong to
`develop-python-test-evidence`. Public source/API and Sphinx documentation
procedure belongs to `document-python-research-software`.

## Stop boundary

Stop when a comparison-critical convention is missing, contradictory, or not
aligned; when scientific meaning or acceptance remains a human choice; or when a
proposed change would introduce a new public API or broader gauge/reduction
framework. Report the exact missing contract rather than selecting a convention
for implementation convenience.
