# Canonical bulk-silicon calculation layout migration

## Status

This document is a proposed pre-move inventory for retiring the current mixed
`analysis/`, `simulations/`, `common_space/`, `research-protocol/`, and
`technical-report/` layout.

It proposes destinations and migration gates; implementation remains separately
authorized after the path and checksum contracts are reconciled. It does not itself move or delete retained
calculation data, rewrite a retained execution, authorize Quantum ESPRESSO or Wannier90,
or establish scientific acceptance.

The current inventory contains:

- 18 immediate analysis families;
- 32 simulation-preflight directories;
- 35 simulation-evidence directories;
- four overlapping protocol documents; and
- two generations of root technical report.

The legacy names often encode campaign shorthand, software versions, numerical settings,
and outcomes in one path. The target layout instead names the scientific owner. Meshes,
band counts, windows, software versions, and exact source identities belong in typed
inputs, execution records, and provenance manifests.

## Governing rules

1. A scientific question has one calculation-family owner.
2. Each maintained family follows the calculation-package lifecycle in
   [`docs/architecture/v3/calculations/implementation.md`](../../../docs/architecture/v3/calculations/implementation.md).
3. Authored inputs and schemas live at the family root. Exact consumed copies live in
   the execution directory.
4. Calculation, independent verification, rendering, sealing, and package verification
   remain separate stages.
5. Reusable QE, QEXSD, pw2wannier90, and Wannier90 mechanics remain in
   `projectkoios-simulations`.
6. Reusable tight-binding and Slater--Koster mechanics remain in Project Koios PhysKit.
7. KSD retains silicon-specific composition, policy, scientific disposition, evidence,
   and interpretation.
8. A campaign code such as `C6-B20-W21` may remain in retained metadata but shall not be
   the canonical family-directory name.
9. Historical bytes are not silently edited to resemble the new layout.
10. No compatibility alias, symlink, dual read, dual write, or fallback path is created.
11. A legacy path is removed only after every incoming path, checksum, and provenance
    binding has an explicit replacement or an explicit immutable-history disposition.
12. Generated caches such as `__pycache__/` are not migrated.

## Target hierarchy

```text
calculations/Si/bulk/
├── README.md
├── protocol/
│   ├── protocol.tex
│   ├── evidence-policy.md
│   └── decisions/
├── parent-source/
│   ├── structure-relaxation/
│   ├── finite-setting-selection/
│   ├── ground-state/
│   └── band-structure/
├── wannier-source/
│   ├── construction-grid/
│   ├── preprocessing/
│   ├── interface-conversion/
│   ├── localization/
│   └── qualification/
├── reduction/
│   ├── common-space/
│   │   ├── rank-diagnosis/
│   │   ├── independent-verification/
│   │   └── symmetry-diagnosis/
│   ├── hopping/
│   │   ├── full-source-characterization/
│   │   ├── support-analysis/
│   │   ├── shell-refitting/
│   │   ├── gauge-locality/
│   │   └── locality-comparison/
│   └── slater-koster/
│       ├── model-definition/
│       ├── spectral-only/
│       ├── global-unitary/
│       ├── rank-nine/
│       └── new-source/
├── evaluation/
│   ├── development-parent-comparison/
│   ├── source-relative-band-edge/
│   ├── independent-convention-verification/
│   └── confirmation/
├── controls/
│   └── vogl-sp3s-star/
├── reports/
│   └── program-synthesis/
└── archive/
    └── legacy-layout/
```

Only owners with actual protocol, input, implementation, execution, or retained-evidence
content are created during migration. Empty future-branch directories are not created as
placeholders. The first canonical decision record is the
[QE simulation design informed by finite-rank studies](protocol/decisions/qe-simulation-design-from-rankn.md).

## Calculation-family shape

Each executable leaf uses the maintained package shape rather than inventing a
silicon-specific framework:

