# H1 — Harness contract and package boundary

Status: human-accepted H1 retained with the bounded version-1 `H2-HC01` Option-A contract/resource correction active under H2; no interface/version expansion

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

## Resolved decision and bounded correction

The human PI resolved `.pi/checkpoints/H1-HC01-harness-contract.json` as Option B
on 2026-08-04: accept the H1 architecture subject to exactly one bounded
contract-only correction. H1 must introduce the neutral `DiagnosticPath`
semantic primitive and change `ValidationIssue.path` from
`ResourcePath | None` to `DiagnosticPath | None` without weakening
`ResourcePath` or `OwnershipScopePath`. The correction must reconcile all
affected contract evidence, intended Python/Rust mappings, planned H2 tests,
planned H3 schemas and fixtures, maintained documentation, validation, and
focused independent reviews while retaining the original finding and correction
trace.

The human PI granted final Option-A acceptance through resolved
`.pi/checkpoints/H1-HC02-final-acceptance.json` on 2026-08-04. H1 is closed as
human-accepted `PASS` after one deterministic closeout validation. The accepted
contract, correction history, reviews, and checkpoint responses remain retained.
H3 was not activated. H3-H5, P2-P11, implementation, resource/schema creation,
external or scientific execution, and publication remain blocked.

## Bounded H2-HC01 correction

Resolved `H2-HC01` Option A authorizes only the directly affected version-1
boundary correction: `ResourceReference` self-dependency and duplicate
`ResourceManifest` entries remain structurally representable, while
`ValidateResourceManifest` owns manifest relations and downstream actions
short-circuit on its failure. Intrinsic constructor/deserializer validation,
all public interfaces/codes/versions, and extension-only generic/local policy
remain unchanged. This is a pre-H2-acceptance correction, not H1 reopening or
successor activation.

## VVUQ boundary

Software-contract review is required. Numerical verification is required only if H1 authorizes an actual numerical algorithm. Scientific validation and UQ are not applicable.
