# HarnessConfiguration source and wire decision

## Problem

**Human choice.** Direct Architecture-v2 implementation and direct v1 configuration
cutover are approved. Before coding, the public contract must determine whether
`HarnessConfiguration` is an authored document, a resolved aggregate, or both. This
choice controls whether Pi settings are duplicated, how source identity is retained,
and what JSON serialization means.

## Observed current behavior

**Observed fact.** The implemented `PiHarnessConfigurationDeserializer` consumes
explicit `.pi/settings.json` bytes and deliberately ignores Pi-owned members outside
the narrow harness-consumed subset.

**Observed fact.** Current v1 control configuration is fragmented among
`.pi/settings.json`, command-line arguments, private constants in
`python/src/ksdft2effmass/harness/pi/local/control/inputs.py`, and the default control
database path.

**Observed fact.** Pi still requires its own project-settings document for Pi runtime
behavior. The harness cannot become the owner of Pi's complete settings schema.

**Observed fact.** The approved architecture requires a resolved
`HarnessConfiguration` that encapsulates `PiHarnessConfiguration`,
`HumanReviewConfiguration`, and `HarnessPersistenceConfiguration` without containing
live services or authority.

**Inference.** One JSON type cannot simultaneously be a minimal human-authored source,
a resolved snapshot containing normalized Pi values, and a provenance-bearing
resolution result without conflating distinct object responsibilities.

## Decision requirements

Accepted requirements are:

- one authoritative place for harness-owned authoring values;
- Pi retains authority over `.pi/settings.json`;
- resolved `HarnessConfiguration` encapsulates `PiHarnessConfiguration`;
- direct v1 cutover without an adapter, alias, or shadow authority;
- canonical JSON initially and YAML deferred;
- explicit source identities and fail-closed resolution;
- concrete immutable DataObjects rather than a generic configuration protocol; and
- no live repositories, connections, credentials, or grants in configuration.

The remaining human choice is the allocation of authored source, resolved value, and
serialized snapshot responsibilities.

## Option A

**Conceptual model**  
One human-authored canonical `HarnessConfiguration` JSON document contains all nested
resolved values, including the normalized Pi subset.

**Authority**  
The document becomes harness authority, while `.pi/settings.json` remains Pi authority.
Agreement must be checked because Pi values are represented twice.

**Ownership/dependency**  
`HarnessConfigurationJsonDeserializer` owns the full harness document;
`PiHarnessConfigurationDeserializer` separately owns Pi settings.

**Runtime/dispatch**  
Composition loads both documents and rejects disagreement before constructing
services. State and persistence remain outside configuration.

**Migration**  
V1 constants and CLI values move into the new document; normalized Pi disablement is
copied into it and compared with `.pi/settings.json`.

**Reversibility**  
Git can revert the cutover, but every Pi-settings change must update two sources.

**Failures**  
Stale duplicated Pi values create frequent mismatch failures and unclear edit order.

**Complexity**  
Few public types but substantial synchronization policy.

**Maintenance**  
High ongoing duplication cost.

**Context-window consequences**  
One file is easy to inspect, but agents must remember that part of it mirrors another
authority.

**Future compatibility**  
Poor fit if Pi settings evolve independently.

**Advantage**  
A single directly editable JSON object appears to contain everything.

**Risk**  
Creates exactly the duplicate Pi authority the architecture intended to avoid.

## Option B

**Conceptual model**  
A human-authored `HarnessConfigurationSource` JSON document contains only harness-owned
values and an explicit root-relative `pi_settings_path`. `HarnessConfigurationResolver`
combines that source with exact Pi settings bytes and returns
`HarnessConfigurationResolutionResult`, whose successful variant contains the resolved
`HarnessConfiguration`, ordered source content identities, and one configuration
snapshot identity.

**Authority**  
The source document owns harness-native values; `.pi/settings.json` owns Pi values. The
resolved aggregate is an immutable result, not a second editable authority.

**Ownership/dependency**  
Subsystem DataObjects own their fields. The resolver composes
`HarnessConfigurationSource` and `PiHarnessConfiguration`; the resolution ResultObject
owns provenance and snapshot identity.

**Runtime/dispatch**  
Application composition loads the exact source path, loads its explicitly referenced Pi
path, resolves once, and injects the successful resolved aggregate. No ambient fallback
is permitted.

**Migration**  
V1 hard-coded harness paths move into the source document. Existing Pi parsing remains
its nested owner. Current v1 consumers are changed directly to receive the resolved
aggregate or fields derived from it; no migration adapter remains.

**Reversibility**  
The source and direct cutover are a focused Git-revertible change.

