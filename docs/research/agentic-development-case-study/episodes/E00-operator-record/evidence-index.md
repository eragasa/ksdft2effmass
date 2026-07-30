# E00 evidence index: operator-record refactor

Episode `E00` is retrospective and serves as a pilot. Evidence is reconstructed
from repository files after the operator-record task was accepted.

## Accepted task record

- `.pi/tasks/operator-record-refactor.md` records final human acceptance on
  2026-07-30, accepted scope, public API, validation evidence, consequences, and
  scientific limitations.

## Control-plane evidence

- `AGENTS.md` records the DataObject/ActionObject policy, operator-record
  control-plane policy, completion gates, human authority, and durable handoff
  expectations.
- `.pi/skills/develop-operator-records/` records focused operator-record skill
  policy.
- `.pi/skills/design-data-action-objects/` records DataObject/ActionObject
  policy.

## Public contract evidence

- `python/src/ksdft2effmass/operators/` contains the accepted public API and
  implementation.
- `specification/operator-record/v1/operator-record.schema.json` is the public
  schema-version-1 contract.
- `specification/operator-record/v1/valid/` and
  `specification/operator-record/v1/invalid/` contain conformance fixtures.

## Verification evidence

- `python/tests/ksdft2effmass/operators/` contains object-scoped tests.
- `docs/concepts/operator-records.rst` and `docs/api/operators.rst` document the
  accepted API and conventions.
- The accepted task record lists the validation commands and outcomes accepted by
  the human PI.

## Unavailable retrospective evidence

The repository record does not provide complete exact prompts, model versions,
token counts, wall-clock runtimes, or final commit identifiers for E00. These
fields are recorded as unknown rather than reconstructed from memory.
