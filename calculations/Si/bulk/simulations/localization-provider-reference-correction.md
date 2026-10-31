# Localization provider reference-space correction

## Scope

This record disposes the initial ProjectKoios provider rejection of the fresh
`C6-B20-W21` AiiDA-precise localization occurrence. It changes no calculator input,
output, tolerance, optimizer setting, target space, or authorization boundary.

## Finding

The initial provider compared gauge and disentanglement k-points with the NNKP
presentation. Wannier90 3.1.0 writes NNKP fractional coordinates with eight decimal
places but writes `u` and `u_dis` coordinates with ten. The canonical construction WIN
contains twelve decimal places. Comparing the ten-decimal output with the lossy
eight-decimal derivative produced an artificial maximum residual of
`3.3000000509986194e-9`.

Direct comparison with the canonical WIN block gives
`3.300004713935323e-11` for both matrix outputs. Both pass the unchanged prospectively
declared `1.0e-10` fractional tolerance. There is no observed reciprocal-point
permutation.

## Correction

ProjectKoios now:

1. parses the canonical WIN k-point block from the authenticated construction input;
2. correlates derived NNKP coordinates with WIN under the explicit `1.0e-8` native
   serialization bound;
3. compares `u` and `u_dis` order with canonical WIN under the unchanged request gate;
4. records the two maximum residuals; and
5. supports authenticated no-calculator reverification of an existing occurrence.

The correction has focused tests for the native precision mismatch, true NNKP order
disagreement, and non-mutating no-calculator reverification.

## Evidence disposition

The initial provider result remains immutable false-negative audit evidence. It does not
invalidate the native occurrence or its outputs. The authenticated no-calculator
reverification passed all provider gates with no tolerance change and no additional
calculator invocation.

Current disposition: **provider eligible after correction of a verifier reference-space
defect**.

This disposition permits S30 full untruncated characterization. It does not establish a
global localization minimum, interpolation accuracy, development-target passage,
confirmation, full-operator acceptance, spatial-truncation acceptance, or
Slater--Koster validity.

## Identities

| Artifact | SHA-256 |
|---|---|
| original provider false negative | `2c373ab63e23b3be86b1c66c9da809e596805eaccbd052e2db2e441926cb2b64` |
| corrected ProjectKoios verifier implementation | `9c24755c656a1ed2b7b31d5da432aa4358eb6f6735c98f7a856a519593fad680` |
| no-calculator provider reverification | `23a0a6fe182abd0b5d2f7dcd142f27f81d6d6cca4fe9852be1950b5b622548b6` |
| reconciled eligibility summary | `0b2a0e6bab52574c353d780f562afe11d07bb1400bf149fa1178ddb5e8504e4c` |
| eligible HR | `24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55` |
| eligible `u` | `41758b721b79cae233689b4fb9fa359e750b82da8ed5bcd13b1d5faf3c5d8bf3` |
| eligible `u_dis` | `3c1d3574f3bf783cf7b54d8e9fd00fa5811ef05a56240850d46f43a2c95b7ace` |
