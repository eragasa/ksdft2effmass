# Pi project settings consumed by harness control

## Scope

`.pi/settings.json` is the repository's project-local Pi configuration. Pi owns its complete settings contract and runtime discovery behavior. The v1 project-local Harness control generator consumes only the subset documented here to derive its repository role projection.

The public `PiHarnessConfiguration` DataObject is the normalized software contract for the consumed subset, and `PiHarnessConfigurationDeserializer` owns conversion from caller-supplied JSON bytes. Public `PiHarnessAgentDefinitionResolver` composes exact descriptor bytes with that configuration into immutable `PiHarnessAgentDefinition` before database ingestion. This page is explanatory documentation, not a second configuration file, schema, resource manifest, executable-agent registry, or source of Task authority.

## Consumed structure

The control generator accepts this shape:

```json
{
  "subagents": {
    "agentOverrides": {
      "package.name": {
        "disabled": true
      }
    }
  }
}
```

The override key is the exact Pi runtime name formed from descriptor frontmatter:

```text
<package>.<name>
```

Matching is exact and performs no prefix stripping, case normalization, or fallback lookup.

## Projection behavior

For each present `.pi/agents/*.md` descriptor:

- an exact override with `"disabled": true` produces `enabled = 0` in the generated v1 `agent_definition` row;
- `"disabled": false` or no matching override produces `enabled = 1`;
- an override for an absent historical descriptor creates no row; and
- unrelated override fields do not become Harness capabilities or authority.

The maintained source-aware verifier requires `.pi/settings.json` as a regular canonical input. Bounded noncanonical `HarnessControlMigrator` requests may omit the file, in which case agent ingestion applies no overrides.

The selected settings document, `subagents`, and `agentOverrides` values must be JSON objects when present. Override names must be nonempty strings, each override must be an object, and `disabled` must be a JSON boolean when present. Invalid consumed structure rejects candidate generation before maintained control publication.

## Authority and runtime boundary

The generated `agent_definition` and `agent_skill_route` tables are repository projections. They do not launch, enable, authorize, or observe a Pi child. Pi independently applies its runtime configuration, scope precedence, descriptor discovery, and executable-agent resolution.

A projected enabled role provides no Task selection, path ownership, protected-action permission, operation authority, acceptance, or evidence that the role is executable in the current Pi process. Runtime reconciliation remains a separate v1-to-v2 migration increment.

## Current provenance limitation

V1 source selection reads the canonical settings bytes and deserializes them before database ingestion, but `agent_definition` does not retain the settings content identity responsible for `enabled`. The prospective migration keeps repository role identity, descriptor content identity, settings identity, and Pi runtime identity distinct and moves source observation toward one closed compiler snapshot. This page does not claim that those v2 identity and snapshot contracts are implemented.

## Implementation and verification

The public configuration and projection-ready agent-definition contracts are owned by `python/src/ksdft2effmass/harness/pi/configuration.py`. Project-local source selection resolves those values before project-local database ingestion, which only inserts the normalized definitions.

Maintained software-verification evidence is under:

- `python/tests/software_verification/ksdft2effmass/harness/pi/test__PiHarnessConfiguration.py`;
- `python/tests/software_verification/ksdft2effmass/harness/pi/test__PiHarnessConfigurationDeserializer.py`;
- `python/tests/software_verification/ksdft2effmass/harness/pi/local/dbcontrol/test__HarnessControlMigrator.py`; and
- `python/tests/software_verification/ksdft2effmass/harness/pi/local/dbcontrol/test__HarnessControlVerifier.py`.

Passing structural checks establishes only the documented repository-projection behavior. It does not establish Pi runtime availability, Task authority, scientific validation, uncertainty quantification, or human acceptance.
