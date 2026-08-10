<!-- Generated from SQLite control state; do not edit. -->
# Decompose Python conformance around one parsed model

[Task index](index.md) · [Previous](./harness.simplify-2.control-decomposition.md) · [Next](./harness.simplify-2.resource-decomposition.md)

## Status

`inactive`: decomposed work package R2.3; separate explicit human activation required and no automatic successor activation

## Objective

Decompose `python/src/ksdft2effmass/harness/pi/evidence/python_conformance.py` around one immutable parsed test-module model and independent deterministic rule evaluators.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.adapter-retirement`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Parse each selected Python test module once into one immutable internal `PythonTestModuleModel`.
- Separate naming, documentation, parameterization, ownership, migration, and repository-conformance rule ownership while preserving their accepted semantics.
- Return deterministically ordered structured findings through the existing supported conformance result and Action surfaces.
- Synchronize focused maintained test evidence and directly affected evidence documentation using the owning test-evidence procedure.
- Review and, if appropriate, consolidate ownership of the explicit evidence-module inventory reconciliation mechanism with Python conformance's parsed model and rule owners.

## Completion criteria

- One AST parse supplies one immutable module model to independent rule evaluators, and no evaluator reparses source or owns another rule domain.
- Accepted evidence identities, historical aliases, naming, documentation, parameterization, ownership, migration, finding order, public imports, and execute signatures remain stable.
- Focused conformance tests, complete evidence and repository conformance, the maintained harness software-verification suite, Ruff, mypy, documentation validation, and dependency-lock nonmutation checks pass.
- The work package completes without activating its successor.
- The explicit evidence-module inventory reconciliation mechanism is reviewed for duplication with the parsed model and rules, and any appropriate ownership consolidation preserves its validated explicit-input and transactional projection contract.

## Exclusions

- Do not weaken evidence requirements, change accepted identifiers, expected values, tolerances, skips, or evidence classifications merely to obtain passing checks.
- Do not claim scientific validation or uncertainty quantification from software-conformance results.
- Do not implement R2.4 through R2.7, activate another work package, add dependencies, modify scientific/package-source modules, or perform protected or release actions.

## Historical source

No archived source.
