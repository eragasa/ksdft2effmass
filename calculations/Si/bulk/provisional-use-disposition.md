# Provisional downstream-use disposition

**Recorded:** 2026-10-22

## Decision

C48/K8 (48/192 Ry and a shifted $8\times8\times8$ mesh) may be used for
**provisional downstream development and exploratory analysis**.

The recurring IEEE report is retained as a known numerical-runtime limitation. It is
not, by itself, a blanket blocker on planning, software development, verified-data
analysis, valley-tracking development, Wannier-interface development, or other work
that is explicitly labelled provisional.

## Evidence basis

- All nine SCF and nine linked NSCF invocations exited zero and emitted `JOB DONE.`.
- The compact result audit found the retained matrix complete and internally
  consistent.
- Adjacent finite-setting comparisons support the recorded provisional C48/K8 choice.
- Instrumented builds deliberately converted normally masked IEEE flags into fatal
  traps. Those traps localize possible flag sources but do not establish corruption of
  the successful retained calculations.
- One source was external OpenCL discovery during startup. A second reproducible
  divide-by-zero occurred below `ZHEGVX` during initial-wavefunction subspace
  diagonalization. Its effect on final retained observables remains unmeasured.

## Still pending before production or publication-grade acceptance

1. a bounded comparison using an independently identified established QE/toolchain
   path;
2. comparison of physical observables and numerical residuals rather than stderr alone;
3. the mixed cutoff--mesh interaction check implied by C48/K8;
4. acceptance of the production lattice and complete parent identity; and
5. all later valley, effective-mass, Wannier, joint-admissibility, withheld, and
   sensitivity gates.

## Nonclaims and authority boundary

This decision does not establish infinite-basis convergence, accept a production
parent, validate the pseudopotential or silicon Hamiltonian, qualify a Wannier model,
or authorize publication-grade claims.

It also does not authorize any new Quantum ESPRESSO or Wannier90 invocation. Each new
protected execution still requires a separately bounded authorization.

## Historical-record boundary

The checksum- and provenance-bound historical disposition under
`calculations/bulk-silicon/production-convergence-preflight/` remains unchanged. That
record captured the earlier conservative `block_pending_diagnosis` decision. This file
is the successor planning disposition for the canonical `calculations/Si/bulk/` owner;
it does not rewrite or relabel the historical evidence.
