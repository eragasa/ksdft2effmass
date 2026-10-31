# Accepted-S1 `C6` disentanglement-budget-extension preflight

This directory retains the authorized no-execution preparation for one fresh Wannier90
3.1.0 optimizer-eligibility occurrence. Relative to the blocked 2000-step `C6`
occurrence, the exact native input changes only:

```text
dis_num_iter = 2000  ->  4000
```

A bytewise diff confirms that this is the only WIN change. The fresh occurrence retains
the exact Gamma-origin `6 x 6 x 6` mesh, 12 bands, rank 10, projections, windows,
tolerances, mixing, preconditioner, CG reset interval, line-search defaults,
Wannierisation controls, and authenticated NNKP/EIG/AMN/MMN bytes. It consumes no
checkpoint or failed output.

The blocked predecessor completed natively but ended iteration 2000 at absolute
fractional change `4.679e-8` against the unchanged dimensionless `1.0e-10` criterion.
Its final 201 changes decreased monotonically; final-100 and final-200 log-linear fits
extrapolate crossings near iterations 2757 and 2802. These diagnostics support one
bounded test only and are not convergence evidence.

The maintained ProjectKoios localization input preparer authenticated the 216-point,
12-band, rank-10, eight-neighbor interface. No proposed occurrence root was created, no
failed checkpoint was consumed, and no calculator was invoked.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000-v1`
- command: `wannier90.x silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- one process, one invocation, zero retries
- timeout: 600 seconds
- retained-byte ceiling: 64 MiB

Eligibility requires return code zero, native completion, converged disentanglement,
converged Wannierisation, no maximum-iteration warning, declared HR and unitary outputs,
unitary/isometry residuals at most `1e-8`, k-point agreement within `1e-10`, and
Hamiltonian Hermiticity residual at most `1e-8 eV`. Passing establishes provider
eligibility only, not a global optimum or scientific adequacy.

If this occurrence fails, the protocol forbids another automatic budget extension or
`C8` escalation.

## Identities

| Artifact | SHA-256 |
|---|---|
| prepared `silicon.win` | `2ddfb1b51cfd476cc6444f8bfec8ae3ef229e882c2e6e5f1ee5bf94addd43e64` |
| localization input manifest | `d285df27cf085c61112bc9c0d79c4056b710708e379359ecb838b793272aee48` |
| input transformation | `f79ed6411c3aa1eac9f1eda0d68e224632b02761b0aa27d296340599623cb36c` |
| campaign preflight | `11fe14f4b7b851fa67247f8e5d1fcf7db47d2ab6fe1201a40b18b970111cf844` |
| authorization request | `31075266d039efc37c70d6d55afdf3f5a4fc0d09719c971c0c2086e2d5f82fbc` |
| budget-extension decision | `c0dc41bce705c9637e88bbf607f6db8599cbae564bbc8d46182dbf8277b8c181` |
| amended research protocol | `36ac947bb316af52675a038f0950a6bdacd7a9d13dbb5770812b4cc499df33eb` |

## Authorization boundary

Status: **authorization consumed by one occurrence**.

The immutable request retains its original `authorization_granted: false`; the separate
consumed-authorization record is retained with the occurrence. Disentanglement converged
at iteration 3068, but Wannierisation did not meet its six-step spread-change gate by
iteration 4000, so the provider rejected the output. Evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis4000-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis4000-blocked/).
The prospective stop rule now applies: no automatic retry, further budget extension, or
`C8` escalation follows. `C12`, confirmation, component-operator construction, and
Slater--Koster reduction remain unauthorized.
