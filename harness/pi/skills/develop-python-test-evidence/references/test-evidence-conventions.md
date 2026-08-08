# Maintained Python Test Evidence Conventions

## Evidence classes

Classify the claim before designing the test.

| Evidence class | Required meaning |
|---|---|
| Software verification | The implemented public software contract behaves as specified |
| Numerical verification | A numerical implementation agrees with an independently derived mathematical result |
| Scientific validation | A declared use is adequate against trusted physical, experimental, or scientific reference evidence |
| Uncertainty quantification | Declared uncertainty sources are characterized or propagated under an uncertainty model |

Software verification does not establish numerical correctness or scientific validity. Numerical
verification does not establish physical adequacy. Scientific validation requires an actual
validation protocol and independent reference; UQ requires an uncertainty model or protocol. Do
not claim an evidence class that the test does not execute. Keep parent-model,
numerical/discretization, and model-reduction errors distinct.

## Primary module ownership

Every maintained module has exactly one primary ownership kind.

- **`class_owned`**: one public class is the sole system under test. Prefer
  `test__ClassName.py`; an approved cohesive facet may use `test__ClassName__facet.py`. Do not use
  the module as a dumping ground for collaborators or unrelated artifacts. Cross-object behavior
  belongs to the ActionObject or genuine Workflow that owns the operation.
- **`artifact_owned`**: one schema or fixture family, wire contract, package/public import surface,
  dependency direction, command, wheel, interoperability relation, or cross-object agreement is
  primary. Use a meaningful package directory and concise names such as:

```text
integration/provenance/test__public_api.py
integration/provenance/test__package_wheel.py
integration/provenance/test__json_contract_v1.py
```

Do not encode every package segment or language unless necessary. `boundary_owned` is not a generic
primary kind. The validator's explicit ownership input identifies module path, mode, evidence class,
and class or artifact owner. A local profile may supply roots, markers, namespaces, and approved
exceptions; the skill does not infer them.

## Module documentation

The opening identifies the evidence class and owned class or artifact. Then use these headings once
and in order:

```text
Facet and represented meaning
Intrinsic and cross-object scope
VVUQ and scientific exclusions
```

State the public surface or artifact, represented meaning, intrinsic versus cross-object
responsibility, evidence class, authoritative oracle, limitations, and excluded claims. The headings
`Evidence class and represented meaning` and `Owned contract, oracle, and scope` are superseded and prohibited.
Do not repeat repository history or full process policy.

## Test-function naming

Use `test_<surface>__<facet>__<behavior>`. Names state public behavior, not merely that validation
occurred. The maintained validator owns the accepted structural surface vocabulary. Current core
surfaces distinguish construction, fields, properties, methods, class/static methods, protocols,
public APIs, artifacts, and Workflows. Name semantic subjects explicitly in the applicable surface
or facet, for example:

```text
test_artifact__schema__...
test_artifact__serialization__...
test_public_api__package__...
test_artifact__dependency__...
```

Identify special methods as methods: `test_method__eq__...`, `test_method__hash__...`,
`test_method__repr__...`, `test_method__call__...`, and `test_method__getitem__...`. Do not label
equality, hashing, lookup, construction, or an ordinary field as a property. Avoid vague facets such
as `general`, `behavior`, or `misc`.

## Test documentation

Every evidence-owning test documents these fields in order:

```text
Evidence ID
Requirement
Method
Oracle
Acceptance
Interpretation
Limitations
```

**Evidence ID** is the stable owner identity. **Requirement** states the public contract or
mathematical claim, not assertion syntax. **Method** states public inputs and operation without
disguising the oracle. **Oracle** states independently known behavior or value and its source.
**Acceptance** states the exact value, exception, representation, tolerance, ULP bound, or residual
criterion. **Interpretation** distinguishes plausible software, fixture, oracle, contract,
numerical, and scientific failures. **Limitations** identifies excluded inputs, regimes,
dependencies, and claims. Concise case-specific formatting is preferred over boilerplate.

