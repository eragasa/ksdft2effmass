# PI Harness Project-Local Extension Model

## Purpose

The local extension layer supplies the information that makes a generic harness applicable to `ksdft2effmass` without contaminating the reusable core.

The local layer is an adapter and configuration boundary, not a fork of the harness.

## Python-local layer

Active H4 places project-specific Python functionality under

```text
python/src/ksdft2effmass/harness/pi/local/
```

Its public package exports 30 names: record adapters
(`AdaptAgentRecords`, `AdaptChainRecord`, `AdaptCheckpointRecords`,
`AdaptChecksumCatalog`, `AdaptEvidenceOwnershipManifest`,
`AdaptOwnershipManifest`, `AdaptSkillInventory`, `AdaptTaskRecords`, and
`SelectEvidenceModules`); composition and validation actions
(`LoadLocalHarnessContext`, `ValidateLocalRepository`); routing actions and
records (`SelectValidationRoute`, `RollBackValidationRoute`, `ValidationRoute`,
`RouteConfiguration`, and `RouteSelection`); shadow records/actions
(`LegacyInvocation`, `ShadowObservation`, `ShadowPairResult`,
`ShadowReplayResult`, `CompareShadowPair`, and `ReplayShadowSuite`); and local
records/results (`RepositoryRoots`, `LocalHarnessContext`, `LocalIssue`,
`LocalValidationResult`, `AdaptationResult`, `EvidenceOwnershipRelation`,
`AdaptedRepositoryRecords`, and `RepositoryValidationResult`).

These APIs adapt caller-supplied bytes and observations; they do not discover or
execute legacy commands. `SelectValidationRoute` and
`RollBackValidationRoute` are pure actions over caller-supplied
`RouteConfiguration` values; neither writes route configuration or restores
filesystem resources. The concrete live consumer is
`.pi/skills/validate_harness.py`, and `harness/local/validation-route.json` is
its single route owner. The local package imports the generic harness. The
generic package does not import the local package or project-domain modules.

## Textual-local layer

Active H4 places project-specific textual resources under

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

The caller constructs `RepositoryRoots` with three absolute, existing, distinct
paths: the repository root, `harness/pi/` generic resource root, and
`harness/local/` local resource root. Both resource roots must be below the
repository root. `LoadLocalHarnessContext` also receives exact profile and
manifest bytes plus their declared SHA-256 identities; it validates the v2
profile/manifest composition before returning a context. There is no current-
working-directory fallback, environment lookup, or ambient profile discovery.
This makes tests reproducible and prevents accidental coupling to invocation
location.

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

## Retained ownership compatibility

The P1 v1 evidence inventory retains the local spelling `boundary_owned`. The
local `AdaptEvidenceOwnershipManifest` maps it to the generic
`artifact_owned` kind and adds explicit `agreement` relation metadata with the
preserved left/right owner IDs and direction `none`. It does not introduce a
third generic ownership kind or change the historical P1 manifest.

## Testing the boundary

`artifact_owned` relation tests establish:

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
