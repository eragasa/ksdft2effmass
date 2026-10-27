# Anisotropic 3-D numerical method

## Objective-construction and evaluation samples

The source protocol separates decisive reciprocal samples from downstream diagnostics.

- Objective construction uses the declared `9 x 11 x 13` reduced-coordinate product
  mesh.
- Evaluation uses a disjoint half-shifted `10 x 12 x 14` mesh.
- Both use deterministic C ordering with the final coordinate varying fastest.
- Only objective-construction values define quadratics, witnesses, certificates, and
  dispositions.
- Evaluation reports residuals without tuning controls.

## Spectral loss

The spectral channel uses a positive anisotropic coordinate weight so it is not
Parseval-identical to the complete-block operator loss.

- The weight contains separate first harmonics for the three reduced coordinates.
- Its analytic lower bound remains positive.
- The loss is normalized by total weight and one electron-volt scale.
- The target and candidate use the same zero energy reference.
- The exact formula remains authoritative in the source protocol.

## Operator loss and metric

The operator channel and inter-set metric count every represented block through orbit
multiplicity.

- The complete inventory contains 32 represented blocks.
- Omitted target coefficients remain visible in smaller classes.
- One normalized complete-block metric is used for every class.
- Active parameter count does not change normalization.
- The common coefficient box is the affine domain for every class.

## Certificate method

Each nonempty quadratic set may use directional full-ellipsoid support only after its
containment premise is independently verified.

- Reconstruct the completed-square center and matrix.
- Reconstruct threshold radius after subtracting minimum squared loss.
- Reconstruct support in the retained direction.
- Verify every coordinate extremum lies in the box.
- Normalize the support gap by the metric dual norm.
- Enclose square roots conservatively before comparing with resolution.

## Exact reconstruction

The declared mesh and finite Fourier inventory permit an independent rational
reconstruction of the objective-construction quadratic.

- Parent hopping coefficients are rational binary fractions.
- Weight Fourier coefficients are rational.
- Basis-product frequencies remain below the declared no-alias limits.
- Discrete Fourier orthogonality reduces Gram entries to rational constant coefficients.
- The future verifier must avoid producer trigonometric rows for this decisive check.

## Sources and references

The exact controls and exploratory numerical observations remain in the source package.

- [Maintained protocol](../../../../../../../calculations/periodic3d/rank1/anisotropic-hopping-support-hierarchy/protocol.md).
- [Exploratory threshold design](../../../../../../../calculations/periodic3d/rank1/anisotropic-hopping-support-hierarchy/threshold-design.md).
- No external interval or convex-support implementation has yet been selected or cited.
- Future class pages must cite the exact numerical owner and primary method reference when applicable.
