# Class-Owned Test Evidence Documentation

This reference defines the reusable documentation grammar for maintained Python
software-verification and numerical-verification evidence, and for any future
scientific-validation evidence that is separately authorized. It is a writing
and review convention, not evidence that scientific validation or uncertainty
quantification exists.

## Evidence classes

- **Software verification** checks an implemented software contract: public
  construction, invariants, behavior, error taxonomy, serialization, imports, or
  technical integration. It does not establish numerical correctness merely
  because values appear in assertions.
- **Numerical verification** checks implementation of stated mathematics with a
  result derived independently of the production algorithm. It records units,
  scale regime, numerical representation, and an explicit exact or tolerance
  acceptance rule. It does not establish agreement with nature or an
  independent physical reference.
- **Scientific validation** compares a declared model and use case with
  independent reference evidence under an authorized validation protocol. It is
  future work unless repository artifacts explicitly provide it. Do not infer a
  marker or evidence-ID family, relabel software/numerical evidence, or claim
  validation from passing tests.
- **Uncertainty quantification** identifies and propagates uncertainty sources.
  Error handling, parameterization, multiple scales, or tolerance testing alone
  is not UQ.

## Exact module headings

Every migrated class-owned evidence module uses these headings, exactly once and
in this order, in its module docstring:

```text
Evidence class and represented meaning
Owned contract, oracle, and scope
VVUQ and scientific exclusions
```

The first section names the evidence class and distinguishes the physical model,
mathematical object, finite/numerical representation, and software surface where
applicable. The second identifies the primary system under test, the owned
contract, the oracle source, and the included scale/unit regime. The third says
what passing and failure mean and explicitly excludes unsupported numerical
verification, scientific validation, UQ, physical correctness, and cross-language
conformance.

## Exact test and helper fields

Each migrated test-function docstring and each nontrivial evidence-helper
docstring uses these fields, exactly once and in this order:

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
  normally owns one identifier; an explicitly inventoried, same-stem inclusive
  range is permitted when each parameter has a one-to-one identifier mapping.
  A helper says that it supports named evidence and owns no separate identifier.
- **Requirement** states one externally meaningful public contract or
  mathematical claim without restating the assertion.
- **Method** identifies public inputs, action, controlled fault, parameter
  regime, and warnings policy. It does not present the production algorithm as
  an oracle.
- **Oracle** states the independently known expected result and how it was
  obtained. For software evidence this may be an exact public contract, wire
  schema, language rule, or error taxonomy. For numerical evidence it must not
  call, copy, or algebraically disguise the production algorithm under test.
- **Acceptance** gives the exact result, exception, ordering, representation, or
  justified tolerance/ULP rule. Numerical tolerances state units or
  dimensionlessness, boundary inclusivity, zero handling, and scale.
- **Interpretation** explains what pass and failure imply and names plausible
  evidence, fixture, platform, or contract defects when failure is not uniquely
  attributable to production code.
- **Limitations** states excluded inputs, regimes, dependencies, physical
  conclusions, scientific validation, UQ, and cross-language claims.

Historical modules whose first docstring line is the durable owner declaration
remain valid inputs to the reusable evidence-ID audit. Migration to the fielded
grammar changes documentation structure; it must not silently renumber IDs or
change scientific meaning.

## Semantic naming grammar

Migrated test functions use exactly:

```text
test_<surface>__<facet>__<behavior>
```

`<surface>` is one of `constructor`, `field`, `property`, `method`,
`classmethod`, `staticmethod`, `protocol`, `public_api`, `artifact`, or
`workflow`. `<facet>` names the public field, method, protocol operation,
artifact boundary, or cohesive contract facet. `<behavior>` states the expected
observable behavior. All segments are lowercase snake case. Evidence IDs do not
appear in function names; renames require a complete old-to-new pytest node-ID
map.

## Ownership types

- **Class-owned:** one public DataObject, ResultObject, ActionObject, Workflow, or
  error object is the sole primary SUT. Collaborators only construct inputs or
  observe public outcomes.
- **Artifact-owned integration:** a public schema, fixture family, import
  surface, dependency boundary, command, or interoperability artifact is the
  primary owner. Do not fabricate a class owner.
- **Helper:** setup or assertion mechanics shared by local evidence. A helper
  owns no evidence ID, makes no independent pass claim, and must not hide an
  oracle or scientific convention.
- **Protected historical:** accepted or closed evidence retained unchanged until
  a separately authorized migration. Inventory it; do not treat age or
  structural nonconformance as permission to edit it.

Cross-object behavior belongs to the ActionObject or Workflow that owns the
operation. Technical integration belongs to an artifact owner, not an artificial
production Workflow.

## Evidence-module filename convention

A class-owned module is named exactly ``test__<ClassName>.py``, where the
case-sensitive stem after ``test__`` is the sole public SUT's exported class
name. Its executable ownership declaration is exactly ``SUT = <ClassName>``;
the filename, imported class, module documentation, manifest owner, and SUT
assignment must agree. Facet suffixes are permitted only for separately
approved layouts that name them explicitly; they are not inferred from this
convention.