```text
family-name/
├── README.md
├── protocol.md
├── evidence-policy.md
├── inputs/
├── schemas/
├── technical_report/
├── run_01_calculation.py
├── run_02_verification.py
├── run_03_render.py
├── run_04_seal.py
├── verify_package.py
└── executions/
    └── descriptive-execution-id/
        ├── execution.json
        ├── inputs/
        ├── schemas/
        ├── results/
        ├── verification/
        ├── figures/
        ├── technical_report/
        ├── provenance.json
        ├── source.sha256
        ├── SHA256SUMS
        └── evidence-package-identity.txt
```

A family may initially implement only the stages that exist. Missing later stages remain
absent and are reported as absent; empty scripts are not installed.

## Root and protocol migration

| Current path | Canonical destination | Disposition |
|---|---|---|
| `README.md` | `README.md` | Rewrite as the canonical navigation and status page after the new owners exist. |
| `development-plan.md` | `protocol/decisions/program-development-plan.md` | Retain scientific gates; remove path-specific navigation that becomes stale. |
| `provisional-use-disposition.md` | `protocol/decisions/provisional-parent-use.md` | Preserve the human disposition and its exact evidence bindings. |
| `evidence-crosswalk.md` | `protocol/evidence-policy.md` plus execution-local provenance | Split policy from path inventory; do not duplicate execution manifests. |
| `research-protocol/controlled-reduction-protocol-hopping-first.tex` | `protocol/protocol.tex` | Proposed future destination of the controlling protocol; the present path remains authoritative until a separately reviewed migration. |
| `research-protocol/research-protocol.tex` | `archive/legacy-layout/protocols/parent-construction.tex` | Preserve the current exact bytes and path now; any future move requires every bound identity to be closed explicitly. |
| `research-protocol/controlled-reduction-protocol.tex` | `archive/legacy-layout/protocols/controlled-reduction.tex` | Preserve the current exact bytes and path now; any future move requires every bound identity to be closed explicitly. |
| `research-protocol/controlled-reduction-protocol-post-s110.tex` | `archive/legacy-layout/protocols/post-s110.tex` | Preserve the current exact bytes and path now; any future move requires every bound identity to be closed explicitly. |
| `research-protocol/README.md` | `protocol/README.md` | Replace the four-document authority discussion with one current authority and an exact revision ledger. |
| `technical-report/` | `reports/program-synthesis/` | Select one maintained report source; retain superseded report bytes under the legacy archive. |

## Analysis-family migration

| Current path under `analysis/` | Canonical destination | Scientific role |
|---|---|---|
| `construction-mesh-adequacy-recommendation/` | `wannier-source/construction-grid/decisions/mesh-adequacy/` | Construction-grid decision and reserved confirmation geometry. |
| `provider-eligible-operator-qualification/` | `wannier-source/qualification/` | Structural and provider eligibility of the fixed Wannier source. |
| `conduction-frozen-gauge-sensitivity/` | `wannier-source/localization/executions/conduction-frozen-gauge-sensitivity/` | Blocked-source localization sensitivity study. |
| `c6-b20-w21-untruncated-characterization/` | `reduction/hopping/full-source-characterization/` | Full retained hopping source, reconstruction, and locality characterization. |
| `c6-b20-w21-spatial-truncation-design/` | `reduction/hopping/support-analysis/inputs/` | Authored complete-shell support family and gates. |
| `c6-b20-w21-spatial-truncation-evaluation/` | `reduction/hopping/support-analysis/executions/complete-shell-evaluation/` | Complete-shell source-relative evaluation. |
| `c6-b20-w21-spatial-truncation-disposition/` | `reduction/hopping/support-analysis/decisions/full-support-retention/` | Human full-support disposition; not a calculation result. |
| `c6-b20-w21-hopping-pareto-synthesis/` | `reduction/hopping/locality-comparison/` | Channel-separated locality comparison and interval-aware Pareto composition. |
| `c6-b20-w21-tau1-tau2-posthoc-exploration/` | `reduction/hopping/support-analysis/executions/posthoc-threshold-map/` | Post-hoc threshold map; remains distinct from prospective support selection. |
| `c6-b20-w21-refitted-ws-shell-witness-posthoc/` | `reduction/hopping/shell-refitting/` | Shell-scale refitting witnesses; no global infeasibility claim. |
| `c6-b20-w21-wannier-only-fidelity-ladder/` | `reduction/hopping/support-analysis/executions/source-relative-refinement/` | Independent-mesh source-relative support transfer. |
| `c6-b20-w21-gauge-alignment-locality/` | `reduction/hopping/gauge-locality/` | Gauge attack, alignment, and locality development study. |
| `c6-b20-w21-slater-koster-definition-fit/` | `reduction/common-space/rank-diagnosis/` | Rename according to the actual stopped result: common-space rank diagnosis, not a completed fit. |
| `c6-b20-w21-revealed-408-development/` | `evaluation/development-parent-comparison/` | Direct-parent development overlay. |
| `withheld-parent-validation-preflight/` | `evaluation/development-parent-comparison/inputs/` | Frozen parent-comparison geometry and criteria; the historical name no longer describes its revealed status. |
| `c6-b20-w21-wannier-only-comprehensive-band-edge/` | `evaluation/source-relative-band-edge/` | Source-relative non-SOC band-edge diagnostics. |
| `c6-b20-w21-independent-convention-audit/` | `evaluation/independent-convention-verification/` | Independent mass-convention and cyclic-to-ordinary checks. |
| `controls/` | `controls/` | Keep the owner; move `vogl-sp3s-star/` directly to the canonical control path. |

