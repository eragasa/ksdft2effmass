# Triage publication documentation

Status: completed; human dispositions recorded and hierarchy handoff accepted on 2026-08-09

Task identity: `harness.simplification.docs-json.publication.triage`

Parent task: `harness.simplification.docs-json.publication`

## Objective

Inventory `docs/conferences/` and `docs/papers/`, apply deterministic classifications where repository evidence permits only one reasonable result, and send only genuinely ambiguous files for human classification before hierarchy changes.

Additional roots require current human authorization. Bind the inventory to one Git revision or accepted worktree state. For tracked files, path and Git object identity are sufficient; hash only content not identified by Git. Record symlinks without following them outside the selected roots.

## Triage rule

Classify mechanically when explicit repository evidence unambiguously identifies generated output, editor or temporary material, direct project documentation, working source, a submission snapshot, an external reference, provenance, or a historical artifact. Filename resemblance or folder location alone is not enough for a material classification.

Return only ambiguous or materially consequential cases to the human. The human may accept the proposed set as a whole and decide the ambiguity queue; a separate response for every obvious file is not required. `unresolved` is a valid disposition when evidence remains insufficient.

## Output and completion

Produce one temporary triage record containing the bounded inventory, deterministic classifications with reasons, and the ambiguity queue. Completion requires complete selected-root path coverage, no duplicate paths, disposition of every ambiguity, and a compact input for `harness.simplification.docs-json.publication.hierarchy`.

The temporary record is `.pi/evidence/docs-json/publication-triage.json`. It covers 23 regular files at revision `107f6b1d39be1af460c03183e880d3063f1320a0`: 22 tracked files by Git object identity and one untracked `.DS_Store` by SHA-256. Twenty-one classifications are deterministic. The human PI disposed the remaining cases by authorizing deletion of `LA2.pdf` and assigning the empty `ksdft2effmass.paper.md` as the publication-root index at `docs/publications/ksdft2effmass.publications.00.md`. Independent review identified the empty file as a missing ambiguity before that human disposition. The accepted record is the compact input to `harness.simplification.docs-json.publication.hierarchy`.

This Task does not move, rename, delete, rewrite, publish, submit, or release files. Human authorization activates only this bounded inventory and triage.
