# Anisotropic 2-D numerical method

## Coordinate construction

The future implementation must retain directional information throughout the finite
Fourier and coefficient calculations.

- Use deterministic reduced-coordinate sample order.
- Use deterministic integer-representative order.
- Construct symmetry orbits without axis permutations unless explicitly admitted.
- Retain orbit multiplicities for complete block sums.
- Compute physical lengths through the declared lattice metric.

## Loss construction

Spectral and operator losses must respond differently to omitted directional content
without changing parameter identity.

- Select positive nonuniform spectral weights before threshold design.
- Evaluate the operator channel over the complete maximal block domain.
- Keep one common energy scale and coordinate normalization.
- Retain omitted target coefficients in smaller-class residuals.
- Reconstruct direct residuals independently of any quadratic owner.

## Certificate construction

The certificate must be reviewed for the actual active dimension and anisotropic metric.

- Retain feasible witnesses and upper-bound pairs separately.
- Retain the support direction and orientation.
- Reconstruct dual-metric normalization.
- Verify domain containment before using unconstrained ellipsoid support.
- Report failed premises rather than coercing a disposition.

## Unresolved controls

No numerical value is frozen at this architecture stage.

- Mesh dimensions remain open.
- Parent coefficients remain open.
- Weights and thresholds remain open.
- Metric resolution remains open.
- Arithmetic and tolerance policies remain open.

## Sources and references

Detailed numerical references will be assigned only after the exact methods and owner
contracts are selected.

- Shared evidence semantics define result meaning.
- PhysKit documentation will be cited for consumed lattice primitives.
- Numerical-owner documentation and primary literature will be cited by the implementing class.
