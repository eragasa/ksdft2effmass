# Maintained Test Evidence Documentation

This reference defines a reusable documentation grammar for maintained Python
software-verification and numerical-verification evidence. It is a writing and
review convention; applying it does not establish scientific validation or
uncertainty quantification.

## Evidence classes

- **Software verification** checks an implemented software contract such as
  construction, invariants, behavior, error taxonomy, serialization, imports,
  or technical integration. Numeric values in assertions do not by themselves
  make a test numerical verification.
- **Numerical verification** checks implementation of stated mathematics using
  a result derived independently of the production algorithm. It records units,
  scale regime, representation, and an explicit exact or tolerance rule.
- **Scientific validation** compares a declared model and use with independent
  reference evidence under a separately authorized protocol. It must not be
  inferred from passing verification tests.
- **Uncertainty quantification** identifies and propagates uncertainty sources.
  Error handling, parameterization, multiple scales, or tolerance testing alone
  is not uncertainty quantification.

## Exact module headings

Every migrated evidence module uses these headings exactly once and in this
order in its module docstring:

```text
Evidence class and represented meaning
Owned contract, oracle, and scope
VVUQ and scientific exclusions
```

The first section names the evidence class and distinguishes the modeled
subject, mathematical object, finite or numerical representation, and software
surface where applicable. The second identifies the primary system under test,
owned contract, oracle source, and included scale or unit regime. The third
states what passing and failure mean and explicitly excludes unsupported
numerical verification, scientific validation, uncertainty quantification,
physical correctness, and cross-language conformance.

## Exact test and helper fields

Each migrated test-function docstring and each nontrivial evidence-helper
docstring uses these fields exactly once and in this order:

```text
Evidence ID
Requirement
Method
Oracle
Acceptance
Interpretation
Limitations
```

Each field has a nonempty body.

- **Evidence ID** gives one stable authoritative identifier. A parameterized test
  normally owns one identifier; an explicitly inventoried same-stem inclusive
  range is permitted only with a one-to-one parameter mapping. A helper states
  that it supports named evidence and owns no identifier.
- **Requirement** states one externally meaningful public contract or
  mathematical claim without restating an assertion.
- **Method** identifies public inputs, action, controlled fault, parameter
  regime, and warnings policy. It does not present the production algorithm as
  an oracle.
- **Oracle** states the independently known expected result and its derivation.
  A software oracle may be an exact public contract, wire schema, language rule,
  or error taxonomy. A numerical oracle must not call, copy, or algebraically
  disguise the production algorithm under test.
- **Acceptance** gives the exact result, exception, ordering, representation, or
  justified tolerance or ULP rule. Numerical tolerances state units or
  dimensionlessness, inclusivity, zero handling, and scale.
- **Interpretation** explains pass and failure implications and identifies
  plausible implementation, evidence, fixture, platform, oracle, or contract
  defects when failure is not uniquely attributable.
- **Limitations** states excluded inputs, regimes, dependencies, physical
  conclusions, scientific validation, uncertainty quantification, and
  cross-language claims.

Historical evidence whose first docstring line is a durable owner declaration
may remain a valid audit input. A documentation migration must not silently
renumber identifiers or change represented meaning.

## Semantic naming grammar

Migrated test functions use exactly:

```text
test_<surface>__<facet>__<behavior>
```

`<surface>` is one of `constructor`, `field`, `property`, `method`,
`classmethod`, `staticmethod`, `protocol`, `public_api`, `artifact`, or
`workflow`. `<facet>` names the public member, protocol operation, artifact
boundary, or cohesive contract facet. `<behavior>` states expected observable
behavior. Every segment is lowercase snake case. Evidence identifiers do not
appear in function names. Renames require a complete old-to-new test node-ID
map.

## Ownership and relation grammar

The reusable primary ownership kinds are exactly:

- **`class_owned`:** one public immutable data object, result object, stateless
  action object, workflow, or error object is the sole primary system under
  test. Collaborators only construct inputs or observe public outcomes.
- **`artifact_owned`:** a public schema, fixture family, import surface,
  dependency boundary, command, or interoperability artifact is the primary
  owner. Do not fabricate a class owner.

A helper supplies setup or assertion mechanics shared by local evidence. It owns
no evidence identifier, makes no independent pass claim, and must not hide an
oracle or convention. Protected historical evidence remains unchanged until a
separately authorized migration; structural nonconformance is not permission to
edit it.

Cross-object behavior belongs to the action or workflow that owns the operation.
Technical integration belongs to `artifact_owned` evidence rather than an
artificial production workflow. Its optional relation metadata consists of:

```text
relation_kind
left_side_id
right_side_id
direction
```

`relation_kind` is one of `intrinsic`, `agreement`, `directional_mapping`, or
`package_surface`. `direction` is one of `none`, `left_to_right`, or
`right_to_left`. `intrinsic` and `package_surface` require `none`; `agreement`
requires two named sides and `none`; `directional_mapping` requires two named
sides and a non-`none` direction. Relation metadata describes one artifact-owned
relation; it does not introduce another ownership kind.

Module placement, filename policy, declarations, identifier namespaces, marker
inventories, and migration mappings are supplied by an explicit local profile or
extension. This generic grammar neither selects nor validates them.

## Parameterization

Use parameterization only when one requirement, method, oracle form, acceptance
rule, and interpretation apply across a declared input partition. Give each case
a stable meaningful ID rather than an ordinal. Document boundary values, signs,
scales, canonicalization, warning policy, excluded zeros, and pass/fail
partition. Split cases whose requirements or failure meanings differ.
Collection count and evidence-owner count remain separately traceable.

## Exact representation and oracle independence

Use exact equality for exact represented state, canonical text, deterministic
ordering, enum or error identity, and immutable value semantics. Do not weaken an
exact contract with approximate comparison. Use approximate comparison only when
the mathematical or numerical contract authorizes it, and document the norm,
tolerance, units, scale, boundary, and floating-point representation.

An independent oracle must be available without executing the behavior under
test. Acceptable sources include a public invariant, fixed schema, exact
language semantics, hand-derived analytical result, higher-precision or
independently implemented calculation, or approved external reference. A
production helper, private method, production constant used as the sole expected
value, renamed invocation of the same routine, or multiple agreeing reviews is
not independent. A production constant may select inputs only when the approved
value is anchored independently.

## Review checklist

### Structural review

- exact module headings occur once and in order;
- exact test and helper fields occur once, in order, with nonempty bodies;
- declared evidence namespace, hierarchy, and owner agree;
- identifiers are unique and helpers own none;
- function names follow the semantic grammar and omit evidence identifiers;
- the primary class or artifact owner is explicit;
- parameter IDs and old/new node mappings are complete;
- software, numerical, scientific-validation, and uncertainty claims remain
  distinct.

### Semantic review

- the requirement is public and non-tautological;
- the method exercises the public boundary without hidden invalid-state
  mutation;
- the oracle is genuinely independent and applicable to the represented regime;
- acceptance matches exact-representation or justified tolerance policy;
- units, shapes, scale, warning behavior, zero and boundary behavior, and
  parameterization are adequate;
- interpretation distinguishes implementation, fixture, oracle, environment,
  and contract failures;
- limitations exclude unsupported physical, scientific-validation,
  uncertainty-quantification, and portability conclusions;
- assertions, fixtures, schemas, source, specification, and documentation retain
  the same public and represented meaning.

Structural tooling reports syntax and inventory conformance only. It cannot
establish oracle independence, mathematical correctness, tolerance adequacy,
scientific validity, uncertainty-quantification adequacy, or human acceptance.
