# Appendix D numerical-experiment protocol

## Evidence status and authority

This protocol governs a **calculated illustrative numerical experiment**. It
operationalizes Appendix D of the research monograph without replacing its
mathematical definitions. It does not define a public software API and does not
provide semiconductor evidence, scientific validation, or uncertainty
quantification.

The experiment addresses the appendix's central question: after a common
numerical state space has made subtraction possible, what additional choices are
required before the result can be interpreted as a physical potential?

## Declared continuum model

The continuum reference is the Dirichlet realization

$$
\hat H_{\mathrm{box}}
=-\frac{\hbar^2}{2m}\frac{d^2}{dx^2},
\qquad
\mathcal D(\hat H_{\mathrm{box}})=H^2(0,L)\cap H_0^1(0,L),
$$

on $L^2(0,L)$, with $\psi(0)=\psi(L)=0$. Its eigenvalues are

$$
E_n=\frac{\hbar^2\pi^2n^2}{2mL^2}.
$$

The interior physical potential is zero. Confinement belongs to the operator
domain rather than to a finite-valued interior multiplication potential.

## Finite realization and state spaces

For $N$ interior points and $h=L/(N+1)$, the numerical state space is
$\mathcal V_h\cong\mathbb R^N$. The second-order Dirichlet matrix is

$$
(\mathbf H_h)_{jj}=\frac{\hbar^2}{mh^2},
\qquad
(\mathbf H_h)_{j,j\pm1}=-\frac{\hbar^2}{2mh^2}.
$$

The retained coordinate space is $\mathbb R^M$. If
$\boldsymbol\Phi_M\in\mathbb R^{N\times M}$ contains the lowest orthonormal
discrete eigenvectors, then

$$
\mathbf P_M=\boldsymbol\Phi_M\boldsymbol\Phi_M^T,
\qquad
\mathbf H_h^{(P_M)}=\mathbf P_M\mathbf H_h\mathbf P_M,
\qquad
\mathbf H_{\mathrm{red}}=
\boldsymbol\Phi_M^T\mathbf H_h\boldsymbol\Phi_M.
$$

The embedded $N\times N$ matrix and retained-coordinate $M\times M$ matrix are
not subtracted without the declared embedding.

## Three residual constructions

The retained $N=8$, $M=3$ calculation must distinguish:

1. **Consistently compressed physical potential**
   $$
   \mathbf P_M\mathbf H_h\mathbf P_M-
   \mathbf P_M\mathbf T_{\mathrm D,h}\mathbf P_M=\mathbf0.
   $$
2. **Unmatched compression**
   $$
   \mathbf P_M\mathbf H_h\mathbf P_M-\mathbf T_{\mathrm D,h}
   =-\mathbf Q_M\mathbf T_{\mathrm D,h}\mathbf Q_M,
   \qquad \mathbf Q_M=\mathbf I-\mathbf P_M.
   $$
   This is the discarded kinetic sector, not a physical potential.
3. **Boundary-realization difference**
   $$
   \mathbf H_{\mathrm D,h}-\mathbf H_{\mathrm{cyclic},h}.
   $$
   The cyclic closure is a declared finite-space comparison reference. The
   result is not a representation-independent continuum potential.

Independent verification checks the closed-form finite-difference spectrum,
projector identities, embeddings, zero consistent residual, discarded-sector
identity, and the two corner couplings of the boundary residual.

## Convergence studies retained as supporting evidence

All sweeps use $N=8,16,32,64,128,256$ where applicable.

- Fixed continuum modes $n=1,2,3$ test second-order eigenvalue convergence.
- Full spectra test nonuniform finite-difference dispersion as $n/(N+1)$ is
  held approximately fixed.
- Fixed higher modes enter when available: $n=8$ from $N=8$, $n=16$ from
  $N=16$, and $n=32$ from $N=32$.
- Nodal sine-vector overlap and $HV-V\Lambda$ residuals diagnose the discrete
  eigensolver. They do not measure continuum interpolation error.

These studies establish numerical behavior of the declared discretization.
They are not the primary identifiability argument and do not establish uniform
spectral or operator convergence.

## Norm studies retained as supporting evidence

Raw and same-grid-normalized Frobenius, spectral, and maximum-entry norms are
recorded. Raw norms are not compared as operator-convergence metrics across
changing dimensions. Same-grid ratios answer different questions:

- Frobenius ratios measure aggregate matrix magnitude;
- spectral ratios measure worst-case Euclidean action; and
- maximum-entry ratios are basis-dependent local diagnostics.

A small value in one norm does not assign a physical category to a residual.
The reference operator and admissible model class remain prior inputs.

## Executable identifiability demonstration

On the declared $M=3$ retained coordinate space, the experiment records two
distinct exact decompositions of the same $\mathbf H_{\mathrm{red}}$:

$$
\mathbf H_{\mathrm{red}}=
\mathbf T_{\mathrm D,red}+\mathbf0
$$

and, for a declared illustrative Hermitian shift $\mathbf K$,

$$
\mathbf H_{\mathrm{red}}=
(\mathbf T_{\mathrm D,red}-\mathbf K)+\mathbf K.
$$

The second equality is algebraically valid but carries no physical assignment.
It demonstrates that the reduced Hamiltonian alone does not identify a unique
kinetic--potential decomposition.

The same illustrative $\mathbf K$ is fitted in Frobenius norm to four nested
model classes: scalar identity, diagonal in the retained basis, real symmetric
tridiagonal, and arbitrary real symmetric. The unrestricted class fits exactly;
restricted classes leave different unexplained residuals. This demonstrates why
an admissible model class must be declared before a potential fit is
scientifically informative.

## Traceability to Appendix D

| Appendix D requirement | Retained evidence |
|---|---|
| Continuum operator and domain | This protocol and Appendix D |
| Second-order finite realization | `input.json`, `run_experiment.py`, `result.json` |
| Full and retained spaces, projection and embedding | `result.json`, `verify_result.py` |
| Three inequivalent residuals | `result.json`, `residual-matrices.png` |
| Fixed-mode numerical convergence | `convergence-result.json`, `convergence-series.png` |
| High-index dispersion and eigenpair quality | `eigenpair-sweep-result.json`, higher-eigenpair graphics |
| Norm dependence | `norm-sweep-result.json`, norm graphics |
| Decomposition nonuniqueness | `identifiability-result.json` |
| Dependence on admissible model class | `identifiability-model-classes.png` and verifier |
| Integrated provisional narrative | `appendix-d-draft-report.md`, `appendix-d-draft.tex` |
| Reproducibility and identities | reproduction scripts, verification scripts, `SHA256SUMS` |

## Acceptance boundary

Passing the retained verifiers establishes agreement with the stated finite
mathematics and analytical oracles under binary64 arithmetic. It does not select
a physically correct alternative kinetic reference, validate any fitted model
class, establish a continuum boundary potential, or transfer conclusions to a
material system.
