---
name: document-research-python
description: Documents public research-software Python APIs and Sphinx pages. Use for new public Python APIs, scientific data models, numerical conventions, serialization schemas, and Sphinx conceptual or API documentation.
---

# Document Research Python

Use this skill when public Python APIs or scientific conventions are created or changed.

## Load first

For maintained test-evidence documentation or review, read
`references/test-evidence-documentation.md`. It owns the unified module headings,
per-test/helper fields, semantic naming grammar, evidence ownership types,
parameterization rules, exact-representation policy, independent-oracle rules,
and structural-versus-semantic review boundary.

## Requirements

- Write complete NumPy-style docstrings for public modules, classes, methods, functions, properties, enums, exceptions, parameters, returns, raised exceptions, dataclass fields, public attributes, and examples when practical.
- Define symbols, units, shapes, index ordering, gauge, energy-zero, and tolerance conventions at the point where they enter the public model.
- Distinguish physical model, mathematical operator, numerical representation, and software implementation.
- Document validation rules and exception cases; do not hide scientific assumptions in tests or private methods only.
- Document every private method and private attribute in maintained first-party source. Explain owned responsibility, accepted and rejected types, canonicalization, invariants, error taxonomy, why the method or state is private, and whether the logic is mechanical, numerical, or scientific.
- Add nearby comments for scientifically, numerically, or architecturally meaningful local variables such as canonicalized values, residuals, norms, singular values, compatibility findings, validation state, unit conversions, shapes, and deterministic ordering state.
- Keep Python-version claims consistent with the supported Python 3.14 environment.
- Include runnable examples using the supported public import path.
- Add or update Sphinx conceptual documentation and API reference pages.
- Integrate new pages into a discoverable toctree.
- Build Sphinx with warnings treated as errors, for example by discovering the repository's actual command and using `sphinx-build -W` semantics.
- Do not commit generated `_build` artifacts.

## Review checklist

- Are claims limited to implemented behavior or explicitly marked as planned?
- Are DataObject/ActionObject boundaries visible to users?
- Are serialization schemas versioned with fixed field names?
- Are examples executable without private imports?
- Does the docs build pass with warnings as errors?
- Do source docstrings, tests, public schemas or fixtures, Sphinx API pages, concept pages, and control-plane records describe the same behavior?
- Does read-only documentation review report no unresolved material source-documentation findings?
- For migrated test evidence, do the exact headings, fields, names, ownership,
  parameterization, representation, oracle-independence, and limitation rules in
  `references/test-evidence-documentation.md` pass both structural and semantic
  review?

## CPN-compatible invocation profiles

This skill is applied by an external agent/harness outside CPN guard evaluation.
A request selects `REVIEW_ONLY`, `AUTHORIZED_DOCS_WRITE`, or
`AUTHORIZED_TEST_EVIDENCE_DOC_WRITE` and records the task and
parent-workflow/attempt identities, immutable source/test/schema/fixture and
documentation references, authoritative conventions, expected output shape,
permitted paths, evidence classification, and stop policy.

`REVIEW_ONLY` permits inspection and deterministic read-only commands only.
`AUTHORIZED_DOCS_WRITE` may edit only explicitly assigned documentation paths.
`AUTHORIZED_TEST_EVIDENCE_DOC_WRITE` requires a separately validated test-writer
assignment and may edit only the assigned test evidence's docstrings and semantic
function names; assertions, fixtures, parameters, dependencies, and scientific
meaning remain unchanged unless separately authorized. The profile supplies no
test ownership by itself. No profile transfers source, schema, fixture,
dependency, or generated-output ownership. No profile may silently broaden
scientific claims, launch downstream work, or convert review agreement into
acceptance.

The result must report:

```text
skill identity and content hash
request, task, parent-workflow, and attempt identities
input and produced artifact identities
profile and owned task class
PASS | FAIL | BLOCKED | PARTIAL
structured documentation findings or changes
deterministic commands and exact results
mutation summary
warnings and residual risks
human decisions required
```

Sphinx warnings-as-errors is a deterministic tool result with the command,
environment, source identity, and temporary output location recorded; prose
review cannot substitute for it. Missing references, contradictory public
contracts, unauthorized mutation, or a failed required command produces a
structured failure and stops the affected work. Retries require an immutable
parent authorization identity or a request's pre-authorized retry policy, use new
attempt identities, and retain prior findings. Read-only replay against identical
artifact identities is observationally idempotent; writer replay requires parent
verification of current file identities. Stop after the requested result and do
not generate or commit `_build` output, accept the task, or launch a successor.