The calculation-incubated `common_space/diagnostics/` implementation moves into
`reduction/common-space/rank-diagnosis/` only as calculation composition. Reusable
matrix behavior must first have a reviewed source owner. The future independent verifier
belongs to `reduction/common-space/independent-verification/` and must not import the
producer calculation implementation.

## Parent-source simulation migration

Preflight and evidence directories for one scientific family are merged into authored
root inputs plus immutable execution directories. A preflight is not retained as a
parallel family after its consumed inputs are copied into the execution.

| Current simulation path or paired paths | Canonical destination |
|---|---|
| `evidence/...right-handed-kpoint/` | `parent-source/finite-setting-selection/executions/initial-shifted-mesh-scan/` |
| `evidence/...right-handed-gamma-kpoint/` | `parent-source/finite-setting-selection/executions/gamma-centered-mesh-scan/` |
| `evidence/...right-handed-gamma-k10-encut/` | `parent-source/finite-setting-selection/executions/wavefunction-cutoff-scan/` |
| `evidence/...vc-relax-failed-volume/` | `parent-source/structure-relaxation/executions/volume-only-rejected/` |
| `evidence/...vc-relax-ibrav2/` | `parent-source/structure-relaxation/executions/fcc-native-relaxation/` |
| `preflight/s1-gamma-c42-kpoint-confirmation/` and matching evidence | `parent-source/finite-setting-selection/executions/relaxed-structure-mesh-confirmation/` |
| `preflight/s1-gamma-k10-cutoff-confirmation/` and matching evidence | `parent-source/finite-setting-selection/executions/relaxed-structure-cutoff-confirmation/` |
| `preflight/accepted-s1-parent-scf-gamma-k10-c42/` and matching evidence | `parent-source/ground-state/executions/accepted-finite-setting-parent/` |
| `evidence/...parent-bands-l-gamma-x-gamma-b20/` | `parent-source/band-structure/executions/l-gamma-x-gamma-context-path/` |
| `structures/` | The consuming parent-source family `inputs/`; the exact relaxed structure also remains copied into each consuming execution. |
| `accepted-stable-pair.json` | `parent-source/finite-setting-selection/decisions/accepted-finite-setting-pair.json` |
| `candidate-stable-pair-disposition.json` | `parent-source/finite-setting-selection/decisions/candidate-pair-disposition.json` |

## Wannier-source simulation migration

### Construction-grid NSCF families

