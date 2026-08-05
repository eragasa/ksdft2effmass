# PI Harness Skills and Textual Resources

## Resource boundary

The accepted H3 snapshot and active H4 integration place reusable non-Python harness material under

```text
harness/pi/
```

Project-specific material will belong under

```text
harness/local/
```

Markdown under `harness/pi/` is operational agent material. Scientific explanation, user guides, and maintained architecture discussion remain under `docs/`.

## Generic resource layout and identity

H3 established the generic tree, direct references, schemas, fixtures, and
manifests consumed by H2. Its accepted checksum catalog remains the historical
version-1 rollback identity. H4's current live resource composition is manifest
version 2: `pih.generic.resources` extends to
`ksdft2effmass.local.resources`, and the explicitly supplied
`ksdft2effmass.profile.v2` binds both manifest IDs and version 2. Resource entry
schema and format versions remain 1; manifest revision and resource format are
distinct identities. The v2 rename and content identities do not rewrite the
accepted H3 v1 evidence.

Only required files should be included. A skill should not accumulate redundant README files, changelogs, installation guides, or copied project history.

## Skill design

`SKILL.md` should contain concise routing and procedure. Detailed conventions and examples belong in directly referenced files. References should remain one level from `SKILL.md` so an agent can discover the required material without deep reference chasing.

A reusable skill must state when it applies in its trigger description. It must not depend on an agent already knowing project-specific filenames or task IDs.

## Evidence-documentation skill source

The canonical live `document-python-research-software` skill and its directly
referenced test-evidence grammar are the sole maintained source. The former
`document-research-python` name is retained only in H3 historical identity and
H4 rename traceability; it is not a live alias or competing grammar. The generic
capability supports:

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

The generic and local manifests identify each reusable resource by stable
`resource_id`, kind, format version, manifest-root-relative path, SHA-256 content
identity, and dependency IDs. The generic manifest is the authoritative generic
inventory; the local manifest may only extend its named generic base. Neither a
filesystem path nor a stale task/checkpoint snapshot is a resource identity.

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
