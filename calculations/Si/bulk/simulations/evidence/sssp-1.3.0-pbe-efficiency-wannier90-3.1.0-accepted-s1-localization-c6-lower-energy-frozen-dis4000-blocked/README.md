# Blocked accepted-S1 `C6` 4000-step localization evidence

This directory retains compact evidence for the separately authorized fresh Wannier90
3.1.0 occurrence that changed only `dis_num_iter` from 2000 to 4000. The request SHA-256
was `31075266d039efc37c70d6d55afdf3f5a4fc0d09719c971c0c2086e2d5f82fbc`; the exact
input SHA-256 was
`2ddfb1b51cfd476cc6444f8bfec8ae3ef229e882c2e6e5f1ee5bf94addd43e64`.
Exactly one fresh local process ran with a 600-second timeout, 64 MiB ceiling, zero
retries, and no checkpoint or failed-output consumption.

Native Wannier90 returned zero and completed in 359.302 seconds. Disentanglement
converged at iteration 3068 with final fractional change `-9.869e-11` against the
unchanged dimensionless `1.0e-10` criterion. Wannierisation did not satisfy its gate by
iteration 4000, so the ProjectKoios provider correctly rejected the output.

The final absolute spread change was `1.26e-5 angstrom^2`, 6300 times the unchanged
`2.0e-9 angstrom^2` tolerance. Across the whole Wannierisation trajectory, 14 individual
iterations met the single-step tolerance, but the longest consecutive run was two,
below the required six. The maximum absolute spread change after iteration 3000 was
`0.823 angstrom^2`; the late trajectory was not monotonic and contained large
excursions. These observations establish optimizer nonconvergence, not arithmetic
instability or target-space adequacy/inadequacy.

The external occurrence contains 30 files and 35,370,534 bytes. Its generated HR and
unitary artifacts are failure evidence and are not eligible operator inputs.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `68dd8441bc2f3b430a71e3abfa68780c13305a618e40dffebab697b7138cdad2` |
| consumed authorization | `edb18273b9d08ff94606f8897e563949f47f6ff6caca9dd2f56b378138ac1e47` |
| native WOUT | `f2a00f76574fc5715d1f412f35e36df8654cb9a52ffec0b460ace0099e27181b` |
| provider result | `134bcd63979ea1b9cf2b5128156932d42a8a8a01f9e351c0f6a4f7bc39c6e1ae` |
| trajectory analysis | `bdb9e865a2cbdf81e079cd2b6b9563777e34b0a32d08a5acebba0d996c953d39` |
| campaign result | `96065b18d11e7425b3ce6c9737a787d499b45d3822a4f59797df99f588290857` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000-v1`.

## Disposition

This is an optimizer-Wannierisation-convergence failure. There is no provider-eligible
`C6` operator. Under the prospective stop rule, no automatic further iteration-budget
extension or `C8` escalation follows. Any changed optimizer, target space, or mesh is a
new scientific decision. Direct-parent confirmation, component-operator construction,
and Slater--Koster reduction remain blocked.
