# H3 — Skills and textual-resource extraction

Status: closed as human-accepted `PASS` through resolved `H3-HC01`; H2 prerequisite satisfied but H2 remains inactive and separately authorized

## Objective

Create accepted generic operational skills and textual resources under `harness/pi/`, with project profiles/extensions under `harness/local/`, without copying project-specific task IDs, evidence prefixes, scientific semantics, or repository paths into the generic layer.

## Activation and prerequisite

`H1:human_accepted` is satisfied through resolved `H1-HC02`. The human PI
separately activated H3 on 2026-08-04 in the instruction titled "Activate and
execute H3 under its existing accepted task, chain, H1 contract, ownership,
review, and validation requirements". Activation is retained at
`.pi/evidence/pi-harness-incubation/H3/activation.json`. The required version-2
ownership manifest is
`.pi/evidence/pi-harness-incubation/H3/task-ownership.json`; it must validate
before any resource writer edits. This activation authorizes H3 only and does
not activate H2, H4, H5, or P2.

## Planned scope

Subject to H1 approval, extract only classified generic skills, directly referenced one-level resources, templates, schemas, manifests, and parameterized validators. Project-local profiles supply marker names, evidence-ID namespaces, paths, and scientific/task extensions. Resource identities require kind, version, stable identifier, dependencies, and content identity where required.

## Evidence

Resource-manifest validation; missing/duplicate/incompatible resource cases;
reference resolution; explicit-profile use; project-leakage checks;
software/numerical evidence-classification behavior; independent oracle and
ownership review; documentation and integration review. The planned
`ValidationIssue` schema must use `DiagnosticPath | null`, with valid fixtures
for a regular-file spelling, directory-tree ownership-scope spelling, and
`null`; invalid fixtures for absolute, traversal, non-NFC, malformed, control,
repeated/trailing-separator, and Windows/platform-specific forms; and canonical
JSON vectors for later Python/intended Rust round-trip agreement.

## Exclusions

No generic Python implementation owned by H2, no silent skill retirement, no replacement of authoritative `.pi` runtime state, no package publication, no P2 work, and no scientific execution.

## Sequence rule

H3 precedes H2 and must not overlap H2. It establishes the accepted generic and
local textual resource identities that H2 consumes.

## Final acceptance

The resource validator, separate control checks, one consolidated correction
cycle, and three final independent read-only reviews reported `PASS`. The human
PI accepted Option A through resolved
`.pi/checkpoints/H3-HC01-final-acceptance.json` on 2026-08-04. H3 is closed as
human-accepted `PASS`. This acceptance satisfies H2's H3 prerequisite but does
not activate H2 or any other successor.

## Stop

H3 concludes only at separate human acceptance. Accepted H3 satisfies H2's task
prerequisite but does not activate H2; H2 requires its own separate human
authorization.
