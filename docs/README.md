# Documentation authoring contract

`docs/` contains maintained repository-first research, proof, publication,
architecture, computational, historical, and meeting documentation. The
software-facing Sphinx source is isolated under `doc/sphinx/`. Authors edit
these files directly and review the resulting prose and navigation. Generated
pages, build output, caches, temporary editor files, and compiled publication
artifacts do not belong under either documentation root; keep reproducible
inspection output under its owning generated-artifact location. The retired `tasks/`
and `harness/` trees must not be recreated as documentation or planning control.
Historical human-decision records still bound to retained calculation provenance live
under `.pi/checkpoints/` as an immutable archive, not active task state. Any future
generated inspection view must remain outside `docs/` and explicitly
non-authoritative.

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

Use Markdown (`.md`) for repository-first narrative documentation under
`docs/`. Use reStructuredText (`.rst`), or MyST Markdown where already required,
for Sphinx sources under `doc/sphinx/`. Use the established syntax of the
selected format rather than maintaining duplicate Markdown and reStructuredText
copies. `doc/sphinx/index.rst` is the Sphinx root.

## Validation and delivery

From the repository root, run the affected checks first and then the applicable
documentation gates:

```sh
uv run --project python sphinx-build -W --keep-going -b html doc/sphinx /tmp/ksdft2effmass-docs-html
uv run --project python sphinx-build -W --keep-going -b linkcheck doc/sphinx /tmp/ksdft2effmass-docs-linkcheck
git diff --check
```

Remove or place build output outside the repository; never retain it under
`docs/`. Check local links as part of Sphinx validation and verify external links
when network access permits. If a gate already fails at the unchanged base,
record the baseline command and failure separately and show that the edit adds
no new failure.

Ordinary prose edits require only the applicable documentation and link checks.

Review the complete diff for technical accuracy, claim status, format, links,
navigation, and unintended generated files. Commit only validated, in-scope changes
when the current human instruction requests a commit. Do not stage unrelated work.
Push only with explicit authorization, and never push directly to `main` or perform
release actions without explicit human authority.
