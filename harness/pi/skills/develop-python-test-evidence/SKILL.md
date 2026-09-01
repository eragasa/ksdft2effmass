---
name: develop-python-test-evidence
description: Designs, writes, modifies, restructures, names, documents, and reviews maintained Python test evidence, fixtures, parameterization, numerical verification, and separately authorized validation or UQ tests.
---

# Develop Python Test Evidence

## Purpose

Use this skill for maintained Python tests and test-owned fixtures: creating or
modifying tests, restructuring modules, naming evidence, designing semantic
parameterization, documenting cases, establishing independent oracles, and
reviewing evidence claims. Task and path authority remain external to this skill.

## Load first

Read `references/test-evidence-conventions.md` completely. Use
`design-data-action-objects` for general object architecture,
`develop-operator-records` for represented-operator contracts,
`document-python-research-software` for public source/API/Sphinx documentation,
and `develop-architecture-decision` for a material open architecture choice.

## Evidence classification

| Evidence class | Establishes |
|---|---|
| Software verification | Public software-contract behavior |
| Numerical verification | Numerical implementation against an independent mathematical oracle |
| Scientific validation | Adequacy against trusted physical, experimental, or scientific reference evidence |
| Uncertainty quantification | Characterization or propagation of uncertainty |

Verification classes do not imply physical adequacy. Scientific validation and
UQ require separately authorized protocols. A test must claim only the evidence
class it actually executes.

## Ownership and naming

Choose exactly one primary module owner:

- `class_owned` for one public class as the sole system under test; or
- `artifact_owned` for a schema or fixture family, package/public surface,
  dependency direction, wire contract, command, or cross-object agreement.

Do not use `boundary_owned` as a generic primary kind. Prefer one class per
class-owned module and cohesive, concise artifact-owned integration modules.
Name evidence-owning tests
`test_<surface>__<facet>__<behavior>` after public behavior, using the surface
vocabulary accepted by the maintained validator. Identify special methods as
methods, for example `test_method__eq__...` and `test_method__getitem__...`.

## Oracle and documentation summary

Use public contracts, schemas, exact language semantics, independently derived
mathematics, or trusted reference data as oracles. Do not use private behavior or
a reproduction of the production algorithm as the primary oracle. Use exact
acceptance for exact contracts and justified tolerances for numerical contracts.

Each module declares an evidence profile. The sole normative field and
class/profile requirements are the versioned generic resource
`evidence/python-test-evidence-profile-matrix-v1.json`; this skill does not
repeat them. Required and present optional fields use `Label: value` paragraphs
with one blank line between paragraphs. Helpers remain ID-free, semantically
named, and non-tautological. Parameterized cases use explicit semantic IDs.

## Deterministic-validator boundary

`PythonConformanceValidator` and its thin CLI own structural enforcement. Invoke
it on explicit module paths and an explicit ownership file:

```text
python3 -m <project-harness-cli-module> validate-python-conformance \
  --ownership <ownership.json> \
  --profile-matrix harness/pi/evidence/python-test-evidence-profile-matrix-v1.json \
  <test-module> [<test-module> ...]
```

Replace `<project-harness-cli-module>` with the explicit module selected by the
project-local harness configuration; do not infer it from the current directory.
Supply `--migration-map <map.json>` only for an authorized rename or migration
with predecessors. Structural PASS does not establish semantic correctness,
cohesion, oracle independence, mathematical correctness, tolerance adequacy,
scientific validity, UQ adequacy, or human acceptance.

## Essential stop conditions

Stop when the public or mathematical contract, evidence class, primary owner,
independent oracle, acceptance rule, or separately required validation/UQ
protocol is missing or conflicting. Do not invent scientific meaning, weaken an
exact contract, renumber evidence IDs, or mutate production behavior merely to
make a test pass.
