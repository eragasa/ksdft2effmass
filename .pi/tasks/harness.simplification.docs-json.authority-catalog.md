# Build a temporary documentation/control comparison baseline

Status: active; authorized by the human PI on 2026-08-09; no successor activates automatically

Task identity: `harness.simplification.docs-json.authority-catalog`

Parent task: `harness.simplification.docs-json`

## Objective

After publication hierarchy normalization, compare human-readable material under `docs/` with the selected JSON control surface and explicitly selected transitional control records. Apply repository precedence to identify deterministic documentation corrections and isolate only genuinely unresolved authority questions.

The catalog set is a temporary migration aid, not authority, a runtime registry, or permanent architecture.

## Bounded catalog set

Create only:

```text
docs-initial.json
control-initial.json
authority-mappings.json
docs-residual.json
control-residual.json
catalog-manifest.json
```

The initial catalogs are immutable inventories from one exact Git revision and explicitly selected roots. The residual catalogs are derived; they never replace the initial snapshots. The manifest records the revision, roots, inclusion rules, tool identity, counts, and file identities needed to reproduce the set.

Extraction metadata, predecessor relationships, and authority context belong directly on the relevant entry or mapping. Do not create separate extraction, crosswalk, or context registries.

## Inventory and extraction

For each included path, retain path, Git mode, file kind, Git object identity or SHA-256 when Git does not identify the content, declared identifiers, explicit local references, and parse status. Supported structured or textual extraction may add an exact selector or span and rule identity. Unsupported or failed extraction remains visible and never means “no claim.”

Reference source rather than copying it. Store path, selector or span, digest, and classification by default; include only the shortest excerpt needed to make a mapping intelligible.

Preserve relevant links to the accepted predecessor `harness-component-inventory` using semantic relationships such as `same_component`, `successor_of`, `split_from`, `merged_from`, `not_present_in_predecessor`, or `outside_predecessor_scope`. Opaque historical IDs appear only as provenance. Cite higher-authority context directly on a mapping when needed; context files are not subtraction candidates.

## Mapping and correction rule

A mapping records one represented subject and keeps these dimensions separate:

```text
relationship
lifecycle on each side
consistency
authority effect
review status
coverage: partial | whole_file
```

Use explicit identifiers, links, exact content identity, and bounded textual signals to propose mappings. Similarity alone cannot establish a relationship.

Apply repository precedence immediately:

- if one accepted contract determines the correction, mark it `deterministic_correction`;
- if both representations agree or are intentionally historical, record that without human review;
- ask the human only when current applicable claims conflict, precedence does not resolve them, and at least two materially different defensible choices remain.

Documentation may own subject-matter explanation, but it never independently activates a Task, supplies executable scope, selects a successor, or establishes completion or acceptance.

## Residual derivation

Remove a path from a residual catalog only for a reviewed `whole_file` mapping. A partially mapped file remains in the residual catalog with mapped selectors retained in `authority-mappings.json`.

```text
initial paths = fully mapped paths ∪ residual paths
fully mapped paths ∩ residual paths = empty
partially mapped paths ⊆ residual paths
```

## Five-step workflow

1. Select the exact revision, roots, inclusion rules, and temporary location.
2. Inventory and extract both sides into immutable initial catalogs.
3. Review mappings, apply deterministic precedence, and resolve only the ambiguity queue with the human.
4. Derive residual catalogs and report deterministic corrections plus unresolved cases.
5. Delete the catalog set when the parent migration is accepted, retaining only a compact revision/count/checksum summary when useful.

If repository changes invalidate the set, discard it and regenerate it; do not add refresh or supersession machinery. Runtime behavior must never depend on it.

## Completion

Completion requires complete path coverage for the declared roots and revision, valid JSON, reproducible identities and counts, explicit treatment of parse failures, a verified whole-file/residual partition, and bounded semantic claims.

The baseline may claim complete path coverage only for its declared inputs. It must not claim complete semantic extraction or repository-wide authority analysis. It does not modify represented files, resolve scientific meaning, or introduce SQLite.