## Evidence identifiers and parameterization

One evidence-owning function normally owns one stable identifier, unique within the maintained
inventory. Helpers own none. Preserve an identifier when a test moves or is renamed without changing
meaning. Create a migration record only for an authorized migration with a predecessor; ordinary new
tests require no migration map.

Use explicit `pytest.param(..., id="semantic_partition")` cases. IDs describe semantic partitions,
not ordinals, raw values, paths, autogenerated values, object representations, or opaque
abbreviations. A reused family may be assigned once before use to a module-local tuple, or an
immutable-in-practice list, of explicit cases. Do not dynamically generate cases when that prevents
deterministic collection accounting, and do not duplicate blocks merely to satisfy validation.

One parameterized test may remain one evidence owner when every case shares requirement, method
shape, oracle form, acceptance rule, and failure interpretation. Split independently meaningful
partitions when those differ.

## Helpers

Use visible semantic names such as `make_run_manifest` or `assert_canonical_payload`. A small helper
is acceptable even when direct construction is possible. Helpers own no evidence identifier or
independent pass claim, document their support role when nontrivial, do not hide requirements,
partitions, tolerances, units, or oracles, and do not embed expectations that make the test
tautological.

## Cohesion and layering

One evidence owner represents one coherent public behavior. Separate constructor mapping, intrinsic
invariants, equality, immutability, serialization, schema agreement, and runtime agreement when they
have distinct requirements, oracles, or failure meanings. Do not mechanically split a cohesive
property-delegation map when the exact mapping is one represented behavior.

Keep schema validation, runtime construction/deserialization, canonical serialization, and fixture
orchestration distinct. Schema success establishes wire shape; runtime behavior establishes semantic
and cross-field rules; a round trip establishes only its representation contract. Use integration
tests for genuine cross-surface contracts and public imports rather than private access.

## Oracle and acceptance quality

An oracle exists independently of the behavior under test. Suitable sources include public
contracts, fixed schemas, exact language semantics, hand-derived mathematics, higher-precision or
independently implemented methods, and approved trusted reference data. Private helpers, production
constants as sole expectations, the production algorithm rewritten in the test, and reviewer
agreement are not independent oracles. Avoid broad assertion loops that hide independently meaningful
cases.

Use exact equality for exact represented state, canonical bytes/text, ordering, enums, identifiers,
and exact mathematical zeros. Approximate acceptance requires a documented mathematical/numerical
contract. State, where applicable: quantity and representation; units; dtype/precision and scale;
independent result; absolute, relative, ULP, or residual criterion and boundary; zero/subnormal
handling; and nonfinite behavior. A nonzero reference criterion must not accidentally accept zero.
Keep test forward-error bounds distinct from production tolerance and scientific acceptance.
Scientific validation and UQ require separately authorized protocols.

## Deterministic structural validation

`ValidatePythonTestEvidence` and its thin CLI own mechanical checks over explicit module bytes and
ownership metadata, including implemented checks for ownership declarations, headings, naming,
evidence fields and identifiers, helper names, semantic parameter IDs, prohibited structural
patterns, optional migration-map shape, and static collection accounting. This reference defines
semantic convention, not validator implementation.

Structural PASS cannot establish semantic correctness, cohesion, oracle independence, mathematical
correctness, tolerance adequacy, scientific validity, UQ adequacy, provenance truth, or human
acceptance. Semantic review remains necessary.

## Routing and stop boundary

Use `design-data-action-objects` for object architecture, `develop-operator-records` for
operator-specific contracts, `document-python-research-software` for public source/API/Sphinx docs,
and `develop-architecture-decision` for a material open architecture choice.

Stop when authority, evidence class, primary owner, public or mathematical requirement, independent
oracle, acceptance rule, or separately required validation/UQ protocol is missing or conflicting.
Do not change expected values, weaken tolerances, add skips, renumber identifiers, or alter production
behavior merely to obtain a pass.
