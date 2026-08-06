# Maintained Python Test Evidence Conventions

Read this reference completely before designing, writing, modifying, migrating, or reviewing maintained Python tests. It is reusable: project paths, evidence prefixes, class names, marker inventories, and control-plane locations come only from explicit caller input or a local extension.

## 1. Claims and evidence classes

Classify every owner and case before writing it.

- **Software verification** checks an implemented software contract: construction, fields, properties, methods, protocols, errors, serialization, public imports, schemas, fixtures, or technical integration. Numeric values alone do not make numerical verification.
- **Numerical verification** checks implementation of stated mathematics against a result derived independently of the production algorithm. State the represented mathematical object, units, dtype/precision, shape, scale regime, oracle derivation, and exact or tolerance rule.
- **Scientific validation** compares a declared model and use case with independent reference evidence under separately recorded authorization and protocol. Verification never implies validation.
- **Uncertainty quantification (UQ)** identifies and propagates declared uncertainty sources under separately recorded authorization and method. Error handling, parameterization, scale variation, or tolerance tests alone are not UQ.

Keep parent-model, numerical/discretization, and model-reduction errors distinct. A passing test is evidence only for its stated requirement and acceptance rule; it is not general physical correctness, portability, release readiness, or human acceptance.

## 2. Primary ownership and placement

The only generic primary ownership kinds are exactly:

- **`class_owned`**: one public immutable data object, result object, stateless action object, workflow, protocol implementation, or error object is the sole primary system under test (SUT). Collaborators construct inputs or expose outcomes but do not become co-owners.
- **`artifact_owned`**: one public schema, fixture family, wire format, import surface, dependency boundary, command, or interoperability relation is primary. Do not fabricate a class or workflow owner for technical integration.

Cross-object behavior belongs to the action object or genuine workflow that owns the operation. Agreement, mapping, package-surface, and schema/fixture checks are artifact-owned. Optional relation metadata is `relation_kind`, `left_side_id`, `right_side_id`, and `direction`; kinds are `intrinsic`, `agreement`, `directional_mapping`, and `package_surface`, while directions are `none`, `left_to_right`, and `right_to_left`. Intrinsic/package-surface use `none`; agreement names both sides and uses `none`; directional mapping names both sides and a non-`none` direction.

Every structured ownership entry declares `mode`, `evidence_class`, and `path`, plus `sut` for `class_owned` or a concrete `artifact` name for `artifact_owned`. `evidence_class` is exactly `software_verification`, `numerical_verification`, `scientific_validation`, or `uncertainty_quantification`; the latter two still require separate authorization. The raw module opening must agree exactly with this structured class and owner. A local profile supplies roots, markers, ID namespaces, and accepted filename exceptions. Generic tooling must not infer them.

## 3. Filenames, SUT agreement, and module opening

A class-owned file is `test__<PublicClass>.py` or an explicitly authorized cohesive facet file `test__<PublicClass>__<facet>.py`. Case-sensitive filename class, explicit ownership input, public import, module prose, and `SUT = PublicClass` agree. An artifact-owned file is `test__<descriptive_lowercase_snake_case>.py`; `_to_` is reserved for a directional relation.

The module docstring begins exactly with an applicable declaration such as:

```python
r"""Software verification of ``PublicClass``.
```

Use `Numerical verification of ...`, `Scientific validation of ...`, or `Uncertainty quantification of ...` only when that class is applicable and authorized. Artifact-owned openings identify the concrete artifact rather than inventing a class.

## 4. Exact maintained module headings

After the opening, every newly migrated module contains these headings exactly once and in this order:

```text
Facet and represented meaning
Intrinsic and cross-object scope
VVUQ and scientific exclusions
```

`Facet and represented meaning` identifies the evidence class, public facet, modeled subject where relevant, mathematical object, finite/numerical representation, and software surface. `Intrinsic and cross-object scope` identifies the SUT/artifact, owned contract, collaborators/relations, oracle source, units and scale. `VVUQ and scientific exclusions` states precise pass/failure meaning and excludes unsupported numerical verification, validation, UQ, physical correctness, portability, and cross-language claims.

