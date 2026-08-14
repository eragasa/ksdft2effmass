# V2-ISSUE-014: Required-failure policy wording

**Severity:** Deterministic documentation correction

**Scope:** Scientific-workflow failure semantics prose

## Conflict

`workflow/scientific/index.md` uses the dense compound `stop-on-first-required-failure` while the same section uses the open term “required failure.” The intended prose policy should not appear to introduce a separate undeclared identifier.

## Required correction

Replace the dense compound with direct prose: “stopping after the first required failure.” Retain “required failure” as the represented concept.

## Acceptance condition

The scientific-workflow failure policy uses one consistent term without implying an undefined public policy identifier.
