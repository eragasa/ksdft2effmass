# Per-file human mediation for Task-document migration

Decision identity: `harness.simplification.task-control.task-document-human-mediation`

Input revision: `c72ceb132dafd1fadcc217758092bbfb7f9f2555`

Related decision: `.pi/evidence/task-control/task-graph-selection-state-decision.md`

Decision status: resolved by current human authority

## Human direction

> this needs to be human-mediated for each file since it contains, project information that might be clobbered especially things like latex equations and mermaid document requirements

## Normalized decision

Every documentation file participating in Task JSON migration requires an individual human review and explicit disposition before its source bytes are replaced or JSON becomes authoritative for that file. Files may not be batch-approved merely because structural checks or another file's migration passes.

## Required per-file packet

Each file review must bind:

- exact source path, Git object identity when tracked, byte count, and SHA-256;
- candidate `HarnessTask` fields and canonical JSON;
- every source span mapped to a JSON field, retained documentation-owned narrative, historical evidence, or proposed removal;
- candidate maintained Markdown rendering;
- exact source/rendered diff and a list of unmapped spans;
- explicit handling of LaTeX, Mermaid, code fences, links, tables, directives, and other project-specific syntax; and
- one human disposition: accept this file, revise the mapping, retain documentation ownership, or defer.

## Preservation rule

LaTeX equations, Mermaid blocks, code fences, and other opaque project content are preserved byte-for-byte unless the human explicitly accepts a stated transformation for that exact file. Parsers and renderers must not normalize, reflow, reinterpret, or silently drop opaque blocks. Successful JSON round trips and rendering checks establish only software conformance; they do not provide the required human disposition.

## Migration flow

Files migrate serially. The migration prepares one immutable review packet, stops for the human disposition, records that decision against the exact packet, applies only the accepted file migration, verifies the resulting bytes and JSON round trip, and only then prepares the next file. Automatic continuation, batched acceptance, and inference from silence are prohibited.

## Boundaries

This decision does not activate a migration Task or authorize implementation, source replacement, documentation deletion, scientific interpretation, publication changes, dependency changes, protected execution, or automatic successor activation. It defines a required human-mediated safety boundary for a future explicitly authorized migration.