The headings `Evidence class and represented meaning` and `Owned contract, oracle, and scope` are superseded and prohibited in newly migrated evidence. They may remain only in untouched historical material outside the explicitly supplied migration paths.

## 5. Test surfaces and semantic names

Tests use `test_<surface>__<facet>__<behavior>`, in lowercase snake case, without an evidence ID in the name. The generic surfaces are:

- `constructor`: public construction, factory-call construction, and constructor error partitions;
- `field`: stored public dataclass/record fields and their invariants;
- `property`: only an actual public `@property` descriptor—never equality or an ordinary field;
- `method`: public instance methods, including the explicitly classified special-method value behaviors `eq`, `hash`, and `repr`;
- `classmethod`, `staticmethod`: the corresponding public callable;
- `protocol`: actual Python protocol operations other than the explicitly method-classified `eq`, `hash`, and `repr`, including iteration, containment, ordering, context management, and conversion;
- `public_api`: public exports/import inventory;
- `artifact`: schemas, fixtures, wire formats, commands, dependencies, or interoperability boundaries;
- `workflow`: a genuine public workflow/action composition.

The facet names the actual member or cohesive contract: examples include `test_method__eq__compares_complete_represented_state`, `test_method__hash__is_disabled_for_mutable_values`, `test_method__repr__shows_public_identity`, `test_property__residual__returns_declared_units`, and `test_constructor__identifier_type__rejects_bytes`. Do not label `==` as `property` or `protocol`, collapse unrelated surfaces under `behavior`, or name tests after implementation details. Renaming requires a complete one-to-one old/new pytest node-ID map.

## 6. Cohesion and splitting

One collected test has one requirement, one method shape, one oracle form, one acceptance rule, and one failure interpretation. Combine cases only when these remain identical across a declared partition.

Cohesive: parameterize several invalid identifier strings that all must raise the same public exception for the same grammar. Split: wrong semantic types (`TypeError`) from malformed values (`ValueError`); equality from immutability; constructor mapping from an actual property; schema shape from runtime semantic relations; exact-zero cases from nonzero tolerance cases. A loop over unrelated fields, exceptions, or acceptance rules hides meaningful cases and must become named pytest parameters or separate tests.

## 7. Exact function documentation

Every migrated test and every nontrivial evidence helper has these fields exactly once, in order, with nonempty bodies:

```text
Evidence ID
Requirement
Method
Oracle
Acceptance
Interpretation
Limitations
```

- **Evidence ID** gives one stable authoritative test identifier. A helper says it owns no identifier and names the evidence it supports without claiming an independent result.
- **Requirement** states one externally meaningful public contract or mathematical claim, not the assertion syntax.
- **Method** identifies public inputs/action, controlled fault, parameter partition, representation, and warning policy. It does not use the production algorithm as oracle.
- **Oracle** states the independently known result and derivation/source.
- **Acceptance** states exact value, exception, ordering, bytes/text, representation, or justified inclusive tolerance/ULP rule.
- **Interpretation** explains pass and failure, separating plausible implementation, fixture, oracle, environment, and contract defects.
- **Limitations** excludes inputs/regimes/dependencies and unsupported physical, validation, UQ, portability, and cross-language conclusions.

RST underlines are permitted, but field names and order are exact. Preserve durable historical owner declarations and IDs during migration.

## 8. Helpers

Helpers provide setup or assertion mechanics. They own no evidence identifier, make no independent pass claim, and must not hide an oracle, tolerance, unit convention, parameter partition, or public requirement. Use nonprivate semantic names such as `make_valid_operator_record`, `execute_with_runtime_warnings_as_errors`, and `assert_normal_binary64_error_within_bound`; prohibit `_helper`, `_make_record`, `helper`, `setup`, `check`, and ordinal names such as `make_case_1`.

Nontrivial helper docstrings use all seven fields. Their `Evidence ID` body explicitly says `Owns no identifier; supports ...`. A trivial imported fixture need not acquire evidence prose merely to satisfy a mechanical count.

## 9. Parameterization and stable case IDs

