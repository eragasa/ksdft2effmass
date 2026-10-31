# Blocked accepted-S1 `C6` localization evidence

This directory retains compact evidence for the separately authorized `C6` Wannier90
3.1.0 localization occurrence. The request SHA-256 was
`7ed68715f0376b61999610343fa0833d7c04795280e9690088658eed8b468431`; the exact
input SHA-256 was
`0d5b693972309245f0ce04fca42e8806a8c33017af7d0e184424dec0b429694c`.
Exactly one local process ran with a 600-second timeout, 64 MiB ceiling, and zero
retries.

Native Wannier90 returned zero and completed in 197.703 seconds, but the provider
correctly rejected the output because the declared disentanglement convergence gate was
not met. At iteration 2000, the absolute fractional change was `4.679e-8`, which is
467.9 times the unchanged dimensionless `1.0e-10` tolerance. Wannier90 printed both the
maximum-disentanglement-iteration warning and the explicit statement that
Disentanglement convergence criteria were not satisfied. Subsequent Wannierisation
converged at iteration 316, but that does not repair the unconverged input subspace.

The final 201 disentanglement changes, iterations 1800--2000, decrease monotonically.
Log-linear fits to the last 100 and 200 values extrapolate tolerance crossings near
iterations 2757 and 2802. These are diagnostic extrapolations, not completed convergence,
a global-minimum claim, or authority for a retry.

The external occurrence contains 30 files and 30,801,194 bytes. Its generated HR and
unitary artifacts are retained as failure evidence and are not eligible operator inputs.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `e944b9e2f268cbd049d343ba65be001cf645b0496d8285a208111beacf12fe50` |
| consumed authorization | `5a8dd877bc2a002afb9a1cfe710ffcf82fea3b9d7f10c00f80dafe4c82074f05` |
| native WOUT | `dd8599308ae3bef123a15bbc980ece0c7d668ee92392f738aa8b4a9021413998` |
| provider result | `06c02ced0bf83c22c70e97dec7c3c2437f5cd3737063e44979086b4951b11ace` |
| trajectory analysis | `971249965dc13b6c3aee779f7196068493ceedd46f45056ce43a998ed19fb4dd` |
| campaign result | `afbdf5c5cdb2afa602e4235372c01d53cf03b0b4f1174ec37549a0bfe098615a` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis2000-v1`.

## Disposition

This is an optimizer-disentanglement-convergence failure, not evidence of arithmetic
instability, target-space adequacy, or target-space inadequacy. There is no
provider-eligible `C6` operator. No retry, iteration-budget extension, `C8`, `C12`,
direct-parent confirmation, component-operator construction, or Slater--Koster reduction
is authorized.
