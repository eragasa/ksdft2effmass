---
name: develop-python-test-evidence
description: Designs, writes, modifies, and reviews maintained Python software-verification, numerical-verification, and separately authorized validation or UQ tests. Use when creating class-owned or artifact-owned pytest evidence, test fixtures, parameterized cases, independent oracles, acceptance rules, test documentation, or test-evidence audits.
---

# Develop Python Test Evidence

Use this skill for maintained pytest evidence, including new tests, controlled migrations, fixtures, parameter cases, documentation, deterministic structural audits, and semantic review.

## Load first

Read `references/test-evidence-conventions.md` completely before acting. Do not rely on this concise entry point as a substitute: the reference owns classification, ownership, placement, module and function documentation, surface naming, cohesion, helpers, parameterization, evidence identifiers, oracles, acceptance, schema/runtime layering, migration, reporting, workflow, and invocation rules.

## Required invocation

Select exactly one reference-defined profile: `REVIEW_ONLY`, `AUTHORIZED_TEST_EVIDENCE_WRITE`, or `AUTHORIZED_TEST_EVIDENCE_DOC_WRITE`. Supply immutable request/task/attempt identities, explicit paths, structured `class_owned` or `artifact_owned` ownership, authoritative contracts, the expected result shape, and a stop policy. Writer profiles also require explicit writer authority and permitted mutation paths.

Run structural validation strictly on explicitly supplied new or migrated paths. Inventory other paths as diagnostic legacy debt only. Structural results cannot decide whether a surface is semantically correct, a test is cohesive, an oracle is independent, mathematics is correct, a tolerance is adequate, or scientific validation/UQ/human acceptance is established.

Return input and output identities, profile, ownership, paths, evidence classification, findings or changes, commands and exact results, mutation summary, collection/evidence counts, residual risks, and human decisions required. Stop on missing authority, conflicting contracts, invalid ownership, incomplete mapping, unauthorized mutation, or failed required gates. A retry uses a new attempt identity and verified current inputs. Do not dispatch successors or claim acceptance.
