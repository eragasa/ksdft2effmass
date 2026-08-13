<!-- Generated from SQLite control state; do not edit. -->
# Define the documentation contract and classify the current tree

[Task index](index.md) · [Previous](./docs.human-readable.computational-names.md) · [Next](./docs.human-readable.cutover.md)

## Status

`inactive`: Planned first child; separate explicit activation required and no automatic successor activation.

## Objective

Define docs/ as human-authored source and produce a complete bounded disposition inventory before moving or deleting documentation.

## Parent and prerequisites

- Parent: `docs.human-readable`

## Authority references

- AGENTS.md
- docs/conf.py
- docs/index.rst

## Authorized scope

- Create docs/README.md as the concise docs/ authoring contract covering source ownership, prohibited generated content, index and filename conventions, Markdown versus reStructuredText use, validation commands, review, commit, and push expectations.
- Inventory every tracked docs/ file and assign exactly one retain, rename, move, merge, historical, generated, or delete disposition with a proposed destination and reason.
- Update repository documentation policy only as needed to make ordinary prose edits independent of harness-state synchronization.

## Completion criteria

- docs/README.md exists and unambiguously states that maintained docs/ files are human-authored and that generated artifacts are prohibited there.
- The inventory covers every tracked docs/ file, identifies generated Task Markdown and opaque version-numbered families, and has no unresolved disposition.
- Documentation links and the warnings-as-errors Sphinx build pass; no file is moved or deleted in this Task.

## Exclusions

- Do not modify harness projection behavior, move or delete documentation, change scientific content, add dependencies, or activate a successor.
- Do not infer that generated, historical, or opaque naming alone makes content deletable.

## Historical source

No archived source.
