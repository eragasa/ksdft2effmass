---
name: develop-operator-records
description: Guides represented finite operators, their immediate metadata, Hermiticity, compatibility, differences, residuals, serialization, and comparison prerequisites.
---

# Develop Represented Finite Operators

## Purpose and scope

Use this skill only for represented finite operators and their immediate
scientific and software contracts. It covers state-space and basis identity and
ordering, geometry, units and energy reference, matrix representation,
Hermiticity, compatibility, represented differences, residuals, serialization,
and comparison prerequisites. It is not a general linear-algebra skill.

## Required guidance

Read `references/operator-record-architecture.md` before operator work. Apply
`design-data-action-objects` for general object ownership. Route maintained test
creation or restructuring to `develop-python-test-evidence`, public source/API or
Sphinx documentation to `document-python-research-software`, and a material open
architecture choice to `develop-architecture-decision`.

## Represented-operator model

For an abstract operator $\hat O$ and ordered basis
$\{|b_i\rangle\}_{i=0}^{N-1}$, the represented matrix is

$$
O_{ij}=\langle b_i|\hat O|b_j\rangle.
$$

A complete represented operator identifies the finite-dimensional state space,
basis and ordering, matrix, units, geometry, energy reference, and applicable
spin, gauge, or coordinate conventions. Equal matrix shape does not establish
compatible meaning.

Under a unitary basis change $U$,

$$
O' = U^\dagger O U.
$$

The coordinates change without necessarily changing the underlying operator.
A coordinate-dependent matrix difference is not automatically physical, and
spectral agreement alone does not establish gauge equivalence.

## Operator-specific ownership

- Operator-record DataObjects own intrinsic metadata and representation
  invariants only.
- Hermiticity tolerance and evaluation belong to a Hermiticity analyzer
  ActionObject; the structured outcome is an immutable ResultObject.
- Compatibility of independently valid operator records belongs to a named
  compatibility ActionObject.
- Signed differences and residual metrics belong to named analysis
  ActionObjects, not to the operator record.
- Serialization and deserialization belong to a serializer ActionObject.
- A comparison composition is a Workflow only when it is a genuine reusable
  multi-step operation with explicit inputs, outputs, and dependencies.
- ResultObjects are semantic DataObjects and require no nominal base class.

## Compatibility and numerical rules

Before subtraction, residual analysis, or comparison, check every convention
that affects represented meaning, including state-space identity, dimension,
basis ordering, units, geometry, energy reference, spin convention, and gauge or
coordinate alignment. Require alignment or an invariant comparison when exact
coordinate compatibility is absent.

Keep exact matrix values, Hermiticity residual, scale or normalization,
tolerance, structured result, and scientific interpretation distinct. Numerical
norms and residuals must define their mathematical quantity, units, and
normalization; handle zero scale explicitly; reject or report nonfinite
intermediates; use scale-safe computation where overflow is possible; and expose
structured numerical failure instead of silently returning `inf` or `nan`.

Operator serialization must preserve exact represented metadata, keep schema and
runtime behavior consistent, use explicit field and enum vocabularies, and fail
on unsupported or ambiguous representations. A round trip does not establish
physical validity.

## Evidence and scientific-claim boundary

- Construction and invariant tests are software verification.
- Independently derived analytical norm or residual checks may be numerical
  verification.
- Comparison with a physical system or trusted scientific reference is
  scientific validation.
- Uncertainty propagation or sensitivity analysis is UQ.

No evidence class implies another. A software Hermiticity tolerance check does
not prove physical correctness.

## Stop conditions

Stop when basis, gauge, geometry, units, energy reference, spin convention,
scientific acceptance, or another comparison-critical meaning is missing or
conflicting. Report the unresolved contract without inventing alignment,
conversion, physical equivalence, validation, or acceptance. Do not expand this
skill into a gauge-equivariant reduction framework or introduce new public APIs
without separate authority.