An artifact-owned module instead uses a descriptive lowercase snake-case name:
``test__<artifact_or_boundary>.py``. The name identifies the concrete public
artifact, contract, or integration boundary and must not imply a class or
production Workflow owner. For a two-sided boundary or agreement, name both
sides in their documented comparison order, for example
``<left>_<right>_contract`` or ``<left>_<right>_agreement``. Reserve ``_to_``
for a genuinely directional transformation, dependency, or flow from the
left-hand side to the right-hand side; do not use it for symmetric or
conjunctive agreement. Workflow or subnet segments must reproduce the exact
approved lowercase snake-case name in the authoritative task or architecture
record. For the maintained CPN package that segment is ``workflow_cpn``.
Generic ownership names such as ``integration``, ``contract``, ``schema``,
``fixtures``, ``dependency_direction``, ``public_contract``, ``workflow``, or
``subnet`` are prohibited when they omit the owned domain or one side of the
boundary.

The architecture-approved P1 artifact filenames are exactly:

- ``test__workflow_cpn_python_public_api.py``;
- ``test__workflow_cpn_v1_python_json_contract.py``;
- ``test__workflow_cpn_v1_json_fixtures_python_runtime_contract.py``;
- ``test__workflow_cpn_python_import_dependency_direction.py``;
- ``test__workflow_cpn_python_snakes_and_deferred_engine_isolation.py``.

A controlled rename preserves evidence IDs, assertions, fixtures,
parameterization, and scientific/public-contract meaning. In the same migration
batch, update every ownership manifest and inventory entry, deterministic gate
invocation, completeness matrix, checksum catalog, documentation reference, and
old-to-new pytest node-ID map. The map is one-to-one and records both the old
module/function node and new module/semantic-function node for every evidence
owner. Stale aliases or duplicate old/new modules are prohibited. If a protected
record must retain an old path historically, label it as superseded history
rather than rewriting it.

Filename, manifest, inventory, SUT-assignment, field, marker, and node-map checks
are structural. Whether the chosen artifact name faithfully describes the
scientific or software boundary, whether a relation is directional, whether a
Workflow/subnet name has architecture authority, and whether conjunctive facets
remain one valid requirement are semantic review decisions. Structural tooling
must not claim those decisions or split accepted evidence identifiers.

## Parameterization

Use parameterization only when one requirement, method, oracle form, acceptance
rule, and interpretation apply across a declared input partition. Give every
parameter a stable, meaningful ID describing the varied regime rather than an
ordinal. Document boundary values, signs, scales, canonicalization, warning
policy, excluded zeros, and expected pass/fail partition. If parameter cases
have different requirements or failure meaning, split them into separate tests.
Collection count and evidence-owner count are distinct and must both remain
traceable.

## Exact representation and oracle independence

Use exact equality for exact represented state, canonical text, deterministic
ordering, enum/error identity, and DataObject value semantics. Do not weaken an
exact contract with approximate comparison. Use approximate comparison only when
the mathematical/numerical contract authorizes it, and document the norm,
tolerance, units, scale, boundary, and floating-point representation.

An independent oracle must be available without executing the behavior under
test. Acceptable sources include a public invariant, fixed schema, exact
language semantics, hand-derived analytical result, a higher-precision or
independently implemented calculation, or an approved external reference.
Reusing a production helper, private method, production constant as the sole
expected value, the same library routine with renamed variables, or multiple
agreeing AI reviews is not independent. Production constants may select inputs
only when the approved value is also asserted or otherwise anchored
independently.

## Review checklist

### Structural review

- exact module headings occur once and in order;
- exact test/helper fields occur once, in order, with nonempty bodies;
- module marker, evidence-ID prefix, hierarchy, and owner agree;
- identifiers are unique and helpers own none;
- function names follow `test_<surface>__<facet>__<behavior>` and omit IDs;
- primary SUT or artifact owner is explicit;
- parameter IDs and old/new node mappings are complete;
- software, numerical, future scientific-validation, and UQ claims remain
  distinct.

### Semantic review

- the requirement is public and non-tautological;
- the method exercises the public boundary without hidden invalid-state mutation;
- the oracle is genuinely independent and applicable to the represented regime;
- acceptance matches exact-representation or justified tolerance policy;
- units, shapes, scale, warning behavior, zero/boundary behavior, and
  parameterization are adequate;
- interpretation distinguishes implementation, fixture, oracle, environment,
  and contract failures;
- limitations exclude unsupported physical, scientific-validation, UQ, and
  portability conclusions;
- assertions, fixtures, schemas, source, specification, and documentation retain
  the same scientific and public-contract meaning.

Structural tooling can report syntax and inventory conformance only. It cannot
establish oracle independence, mathematical correctness, tolerance adequacy,
scientific validity, UQ adequacy, or human acceptance.
