# Defect-2D Stage B multi-route result

## Evidence status

This report records a calculated synthetic numerical-verification result for the
accepted isotropic scalar parent. HC08 human-accepts this exact bounded evidence
and authorizes managed closeout only. It is not DFT, production Wannier90,
silicon or dopant validation, material transfer, uncertainty quantification,
publication, or evidence for Stages C--E.

The first HC05 attempt and the HC06 retry failed before matrix construction. Both
failures remain in `stage-b-execution-failure.md` and their original logs. HC07
authorized one schema-corrected attempt with no further retry. That attempt
completed once and produced `stage-b-result.json`.

## Bound calculation

- parent case: $(\lambda_x,\lambda_y,\lambda_{xy})=(0.5,0.5,0)$;
- represented space: one spinless scalar $8\times8$ periodic supercell,
  dimension 64;
- twists: Gamma and $(0.37,-0.23)$ turns;
- plants: central and off-axis point-onsite defects of strength $-0.25E_G$;
- matrix routes: centred uniform-link Route A and reduced seam Route B;
- schedules: fresh-process A-then-B and B-then-A;
- bridge: one deterministic lift/gauge equivalence relation;
- retained parent hoppings: 61 through squared radius 18;
- network and external scientific executables: none.

The completed process ran for 2.50 seconds and reported maximum resident set size
56,639,488 bytes. The compact JSON result occupies 3,035,507 bytes, below the
30 MiB authorization bound.

## Inventory and criterion disposition

The exact retained inventory is:

| Record class | Count |
|---|---:|
| execution schedules | 2 |
| matrix routes per schedule | 2 |
| known-map route evaluations | 72 |
| matched bridge records | 36 |
| blind candidate rows | 2,304 |
| known-case schedule comparisons | 36 |
| bridge schedule comparisons | 18 |
| blind-summary schedule comparisons | 6 |

The runner reports `status=pass` with no failed criterion. The independent
verifier reports:

```text
defect_2d_stage_b_reconstruction=PASS
defect_2d_stage_b_criteria=PASS
maximum_independent_reconstruction_difference=7.8452687268361823e-13
```

The independent difference is below the frozen $10^{-10}$ route/covariance
criterion. The verifier reconstructs Route A through sampled dispersion and a
Fourier transform and Route B through independently assembled seam-shift
factors; it does not import the runner.

## Known-map and bridge results

Across both routes and schedules, the largest retained values are:

| Diagnostic | Maximum |
|---|---:|
| recovered Hermiticity defect | $5.5511\times10^{-17}$ |
| recovery maximum-entry defect | $2.2377\times10^{-16}$ |
| recovery Frobenius defect | $3.0792\times10^{-16}$ |
| onsite-amplitude defect | $2.2377\times10^{-16}$ |
| canonical bridge maximum-entry residual | $5.5511\times10^{-17}$ |
| canonical bridge Frobenius residual | $1.6682\times10^{-16}$ |
| attacked bridge maximum-entry residual | $2.2204\times10^{-16}$ |
| attacked bridge Frobenius residual | $3.5373\times10^{-16}$ |
| plant bridge residual | $0$ |
| pristine cross-route eigenvalue difference | $4.7184\times10^{-16}$ |

The retained hopping inventory has zero Hermiticity defect and maximum $D_4$
defect $6.1616\times10^{-16}$. Known-case and bridge schedule differences are
exact zero in the retained comparison records. No route or schedule was selected,
averaged, ranked, or voted.

## Blind identifiability result

Both routes and both schedules reproduce the frozen unresolved-map disposition:

- Gamma: 512 tied maps per route and schedule;
- generic twist: 64 tied translations per route and schedule;
- issue code: `DEFECT_2D.SITE_MAP_UNRESOLVED`;
- selected map: null;
- extracted operator: null.

All 2,304 candidate rows are retained with route, schedule, case, operation,
translation, transformed twist lift, comparison twist, integer lift, objective,
and median shift diagnostic. The largest minimum blind objective is
$7.3925\times10^{-17}$ and the maximum ambiguity-set shift deviation is zero.
This is the expected identifiability stop, not a failed extraction or permission
to select the planted site.

## Adverse controls

Omitting the known $0.137E_G$ energy shift produces maximum-entry residual
$0.137E_G$ and Frobenius residual $1.096E_G$. Holding the generic twist fixed
instead of applying the route-appropriate transformation produces maximum-entry
residuals $9.9786\times10^{-3}E_G$ in Route A and
$4.0653\times10^{-2}E_G$ in Route B, while the correct transformed-twist
residuals remain at approximately $7.176\times10^{-16}E_G$. The adverse controls
therefore discriminate the declared failures.

## Retained execution and verification history

- first invocation failure: `stage-b-execution.log`;
- corrected-path schema failure: `stage-b-retry-execution.log`;
- completed HC07 process: `stage-b-schema-corrected-execution.log`;
- verifier invocation-path failure: `stage-b-verification-invocation-failure.log`;
- completed independent verification: `stage-b-verification.log`.

None of the failed invocations produced or replaced `stage-b-result.json`. The
successful runner and verifier both refuse overwrite.

## Reproduction

From `python/`, independent verification and retained-data plotting use
repository-relative or canonical paths:

```bash
uv run python \
  ../calculations/research-monograph/impurity-defect-2d/verify_stage_b.py \
  --result calculations/research-monograph/impurity-defect-2d/stage-b-result.json \
  --repository-root /Users/eugene/repos/ksdft2effmass

uv run python \
  ../calculations/research-monograph/impurity-defect-2d/plot_stage_b.py \
  --result /Users/eugene/repos/ksdft2effmass/calculations/research-monograph/impurity-defect-2d/stage-b-result.json \
  --output /tmp/stage-b-summary.svg
```

The retained SVG was regenerated byte-for-byte from the result.

## Limitations

This bounded result verifies the declared finite synthetic scalar-onsite,
$D_4$, gauge-bridge, schedule, ambiguity, and adverse-control contracts only. It
does not establish an absolute blind site map, a material impurity operator,
scientific validation, uncertainty quantification, general gauge equivalence,
optimizer behavior, Stage C directional/nonlocal extraction, finite-area or
shape convergence, continuum transfer, publication readiness, or release
status. HC08 human-accepts only this exact synthetic evidence boundary; it does
not authorize a rerun or successor stage.
