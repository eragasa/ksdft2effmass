# Architecture-v2 HarnessConfiguration implementation proposal

## Purpose

This proposal defines the next bounded decision before source implementation of the
human-approved Architecture-v2 `HarnessConfiguration` direction. It does not activate
or implement that source contract. The reviewed architecture remains the candidate in
`docs/architecture/v2/ksdft2effmass/harness/configuration.md`.

## Current implementation boundary

The implemented package exposes `ksdft2effmass.harness.pi` and its narrow
`PiHarnessConfiguration`. There is currently no implemented
`ksdft2effmass.harness` package API, no Architecture-v2 `SnapshotIdentity` or
`ContentIdentity` implementation, no `HarnessConfiguration` JSON wire contract, and
no implemented `HarnessStateAtomicRepository`.

The accepted Architecture-v2 plan previously deferred Architecture-v2 source
implementation. The configuration review accepted only the prospective ownership and
dependency direction. It explicitly did not authorize Python source, schemas, fixtures,
dependencies, YAML, migration, commits, or activation.

## Material implementation choices

### Option A — Extend the implemented v1 Pi harness

Add `HarnessConfiguration` and related objects under
`ksdft2effmass.harness.pi`, using the existing `ArtifactIdentity` and current public
wire helpers.

**Advantage:** Smallest immediate code change and direct reuse of implemented
infrastructure.

**Risk:** Creates another transitional v1 public API whose ownership and identity types
do not match the selected Architecture-v2 package. A later migration would need to
preserve or explicitly break that additional contract.

### Option B — Introduce the first narrow Architecture-v2 package slice

Create the public `ksdft2effmass.harness` package with only the configuration
DataObjects, source-resolution result, validator, and canonical JSON serializer and
deserializer. Introduce only the identity primitives required by this slice or first
complete their owning Architecture-v2 identity contract.

**Advantage:** Implements the selected target ownership directly and avoids expanding
the transitional `harness.pi` API.

**Risk:** Establishes the first v2 source boundary before the broader HarnessState,
authority, persistence, and migration contracts are implemented. Incorrect identity or
package choices could constrain the rest of the v2 port.

### Option C — Defer configuration source until the HarnessState foundation exists

Implement Architecture-v2 identity primitives, `HarnessState`, and application
composition before adding configuration.

**Advantage:** Configuration fields can bind final identity and repository contracts
without temporary types.

**Risk:** Delays the configuration vertical slice and may let composition decisions
remain implicit while the larger foundation is built.

## Recommendation

**Option B is human-approved with a direct v1 cutover and no compatibility adapter.**

The implementation remains split by contract rather than by runtime coexistence:

1. First accept the exact minimal public field and identity contract for the
   configuration slice.
2. Then implement the Architecture-v2 source and replace current v1 configuration
   consumers in the same bounded change.

This keeps the implementation target-owned and prevents a transitional v1
`HarnessConfiguration`, shadow path, compatibility adapter, or alias. Existing
`PiHarnessConfiguration` remains only as the Pi-owned nested component. Git provides
the rollback boundary. Option C remains defensible but is not selected.

## Proposed first implementation slice

The first source slice should be limited to:

- `HarnessConfiguration`;
- `HumanReviewConfiguration`;
- `HarnessPersistenceConfiguration`;
- composition with the existing normalized `PiHarnessConfiguration` as the nested
  Pi-owned component;
- one exact configuration snapshot/source-identity contract;
- `HarnessConfigurationResolver`;
- `HarnessConfigurationValidator`;
- `HarnessConfigurationJsonSerializer`;
- `HarnessConfigurationJsonDeserializer`;
- canonical JSON runtime contract and focused representative examples;
- focused software-verification tests; and
- synchronized public API, concept, migration, and architecture documentation.

The slice should exclude YAML, new dependencies, live repository construction,
SQLite connections, filesystem discovery, environment lookup, authority grants,
credentials, human-response interpretation, automatic successor activation,
scientific behavior, and protected execution.

## Exact decisions still required before coding

The following decisions are implementation-blocking rather than ordinary coding
details:

1. **Source package:** whether the first v2 slice may create the public
   `ksdft2effmass.harness` package now.
2. **Identity contract:** whether configuration resolution uses the prospective
   `SnapshotIdentity` plus ordered `ContentIdentity` source bindings, or introduces a
   dedicated configuration-source record composed from those identities.
3. **Resolved-result contract:** the closed success/failure ResultObject returned by
   `HarnessConfigurationResolver`.
4. **Public fields:** exact fields and types of the three configuration DataObjects.
5. **Persistence path semantics:** repository-relative only in the first slice, or an
   explicit representation for separately authorized external locations.
6. **Human-review paths:** whether packet artifacts and decision projections are two
   distinct optional roots.
7. **Retention:** whether the first slice supports a closed retention vocabulary or
   defers retention entirely.
8. **Wire contract:** exact JSON member names, order, final LF, duplicate-key handling,
   unknown-member behavior, without requiring a separate JSON Schema artifact.
9. **Pi composition:** the exact boundary by which the resolver constructs and embeds
   the existing `PiHarnessConfiguration` value from explicit Pi settings bytes.
10. **Cutover inventory:** the complete set of current v1 constants, CLI inputs, and
    configuration consumers replaced by the new aggregate in the direct cutover.

## Proposed decisions

For the smallest coherent first slice, the recommendation is:

- create `ksdft2effmass.harness` as the Architecture-v2 public package and cut current
  v1 configuration consumers over in the same bounded change;
- use `SnapshotIdentity` for the complete resolved configuration and ordered
  `ContentIdentity` bindings for each source, without a new generic identity class;
- return a closed `HarnessConfigurationResolutionResult` with `resolved` and `failed`
  variants;
- restrict configured paths to normalized repository-relative paths;
- represent review packet and decision-projection roots as distinct optional fields;
- defer retention policy;
- use canonical JSON with strict duplicate, missing, unknown, type, version, and
  invariant rejection for the harness-owned wire;
- construct and embed the existing normalized `PiHarnessConfiguration` through the
  resolver from explicit Pi settings bytes; and
- remove superseded hard-coded or fragmented v1 configuration routes without a shadow
  adapter, compatibility alias, or dual authority.

## Verification proposal

Software verification should cover:

- exact semantic types and Boolean exclusion;
- frozen/slotted operational immutability;
- intrinsic and cross-object invariants under the owning DataObject or ActionObject;
- deterministic source ordering and snapshot identity;
- strict harness-owned JSON decoding, duplicate-key rejection, canonical encoding, and
  exact round trip;
- Pi open-format compatibility without duplicated Pi authority;
- root-relative path rejection partitions;
- absence of filesystem, environment, repository, database, network, clock, or
  subprocess effects;
- exact public imports and dependency direction; and
- compatibility with the unchanged v1 test suite.

Passing would establish only the documented software contract. It would not establish
successful repository construction, persistence, human authority, scientific validity,
or protected-execution authorization.

## Recommendation boundary

The human approved direct Architecture-v2 implementation followed by direct v1
configuration cutover, without an adapter. Exact public fields, identities, JSON wire
members, and the cutover inventory still require the bounded contract report before
coding. Dependency addition, YAML, commit, push, scientific work, and protected
execution remain separately unauthorized.
