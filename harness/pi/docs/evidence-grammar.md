# Evidence grammar and claim boundary

## Primary ownership

The generic maintained-test-evidence grammar has exactly two primary ownership kinds:

- `class_owned`: one public immutable data object, result object, stateless action object, workflow, or error object is the sole primary system under test;
- `artifact_owned`: a public schema, fixture family, import surface, dependency boundary, command, or interoperability artifact is the primary owner.

A helper owns no evidence identifier or independent pass claim. Protected historical evidence remains inventoried and unchanged until a separately authorized migration. Neither helper nor protected-historical status is a third primary ownership kind.

Cross-object behavior belongs to the action or workflow that owns the operation. Technical integration belongs to an artifact rather than an invented class. Newly migrated modules use `Facet and represented meaning`, `Intrinsic and cross-object scope`, and `VVUQ and scientific exclusions`; the former evidence-class/owned-contract headings are superseded. The full reusable headings, fields, naming, cohesion, helpers, parameterization, exact-representation, schema/runtime layering, workflow, invocation profiles, and independent-oracle procedure is owned by `pih.reference.test-evidence-conventions.v1`; this page summarizes identity and consumption boundaries rather than duplicating that procedure.

## Artifact relation metadata

Agreement, mapping direction, and package-surface relationships are metadata on one `artifact_owned` owner, not additional ownership kinds. Version 1 represents the relation with:

```text
relation_kind
left_side_id
right_side_id
direction
```

`relation_kind` is `intrinsic`, `agreement`, `directional_mapping`, or `package_surface`. `direction` is `none`, `left_to_right`, or `right_to_left`.

- `intrinsic` and `package_surface` require `direction = none`;
- `agreement` names both sides and requires `direction = none`;
- `directional_mapping` names both sides and requires a non-`none` direction.

A symmetric two-sided agreement must not be described as a directional flow. Relation metadata records the artifact boundary being checked; it is not a mandatory Python class and does not itself demonstrate conformance.

## Evidence classes

Software verification checks an implemented software contract. Numerical verification checks implementation of stated mathematics against an independently derived result and declares representation, units or dimensionlessness, scale, and an exact or tolerance rule. Numeric test data alone do not turn software verification into numerical verification.

Scientific validation and uncertainty quantification are separate claim classes. Scientific validation requires an independently authorized comparison of a declared model and use with reference evidence. Uncertainty quantification requires identification and propagation of uncertainty sources. Passing structural, software, schema, fixture, canonicalization, or numerical checks cannot be relabeled as either claim.

Project profiles supply marker vocabulary, evidence namespaces and ranges, scope-to-marker rules, and protected migration debt. Generic resources contain no project prefixes or repository-specific paths. Classification data control which identifiers are structurally valid; they do not prove that the documented oracle is independent or that the asserted scientific interpretation is sound.

## Deterministic owners and maintained audit command

| Capability | Owner |
|---|---|
| Evidence-ID and executable-marker audit | `IdentifierAuditor` |
| Complete test-module structural convention | `PythonConformanceValidator` |
| Semantic test design and review | `develop-python-test-evidence` |

`IdentifierAuditor` accepts only supplied module bytes and an explicit project profile. A project-local wrapper may read one explicitly selected maintained inventory and only its listed modules beneath an explicit absolute root. Generic documentation does not select a project package, profile path, inventory path, or runtime-state root; the project-local command documentation owns those arguments.

The production ActionObject is the sole evidence-ID parser and policy owner. The former standalone AST script is retired; historical evidence may continue to name the command that produced it.

## Validation claim boundary

Resource-contract validation may establish only the behavior it directly checks: resource and schema structure, manifest closure and acyclicity, exact content hashes, supported versions, extension-only overlay rules, project-leakage rejection, explicit-root resolution, fixture/oracle consistency, canonical JSON vectors, and evidence-classification structure.

A `PASS` means only that the supplied resources satisfy those declared structural and software-contract checks. It does not establish:

- skill authorization, execution success, or human acceptance;
- correctness of a future Python-consumer implementation or intended Rust implementation;
- oracle independence, mathematical correctness, or tolerance adequacy unless separately reviewed under an applicable numerical claim;
- provenance, semantic interchangeability, physical correctness, package readiness, or publication readiness;
- scientific validation or uncertainty quantification.

Resource-contract checks contain no scientific calculation and make no scientific-validation or uncertainty-quantification claim. Their fixtures are textual software-verification evidence; a numerical-verification label supplied by a project is classification input, not a newly executed numerical result.

## Consumption by the later Python consumer

Subject to separate resource-task human acceptance and separate activation of the later Python consumer task, that consumer uses the grammar identity, schemas, project-profile rules, fixtures, and canonical vectors without redefining their meanings. Class-owned consumer tests attach to the relevant accepted public object or action. Artifact-owned consumer tests attach to concrete resource, import, path-confinement, canonical-wire, or generic/local dependency boundaries and record any agreement or mapping as relation metadata.

The later Python consumer must preserve `class_owned` and `artifact_owned` as the only generic primary kinds. A project-local compatibility adapter may preserve an accepted legacy spelling and expose a comparison as artifact relation metadata, but generic code and resources must not depend on that local adapter. This handoff is an input contract only: it neither launches the consumer task nor retires, migrates, or dispatches any current skill or test.
