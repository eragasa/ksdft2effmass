# Response to continued referee review — revised manuscript

## Review disposition

- **Review outcome:** `CHANGES_REQUIRED`
- **Operator request:** `NONE`
- **Manuscript status:** framing accepted; two requested numerical-convention checks completed; complete independent reconstruction and public archival packaging remain blockers

The review is accepted. The scientific scope was not expanded. No QE, Wannier90,
optimization, valley search, Hamiltonian construction, or new band-edge calculation was
performed. The response adds a separate no-producer convention/inventory audit and
updates the manuscript to report exactly what that audit does and does not establish.

## Responses and checks

### 1. Silicon, Discussion, Conclusions, and appendices

**Disposition:** `NO_ACTION_REQUIRED`

The review finds that the revised results, Discussion, Conclusions, and appendices retain
the intended boundaries. The manuscript continues to distinguish exact theorem,
bounded numerical demonstration, source-relative reduction fidelity, DFT-parent
adequacy, and unsupported physical claims.

No additional scientific conclusion was added in response.

### 2. Six-valley mass conventions

**Disposition:** `NO_ACTION_REQUIRED` after independent convention audit

A new calculation-local audit consumes the authenticated comprehensive band-edge result
but imports no silicon producer. For all four models and all six signed-axis valleys it
independently recomputes:

- inversion consistency of the retained mass and inverse-mass tensors;
- principal masses from the retained mass tensor;
- single-valley DOS mass from `det(M)^(1/3)`;
- single-valley conductivity mass from `3 / trace(M^-1)`;
- the six-valley DOS convention `[sum_v sqrt(det(M_v))]^(2/3)`; and
- the equal-population conductivity convention
  `3 / trace[(1/6) sum_v M_v^(-1)]`.

The maximum absolute difference from the retained values is
`6.217248937900877e-15`. The audit confirms that the six-valley conductivity value is
formed from the average inverse-mass tensor, not from an average of scalar conductivity
masses.

This is a formula-level independent check. It does not independently reconstruct the
valley coordinates, Hessians, or Hamiltonians that supplied the tensors.

### 3. Finite-cyclic conversion ledger

**Disposition:** `NO_ACTION_REQUIRED` for the exact inventory rule; `MUST_FIX` for full coefficient reconstruction

The new audit independently enumerates the complete centered size-six cyclic inventory
and retains a machine-readable 216-record conversion ledger. It verifies the exact
production rule:

1. enumerate `{-3,-2,-1,0,1,2}^3` in first-axis-outer ordering;
2. remove every mode having at least one `-3 = -N/2` component; and
3. map every remaining mode identically to `{-2,-1,0,1,2}^3`.

The ledger records 91 removed negative-Nyquist-boundary modes and 125 retained ordinary
modes. It reproduces the retained ordering and FCC metric labels exactly and the
physical radii to `3.552713678800501e-15 angstrom`. Each retained record also binds the
reference and attacked per-state displacement powers already present in the source
result.

The historical result does not retain all 216 cyclic coefficient matrices. Therefore
the audit cannot independently reconstruct the removed-mode coefficient values or their
power. That remains part of the complete rank-10 Fourier reconstruction blocker.

### 4. Retained audit package

**Disposition:** `NO_ACTION_REQUIRED`

The package is retained at:

`calculations/Si/bulk/analysis/c6-b20-w21-independent-convention-audit/`

Key identities:

- audit result: `56c15bd597056cb1a607f2cd88100bb10da94af55d29f6606d868fb353d513cc`;
- conversion ledger: `36f4e06e58081f2b6e13e42b77bf6b5b6f45aa337c2983bbb02596b7c932e036`;
- manifest: `7b85ebd9d9cfd534e42519e491344ad561aa03c99bc71d3491ac9105142f79ec`.

The renderer is not involved. The audit uses direct NumPy arithmetic and integer
enumeration, authenticates both consumed result files, is deterministic, and refuses to
overwrite retained outputs.

### 5. Independent scientific reconstruction

**Disposition:** `MUST_FIX`

The convention audit narrows two technical uncertainties but does not promote the
silicon case study to independent publication evidence. The following remain pending:

1. reconstruct the rank-10 attacked and reference fields from authenticated source
   bytes;
2. independently perform the centered transform and recover all cyclic coefficient
   matrices;
3. reconstruct conversion-removed power, ordinary coefficients, shell classifications,
   and support-error curves;
4. reproduce the frozen fidelity ladder, valleys, Hessians, valence operators, and
   symmetry diagnostics; and
5. independently reconstruct the complete rank-two numerical endpoint.

### 6. Public reproduction archive

**Disposition:** `MUST_FIX` before submission

The repository records and hashes are not yet a public archive with a frozen executable
environment and independent reproduction entry point. Archive creation, publication,
DOI assignment, and release remain separately authorized actions and were not performed
for this response.