| Current preflight/evidence identity | Canonical execution destination under `wannier-source/construction-grid/` |
|---|---|
| `accepted-s1-wannier-nscf-4x4x4-b12` | `executions/mesh-4-bands-12-unconverged/` |
| `accepted-s1-wannier-nscf-4x4x4-b12-david` | `executions/mesh-4-bands-12-davidson/` |
| `accepted-s1-wannier-nscf-6x6x6-b12-david-c6` | `executions/mesh-6-bands-12-davidson/` |
| `accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20` | `executions/mesh-6-bands-20-davidson/` |
| `evidence/...withheld-parent-nscf-408-david/` | `evaluation/development-parent-comparison/executions/direct-parent-408/` |

### Wannier90 preprocessing and interface conversion

| Current preflight/evidence identity | Canonical destination |
|---|---|
| `accepted-s1-wannier90-preprocess-sp3sstar` | `wannier-source/preprocessing/executions/atomic-trial-family/` |
| `accepted-s1-wannier90-preprocess-c6-lower-energy-frozen` | `wannier-source/preprocessing/executions/lower-energy-frozen-window/` |
| `accepted-s1-wannier90-preprocess-c6-b20-w21` | `wannier-source/preprocessing/executions/twenty-band-expanded-window/` |
| `accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise` | `wannier-source/preprocessing/executions/twenty-band-expanded-window-precise-controls/` |
| `accepted-s1-pw2wannier90-sp3sstar` | `wannier-source/interface-conversion/executions/atomic-trial-family/` |
| `accepted-s1-pw2wannier90-c6-lower-energy-frozen` | `wannier-source/interface-conversion/executions/lower-energy-frozen-window/` |
| `accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise` | `wannier-source/interface-conversion/executions/twenty-band-expanded-window-precise-controls/` |

### Localization families

| Current identity suffix after `wannier90-localization-` | Canonical execution destination under `wannier-source/localization/` |
|---|---|
| `sp3sstar-blocked` and provider preflight | `executions/atomic-trial-family-blocked/` |
| `conditioned-damped-blocked` | `executions/conditioned-damped-blocked/` |
| `conduction-frozen-blocked` | `executions/conduction-frozen-iteration-500/` |
| `conduction-frozen-iter1000-blocked` | `executions/conduction-frozen-iteration-1000/` |
| `conduction-frozen-cg200-blocked` | `executions/conduction-frozen-cg-steps-200/` |
| `conduction-frozen-cg200-iter4000-blocked` | `executions/conduction-frozen-cg-steps-200-iteration-4000/` |
| `conduction-frozen-cg-reset1-blocked` | `executions/conduction-frozen-cg-reset/` |
| `conduction-frozen-fixed-step1-blocked` | `executions/conduction-frozen-fixed-step/` |
| `conduction-frozen-guiding-centres-blocked` | `executions/conduction-frozen-guiding-centres/` |
| `conduction-frozen-trial-step1-blocked` | `executions/conduction-frozen-trial-step/` |
| `lower-energy-frozen-blocked` | `executions/lower-energy-frozen-initial/` |
| `lower-energy-frozen-dis2000-eligible` | `executions/lower-energy-frozen-disentanglement-2000/` |
| `c6-lower-energy-frozen-dis2000-blocked` | `executions/mesh-6-lower-energy-frozen-disentanglement-2000/` |
| `c6-lower-energy-frozen-dis4000-blocked` | `executions/mesh-6-lower-energy-frozen-disentanglement-4000/` |
| `c6-b20-w21-aiida-precise-eligible` | `executions/twenty-band-expanded-window-precise-controls/` |
| preflight `c6-t1-full-parent-outer-dis4000` | `inputs/expanded-window-twelve-band-unexecuted/` |

Every corresponding preflight directory is consumed into the named execution or retained
as an explicitly unexecuted authored input. Preflight and evidence trees are not kept as
parallel navigation systems.

## Simulation decision-document migration

