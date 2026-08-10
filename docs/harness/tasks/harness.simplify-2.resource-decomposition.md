<!-- Generated from SQLite control state; do not edit. -->
# Decompose resource resolution and routing ownership

[Task index](index.md) · [Previous](./harness.simplify-2.python-conformance-decomposition.md) · [Next](./harness.simplify-2.validation-retirement.md)

## Status

`inactive`: decomposed work package R2.4; separate explicit human activation required and no automatic successor activation

## Objective

Decompose `python/src/ksdft2effmass/harness/pi/resources.py` into independent records, manifests, resolution, refresh or projection, and skill-closure ownership while preserving the distinct manifest-addressed resource tree under `harness/pi/` and simplifying project agent and skill routing.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.python-conformance-decomposition`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Separate resource records, manifest semantics, explicit root-confined resolution, selected identity refresh or projection, and skill-resource closure along the accepted dependency direction.
- Keep immutable records independent of operational Actions and preserve existing public resource Actions, imports, and execute signatures.
- Preserve generic and project-local ownership: generic resources remain project-independent and project-local resources may depend only on accepted generic identities.
- Rationalize maintained harness roles toward implementation, verification, documentation, and read-only integration review with shared policy stored once and task-selected skills.

## Completion criteria

- Records, manifests, resolution, refresh or projection, and skill closure have explicit owners and the dependency direction remains records to manifests to operational consumers.
- Generic resources perform no repository discovery and acquire no project Task identities, policy, or scientific meaning; project-local overlays do not replace generic identities.
- Existing public resource Actions and supported manifests, profiles, descriptors, fixtures, and canonical or live copies remain contract-consistent.
- Focused resource tests, manifest and descriptor closure, local overlay validation, the maintained harness software-verification suite, Ruff, mypy, documentation validation, and dependency-lock nonmutation checks pass.
- The work package completes without activating its successor.

## Exclusions

- Do not duplicate `ResourceManifestValidator`, `ResourceManifestRefresher`, `ResourceResolver`, `SkillResourceValidator`, or canonical-JSON algorithms.
- Do not reverse the generic-to-project-local dependency direction, create implicit CWD or Git-root discovery, or change behavior versions without accepted authority.
- Do not implement R2.5 or R2.6, activate another work package, add dependencies, modify scientific/package-source modules, or perform protected or release actions.

## Historical source

No archived source.
