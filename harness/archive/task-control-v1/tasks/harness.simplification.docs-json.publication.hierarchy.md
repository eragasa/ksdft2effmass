# Normalize publication documentation hierarchy

Status: completed; exact human-selected hierarchy applied and independently reviewed on 2026-08-09

Task identity: `harness.simplification.docs-json.publication.hierarchy`

Parent task: `harness.simplification.docs-json.publication`

## Objective

Use the accepted triage from `harness.simplification.docs-json.publication.triage` to place publication working source, submission snapshots, generated output, external material, provenance, historical artifacts, and direct project documentation in a coherent hierarchy without changing their content or meaning.

## Method

1. Produce one complete old/new path map with link and generated-file impacts.
2. Apply the repository layout and accepted triage directly when they determine one compatible hierarchy.
3. Ask the human only if at least two materially different defensible hierarchies remain.
4. Under the active Task authority, execute the determined or human-selected path map once.
5. Update affected links, navigation, manifests, and checksums, then validate the result.

For unchanged moved files, Git identity or byte equality must be preserved. Submitted and historical provenance must remain distinguishable.

## Completion

Completion requires the applied path map, resolved links, correct generated/external/source treatment, preserved content identities, and a compact handoff to `harness.simplification.docs-json.authority-catalog`.

This Task does not alter scientific or publication claims, publish, submit, or release material. The human PI explicitly authorized deletion of only `docs/conferences/ICMSEP2026/LA2.pdf`, movement of the two publication trees under `docs/publications/`, and creation of `docs/publications/ksdft2effmass.publications.00.md` from the empty tracked conference file. No other deletion is authorized.

## Result and handoff

The complete 23-file map is `.pi/evidence/docs-json/publication-hierarchy-path-map.json`. It records 20 byte-preserving tracked moves, one byte-preserving ignored `.DS_Store` move, the exact authorized deletion, and the populated publication-root index. Six live navigation or path references were synchronized; historical evidence, resolved checkpoints, source triage identities, and replay validators retain their recorded paths.

Deterministic validation confirmed complete one-to-one source coverage, unique paths, all recorded Git object identities, the ignored-file SHA-256, removal of both old roots and only the authorized PDF, resolution of new index links, checkpoint validity, task-state validity, `git diff --check`, and a Sphinx warnings-as-errors build. Consolidated independent review returned no material findings. `harness.simplification.docs-json.authority-catalog` remains inactive and receives the path map as a compact input only.
