# H1 — Harness contract and package boundary

Status: active and blocked at pending `H1-HC01`; corrected contract evidence and final reviews pass; no implementation authorized

## Objective

Define the smallest stable generic harness contract and the package/resource boundary required for incubation and later extraction. Existing scripts are requirement evidence, not automatically the public API.

## Activation and prerequisite

`H0:human_accepted` is satisfied through resolved `H0-HC01`. The human PI
explicitly activated H1 on 2026-08-04 in the instruction titled "Activate and
execute H1 — PI Harness contract and package boundary". Activation is retained
in `.pi/evidence/pi-harness-incubation/H1/activation.json` and authorizes only
this contract task. H1 consumes the accepted 316-component inventory,
classifications, generic/local boundary, source-of-truth map, six finding
resolutions, H3-before-H2 sequencing recommendation, migration constraints, and
proposed minimum contract.

## Planned scope

Subject to accepted H0, H1 may specify:

- immutable record and structured result boundaries;
- stateless validation/loading ActionObjects;
- explicit project-profile semantics;
- resource identity and manifest rules;
- public-contract, profile-schema, resource-manifest, skill, and implementation version layers;
- structured invalid-input versus internal-failure diagnostics;
- path confinement and explicit resource-root behavior;
- exact generic/local/package-extraction boundary;
- clean-revision reproducible validation distinguished from optional
  project-local pre-commit worktree checks; and
- successor task vocabulary reconciled to the accepted primary evidence kinds
  `class_owned` and `artifact_owned` before implementation, with agreement and
  direction represented as artifact relation metadata and legacy terminology
  retained only as explicit project-local compatibility input.

The planned ownership split remains:

```text
generic Python:             python/src/ksdft2effmass/harness/pi/
project-specific Python:    python/src/ksdft2effmass/harness/pi/local/
generic textual resources: harness/pi/
project-specific resources: harness/local/
runtime project state:      .pi/
maintained documentation:   docs/harness/
```

Project-local may depend on generic; generic must not depend on project-local.
Personal and concurrently edited working notes are outside harness authority.
Historical H0 worktree observations about them are nonmutation provenance only,
not required harness resources or reusable validator inputs.

## Exclusions

No production Python or textual-resource implementation, source movement, legacy retirement, package publication, P2 work, or scientific execution. H1 must not silently resolve conflicts retained by H0.

## Required decision

H1 is blocked at `.pi/checkpoints/H1-HC01-harness-contract.json`, a genuine human
checkpoint accepting, correcting, rejecting, or deferring the public
internal API, version boundaries, profile/resource loading, structured errors,
path rules, extraction boundary, and the exact ordered H3-then-H2 ownership
plan. That plan must define paths, profiles, schemas, compatibility boundaries,
and non-overlapping writer/reviewer ownership before H3 or H2 is separately
activated. H1 acceptance does not activate H3.

## VVUQ boundary

Software-contract review is required. Numerical verification is required only if H1 authorizes an actual numerical algorithm. Scientific validation and UQ are not applicable.
