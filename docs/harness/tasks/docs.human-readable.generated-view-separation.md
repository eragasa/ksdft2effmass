<!-- Generated from SQLite control state; do not edit. -->
# Move generated harness views outside docs

[Task index](index.md) · [Previous](./docs.human-readable.cutover.md) · [Next](./docs.human-readable.history-separation.md)

## Status

`inactive`: Planned second child; blocked on the accepted contract and inventory, separate explicit activation required, and no automatic successor activation.

## Objective

Ensure no harness generator writes beneath docs/ by relocating or retiring generated Task Markdown views and updating deterministic projection contracts.

## Parent and prerequisites

- Parent: `docs.human-readable`
- Depends on: `docs.human-readable.contract-and-inventory`

## Authority references

- docs/conf.py
- harness/state/projection-manifest.json

## Authorized scope

- Change the harness projector, manifest, tests, and links so generated Task Markdown is emitted under harness/generated/task-markdown/ or retired when authoritative Task JSON and bounded inspection fully replace it.
- Remove generated docs/harness/tasks/ pages only after every maintained inbound reference has an explicit replacement.
- Synchronize and verify generated control state after the relocation and document the generated directory as non-authoritative inspection output.

## Completion criteria

- No projection-manifest entry or generator destination targets docs/, and no generated Task Markdown remains under docs/harness/tasks/.
- Task JSON remains authoritative, all retained links resolve, projector and verifier tests pass, and synchronized SQLite, SQL, graph, manifest, and generated views agree.
- Sphinx passes with warnings as errors and ordinary docs-only edits no longer require control synchronization.

## Exclusions

- Do not redesign Task semantics, selection state, SQLite authority, scientific workflows, or unrelated harness resources.
- Do not delete generated views until replacement links and inspection access are verified; do not activate a successor automatically.

## Historical source

No archived source.
