# PI Harness Skills and Textual Resources

## Prospective resource boundary

When separately authorized, reusable non-Python harness material will belong under

```text
harness/pi/
```

Project-specific material will belong under

```text
harness/local/
```

Markdown under `harness/pi/` is operational agent material. Scientific explanation, user guides, and maintained architecture discussion remain under `docs/`.

## Generic resource layout

H3 will define the concrete layout before H2 consumes resource and profile
identities. The generic resource tree may contain accepted skills with their
direct references and deterministic scripts, plus required templates, schemas,
and a resource manifest. Exact names and serialized manifest fields remain
contract decisions; no prospective example path is an implemented interface.

Only required files should be included. A skill should not accumulate redundant README files, changelogs, installation guides, or copied project history.

## Skill design

`SKILL.md` should contain concise routing and procedure. Detailed conventions and examples belong in directly referenced files. References should remain one level from `SKILL.md` so an agent can discover the required material without deep reference chasing.

A reusable skill must state when it applies in its trigger description. It must not depend on an agent already knowing project-specific filenames or task IDs.

## Evidence-documentation skill source

The existing `document-research-python` evidence grammar is the sole source for
future extraction or update. H1-H3 must not create an independent duplicate
skill or competing grammar. The generic capability should support:

- software-verification classification;
- numerical-verification classification;
- scientific-validation requirements;
- UQ boundaries;
- test ownership;
- module naming;
- test-function naming;
- evidence traceability;
- independent-oracle requirements;
- structured test documentation.

Project profiles supply marker names and evidence-ID prefixes.

## Resource manifest

The resource manifest should identify each reusable resource by stable identity, kind, version, and path. It should support deterministic checks for missing, duplicated, or incompatible resources.

The manifest must not treat a filesystem path as the resource's only identity.

## Generic versus local content

Generic instructions may explain how to select an evidence-ID prefix from a profile. They must not embed `SV-CPN-*` as a universal convention.

Local resources may define:

- `SV-CPN-*` and other project namespaces;
- repository test roots;
- CPN-specific ownership rules;
- task-specific review requirements;
- scientific-domain extensions.

Local files should extend or configure the generic skill rather than copy it.

## Validation

Resource validation should check:

- required skill metadata;
- referenced-file existence;
- valid resource-manifest entries;
- deterministic script behavior;
- absence of project leakage;
- successful use with an explicit project profile.

Semantic review must still determine whether a skill's oracle and VVUQ guidance are correct.

## Navigation

- [Previous: Python implementation boundary](./ksdft2effmass.harness.03.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Evidence and test conventions](./ksdft2effmass.harness.05.md)
