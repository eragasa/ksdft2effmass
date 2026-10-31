# Wannierisation convergence-policy review

> **Historical review:** its accepted hybrid recommendation is superseded for
> prospective `C6-B20-W21` occurrences by the later
> [`AiiDA-precise convergence adaptation`](aiida-precise-convergence-adaptation-decision.md).
> It remains evidence for the earlier decision and does not reclassify past runs.

## Scope and question

This review asks whether the campaign's absolute Wannierisation gate

```text
conv_tol = 1.0e-10 angstrom^2
conv_window = 3
```

is justified for the rank-10, two-atom bulk-silicon route. It does not revise the
separate dimensionless disentanglement criterion, which the conduction-frozen
construction satisfied at iteration 531. It also does not accept any retained blocked
operator.

## Conclusion

The exact `1.0e-10 angstrom^2`/three-iteration pair is **not justified as a
calculation-specific scientific threshold**. It was selected from the Wannier90 3.1.0
numeric default and explicitly enabled, not derived from a bound on interpolation,
valley, curvature, effective-mass, or locality error. The native default
`conv_window = -1` means the native `conv_tol` value is not, by itself, a default active
three-iteration acceptance policy.

This conclusion does **not** justify accepting the present construction under a looser
gate. The 4000-iteration long-CG trajectory shows that the construction remains
optimizer-sensitive and nonstationary on scientifically consequential scales.

## Evidence

### Native semantics and origin

Wannier90 3.1.0 source sets:

- `conv_tol = 1.0e-10`;
- `conv_window = -1` unless explicitly changed; and
- convergence, when enabled with a window greater than one, by testing the absolute
  total-spread change against `conv_tol` throughout the window.

The campaign's first interface decision described `1.0e-10 angstrom^2` as a
first-candidate coordinate consistent with the numeric default while explicitly enabling
convergence. It did not connect that value to an observable error budget.

At the final spread scale `36.557416368 angstrom^2`, the campaign threshold corresponds
to a relative successive-spread change of about `2.74e-12`. Such a strict value is not
numerically impossible in double precision, but no retained evidence shows that this
particular scale is necessary for the target observables.

### Production-workflow comparison

The commit-pinned AiiDA Wannier90 workflow protocol uses per-atom tolerances:

| Profile | Per-atom tolerance | Two-atom comparison | Window | Iteration budget |
| --- | ---: | ---: | ---: | ---: |
| Moderate | `1.0e-7 angstrom^2` | `2.0e-7 angstrom^2` | 3 | 4000 |
| Precise | `1.0e-9 angstrom^2` | `2.0e-9 angstrom^2` | 6 | 40000 |

For this two-atom cell, the current campaign threshold is 2000 times tighter than the
moderate comparison and 20 times tighter than the precise comparison, while its window
is shorter than the precise window. These workflow values are external practice, not
proof of scientific adequacy for this calculation.

### Current 4000-iteration trajectory

The `num_cg_steps = 200`, `num_iter = 4000` occurrence provides a direct retrospective
comparison:

- its best three-iteration window had maximum absolute change `5.02e-8 angstrom^2`;
- five three-iteration windows met the moderate two-atom comparison;
- no window met the precise two-atom comparison or the campaign gate;
- the first moderate-comparison window began at iteration 1411;
- the reported gradient values over iterations 1411--1417 remained between about
  `0.0359` and `0.0729` in the native report rather than collapsing with the spread
  changes;
- 277 post-1000 iterations had absolute spread changes above `0.05 angstrom^2`; and
- the last such excursion occurred at iteration 3934.

A moderate-policy run would have stopped during a short plateau and would not have
observed the later excursions. Meeting that operational rule therefore cannot be used to
claim that this construction is robust.

### Observable sensitivity

The retained 500/1000 gauge-sensitivity analysis found source-mesh conduction spectra
within `1.43e-5 eV` but dense-grid conduction differences up to `1.433 eV`, near-edge
lowest-band differences up to `1.003 eV`, different diagnostic minima, and materially
different curvature-derived masses. This establishes that structural matrix checks and
source-mesh interpolation alone do not control the downstream observables.

No retained analysis maps a spread-change threshold—whether `1.0e-10`, `2.0e-9`, or
`2.0e-7 angstrom^2`—to an acceptable error in those observables.

## Policy options

### Retain `1.0e-10`, window 3

This is conservative and preserves all historical declarations, but its exact scale is
not calculation-justified. Retaining it would continue to conflate a native numeric
default with a scientific acceptance threshold.

### Adopt the moderate comparison

Using `2.0e-7 angstrom^2`, window 3 would classify the current trajectory as converged
near iteration 1413. The later excursions and existing gauge sensitivity make this
unsafe as a production eligibility rule for the component-operator and effective-mass
route. It may be suitable for exploratory screening only.

### Adopt the precise comparison as an operational gate

Using `2.0e-9 angstrom^2`, window 6 is externally grounded, remains stringent, and
avoids presenting the Wannier90 numeric default as calculation-derived. It is still only
an optimizer eligibility rule, not scientific validation. The current 4000-iteration
trajectory does not satisfy it, so adopting it would not change the present blocked
disposition.

## Recommendation

Prospectively separate two gates:

1. **Optimizer eligibility:** for the two-atom production route, use the AiiDA-precise-
   associated starting policy `conv_tol = 2.0e-9 angstrom^2`, `conv_window = 6`, with
   the exact atom-scaling convention recorded. Require the native convergence message
   and forbid exhaustion of the declared iteration budget. Treat this as an operational
   coordinate subject to later sensitivity evidence, not a universal physical constant.
2. **Scientific acceptance:** independently require the declared construction- and
   withheld-mesh tests for spectra, valley identity and location, edge energies,
   derivatives, curvature/effective masses, and locality/tail sensitivity. Passing the
   optimizer gate is necessary but not sufficient.

Do not rerun the current conduction-frozen construction solely with the precise
threshold: its retained trajectory proves that it would not have met that gate within
4000 iterations. Keep every existing occurrence under its historical `1.0e-10` policy
and retain its blocked disposition. Apply any revised policy only to a prospectively
declared target-space or projection construction.

## Decision recorded

The calculation's scientific owner accepted the recommended precise operational policy.
The prospective scope and non-retroactivity rules are recorded in
[`localization-convergence-policy-decision.md`](localization-convergence-policy-decision.md).
No calculator invocation is authorized or requested by this review or that decision.