| Current document group under `simulations/` | Canonical destination |
|---|---|
| `seed-structure-decision.md` | `parent-source/structure-relaxation/decisions/` |
| finite-setting and stable-pair documents | `parent-source/finite-setting-selection/decisions/` |
| `wannier-interface-decision.md` and parent-band/window decisions | `wannier-source/construction-grid/decisions/` |
| preprocessing and conversion contracts | `wannier-source/preprocessing/` or `wannier-source/interface-conversion/` according to ownership |
| localization window, optimizer, budget, and convergence documents | `wannier-source/localization/decisions/` |
| `localization-provider-reference-correction.md` | `wannier-source/qualification/decisions/` |
| `scientific-contract.md`, `execution-contract.md`, and `verification-plan.md` | Split into the affected family protocols and evidence policies; retire the generic copies. |
| `architecture-plan.md` | `archive/legacy-layout/simulation-architecture-plan.md` after all provider ownership statements are represented by current package documentation. |
| `readiness.md` | Replaced by family-local readiness and root navigation; archive the final legacy snapshot. |
| `preflight/c6-b20-w21-gated-series/` | Split across the common-space, hopping, and reduced-model owners; retain the exact historical series plan in `archive/legacy-layout/gated-series/`. |

## Reports and figures

- A figure belongs to one execution and is generated only from authenticated result and
  verification bytes.
- Directories named `figures-v2`, `figures-v3`, and similar are migrated into separate
  descriptive executions or omitted when they are replaceable renderings of identical
  result bytes.
- A root synthesis report may summarize several families but does not own their results.
- Compiled PDFs remain generated artifacts unless an execution contract explicitly
  admits and checksums them.

## Retirement sequence

1. **Freeze the inventory.** Record every current file, byte size, and SHA-256 digest.
2. **Classify incoming references.** Mark each reference as live, retained execution,
   publication, documentation, test, or external-artifact inventory.
3. **Create one destination family at a time.** Do not create the whole target tree as
   empty scaffolding.
4. **Move active authored material.** Update direct imports and paths without aliases.
5. **Materialize retained executions.** Copy exact consumed inputs and schemas, preserve
   result bytes, and create migration manifests that bind old and new locations.
6. **Verify byte preservation.** Check every retained source/result digest and every
   updated provenance contract.
7. **Switch authority.** Update root navigation, protocols, tests, and publication
   consumers to the canonical owner.
8. **Retire the legacy path.** Remove it only when no live reference remains and the
   migration manifest proves the replacement.
9. **Remove duplicate code.** Reusable behavior must resolve to its library owner;
   calculation packages retain only composition and evidence logic.
10. **Run package checks.** Run affected tests first, then calculation Ruff checks,
    documentation builds, path/reference audits, and `git diff --check`.

## First migration tranche

The first tranche should be the unretained common-space work because it has a small,
explicit boundary and no promoted scientific result:

```text
common_space/diagnostics/
    -> reduction/common-space/rank-diagnosis/
```

That tranche shall:

1. retain CSD0/CSD1 as a calculation producer;
2. keep authenticated parsing in `projectkoios-simulations`;
3. move reusable matrix behavior to an approved source owner before reuse;
4. install direct calculation composition without a generic workflow layer;
5. add an independent verifier under the separate canonical family;
6. preserve fail-closed output-root behavior; and
7. create no retained scientific execution without separate authorization.

The second tranche should consolidate the three spatial-support directories into the
single `reduction/hopping/support-analysis/` family while preserving the distinction
between authored design, calculated evaluation, and human disposition.

## Completion criteria

The legacy layout is retired only when:

- one controlling protocol remains under `protocol/`;
- every maintained scientific operation has one canonical owner;
- every retained execution has immutable inputs, result bytes, provenance, and checksum
  closure at its destination;
- every historical path has a migration-manifest entry;
- no maintained code reads an old path;
- no compatibility aliases or fallback paths exist;
- no campaign shorthand is required to understand a directory name;
- all direct calculation, independent verification, rendering, and package checks pass;
  and
- the old `analysis/`, `simulations/`, `research-protocol/`, `common_space/`, and
  superseded root report paths are removed or retained only beneath the explicit legacy
  archive.
