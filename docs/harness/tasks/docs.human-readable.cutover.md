<!-- Generated from SQLite control state; do not edit. -->
# Verify and complete the human-readable documentation cutover

[Task index](index.md) · [Previous](./docs.human-readable.contract-and-inventory.md) · [Next](./docs.human-readable.generated-view-separation.md)

## Status

`inactive`: Planned seventh and final child; blocked on history separation, separate explicit activation required, and no automatic successor activation.

## Objective

Verify the complete documentation ownership and navigation cutover, correct one consolidated set of findings, and deliver the result through normal commit and push workflow.

## Parent and prerequisites

- Parent: `docs.human-readable`
- Depends on: `docs.human-readable.history-separation`

## Authority references

- docs/README.md
- docs/index.rst

## Authorized scope

- Run complete documentation inventory closure, link, orphan, naming, generated-path, Sphinx, harness, dependency-immutability, and clean-diff checks.
- Obtain one consolidated read-only review of human readability, editability, current-versus-history separation, scientific integrity, and generated-view isolation, followed by at most one bounded correction pass.
- Commit and push the validated documentation cutover so no completed page exists only in an isolated worktree.

## Completion criteria

- No generator or projection manifest targets docs/, every first-level section has an index, current pages use descriptive paths, links resolve, and Sphinx passes with warnings as errors.
- Harness validation and projection agreement pass where harness outputs changed, dependency and lock files are unchanged, and no scientific executable ran.
- The final commit is pushed to origin/dev, the delivery report identifies moved and removed paths and residual limitations, and the coordinating parent is ready for separate human acceptance.

## Exclusions

- Do not perform more than one correction pass, change scientific content or dependencies, execute protected work, publish a release, claim scientific validation, or activate another successor.
- Do not report isolated-worktree content as delivered before the corresponding commit is visible on origin/dev.

## Historical source

No archived source.
