# Proposed bounded Wannier90 convergence study

**Status:** Authorized and performed once; stopped on the declared low-pair
nonconvergence condition.

**Applicable task:** `research-monograph.exercises.periodic-1d`

**Decision basis:** Option B at checkpoint
`RM-PERIODIC-1D-W90-NONCONVERGENCE-HC03` requires one justified change, a
resource estimate, explicit acceptance criteria, and a new protected-execution
checkpoint before any further invocation.

## 1. Why another calculation would be scientifically useful

The completed 500-iteration Wannier90 runs establish that the synthetic
interface is accepted, the exported frames are unitary to their printed
precision, and common-frame operator comparisons are consistent. They do not
establish that Wannier90 reached its spread minimum. Consequently, their centers,
spreads, and gauge-dependent hopping locality cannot be treated as converged
independent localization results.

A converged run would permit conclusions about the Wannier90-selected gauge for
this exact synthetic parent. It would not validate silicon, establish
transferability, or constitute uncertainty quantification.

## 2. Evidence from the stopped iteration histories

Both existing runs were still descending at iteration 500 rather than visibly
stagnating:

| Group | Spread at iteration 400 | Spread at iteration 500 | Last-step spread change | Last RMS gradient |
|---|---:|---:|---:|---:|
| Bands 0--1 | 0.4082127695 | 0.4054710414 | $-1.27\times10^{-5}$ | 0.0131796804 |
| Bands 2--3 | 3.6893439532 | 3.6847245612 | $-2.60\times10^{-5}$ | 0.0185103310 |

Over iterations 401--500, the spreads decreased by approximately
$2.69\times10^{-3}$ and $4.53\times10^{-3}$, respectively. The observed
last-step changes remain about seven orders of magnitude larger than the frozen
`conv_tol = 1.0d-12` rule. The histories therefore support increasing the
iteration ceiling; they do not support weakening the convergence criterion or
changing the localization objective.

## 3. Sole proposed numerical change

Change only:

```text
num_iter = 5000
```

The current value is 500. `num_iter` is a maximum: Wannier90 may stop earlier if
its unchanged `conv_tol = 1.0d-12` and `conv_window = 5` rule is satisfied.

The following remain fixed:

- cosine parent and all parent-plane-wave data;
- $128\times1\times1$ reciprocal mesh;
- retained bands 0--1 and 2--3;
- two Wannier functions per seed;
- identity trial projections;
- `.eig`, `.amn`, and reciprocal-overlap conventions;
- `search_shells = 130`;
- Wannier90 3.1.0 executable and documented identity;
- localization objective and all other Wannier90 settings;
- common-frame alignment and finite-range comparison definitions; and
- prohibition on Quantum ESPRESSO execution.

Each seed would be generated in a new external directory and run from a fresh
state. Existing native outputs would not be overwritten or deleted.

## 4. Proposed bounded execution

For each seed, in order:

1. deterministically regenerate the frozen interface with only the changed
   iteration ceiling;
2. run preprocessing once;
3. generate `.mmn` from that exact `.nnkp` neighbor list;
4. run localization once with one local process; and
5. stop after success, executable failure, resource-limit termination, or the
   5000-iteration ceiling.

No failed stage would be retried automatically. If either seed reaches the new
iteration ceiling without convergence, retain that failure and return to the
human decision boundary.

## 5. Resource estimate and hard envelope

The 500-iteration localization stages required 0.49 and 0.43 seconds and about
24 MB maximum resident memory. Their `.wout` files are about 315 kB each. A
linear estimate for 5000 iterations is approximately five seconds and 3.2 MB of
`.wout` text per seed. Startup, filesystem, and line-search variation make this
an estimate rather than a guarantee.

The proposed hard envelope remains:

- one local process and `OMP_NUM_THREADS=1`;
- five minutes wall time per invocation;
- 512 MiB maximum resident memory per invocation; and
- 50 MiB total output per seed.

These limits are intentionally much larger than the estimate but unchanged from
the previous authorization.

## 6. Acceptance and failure criteria

A seed is **localization-converged** only if Wannier90 itself reports satisfaction
of the unchanged spread criterion before or at iteration 5000. Exit code zero
alone is insufficient.

For a converged seed, the retained comparison must also verify:

- exported unitary-matrix defect no greater than $10^{-8}$;
- pointwise common-frame defect no greater than $10^{-8}$;
- aligned represented-operator defect no greater than $10^{-8}E_G$;
- represented eigenvalue defect no greater than $10^{-8}E_G$; and
- strictly decreasing finite-range eigenvalue error over the retained ranges.

Centers, spreads, hopping blocks, and `hr.dat` serialization errors would be
reported whether or not the direct polar gauge gives the same centers or
locality. Such differences would be interpreted only after common-frame
alignment and would not by themselves invalidate either gauge.

The convergence study passes only if **both** seeds satisfy the Wannier90
convergence rule and all software-verification checks above. Otherwise it is a
retained bounded failure. No tolerance weakening, setting change, or additional
retry is permitted merely to obtain a pass.

## 7. Proposed claim boundary

A passing study would establish a converged Wannier90 localization result for the
identified one-dimensional synthetic parent and fixed interface. It would not
establish semiconductor validation, transferability to silicon, scientific
validation, uncertainty quantification, or production readiness.

## 8. Executed disposition

Checkpoint `RM-PERIODIC-1D-W90-CONVERGENCE-HC04` authorized option A. Both fresh
preprocessing stages completed, and the regenerated `.eig`, `.amn`, and `.mmn`
files are byte-identical to the 500-iteration interfaces. The low-pair
localization then reached iteration 5000 without satisfying the unchanged
convergence rule. Its last spread change was
$-3.24\times10^{-5}$, its last RMS gradient was 0.02098, and its final spread
was 0.362284855 cell$^2$. The higher-pair localization was not invoked because
the declared stop condition had been reached.

The attempted shell virtual-memory guard was not accepted by the operating
system, although measured maximum resident memory was 23,953,408 bytes, well
below the 512 MiB bound. This procedural limitation and all native-output
identities are retained in `wannier90-convergence-attempt.json`.

The convergence study therefore failed its acceptance rule. Increasing the
iteration ceiling alone is not an adequate remedy for the low-pair optimizer
behavior, and no further run is authorized.
