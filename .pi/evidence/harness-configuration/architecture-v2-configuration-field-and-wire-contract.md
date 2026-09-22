# HarnessConfiguration field and JSON wire contract

## Decision status

The human authorized Option B: one harness-owned source document is resolved with
independently authoritative Pi settings into one immutable `HarnessConfiguration`.
Direct Architecture-v2 implementation and direct v1 configuration cutover are the
selected migration direction. This report proposes the exact first-slice fields and
canonical JSON wire required before coding.

## Recommendation

Accept the field contract below for the first implementation slice. It centralizes
values that current v1 composition already treats as selectable while leaving actual
algorithmic and authority policy fixed in their owning contracts.

The source document should be:

`harness/configuration.json`

It is the sole human-authored source for harness-owned configuration. It references
`.pi/settings.json`; it does not duplicate Pi-owned values.

## Public DataObjects

### `HumanReviewConfiguration`

| Field | Type | Contract |
|---|---|---|
| `packet_artifact_root` | `ResourcePath` | Normalized root-relative directory for transient review packets |
| `decision_projection_root` | `ResourcePath | None` | Optional root-relative directory for non-authoritative human-readable decision projections |

The two non-null paths must differ. Neither location stores authoritative
`DevelopmentDecision` state.

### `HarnessPersistenceConfiguration`

| Field | Type | Contract |
|---|---|---|
| `state_database_path` | `ResourcePath` | Root-relative development Harness-state SQLite path |
| `sql_export_path` | `ResourcePath` | Root-relative deterministic recovery SQL projection |
| `projection_manifest_path` | `ResourcePath` | Root-relative projection-manifest path |

The three paths must be distinct. They configure paths only and contain no connection,
repository, lock, timeout, credential, or backend plugin.

### `PythonConformanceConfiguration`

| Field | Type | Contract |
|---|---|---|
| `pyproject_path` | `ResourcePath` | Root-relative Python project configuration |
| `test_root` | `ResourcePath` | Root-relative maintained Python test root |
| `profile_matrix_path` | `ResourcePath` | Root-relative evidence-profile matrix |
| `migration_map_path` | `ResourcePath` | Root-relative predecessor migration map |

Paths are explicit and distinct. Test-module enumeration remains a deterministic action
over `test_root`; individual test modules are not configuration entries.

### `HarnessResourceConfiguration`

| Field | Type | Contract |
|---|---|---|
| `project_profile_path` | `ResourcePath` | Project-local resource profile |
| `generic_manifest_path` | `ResourcePath` | Generic resource manifest |
| `generic_root` | `ResourcePath` | Generic resource root |
| `local_manifest_path` | `ResourcePath` | Project-local resource manifest |
| `local_root` | `ResourcePath` | Project-local resource root |

Each manifest must be lexically beneath its corresponding configured root when the
configuration is resolved. Filesystem existence remains a resolver observation, not an
intrinsic DataObject invariant.

### `HarnessCatalogConfiguration`

| Field | Type | Contract |
|---|---|---|
| `task_root` | `ResourcePath` | Root containing canonical Task records |
| `agent_roots` | `tuple[ResourcePath, ...]` | Strictly sorted unique nonempty roots for agent descriptors |
| `checkpoint_roots` | `tuple[ResourcePath, ...]` | Strictly sorted unique nonempty roots for checkpoint records |
| `skill_roots` | `tuple[ResourcePath, ...]` | Strictly sorted unique nonempty roots for skill resources |

Roots may not repeat across categories. Catalog discovery remains a deterministic
resolver operation and grants no Task or agent authority.

### `HarnessConfigurationSource`

| Field | Type | Contract |
|---|---|---|
| `schema_version` | `int` excluding Boolean | Exactly `1` |
| `pi_settings_path` | `ResourcePath` | Root-relative Pi-owned project-settings source |
| `human_review` | `HumanReviewConfiguration` | Harness review-artifact configuration |
| `persistence` | `HarnessPersistenceConfiguration` | Development state/projection locations |
| `python_conformance` | `PythonConformanceConfiguration` | Python evidence source selection |
| `resources` | `HarnessResourceConfiguration` | Generic and project-local resource selection |
| `catalogs` | `HarnessCatalogConfiguration` | Task, agent, checkpoint, and skill roots |

This is the human-authored canonical JSON object.

### `HarnessConfiguration`

| Field | Type | Contract |
|---|---|---|
| `schema_version` | `int` excluding Boolean | Exactly `1` |
| `pi` | `PiHarnessConfiguration` | Normalized Pi-owned subset resolved from the referenced Pi settings bytes |
| `human_review` | `HumanReviewConfiguration` | Exact source value |
| `persistence` | `HarnessPersistenceConfiguration` | Exact source value |
| `python_conformance` | `PythonConformanceConfiguration` | Exact source value |
| `resources` | `HarnessResourceConfiguration` | Exact source value |
| `catalogs` | `HarnessCatalogConfiguration` | Exact source value |

This is the resolved immutable effective value. Source and snapshot identities belong
to the resolution ResultObject, not to configuration value equality.

### Resolution records

`HarnessConfigurationSourceBinding` contains:

- `role`: exactly `harness_configuration_source` or `pi_project_settings`;
- `path`: exact root-relative source path; and
- `content_identity`: exact SHA-256 `ContentIdentity` of the observed bytes.

