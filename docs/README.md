# Documentation authoring contract

`docs/` contains maintained, human-authored documentation source. Authors edit
these files directly and review the resulting prose and navigation. Generated
pages, build output, caches, temporary editor files, and compiled publication
artifacts do not belong under `docs/`; keep reproducible inspection output under
its owning non-`docs/` generated-artifact location. In particular, Task JSON
under `harness/tasks/` is authoritative and generated Task Markdown must not be
maintained as documentation source.

## Ownership and authority

Follow [`AGENTS.md`](../AGENTS.md) and any applicable scoped instructions. Keep
content in its owning surface:

- physical and mathematical definitions: `specification/`;
- scientific assumptions: `docs/research/`;
- computational workflow dependencies: `docs/computational/`;
- Python dependency declarations and resolutions: `python/pyproject.toml` and
  `python/uv.lock`; and
- public Python behavior: implementation, schemas, fixtures, tests, and the
  corresponding API or concept pages, consistently.

Documentation edits do not authorize changes to scientific meaning, public
contracts, source code, tests, dependencies, control state, or release status.
State whether material is implemented, proposed, illustrative, software
verified, numerically verified, scientifically validated, or uncertainty
quantified; do not strengthen a claim based only on a build or test result.

## Files and navigation

Use one `index.md` or `index.rst` at each maintained section root. An index
orients readers and links to descriptive topic pages; directory listing and
opaque numeric filenames are not navigation. New prose filenames use lowercase
kebab-case and describe the subject, such as `energy-reference.md`. Preserve a
legacy path until an authorized migration updates all inbound links and history.

Use Markdown (`.md`) for repository-first narrative documentation and
reStructuredText (`.rst`) for Sphinx-first API pages, autodoc integration, and
pages that need reStructuredText or Sphinx roles. Use the established syntax of
the selected format rather than maintaining duplicate Markdown and
reStructuredText copies. `docs/index.rst` is currently the Sphinx root.

The bounded disposition inventory for the tree at activation revision
`fa31577ccceb066a66599618cd4ef3ff054a83ba` is
[`harness/reports/docs-human-readable-inventory.json`](../harness/reports/docs-human-readable-inventory.json).
It is a migration report, not a generator or a second documentation authority.

## Validation and delivery

From the repository root, run the affected checks first and then the applicable
documentation gates:

```sh
uv run --project python sphinx-build -W --keep-going -b html docs /tmp/ksdft2effmass-docs-html
uv run --project python sphinx-build -W --keep-going -b linkcheck docs /tmp/ksdft2effmass-docs-linkcheck
git diff --check
```

Remove or place build output outside the repository; never retain it under
`docs/`. Check local links as part of Sphinx validation and verify external links
when network access permits. If a gate already fails at the unchanged base,
record the baseline command and failure separately and show that the edit adds
no new failure.

Ordinary prose edits do not require harness synchronization. Run the sole
control synchronization command and source-aware control validation only when an
authorized change touches canonical control inputs or explicitly requires a
projection update.

Review the complete diff for technical accuracy, claim status, format, links,
navigation, and unintended generated files. Commit only validated, in-scope
changes in a focused commit when the active task requests or permits a commit.
Do not stage unrelated work. Push only with explicit authorization, and never
push directly to `main` or perform release actions without their required human
authority and checkpoint.