**Failures**  
Missing sources, identity changes during observation, invalid Pi consumed fields, and
cross-component incompatibility return a closed failed resolution with no usable
configuration.

**Complexity**  
Adds one source DataObject and one resolution ResultObject, but each has a distinct
responsibility.

**Maintenance**  
One harness-owned authoring file and one independently owned Pi file; no duplicated
values.

**Context-window consequences**  
Reviewers inspect one harness source plus the externally owned Pi source identified by
it. The resolved result states exactly which bytes were composed.

**Future compatibility**  
Supports later subsystem sources without changing the resolved aggregate's ownership
model.

**Advantage**  
Preserves source authority, resolved encapsulation, and provenance without duplication.

**Risk**  
Introduces more explicit public types and requires careful naming of source versus
resolved serialization.

## Option C

**Conceptual model**  
There is no harness-native authored configuration document. Application composition
continues to collect distributed constants and Pi settings, then serializes only a
resolved `HarnessConfiguration` snapshot.

**Authority**  
Authority remains distributed across code constants and Pi settings; the snapshot is a
derived artifact.

**Ownership/dependency**  
Subsystems own values, but no single harness-owned authoring boundary exists.

**Runtime/dispatch**  
A resolver discovers or is passed every distributed input and emits a snapshot.

**Migration**  
V1 hard-coded paths remain or move to other code-owned constants.

**Reversibility**  
Minimal source migration, but future consolidation remains necessary.

**Failures**  
Missing or inconsistent distributed inputs remain difficult to diagnose and review.

**Complexity**  
Few new source types, but composition complexity stays hidden in code.

**Maintenance**  
Configuration remains fragmented.

**Context-window consequences**  
Agents must reconstruct configuration from multiple modules and command surfaces.

**Future compatibility**  
Weak basis for user-facing configuration or alternate deployment locations.

**Advantage**  
Smallest initial implementation.

**Risk**  
Fails the requirement for one authoritative harness-owned configuration location.

## Three-option comparison

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Harness-owned authoring location | One | One | None |
| Pi value duplication | Yes | No | No |
| Resolved aggregate | Yes | Yes | Yes |
| Explicit provenance result | Possible but conflated | Yes | Yes |
| Direct v1 cutover | Possible | Clean | Incomplete |
| Ongoing synchronization burden | High | Low | Medium |
| Responsibility separation | Weak | Strong | Weak |
| Recommended | No | **Yes** | No |

## Recommendation

**Recommend Option B.**

It satisfies the request for one harness-owned configuration location while preserving
Pi's external authority. It also makes the distinction among authored source, resolved
configuration, and resolution provenance explicit:

```text
HarnessConfigurationSource       # canonical authored JSON
        + exact .pi/settings.json bytes
        |
        v
HarnessConfigurationResolver
        |
        v
HarnessConfigurationResolutionResult
        ├── HarnessConfiguration
        │     ├── PiHarnessConfiguration
        │     ├── HumanReviewConfiguration
        │     └── HarnessPersistenceConfiguration
        ├── ordered ContentIdentity bindings
        └── SnapshotIdentity
```

Canonical JSON serialization of `HarnessConfigurationSource` is the authoring wire.
Canonical JSON serialization of resolved `HarnessConfiguration` may be added only as
an identified snapshot/projection contract; it is not an editable authority. This
corrects the earlier broad statement that one serializer/deserializer pair could own
both meanings.

## Deferred questions

After Option B selection, the remaining field-level proposal is:

- `HarnessConfigurationSource(schema_version, pi_settings_path, human_review,
  persistence)`;
- `HumanReviewConfiguration(packet_artifact_root,
  decision_projection_root_or_none)`;
- `HarnessPersistenceConfiguration(state_database_path)`;
- `HarnessConfiguration(schema_version, pi, human_review, persistence)`; and
- `HarnessConfigurationResolutionResult(status, configuration_or_none,
  source_content_identities, snapshot_identity_or_none, findings)`.

Retention policy, external absolute paths, YAML, alternate persistence backends, live
repository construction, and v1 compatibility aliases remain excluded from the first
slice. Exact error codes and canonical JSON member order should be fixed in the
implementation contract after this conceptual allocation is selected.

## Human decision required

Select one:

- `A — One editable HarnessConfiguration document that duplicates normalized Pi values`;
- `B — Separate harness-owned source document and resolved aggregate composed with Pi settings`;
- `C — Resolved snapshot only, retaining distributed code-owned configuration inputs`; or
- `D — Reconsider or defer`.

No source implementation, dependency, YAML support, commit, push, or protected action
is authorized by this decision document alone.
