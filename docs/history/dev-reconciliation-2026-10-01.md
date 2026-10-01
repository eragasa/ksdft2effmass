# `dev` reconciliation with the recovered `main` baseline

## Status and authority

**Status:** Proposed development-branch reconciliation; subject to pull-request review
and CI.

The human owner authorized the Project Koios Bootstrap recommendation on
2026-10-01 with the instruction `recommendation bootstrap authorized`. The authorized
boundary is to use recovered `main` as the active content baseline, preserve `dev`
ancestry, retain independently identified scientific records, broaden pull-request CI
coverage, and avoid history rewriting or unrelated scientific changes.

This record does not authorize a release, a merge to `main`, production electronic-
structure execution, or deletion of external calculation data.

## Reconciliation identity

| Role | Commit |
|---|---|
| Recovered content baseline | `db176a01d019e452d2ecbd732bbbaf7690616fdb` (`origin/main`) |
| Preserved development ancestry | `7bd913151f7e61ed2bdba593df920be36573b502` (`origin/dev`) |
| Ancestry-preserving merge | `8fb6064568419c0e74757e896a007ce60389357a` |
| Baseline and merge tree | `c193b0d5c084784bdd98786e5eb55e862e45277b` |

The merge uses Git's `ours` strategy. Its tree is byte-for-byte identical to the
recovered `main` tree, while its two parents preserve both histories. No path present
in the recovered baseline is removed or overwritten by that merge.

## Preserved development-only scientific records

A path-level comparison identified 16 calculation or provenance files present in the
old `dev` tree but absent from recovered `main`. Those files and the accepted v1
pseudopotential-library specification are restored from the exact `origin/dev` blobs.
Existing recovered-baseline paths are not overwritten.

| SHA-256 | Restored path |
|---|---|
| `fc2e3061725447c4c05b99fbf8ba23c39a0a949858012cd0f33e47e42f10f52c` | `calculations/bulk-silicon/materials-project/mp-149.catalog-entry.json` |
| `838c625bbdfeb7239c525c5f70e61e8dbfda2987e187bf3952d51e55229fe1bf` | `calculations/bulk-silicon/materials-project/mp-149.structure.json` |
| `18b7af553321de5f1801d10580e83ceac3ed7359540c98970d5c83562de4392d` | `calculations/bulk-silicon/materials-project/README.md` |
| `a3811bd94c8847eb43be7e741b45d0b5b1e83bd1a0c4f6138759969ddb9c8c7a` | `calculations/bulk-silicon/materials-project/SHA256SUMS` |
| `fe56b466d9262afa8e21f0bb0656f36477324bc2262accc6c2b4cbb890561150` | `calculations/bulk-silicon/production-convergence-preflight/direct-results-decision-packet.json` |
| `6872e2b1a155eff73afbd685e03c58137e4a19507a91c834d98e7afa1a877355` | `calculations/bulk-silicon/production-convergence-preflight/direct-results-setting-disposition.json` |
| `c21077e05ddc22a63fea5ec798e2a82b6003b565f9721395dbb9812f88f59ebb` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-build-provenance-diagnosis.md` |
| `8ac4425d84e061bae05282a393ad1abc149b6b244ad36dbf24aa98a95e10b352` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-class-separated-nonmpi-c48-classification.md` |
| `16ca04a2abd913c3fb807d35f929443d4518333a49948f761330a2e7ca8f5162` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-instrumented-c48-diagnosis.md` |
| `4cbb18b034720f029a51898ddb7b695dfa72a9c119068e894daaa61da20d4dd7` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-openblas-c48-comparator.md` |
| `9680018fc57ee449cdf133171dcaa6fa458e8485f7f52f857ce84413764bef7e` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-openblas-lldb-first-fault.md` |
| `1c5a122c5e14ebb429f55dd711eab28e81bb7ef8e7e318dd42a18059cc55e24d` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-openblas-nonmpi-c48-comparator.md` |
| `8cfb347386605892726f184c17dd7dc844b0816d3f774adc1410ab7d73d6459e` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-opencl-disabled-c48-diagnosis.md` |
| `afcc48150bb192c7f5a7b356ac1289cca61dc96438612e34333a0e52723cd34a` | `calculations/bulk-silicon/production-convergence-preflight/ieee-warning-read-only-diagnosis.md` |
| `ef2d7524fcefd58d3e3c3755bc5840af2f07e6785cf41b7889a344a68788eadb` | `calculations/bulk-silicon/qe-example01-si-scf-davidson/run_isolated.py` |
| `a94a7dcada452b59ceb3eaf31a54b4f3497dfbb315d4e5628a25812333e9e4d8` | `calculations/bulk-silicon/qe-example01-si-scf-davidson/si.scf.david.isolated.in` |
| `e9acdfd0c20b4181b61ddcc2b2f4632000574f40c88341045aed72b16a284f7c` | `specification/dft-pseudopotential-library/v1/index.md` |

These files are retained records. Their presence does not authorize calculator
execution or establish scientific validation.

## Development-only commit disposition

The old `dev` line contains 14 commits not patch-equivalent to recovered `main`.
Their ancestry remains reachable through the merge parent. Their active-tree
disposition is:

| Commit(s) | Active-tree disposition |
|---|---|
| `b6b0be18`, `c05fc883`, `74ea2707`, `43c8fb84`, `5e2b50b8` | Not restored: obsolete Harness projections, tasks, or administrative control state removed by the accepted recovery baseline. |
| `6430f22f` | Not restored: its superseded `decisions/` and Harness migration must not replace the current `.pi/checkpoints/` authority surface. |
| `c47d3cfc` | Scientific calculation and provenance paths absent from recovered `main` are restored above; application, Harness, task, and generated projection changes are not restored. |
| `cb6622e3`, `b5c568d4` | Deferred for a separate software/public-contract review. The accepted pseudopotential specification is restored above; implementation changes are not mixed into reconciliation. |
| `35ae24af` | Deferred for a separate Wannier90 documentation review; obsolete task and Harness projections are not restored. |
| `b27e0e35`, `96d5e487` | Superseded by the repository's current CI workflow plus the separate all-base pull-request trigger correction. |
| `97f0ab37`, `7bd91315` | Deferred for separate numerical-verification review. Tolerance, result-contract, and gauge-branch behavior are not changed during branch reconciliation. |

Deferred content is preserved in Git ancestry; this reconciliation makes no claim that
it is accepted by the recovered active tree.

## CI boundary

The accompanying CI correction removes the pull-request base-branch filter so stacked
pull requests can receive hosted checks. Push-triggered CI remains limited to `dev`
and `main`. Expensive retained numerical replays remain excluded from the required
hosted profile, and no retained result, tolerance, or expected conclusion is changed.

No electronic-structure or Wannier calculation was executed as part of this
reconciliation.
