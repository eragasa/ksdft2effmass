---
document_id: ksdft2effmass.harness.001.006.000
task_id: harness-current.status
parent: ksdft2effmass.harness.001.000.000
status: current
sphinx: included
---

# Current status and limitations

The generic Python layer, project-local composition, resource trees, local
validation route, schemas, fixtures, skills, agent records, and deterministic
validation scripts are implemented. The current route selects the local
validation path, retains a legacy rollback value, and passes after deterministic
repair of the current-local replay resource identity.

Five durable harness roles are implemented and available for explicit
assignment. They do not activate themselves or grant ownership. The 24
historical phase-specific harness records remain present, and no phase-specific
role is currently active.

## Current strengths

- Generic and project-local dependencies are explicit and tested.
- Public records are immutable and wire contracts are strict.
- Validators use structured deterministic findings.
- Profiles and resource manifests make local policy explicit.
- Route selection, rollback values, and shadow observations have named owners.
- Writer/reviewer ownership can be validated before governed work begins.
- Test evidence distinguishes structural checks from semantic and VVUQ claims.

## Current limitations

Operational information is spread across Markdown and JSON tasks, chains,
checkpoints, ownership manifests, evidence directories, profiles, resource
manifests, route configuration, agent files, and specialized completion records.
Several relations must therefore be synchronized manually.

Validation is also distributed across generic actions, generic scripts, local
replay, live project skills, task-specific validators, and ordinary Python test
commands. Focused checks and full reconciliation exist as practice rather than as
one maintained execution interface.

Additional duplication includes:

- canonical, local, and live skill/resource identities;
- 24 historical task-phase agent definitions retained alongside durable roles;
- repeated parsing and normalization of related operational records;
- repeated command assembly and result interpretation;
- retained legacy and current route machinery.

The current `evidence.py` owns evidence-identifier auditing only. It does not own
an evidence-record repository, event log, query interface, reconciliation index,
or SQLite state. Project-agent simplification and historical-agent retirement
also remain future work.

## Execution environment

Repository Python commands use the project environment rooted at
`python/.venv`. Direct maintained execution from the repository root uses
`python/.venv/bin/python`. The equivalent uv form first changes to `python/` and
then runs `uv run python`. Neither form depends on shell activation. If another
environment is active, leave it or unset `VIRTUAL_ENV` before invoking uv;
mixing the repository-root `.venv` with `python/.venv` produces misleading
warnings and inconsistent tool availability.

## Non-capabilities

The harness does not execute scientific calculations, replace the project CPN,
submit external jobs, publish packages, establish release readiness, or provide
scientific validation or UQ. A future operational-state redesign would require a
separate accepted architecture and implementation task.

## Navigation

- **Index:** <a href="ksdft2effmass.harness.000.000.000.md">Harness documentation</a>
- **Parent:** [Current harness architecture](ksdft2effmass.harness.001.000.000.md)
- **Previous:** <a href="ksdft2effmass.harness.001.005.000.md">Agent and ownership inventory</a>
- **Next:** <a href="ksdft2effmass.harness.002.000.000.md">Harness simplification plan</a>
