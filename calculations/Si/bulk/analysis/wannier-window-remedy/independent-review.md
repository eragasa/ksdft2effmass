## Review

**Scope:** Read-only checkpoint-retention review. Paths below are relative to `calculations/Si/bulk/analysis/wannier-window-remedy/`. The diff tool reports untracked checkpoint files; no committed range or unrelated changes were reviewed.

**No issues found.**

### Correct

- **Bounds:** `original_scripts/ksd_silicon_trial_whitening.py:62–73,152–158` correctly uses exact left-inverse residual lower bounds, normalized-witness upper bounds, and separate native-input/projector and whitening-arithmetic corrections. Floating singular-value calculations supply candidates rather than certify the inequalities.
- **Excluded-band attribution:** `original_scripts/ksd_silicon_gamma_excluded_bands.py:79–110,126–127` conservatively bounds the second Gram eigenvalue, minimum-direction projector error, perturbed row responses, and dominant response share. These support the stated conditional attribution, not occupations or symmetry labels.
- **Pointwise existence:** `findings.md:81–84` and `original_scripts/ksd_silicon_window_feasibility.py:8–17` give a valid construction. If \(W^\dagger Cx=0\), then \(x\in K\); hence \(Cx\in CK\subset W\) while orthogonal to \(W\), forcing \(Cx=0\), then \(x=0\). This proves nonsingular overlap, not a threshold pass or global frame.
- **Provenance and replay:** `reproduce.py:98–173` checks the complete fifteen-artifact inventory, byte identities, script/request bindings, and compact source associations. Lines 176–220 check numerical-module identities and native payloads; lines 320–324 exclusively create output. `tests/test__WindowRemedyCheckpoint.py:51–136` covers native-free inspection, altered observations/request bindings, existing output, and dangling output symlinks.
- **Claim boundaries:** `README.md:5–8,19–35,64–67` and `findings.md:11–14,74–90` preserve the historical SSSP scope, conditional rounding assumptions, display-only bounds, unselected cap, blocked S110, and absence of independent numerical verification or production qualification. These boundaries respect the governing protocol’s progression and human successor-selection authority.

### Validation and limitations

I inspected all five archived scripts and the maintained review targets, consulting only relevant numerical dependency seams. No files were changed and no commands or calculators were run.

The supervisor reports successful integrity tests, typing, Ruff, archive checking, full-216 native-input replay, and Sphinx `-W`. Those results were **not independently rerun** here. I did not independently recompute hashes or the numerical records from external native inputs. This is source/proof review, not CSD1-V, scientific validation, human acceptance, or execution authority.

**Merge verdict:** OK with notes — checkpoint-retention scope only; no merge authorization.

**Review outcome:** NO_BLOCKING_FINDINGS  
**Operator request:** NONE