`HarnessConfigurationResolutionFinding` contains a stable code, optional affected
source path, and sanitized message.

`HarnessConfigurationResolutionResult` contains:

- `schema_version`, exactly `1`;
- `status`, exactly `resolved` or `failed`;
- ordered source bindings, exactly source then Pi settings;
- `snapshot_identity`, present only for `resolved`;
- `configuration`, present only for `resolved`; and
- ordered findings, empty for `resolved` and nonempty for `failed`.

The snapshot identity is SHA-256 over the canonical resolved-configuration JSON bytes
plus the ordered source-binding canonical bytes under a versioned framing contract.
The exact framing must be fixed in the implementation before any digest fixture is
accepted.

## ActionObjects

| ActionObject | Responsibility |
|---|---|
| `HarnessConfigurationSourceJsonSerializer` | Emit canonical source JSON bytes |
| `HarnessConfigurationSourceJsonDeserializer` | Strictly decode explicit source JSON bytes |
| `HarnessConfigurationResolver` | Observe explicitly supplied source and Pi bytes once, validate bindings, and return the closed resolution result |
| `HarnessConfigurationValidator` | Validate cross-component compatibility without filesystem or runtime-service effects |
| `HarnessConfigurationJsonSerializer` | Emit canonical resolved snapshot JSON bytes |
| `HarnessConfigurationJsonDeserializer` | Strictly decode a resolved snapshot for represented replay/inspection only |

Deserializing a resolved snapshot does not establish current source agreement. Only a
successful fresh resolver result supplies a configuration to application composition.

## Canonical source JSON

Recommended initial document:

```json
{
  "schema_version": 1,
  "pi_settings_path": ".pi/settings.json",
  "human_review": {
    "packet_artifact_root": ".pi/reviews/packets",
    "decision_projection_root": ".pi/reviews/decisions"
  },
  "persistence": {
    "state_database_path": "harness/state/harness-control.sqlite3",
    "sql_export_path": "harness/state/harness-control.sql",
    "projection_manifest_path": "harness/state/projection-manifest.json"
  },
  "python_conformance": {
    "pyproject_path": "python/pyproject.toml",
    "test_root": "python/tests",
    "profile_matrix_path": "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json",
    "migration_map_path": ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
  },
  "resources": {
    "project_profile_path": "harness/local/profiles/ksdft2effmass-v2.json",
    "generic_manifest_path": "harness/pi/resource-manifest.json",
    "generic_root": "harness/pi",
    "local_manifest_path": "harness/local/resource-manifest.json",
    "local_root": "harness/local"
  },
  "catalogs": {
    "task_root": "harness/tasks",
    "agent_roots": [
      ".pi/agents"
    ],
    "checkpoint_roots": [
      ".pi/checkpoints"
    ],
    "skill_roots": [
      ".agents/skills",
      ".pi/skills"
    ]
  }
}
```

Canonical JSON rules are:

- UTF-8 without BOM;
- exact member vocabulary and member order shown above;
- two-space indentation;
- literal Unicode;
- arrays for tuples;
- `null` only for optional absence;
- exactly one final LF;
- duplicate, missing, unknown, wrong-type, unsupported-version, and invariant-violating
  values rejected;
- no comments, trailing commas, NaN, or infinity; and
- Pi project-settings bytes remain governed by the open consumed-subset behavior of
  `PiHarnessConfigurationDeserializer`, not by these strict aggregate rules.

## Direct v1 cutover

The same implementation change should:

1. add the canonical source document;
2. resolve it before current control generation;
3. replace private canonical path constants in
   `harness/pi/local/control/inputs.py` with resolved configuration values;
4. replace `_HarnessProjectionRequest.database_path`'s hard-coded default with the
   resolved persistence value at canonical call sites;
5. simplify `harness_projection.py sync` so canonical repository operation uses the
   source document rather than repeated resource/evidence path flags;
6. retain explicit low-level request construction for isolated tests only when it is
   not a second maintained canonical route;
7. update source-aware verification to resolve the same exact configuration;
8. update tests, focused representative JSON examples, API documentation,
   architecture documentation, and maintained projections; and
9. remove superseded canonical CLI flags or constants rather than preserving aliases.

The `check` command remains read-only and resolves the same configured sources. There
is no adapter, shadow mode, dual configuration authority, or automatic fallback.

## Exclusions

The first slice excludes:

- a separate JSON Schema artifact without a demonstrated external consumer;
- YAML and parser dependencies;
- external absolute paths;
- alternate persistence backends;
- retention policy;
- live repository or SQLite connection construction;
- credentials and environment interpolation;
- automatic source discovery outside configured roots;
- Task or successor activation;
- scientific or protected execution;
- publication and release; and
- commit or push unless separately authorized.

## Recommendation and unresolved issues

**Recommendation: accept this exact first-slice field and canonical JSON contract.**

Remaining implementation details that do not require a new public choice are stable
error-code spelling, private helper decomposition, and internal digest framing, provided
they are documented and independently tested before acceptance.

A bounded correction is required if any configured section, path, optionality rule,
canonical JSON rule, direct-cutover target, or exclusion above is not acceptable. No
source implementation begins until the human accepts or corrects this report.
