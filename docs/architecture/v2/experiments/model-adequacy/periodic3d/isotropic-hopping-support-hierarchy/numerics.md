# Isotropic 3-D numerical method

## Reciprocal sampling

The future numerical protocol will use a cubic-symmetric product mesh with deterministic
reduced-coordinate ordering.

- Use equal mesh cardinality on symmetry-equivalent axes.
- Preserve cubic symmetry in the sample inventory.
- Define a disjoint evaluation-only sample.
- Record flattening order explicitly.
- Verify complete-class reconstruction on the objective-construction mesh.

## Spectral weighting

The spectral channel must remain cubic-symmetric without collapsing into the operator
channel through equal-weight Parseval equivalence.

- Select one positive nonuniform cubic-invariant weight.
- Freeze the weight before threshold exploration.
- Normalize by one declared energy scale and total weight.
- Retain raw and normalized weights in strict inputs.
- Check full design rank in the active coordinate system.

## Operator weighting

The represented-operator channel evaluates the complete finite hopping domain.

- Give equal weight to represented blocks unless the protocol states another rule.
- Include cubic orbit multiplicities explicitly.
- Retain omitted target blocks for smaller classes.
- Use one maximal-space metric across all classes.
- Avoid active-dimension renormalization.

## Certificate calculation

The future certificate must be reviewed in the actual active dimension.

- Reconstruct channel minima before declaring nonemptiness.
- Retain common witnesses and feasible pairs separately.
- Retain support directions and dual-metric normalization.
- Verify domain containment before full-ellipsoid support.
- Use conservative arithmetic before comparison with resolution.

## Unresolved controls and references

Detailed numerical controls and sourced algorithms remain open until the protocol and
implementing classes are selected.

- Mesh size remains open.
- Parent coefficients and support order remain open.
- Thresholds and resolution remain open.
- Arithmetic and tolerance policies remain open.
- Primary numerical references will be recorded at the implementing class.
