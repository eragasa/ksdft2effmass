# Defect-2D Stage A null-and-folding report

## Status and scope

**Human-accepted calculated result:** one authorized local synthetic Stage A
execution produced `stage-a-result.json`, and checkpoint
`RM-IMPURITY-DEFECT-2D-STAGE-A-ACCEPTANCE-HC02` accepts that exact evidence
boundary. The result is numerical-verification evidence for the frozen
represented scalar operator only. It is not DFT, silicon or dopant
validation, material transfer, scientific validation, uncertainty
quantification, a theorem, or authorization for Stages B--E.

The execution used authorization
`RM-IMPURITY-DEFECT-2D-STAGE-A-EXECUTION-HC01`, the accepted periodic-2D scalar
parent at $\lambda_{xy}=0$, the exact $6\times6$ and $8\times8$ shape/twist
Cartesian product, and no changed tolerance, retry, network access, external
executable, or overwritten output.

## Folding and null extraction

All eight frozen cases passed the declared thresholds. Across those cases:

| Diagnostic | Maximum | Threshold |
|---|---:|---:|
| folding unitarity maximum-entry defect | $1.2794\times10^{-15}$ | $5\times10^{-12}$ |
| Hermiticity maximum-entry defect | $4.9304\times10^{-32}$ | $10^{-11}$ |
| folded off-block maximum entry | $2.5837\times10^{-16}$ | $10^{-11}$ |
| primitive-block maximum-entry defect | $2.5837\times10^{-16}$ | $10^{-11}$ |
| eigenvalue maximum absolute defect | $2.2204\times10^{-16}E_G$ | $10^{-11}E_G$ |
| recovered-null Frobenius defect | $2.1788\times10^{-16}E_G$ | $10^{-11}E_G$ |
| recovered-null maximum-entry defect | $5.7220\times10^{-17}E_G$ | $10^{-11}E_G$ |
| attack-transform unitarity defect | $2.2204\times10^{-16}$ | $10^{-11}$ |

The separately implemented verifier reconstructed every retained metric through
Kronecker seam/Fourier matrices. It reported reconstruction `PASS`, numerical
criteria `PASS`, and a maximum retained-versus-reconstructed metric difference
of $3.473\times10^{-16}$.

These values are floating-point residuals for this finite represented problem.
They do not estimate parent-model, material, finite-area, model-reduction, or
physical uncertainty.

## Seam-phase oracle

The production seam assembler returned the three frozen controls at twist
$\phi=0.37$ turns:

- noncrossing $0\rightarrow1$: $1$;
- positive crossing $5\rightarrow0$: $-0.6845471059+0.7289686274i$; and
- negative crossing $0\rightarrow5$: $-0.6845471059-0.7289686274i$.

The independent verifier reproduced these values as $1$,
$\exp(+2\pi i\phi)$, and $\exp(-2\pi i\phi)$, respectively. This verifies the
frozen Stage A single-crossing sign convention; it is not a general theorem for
arbitrary displacement or multiple wraps.

## Structured incompatible controls

All four adverse controls stopped before residual formation, with `residual`
retained as null:

| Control | Independently reproduced issue code |
|---|---|
| incorrect supercell geometry | `DEFECT_2D.GEOMETRY_MISMATCH` |
| incorrect boundary phase | `DEFECT_2D.BOUNDARY_PHASE_MISMATCH` |
| lost site correspondence | `DEFECT_2D.SITE_MAP_UNRESOLVED` |
| unknown energy reference | `DEFECT_2D.ENERGY_REFERENCE_UNKNOWN` |

These stops establish only that the frozen represented incompatibilities are
recognized before subtraction. They do not establish the adequacy of any defect
model.

## Execution and reproduction

The measured local process time was 0.16 seconds. `/usr/bin/time -l` reported a
maximum resident-set size of 38,453,248 bytes (about 36.7 MiB), below the bound
of 2 GiB. These are measurements of this invocation on the local machine, not
portable performance guarantees.

From the repository root, the authorized command was:

```bash
python/.venv/bin/python \
  calculations/research-monograph/impurity-defect-2d/run_stage_a.py \
  --design calculations/research-monograph/impurity-defect-2d/study-design.json \
  --execution-authorization \
  calculations/research-monograph/impurity-defect-2d/stage-a-execution-authorization.json \
  --repository-root /Users/eugene/repos/ksdft2effmass \
  --output \
  calculations/research-monograph/impurity-defect-2d/stage-a-result.json
```

The retained result is immutable under the runner's no-overwrite rule. The
independent verification command is:

```bash
python/.venv/bin/python \
  calculations/research-monograph/impurity-defect-2d/verify_stage_a.py \
  --result \
  calculations/research-monograph/impurity-defect-2d/stage-a-result.json \
  --repository-root /Users/eugene/repos/ksdft2effmass
```

The checksum catalog identifies the exact authorization, checkpoint, design,
runner, verifier, parent-derived result, logs, tests, and report.

## Limitations and disposition

Human acceptance applies only to this bounded Stage A evidence. Stage A contains
no planted defect and therefore does not test model-class
selection, blind alignment, $D_4$/$D_2$ covariance of defects, area or shape
convergence, a twist mesh, bound-state observables, composite orbital
alignment, or degenerate projectors. Parent truncation remains inherited and
separate. Passing Stage A does not activate Stage B; any successor requires a
separate explicit human decision.
