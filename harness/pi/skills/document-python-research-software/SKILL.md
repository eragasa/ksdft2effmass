---
name: document-python-research-software
description: Documents public Python source APIs, serialization contracts, concepts, and Sphinx pages under explicit path authorization.
behavior-version: 1
---

# Document Python Research Software

Use this skill for public source docstrings, API and conceptual documentation, Sphinx integration, and serialization-contract documentation.

## Requirements

- Write complete NumPy-style documentation for public modules, objects, members, fields, parameters, returns, exceptions, attributes, and useful examples.
- Define symbols, units, shapes, ordering, reference conventions, invariants, validation behavior, and tolerances where they enter the public contract.
- Distinguish modeled subject, mathematical object, numerical representation, and software implementation.
- Keep source, serialization schemas, fixtures, API pages, concept pages, and implemented behavior consistent.
- Use supported public imports in examples; integrate pages into navigation; run the consuming Sphinx build with warnings as errors; retain no generated output.

This skill may document test results without redefining their evidence class, ownership, grammar, oracle, acceptance, parameterization, assertions, or represented meaning. Creating, restructuring, migrating, or mutating tests requires `develop-python-test-evidence` plus separate test authority. Refer test-evidence review and changes to that skill; documentation authority alone never supplies test authority.

Select `REVIEW_ONLY` or `AUTHORIZED_DOCS_WRITE` and supply immutable input identities and explicit paths. No profile grants source implementation, test, fixture, dependency, external-effect, scientific-meaning, or acceptance authority. Report identities, findings or changes, commands/results, mutation summary, warnings, and residual risks. Stop after the documentation result; do not launch work or claim acceptance.
