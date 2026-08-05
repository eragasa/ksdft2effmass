---
name: document-python-research-software
description: Documents public Python APIs, serialization contracts, conceptual pages, and maintained test evidence under explicit path authorization.
behavior-version: 1
---

# Document Python Research Software

Use this skill when public Python APIs, serialized models, numerical conventions,
or maintained Python documentation are created or changed.

## Load first

For maintained test-evidence documentation or review, read
`references/test-evidence-documentation.md`. It owns the reusable module
headings, per-test and helper fields, semantic naming grammar, evidence ownership
types, parameterization rules, exact-representation policy, independent-oracle
rules, and structural-versus-semantic review boundary.

## Requirements

- Write complete NumPy-style docstrings for public modules, classes, methods,
  functions, properties, enums, exceptions, parameters, returns, raised
  exceptions, dataclass fields, public attributes, and practical examples.
- Define symbols, units, shapes, index ordering, reference conventions, and
  tolerances where they enter the public model.
- Distinguish the modeled subject, mathematical object, numerical
  representation, and software implementation when applicable.
- Document validation rules and exception cases; do not hide assumptions in
  tests or private methods only.
- Document private numerical or architectural policy when its responsibility,
  assumptions, invariants, units, failures, or relationship to the public
  contract are non-obvious. Do not add comments that merely restate types or
  assignments.
- Keep language-version claims consistent with the consuming project's declared
  support policy.
- Use supported public import paths in runnable examples.
- Add or update conceptual and API reference pages, integrate them into the
  consuming documentation's navigation, and run its warnings-as-errors build.
- Do not retain generated documentation-build artifacts.

## Review checklist

- Are claims limited to implemented behavior or explicitly marked as planned?
- Are immutable data, stateless action, and result boundaries visible to users?
- Are serialization schemas versioned with fixed field names?
- Are examples executable without private imports?
- Does the documentation build pass with warnings treated as errors?
- Do source docstrings, tests, schemas, fixtures, API pages, concept pages, and
  governing records describe the same behavior?
- For maintained test evidence, do the exact headings, fields, names,
  ownership, parameterization, representation, oracle-independence, and
  limitation rules in the loaded reference pass structural and semantic review?

## Invocation profiles and authorization policy

An external caller selects exactly one profile and supplies immutable input
identities, an explicit permitted-path set, the requested output shape, and the
stop policy:

- `REVIEW_ONLY` permits inspection and deterministic read-only commands only.
- `AUTHORIZED_DOCS_WRITE` permits edits only to explicitly assigned
  documentation paths.
- `AUTHORIZED_TEST_EVIDENCE_DOC_WRITE` additionally requires separately
  validated test-writer authority and permits only assigned evidence docstrings
  and semantic function names. Assertions, fixtures, parameters, dependencies,
  and represented meaning remain unchanged unless separately authorized.

No profile grants source, schema, fixture, dependency, generated-output, or
external-effect authority. No profile may broaden claims, launch successor work,
or convert review agreement into acceptance. A retry requires a new attempt
identity and either immutable parent authorization or an explicit pre-authorized
retry policy.

The result reports:

```text
skill identity and content hash
request, parent-workflow, and attempt identities
input and produced artifact identities
profile and owned work class
PASS | FAIL | BLOCKED | PARTIAL
structured documentation findings or changes
deterministic commands and exact results
mutation summary
warnings and residual risks
human decisions required
```

A warnings-as-errors documentation build is a deterministic tool result; prose
review cannot substitute for it. Missing references, contradictory public
contracts, unauthorized mutation, or a failed required command produces a
structured failure and stops affected work. Read-only replay against identical
artifact identities is observationally idempotent; writer replay requires
verification of current file identities. Stop after the requested result and do
not accept work or dispatch a successor.
