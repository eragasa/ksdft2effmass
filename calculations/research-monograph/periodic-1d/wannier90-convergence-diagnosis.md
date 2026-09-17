# Read-only diagnosis of Wannier90 convergence failure

**Status:** Diagnosis completed; the proposed remedy was subsequently authorized
and both preconditioned runs converged.

**Applicable task:** `research-monograph.exercises.periodic-1d`

**Authority:** Option B at checkpoint
`RM-PERIODIC-1D-W90-CONVERGENCE-FAILURE-HC05` authorizes read-only diagnosis
and one redesigned proposal. It does not authorize another Wannier90 invocation.

## 1. Question

Why did the synthetic low-pair Wannier90 calculation fail to satisfy its spread
convergence rule after 5000 iterations, and what is the smallest defensible next
change?

The diagnosis separates four possible causes: the interface formulation, the
spread objective, the optimizer, and the convergence rule.

## 2. Retained observations

The 5000-iteration run used byte-identical `.eig`, `.amn`, and `.mmn` interfaces
to the 500-iteration run. Its total spread decreased monotonically at every
recorded step:

| Iteration | Spread / cell$^2$ | Absolute last-step change | RMS gradient |
|---:|---:|---:|---:|
| 0 | 64.4193126647 | 64.4 | 0 |
| 500 | 0.4054710414 | $1.27\times10^{-5}$ | 0.01318 |
| 750 | 0.4046524258 | $4.80\times10^{-7}$ | 0.00235 |
| 985 | 0.4046154188 | $7.42\times10^{-8}$ | 0.00135 |
| 1000 | 0.4046140795 | $8.04\times10^{-8}$ | 0.00105 |
| 2000 | 0.4043583286 | $6.19\times10^{-7}$ | 0.00290 |
| 3000 | 0.4025569708 | $3.30\times10^{-6}$ | 0.00694 |
| 4000 | 0.3918857111 | $1.85\times10^{-5}$ | 0.01587 |
| 5000 | 0.3622848552 | $3.24\times10^{-5}$ | 0.02098 |

The gauge-invariant contribution remained 0.336987054 cell$^2$. The
gauge-dependent contribution therefore fell from about 64.0823 cell$^2$ to
0.02530 cell$^2$. The centers moved from approximately
$\{+0.4972,-0.4972\}a$ at iteration 500 to
$\{+0.35391,-0.35387\}a$ at iteration 5000. The direct Wilson-loop phases
correspond to $\{+0.31602,-0.31602\}a$, but the remaining difference cannot be
interpreted until the Wannier90 optimization converges.

These facts show continuing descent rather than numerical divergence or a
stationary converged result. They do not prove that the direct Wilson gauge and
the eventual Wannier90 gauge must have identical spreads or matrix blocks.

## 3. Interface formulation

Wannier90 reports that shells 1 and 129 satisfy its three-dimensional B1
completeness relation for the $128\times1\times1$ embedding. The selected set
contains two nearest $x$ neighbors with weight 207.480454 cell$^2$ and eight
diagonal $x$--transverse neighbors with weight 0.00633257 cell$^2$. The
synthetic `.mmn` convention applies the same active-direction overlap to those
diagonal neighbors and a unit transverse form factor.

This is an artificial embedding, not a material-derived transverse wavefunction.
It remains a claim limitation. However, it is not identified as the immediate
cause of the observed failure: preprocessing satisfies B1, the fixed interface
is consumed without error, the spread is bounded and strictly decreases, and
the same overlap data support unitary common-frame checks. Altering the mesh or
transverse form factor would change the defined comparison rather than repair a
demonstrated file-format defect.

The identity `.amn` matrices initialize Wannier90 in the raw eigenvector gauge.
The resulting initial spread of 64.4193 cell$^2$ shows that this is a poor
localization starting point. Replacing it with a gauge constructed from the
direct answer would compromise the intended independence of the localization
comparison. A material-like trial-orbital redesign is possible but would add a
new modeling choice and is not the smallest first remedy.

## 4. Objective and convergence rule

The objective is not observed to be ill-defined: it remains finite and decreases
monotonically. Nor is the declared `conv_tol = 1.0d-12` the immediate blocker.
The smallest recorded late-stage spread change, $7.42\times10^{-8}$ near
iteration 985, is still more than 700 times Wannier90's default
$10^{-10}$ tolerance and more than $7\times10^4$ times the declared tolerance.
At iteration 5000 the discrepancy is larger. Weakening the tolerance enough to
accept the retained trajectory would label a visibly evolving gauge as
converged and is therefore rejected.