Use explicit `pytest.param(..., id="semantic_case")` for every meaningful case. IDs describe the partition, not the raw Python representation. Meaningful examples include `empty_identifier`, `bytes_wrong_type`, `negative_one`, `maximum_u64`, and optional neutral evidence-qualified IDs such as `SV-EXAMPLE-001-empty`. Evidence qualification does not transfer ownership or create an additional evidence ID.

Reject ordinal IDs (`case_1`, `1`), raw values (`bad id`, an absolute path, a surrogate, `None`, object repr), whitespace, `::`, slash/backslash paths, memory addresses, pytest-autogenerated IDs, and unstable `repr`. Explicit `ids=[...]` is allowed only when it is a literal, complete, semantic one-to-one list. Record signs, boundaries, scales, canonicalization, warning policy, excluded zeros, and pass/fail partition. Collection count and evidence-owner count are different quantities.

## 10. Evidence identifiers and migration maps

Identifiers are unique over the supplied maintained scope. One parameterized test normally owns one ID; a declared inclusive same-stem range is permitted only when parameters map one-to-one to IDs. Helpers own none. Never renumber merely because a file or function moves.

A rename/migration input is a closed structured object containing explicit unique `expected_old_node_ids` and `expected_new_node_ids` inventories plus `mappings` of exact `old_node_id`/`new_node_id` pairs. The mapping is complete and one-to-one: its old and new sets exactly equal the supplied inventories, every old pytest node ID has exactly one new node ID, and no new node receives multiple old nodes. Preserve IDs, assertions, fixtures, parameterization, represented meaning, and accepted behavior unless separate authority explicitly changes them. Update maintained inventories, replay paths, checksums, and documentation together; never rewrite historical reports/evidence.

## 11. Exact and approximate acceptance

Use exact equality for exact represented state, canonical JSON/text, deterministic ordering, integer/enumeration/error identity, immutable value semantics, exact mathematical zeros demonstrably preserved, and versioned schema fixtures. Do not weaken an exact contract with `approx`.

Approximate comparison requires an authorized mathematical/numerical contract. Document the quantity/norm, absolute and/or relative rule, units or dimensionlessness, dtype/precision, scale regime, boundary inclusivity, zero/subnormal handling, and why the bound is adequate. A nonzero tiny reference uses a criterion that cannot accept zero. Keep production tolerance policy separate from a test-local forward-error bound and from scientific acceptance criteria.

## 12. Independent oracles and controlled faults

An oracle is available without executing or algebraically disguising the behavior under test. Acceptable sources include a public invariant, fixed schema, exact language semantics, hand-derived analytical result, higher-precision calculation, independently implemented method, or approved external reference. Production private methods/helpers, production constants as sole expectations, a renamed call to the same routine, and reviewer agreement are not independent. A production constant may select an input only when its value is independently anchored.

Controlled fault injection may verify a documented public translation boundary when valid inputs cannot reliably trigger it. Name the controlled dependency and expected public error. This verifies the owner’s translation, not the dependency’s correctness. Do not mutate private invalid state or directly test a private method as a substitute for public evidence.

## 13. Schema, fixture, and runtime layering

Schema validation establishes declared wire shape only. Runtime constructors/deserializers establish semantic types, cross-field invariants, canonicalization, and public error taxonomy. Relational validators establish joins, uniqueness, dependency direction, or graph constraints. Fixture orchestration establishes that declared valid/invalid examples reach the intended layer. Keep these evidence owners and failure interpretations separate; a schema pass cannot establish runtime behavior, and a round trip cannot establish scientific correctness.

Version schemas and fixtures, identify exact accepted/rejected layers, resolve references locally where promised, and never change expected fixtures merely to make a test pass.

## 14. Coverage and count reporting

Report at least: supplied module paths; test-function count; explicit static collected parameter-case count (honest `null`/unknown when static collection cannot be determined); unique evidence-owner count; helper count; class-owned versus artifact-owned counts; evidence-class counts; and findings by code/severity. Never equate line coverage, collection count, assertion count, parameter count, or evidence-ID count. State the command, environment, scope, deselection, and failures. Coverage can reveal unexercised code but cannot establish requirement completeness, oracle independence, validation, or UQ.

## 15. Fifteen-step workflow

