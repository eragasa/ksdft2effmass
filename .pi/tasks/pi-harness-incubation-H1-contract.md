# H1 — Harness contract and package boundary

Status: blocked by accepted H0; no implementation authorized

## Objective

Define the smallest stable generic harness contract and the package/resource boundary required for incubation and later extraction. Existing scripts are requirement evidence, not automatically the public API.

## Prerequisite

`H0:human_accepted`. H1 must consume the accepted H0 inventory, classifications, source-of-truth map, and migration constraints.

## Planned scope

Subject to accepted H0, H1 may specify:

- immutable record and structured result boundaries;
- stateless validation/loading ActionObjects;
- explicit project-profile semantics;
- resource identity and manifest rules;
- public-contract, profile-schema, resource-manifest, skill, and implementation version layers;
- structured invalid-input versus internal-failure diagnostics;
- path confinement and explicit resource-root behavior;
- exact generic/local/package-extraction boundary.

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

## Exclusions

No production Python or textual-resource implementation, source movement, legacy retirement, package publication, P2 work, or scientific execution. H1 must not silently resolve conflicts retained by H0.

## Required decision

H1 concludes at a genuine human checkpoint accepting or correcting the public internal API, version boundaries, profile/resource loading, structured errors, path rules, extraction boundary, and disjoint H2/H3 ownership plan.

## VVUQ boundary

Software-contract review is required. Numerical verification is required only if H1 authorizes an actual numerical algorithm. Scientific validation and UQ are not applicable.
