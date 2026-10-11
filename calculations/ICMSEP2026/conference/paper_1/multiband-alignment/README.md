# M2 multiband alignment and locality

This directory retains the prospectively frozen, local synthetic M2 evidence
package for Conference Paper 1. The calculation uses a gapped four-state parent
with a rank-two retained space, a known periodic nonidentity gauge attack,
pointwise and global-unitary alignment channels, block hoppings, finite-range
truncation, and disjoint withheld diagnostics.

- `input.json` and `protocol.md` are the prospectively frozen controls.
- `protocol-freeze.json` preserves their pre-execution SHA-256 hashes;
  `protocol-amendment.json` records the later wording-only clarification without
  presenting it as prospectively frozen.
- `run.py` is the thin typed producer entry point.
- `verify_result.py` reconstructs the protocol without calling `run.py` or the
  library producer Action.
- `result.json`, `verification.json`, `figure-data.csv`, the summary figure,
  `report.md`, and `software.json` are retained outputs.
- `source.sha256` binds the M2 scripts plus direct package modules used for
  frames, alignment, transforms, diagnostics, quantities, and serialization;
  `SHA256SUMS` binds the retained package artifacts. These integrity manifests
  do not establish chronology. `software.json` retains the dirty-worktree
  status rather than presenting the package as a clean release snapshot.

The package establishes bounded synthetic numerical behavior only. It contains
no protected calculator execution, material result, uncertainty quantification,
or scientific acceptance disposition.
