# Research analysis projection

This directory owns the repository-local, rebuildable SQLite projection used to browse
retained research-monograph calculations. The projection indexes files under
`calculations/research-monograph/`; it does not execute calculations, verifiers,
plotting scripts, Quantum ESPRESSO, or Wannier90.

The retained files and their SHA-256 manifests remain authoritative. The database is a
derived navigation and analysis projection only. A projected checksum match establishes
byte identity with a listed manifest entry, not scientific validity, convergence,
uncertainty quantification, publication status, or human acceptance.

## Rebuild

From the repository root:

```bash
uv run --project python python -m \
  ksdft2effmass.campaigns.research_monograph.results_projection
```

The default output is ignored local state:

```text
ui/analysis/build/results.sqlite
```

The builder writes a complete temporary database in the destination directory, checks
SQLite integrity, foreign keys, and path safety, then atomically replaces the output.
It never mutates retained calculation files.

An alternative repository or output may be supplied explicitly:

```bash
uv run --project python python -m \
  ksdft2effmass.campaigns.research_monograph.results_projection \
  --repository /path/to/ksdft2effmass \
  --output /private/path/results.sqlite
```

## Path contract

Every locator in the database is a POSIX path relative to the selected repository
root. No absolute source path is stored. Resolve an artifact with:

```text
<repository-root>/<artifacts.path>
```

The builder rejects symbolic-link artifacts and fails if a projected artifact path is
absolute or contains a parent traversal. Missing or out-of-repository paths listed by a
checksum manifest are recorded as failed observations rather than usable artifact
locators.

## Schema version 1

The database sets SQLite `PRAGMA application_id = 1263748178` and
`PRAGMA user_version = 1`.

- `projection_metadata`: schema and path-semantics declarations.
- `calculations`: one row for each direct calculation directory beneath
  `calculations/research-monograph/`, excluding the non-artifact `campaigns/` staging
  directory.
- `artifacts`: recursive retained files, their safe locators, media/display kind, size,
  computed SHA-256 identity, bounded text preview, and JSON-validity observation.
- `runs`: one row for each valid retained JSON file named as a result document. A run
  row means “retained result document available”; it is not an execution or validation
  claim.
- `scalar_observations`: bounded scalar leaves projected from retained JSON mappings.
  Numbers are metrics; explicit status-like keys are statuses; other scalar leaves are
  descriptors. Array payloads are deliberately not expanded as numeric observations.
- `manifest_observations`: expected and observed SHA-256 identities and the states
  `match`, `mismatch`, `missing`, or `outside_repository`.
- `presentation_artifacts`: view over displayable reports, plots, documents, tables,
  logs, JSON, and text.
- `run_results`: view joining retained result rows to their source artifacts.

Text previews are bounded to 32 KiB and report whether truncation occurred. Consumers
must open source files explicitly when complete content is required.

## Read-only consumption

Consumers should open the projection read-only, for example:

```text
file:/path/to/results.sqlite?mode=ro
```

Atomic replacement gives each completed rebuild a new database file identity. A
long-lived consumer must reopen its read-only SQLite connection after replacement; an
already-open connection may continue reading the previous file generation.
