# Wannier window-remedy diagnostic checkpoint

## Status and scope

Retained local, no-calculator diagnostics of the historical SSSP `C6-B20-W21`
source. **The tested cap is unselected. The original S110 alignment remains
blocked.** These files do not complete CSD0/CSD1/CSD1-V/CSD2, select a successor,
qualify a production parent, or authorize a fit or calculator occurrence.
The [current protocol](../../research-protocol/controlled-reduction-protocol-hopping-first.tex)
and [pending Stage 4 task](../../development-plan.md#pending--qualify-a-window-remedy-wannier-candidate)
continue to govern progression. `inputs/protocol-at-diagnosis.tex` is an exact
snapshot of the protocol bound by the diagnostics, not a competing authority.

See [findings and limitations](findings.md) for the scientific interpretation.

## Contents and provenance

- `results/`: five original compact result records, unchanged from the authorized
  local diagnostics. Floating bounds in these JSON files are display values,
  not outward-rounded exact interval certificates.
- `original_scripts/`: byte-exact exploratory source, including its original
  absolute paths and fixed `/tmp` entrypoints. These are provenance snapshots,
  **not supported APIs or the recommended replay command**.
- `inputs/`: exact request and compact source/protocol snapshots.
- `manifest.json`: byte counts, SHA-256 identities, dependency versions, and the
  source-checkout context. It detects changed bytes; it is not a signature,
  running-process attestation, or scientific acceptance.
- `reproduce.py`: calculation-local replay of the key findings into a fresh
  output directory. It reuses the authenticated archived numerical reference;
  this replay is **not independent numerical verification** of that reference.

Native AMN/EIG/gauge/disentanglement files remain external. No wavefunctions,
checkpoints, native dense matrices, or confirmation values are added here.
The numerical modules used by these diagnostics were uncommitted at retention;
`results/trial-whitening.json` binds their exact source hashes. The displayed
base commit alone does not identify those modules.

## Inspect and reproduce

Use the locked Python environment from the repository root:

```bash
PYTHONPATH=calculations/Si/bulk python/.venv/bin/python \
  calculations/Si/bulk/analysis/wannier-window-remedy/reproduce.py --check-only

PYTHONPATH=calculations/Si/bulk python/.venv/bin/python \
  calculations/Si/bulk/analysis/wannier-window-remedy/reproduce.py \
  --output-root /tmp/si-window-remedy-replay-01
```

The output root must not already exist, including as a dangling symlink. A failed
write can leave an incomplete root; choose a new root, do not overwrite it.
`--check-only` checks retained artifact/script/request identities without opening
external native inputs. Numerical replay additionally requires the exact recorded
provider and local numerical-module source versions and external input bytes.

Explicit `--amn`, `--eig`, `--gauge`, and `--disentanglement` paths can relocate
individual native inputs. Every supplied payload must still match the recorded
size and SHA-256; there is no alternate-source admission. Defaults are the original
recorded absolute paths. The replay recalculates the trial/whitening diagnostics,
Gamma window loss and dominant response, and all-point frozen-state feasibility.
It does not recreate every original result schema or replace the retained records.

The interval approximately `[21.257167314276, 21.418602714893)` eV describes one
membership class **on the sampled construction mesh**. Its midpoint was a test
representative, not a physical optimum, final input, or cap transferable to a
PseudoDojo parent. No finite sample certifies behavior between its points.

## Findings, review, and remaining work

- [Findings and mathematical limits](findings.md)
- [Independent AI source/proof review](independent-review.md)
- [Executed checks and review scope](validation.md)
- [Earlier formal-source admission preflight](source-admission-preflight.md):
  stopped before formal execution on then-missing declaration/completion evidence.
  The source declaration has since been prepared as recorded below; this historical
  preflight is not rewritten. Subsequent producer and CSD1-V work is linked below.
- [Unchanged-source association dossier](source-associations.md): separates supported
  band-gauge lineage from the unresolved nominal/executed geometry identification.
  The earlier [source-association review](source-association-review.md) reported
  **REVIEW_INCONCLUSIVE** before the later full-source statement and adoption.
  Its report is unchanged; current status is given by the adoption/declaration below.
  This does not change the earlier bounded retention review.
- [Geometry-identification draft](../../protocol/decisions/geometry-identification-draft.md):
  proposes an explicit native-source/nominal-metadata distinction. The
  [independent draft review](../../protocol/decisions/geometry-identification-review.md)
  found **NO_BLOCKING_FINDINGS** after correcting the full-CSD0 scope wording.
  The draft itself is not adopted and does not supply the full S30 association or
  lift the admission stop.
- [Full S30 state-space identification statement](s30-state-space-identification.md):
  the separate [independent review](s30-state-identification-review.md) found
  **NO_BLOCKING_FINDINGS**. It conditionally supports the full S30 association on
  CSD0's 216-point domain, without requiring an off-mesh KS embedding. This is not
  full CSD0 passage or execution authority.
- [Scientific-owner adoption and explicit source bindings](../../protocol/decisions/s30-state-identification.md):
  adopts that bounded S30 interpretation under the unchanged CSD0 rule, keeping
  nominal-geometry diagnostics separate. The [prepared source-state declaration](source-state-assertions.json)
  uses the existing v1 wire contract. At preparation time the actual six-role bundle
  was correctly rejected as incomplete; that task performed no retained numerical run.
- [Subsequently authorized CSD1 producer checkpoint](../common-space-producer/):
  contains the actual 216-point reconstruction, geometric construction-index inventory
  and completion evidence. Its two raw-gate failures remain indices 0 and 12; no window
  is selected. Its geometric index relations do not establish electronic symmetry
  attribution or physical validation.
- [Subsequently authorized independent CSD1-V checkpoint](../common-space-verification/):
  authenticates the complete real bundle and verifies/correlates all 216 points under
  the unchanged threshold and declared source/uncertainty contract. CSD2 remains unrun;
  no new window, successor, physical validation or production qualification is established.
- [Pending construction/qualification tasks](../../development-plan.md#pending--qualify-a-window-remedy-wannier-candidate)

The bounded retention review found no blocking findings. It did not independently
rerun numerical analysis or complete CSD1-V. Only the development-plan item for
retaining and reviewing these diagnostics is complete; window selection and every
new-construction/qualification task remain pending.
