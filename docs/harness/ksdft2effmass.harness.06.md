# PI Harness Project-Local Extension Model

## Purpose

The local extension layer supplies the information that makes a generic harness applicable to `ksdft2effmass` without contaminating the reusable core.

The local layer is an adapter and configuration boundary, not a fork of the harness.

## Prospective Python-local layer

When separately authorized, project-specific Python functionality will belong under

```text
python/src/ksdft2effmass/harness/pi/local/
```

It may own:

- profile construction;
- repository-path mapping;
- local validation composition;
- project-specific structured issue codes when approved;
- adapters between generic harness records and `.pi` records;
- explicit routing to project-local skills.

It may import both the generic harness and project-domain modules. The generic layer may not import it.

## Prospective textual-local layer

When separately authorized, project-specific textual resources will belong under

```text
harness/local/
```

It may contain:

- project profiles;
- evidence-ID namespace configuration;
- local skill extensions;
- project templates;
- CPN/QE/Wannier review rules;
- local path inventories.

It must not copy complete generic skills or validators.

## Explicit activation

The harness must not discover the local profile merely because it is executed inside this repository. The caller supplies the profile explicitly.

Conceptually,

```python
profile = load_project_profile(profile_path)
result = validator.execute(record, profile)
```

This makes tests reproducible and prevents accidental coupling to the current working directory.

## Extension limits

The local layer may narrow generic policy when required by the project. It must not silently weaken a generic safety or integrity invariant.

Any override should identify:

- the generic rule;
- the local reason;
- the bounded scope;
- the applicable version;
- tests;
- review and approval.

## Source-of-truth rule

Each rule has one authoritative owner.

- Reusable procedure belongs to the generic harness.
- Project configuration belongs to the local profile.
- Scientific meaning belongs to domain code and architecture documentation.
- Mutable execution state and authorization belong solely to `.pi/tasks/`,
  `.pi/checkpoints/`, and `.pi/chains/`.

If a local file restates a generic rule for convenience, it risks becoming a divergent implementation. Prefer a reference or configured extension.

## Testing the boundary

`artifact_owned` relation tests should establish:

- local configuration is accepted by the generic contract;
- invalid local configuration fails structurally;
- local extensions do not alter generic behavior outside their declared scope;
- generic tests pass when the local tree is absent;
- project integration tests pass when the local profile is supplied;
- no local resource enters the generic package inventory.

## Navigation

- [Previous: Evidence and test conventions](./ksdft2effmass.harness.05.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Migration and shadow replay](./ksdft2effmass.harness.07.md)
