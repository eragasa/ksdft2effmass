# Executable harness-tool placement contract

Status: completed under `.pi/chains/harness-simplification.chain.json`

Task identity: `harness-simplification.agents.executable-tool-placement-contract`

Authority: the current human instruction authorizes this bounded public-contract task without an additional checkpoint. The architecture analysis classified the placement as deterministic because the instruction fixes the material choices; no three-option decision or human checkpoint is applicable.

## Outcome

Accept the executable-tool and proportional-execution contract in `docs/harness/ksdft2effmass.harness.010.030.030.md`. Reusable executable Python belongs to `python/src/ksdft2effmass/harness/pi/`; repository-specific executable composition belongs to its `local/` subtree and may depend on the generic package, never conversely. Generic and local declarative resources remain under `harness/pi/` and `harness/local/`. Compatibility scripts may remain only as thin command wrappers.

The contract uses immutable concrete DataObjects, stateless concrete ActionObjects with a public `execute` boundary, and immutable ResultObjects as semantic DataObject specializations. It introduces no nominal base class, production implementation, dependency, persistence layer, or validator migration.

The exact bounded durable paths for this root-agent task are:

- `.pi/agents/ksdft2effmass-tests.md`;
- `.pi/skills/skill-capability-inventory.json`, limited to the two affected consumer entries;
- this task record;
- `.pi/chains/harness-simplification.chain.json`;
- `docs/harness/ksdft2effmass.harness.010.030.000.md`;
- `docs/harness/ksdft2effmass.harness.010.030.010.md`; and
- `docs/harness/ksdft2effmass.harness.010.030.030.md`.

One read-only `ksdft2effmass-harness-architecture` assignment supplied the deterministic analysis. The root agent owns integration. One read-only `ksdft2effmass-harness-integration-reviewer` assignment supplies the bounded final cross-surface review. No ownership manifest is required because there is one writer, no concurrent writer, no protected source, and the exact paths are stated here.

## Routing correction

The durable project test agent routes permanently only to `develop-python-test-evidence`. `design-data-action-objects` and `develop-operator-records` are subject-specific skills selected by an active task when required. Only the corresponding agent front matter and capability-inventory consumer entries change.

## Successor boundary

The next task is `harness-simplification.agents.validator-migration-pilot`. Its candidate is `harness/pi/validation/validate_python_test_evidence.py`, but it remains inactive. The pilot is limited to an immutable public request DataObject, stateless public validation ActionObject, immutable validation ResultObject, structured deterministic issues, class-owned and artifact-owned software-verification tests, a temporary thin old-script wrapper, and old-command/new-API agreement. It must not prescribe exact module decomposition before inspecting cohesion and must not expand schemas, fixtures, science, or SQLite.

Completion leaves `active_task` null, automatic successor activation disabled, all later stages inactive, and completed history intact.