Increasing only `num_iter` is also rejected as the next remedy. It was already
tested by a factor of ten without meeting the convergence rule, and the final
RMS gradient is larger than it was near iteration 1000. Another ceiling increase
would provide no controlled evidence that the same optimizer will terminate.

## 5. Optimizer diagnosis

Wannier90 3.1.0 used its defaults:

- Fletcher--Reeves conjugate gradients;
- reset after five CG steps;
- parabolic line search with `trial_step = 2.0`; and
- `precond = false`.

The source implements an optional real-space preconditioner that filters the
spread gradient by $1/(1+R^2/\alpha)$. The Wannier90 3.1.0 user guide states that
this option is intended to speed slow spread minimization, especially on fine
reciprocal grids. The present 128-point active-direction mesh and the long,
monotone, nonstationary trajectory match that documented use case.

This supports an **optimizer-conditioning diagnosis**, with the poor identity
initial gauge as a contributing factor. It does not establish that
preconditioning will converge; that remains a prediction to be tested under a
new protected checkpoint.

## 6. One bounded remedy

Change only:

```text
precond = true
```

Keep `num_iter = 5000`, `conv_tol = 1.0d-12`, `conv_window = 5`,
`num_cg_steps = 5`, and `trial_step = 2.0`. Preserve the parent, mesh, bands,
projections, overlap convention, shell search, executable, and comparison
metrics.

This remedy is preferred over a looser tolerance, another iteration-only
extension, answer-derived projections, or an embedding change because it
addresses the documented slow-optimization mode without changing the objective,
accepted convergence rule, or represented physical parent.

## 7. Proposed execution and resource controls

If separately authorized:

1. generate a new external run directory with only `precond = true` added;
2. verify `.eig`, `.amn`, and `.mmn` identity against the retained interface;
3. preprocess both seeds once;
4. localize `low_pair` once;
5. localize `higher_pair` once only if `low_pair` satisfies the unchanged
   convergence rule; and
6. stop without retry on executable failure, resource termination, or
   nonconvergence at iteration 5000.

The existing one-process, five-minute, 512 MiB, and 50 MiB-per-seed envelopes
remain appropriate. Because the prior shell virtual-memory limit was rejected by
macOS, a new execution must use a supervising process that enforces the wall-time
and output limits, polls resident memory, and terminates the child if observed
RSS exceeds 512 MiB. The monitor and its observations must be retained. Expected
resource use remains seconds, tens of MiB of RSS, and a few MiB of text per seed.

## 8. Acceptance rule and claim boundary

Both seeds must have Wannier90 itself report satisfaction of the unchanged
convergence rule before or at iteration 5000. Exit code zero is insufficient.
Each converged output must additionally pass the retained unitary, common-frame,
represented-operator, eigenvalue, and decreasing finite-range-error checks.
Failure of either seed ends the study without automatic retry.

A pass would establish converged Wannier90 localization only for this identified
synthetic parent and interface. It would not establish agreement of all
gauge-dependent quantities with the direct polar construction, semiconductor
validation, transferability to silicon, scientific validation, uncertainty
quantification, or production readiness.

## 9. Read-only provenance

Checkpoint `RM-PERIODIC-1D-W90-PRECONDITIONED-HC06` subsequently authorized the
single-setting remedy for both seeds. With `precond = true`, `low_pair`
converged at iteration 69 and `higher_pair` at iteration 4176 under the unchanged
criterion. The result supports the optimizer-conditioning diagnosis for this
interface; it does not prove that preconditioning is universally required.

The diagnosis used the retained low-pair `.wout` identity
`093b68dcd95fa6f86a41a2f6823d5debbd1df61cb3f967af9a8111a387a9bf41`
and the local Wannier90 3.1.0 sources:

- `wannierise.F90` SHA-256
  `61ca8e53936e53477120d5e1bf670737b497c8b1553b94a7d7837b5caeb21297`;
- `parameters.F90` SHA-256
  `19db3643a6bda79a656da56fc92c3065dd98b51c73bfdcd8b4325b5d892014a2`;
- user-guide `parameters.tex` SHA-256
  `ee1222eda51ddb73e9558b979e49bd2f2b27643d79c9e0d53460275d688db06e`.