1. Confirm task authority, ownership, protected boundaries, and explicit paths.
2. Load this entire reference plus authoritative public/mathematical contracts and local profile.
3. Classify software verification, numerical verification, separately authorized validation, or separately authorized UQ.
4. Select exactly `class_owned` or `artifact_owned` and identify SUT/relation.
5. Inventory existing paths, node IDs, evidence IDs, fixtures, parameters, replay links, and historical constraints.
6. Define one cohesive requirement, public surface, method, oracle, acceptance, interpretation, and limitations per case family.
7. Choose canonical filename, `SUT` declaration, module opening, maintained headings, and semantic test/helper names.
8. Establish independent expected results before invoking production behavior.
9. Choose exact or approximate acceptance and document units, representation, scale, boundaries, zeros, and warnings.
10. Replace hidden meaningful loops/raw parameterization with explicit semantic `pytest.param` cases; record separate collection/evidence counts.
11. Write all seven fields for tests and nontrivial helpers; keep helpers nonprivate and ID-free.
12. For migrations, create and validate the complete one-to-one old/new node map before renaming; preserve historical evidence.
13. Run the cheapest supplied-path structural validation, then focused pytest and applicable schema/fixture, formatting, typing, coverage, link, and documentation gates.
14. Perform semantic review separately for surface correctness (including method-owned `eq`, `hash`, and `repr`), cohesion, oracle independence, tolerance adequacy, layering, claims, and synchronization.
15. Report exact changes/results/counts/residuals, verify unauthorized paths are unchanged, stop, and leave reviewer/human acceptance separate.

## Invocation profiles and authority

Every invocation selects exactly one:

- **`REVIEW_ONLY`**: inspect immutable supplied artifacts and run deterministic read-only commands. It writes no project files and returns structural findings separately from semantic findings.
- **`AUTHORIZED_TEST_EVIDENCE_WRITE`**: create or modify only explicitly assigned tests, test-owned fixtures, parameter cases, test documentation, and migration maps. It requires validated test-writer ownership. It cannot change production source, public contracts, mathematical/scientific meaning, public schemas owned elsewhere, dependencies/locks, external systems, or historical evidence without separate authority.
- **`AUTHORIZED_TEST_EVIDENCE_DOC_WRITE`**: modify only assigned test module/function/helper documentation and authorized semantic test/helper names. It requires test-evidence authority in addition to documentation authority. It cannot change assertions, fixtures, parameter values, decorators, evidence IDs, represented meaning, production source, dependencies, or schemas unless separately authorized.

Required inputs are request/task/parent-workflow/attempt identities, selected profile, immutable artifact identities, explicit paths, structured ownership, authoritative contracts, evidence class, expected result schema, permitted mutations, optional complete migration map, and stop/timeout policy. No profile can infer scientific/public choices, launch protected execution, transmit data, accept work, or dispatch successors.

The result reports skill/content identity; input/output identities; profile and ownership; status (`PASS`, `FAIL`, `BLOCKED`, or `PARTIAL`); structural and semantic findings separately; paths and counts; commands/results; IDs/classes; mutation summary; warnings/residuals; and decisions required. Missing/conflicting authority, unavailable references, invalid ownership, incomplete mappings, partial writes, or failed required gates stop the affected work. Retries retain prior evidence, use a new attempt identity, and verify current file identities. Read-only replay is observationally idempotent; writer replay is not presumed idempotent.

## Structural and semantic review boundary

Deterministic structural tooling may check only explicitly supplied paths for syntax, headings/opening, fields/order, names, ownership/SUT/filename/import agreement, ID occurrence uniqueness, helper declarations, explicit parameter IDs, loops, artifact filenames, and one-to-one maps. It must not impose new-heading strictness repository-wide.

Semantic review must independently decide surface accuracy (including actual `@property` and method-owned `eq`, `hash`, and `repr`), cohesion/splitting, requirement quality, public-boundary validity, oracle independence/applicability, mathematical derivation, tolerance adequacy, schema/runtime layering, evidence class, claim scope, and synchronized meaning. Structural success expressly cannot establish oracle independence, mathematical correctness, tolerance adequacy, scientific validity, UQ adequacy, or human acceptance.
