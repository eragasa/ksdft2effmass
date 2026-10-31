# C6 disentanglement-budget extension decision

## Observed optimizer failure

The exact first `C6` localization occurrence retained the provider-eligible `C4`
construction controls, including `dis_num_iter = 2000`. Native Wannier90 returned zero
and completed, and Wannierisation converged at iteration 316. Disentanglement did not
converge: iteration 2000 ended at absolute fractional change `4.679e-8` against the
unchanged dimensionless `dis_conv_tol = 1.0e-10`. Wannier90 emitted its maximum-iteration
warning and explicit nonconvergence statement, and the ProjectKoios provider correctly
classified the output as ineligible.

This is an optimizer-budget failure. It is not a provider-eligible operator result, a
target-space adequacy result, a target-space inadequacy result, evidence of arithmetic
instability, or evidence of a global optimum.

## Bounded one-variable extension

The operator authorized preparation, but not execution, of one fresh successor changing
only:

```text
dis_num_iter = 4000
```

The final 201 reported disentanglement changes, iterations 1800--2000, decreased
monotonically. Log-linear fits over the final 100 and 200 values extrapolate the declared
tolerance crossing near iterations 2757 and 2802. Those extrapolations justify a bounded
test only; they are not completed convergence.

Retain exactly:

- the accepted structure, parent, Gamma-origin `6 x 6 x 6` construction mesh, and source
  order;
- 12 parent bands, rank 10, and non-spinorial character;
- outer window `[-5.85, 19.02] eV` and frozen window `[-5.85, 8.00] eV`;
- projections `Si:sp3` and `Si:l=0:r=2`;
- dimensionless `dis_conv_tol = 1.0e-10`, `dis_conv_window = 3`, and
  `dis_mix_ratio = 0.2`;
- `num_iter = 4000`, `conv_tol = 2.0e-9 angstrom^2`, and `conv_window = 6`;
- `precond = true`, `num_cg_steps = 200`, native-default dimensionless
  `trial_step = 2.0`, unset `fixed_step`, and disabled guiding centres;
- HR and unitary-matrix output; and
- the authenticated NNKP, EIG, AMN, and MMN bytes.

Start fresh. Do not consume the blocked checkpoint, HR file, unitary matrices, or any
other output from the failed occurrence. The iteration budget is an optimizer-eligibility
coordinate, not a spectral target-space coordinate. Nevertheless it is a real protocol
change and must remain explicit when comparing `C4` and `C6` optimization behavior.

## Stop and interpretation rules

Both native convergence messages remain mandatory. The maximum-iteration warning is
forbidden. Existing unitary, isometry, k-point, and Hamiltonian-Hermiticity gates remain
unchanged.

If the fresh 4000-step occurrence does not converge, stop automatic budget extensions.
Return the optimizer and target-space construction to separate review; do not proceed to
`C8` merely because `C6` lacks an eligible operator.

If it converges, the resulting operator is only provider-eligible. It must still be
characterized against the revealed 408-point development evidence under unchanged
criteria before any confirmation or mesh escalation. Wannier90 local optimization does
not certify a global minimum.

This decision authorizes preflight preparation only. It does not authorize
`wannier90.x`, a retry, checkpoint use, `C8`, `C12`, direct-parent confirmation,
component-operator construction, or Slater--Koster reduction.
