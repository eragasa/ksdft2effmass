<!-- Generated from SQLite control state; do not edit. -->
# Create human-oriented documentation navigation

[Task index](index.md) · [Previous](./docs.human-readable.history-separation.md) · [Next](./evidence-branch-orchestration-profile.md)

## Status

`inactive`: Planned third child; blocked on generated-view separation, separate explicit activation required, and no automatic successor activation.

## Objective

Provide one obvious documentation landing page and index-driven navigation for every first-level maintained section.

## Parent and prerequisites

- Parent: `docs.human-readable`
- Depends on: `docs.human-readable.generated-view-separation`

## Authority references

- docs/conf.py
- docs/index.rst

## Authorized scope

- Create or revise the root landing page around human tasks: start here, architecture, user guide, concepts, computational work, research, API reference, verification, development, publications, and history.
- Add an index.md or index.rst to every first-level maintained documentation section and make explicit navigation the primary discovery mechanism.
- Simplify Sphinx collection and hidden navigation without broadening publication scope for restricted or intentionally uncollected records.

## Completion criteria

- A reader can reach every current first-level documentation section from the root page without knowing repository-specific numeric filenames.
- Every first-level maintained section has an index, no current page relies solely on hidden toctree discovery, and all maintained links resolve.
- Sphinx passes with warnings as errors and no harness synchronization is needed for the navigation-only result.

## Exclusions

- Do not perform bulk filename normalization, rewrite scientific or publication content, expose private material, or activate a successor automatically.
- Do not retain duplicate root pages with conflicting navigation authority.

## Historical source

No archived source.
