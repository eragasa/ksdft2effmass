# Isotropic 2-D scientific method

## Parent construction

The proposed experiment consumes the retained lowest scalar band of the strongest
coupled square-lattice parent and converts its finite hopping representation into an
exact square-symmetric target after defect checks.

- The source reciprocal mesh is finite and explicitly identified.
- Raw Hermiticity, imaginary-part, and square-symmetry defects are measured before projection.
- Accepted symmetry orbits are averaged into real target coefficients.
- The selected common shift is the projected onsite coefficient, $\Delta E=-0.08796825852205918\,E_G$; the shifted onsite target is exact zero.
- Separate source-consistency controls of `1.0e-12 * E_G` admit the disclosed binary64 donor defects.
- Direct-parent evaluation and withheld values remain separate post-decision comparators on two disjoint 480-point symmetry-closed subsets of the selected 31-grid.

## Candidate hierarchy

Every candidate class is embedded in one selected 36-coordinate maximal orbit space.
The exact operations, member order, multiplicities, and prefixes are recorded in the
[maintained inventory](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/orbit-support-inventory.md).

- One real coefficient represents each accepted square-symmetry orbit.
- Canonical representatives use `0 <= b <= a <= 7` and order by `(a*a + b*b, a, b)`.
- Inactive coefficients are fixed to zero.
- The eight classes admit prefix counts `(1, 2, 3, 4, 6, 12, 27, 36)` and complete-block counts `(1, 5, 9, 13, 25, 61, 161, 225)`.
- Model-class expansion changes represented hopping support rather than orbital rank.
- The complete class contains the finite projected target by construction.

## Adequacy channels

The experiment compares spectral fidelity with represented-operator fidelity for the
same coefficient vector.

- The spectral channel uses the selected strictly positive square-symmetric weight $1+\frac{3}{4}[2+\cos(2\pi k_x)+\cos(2\pi k_y)]$ on the source mesh.
- The operator channel evaluates every block in the maximal represented domain.
- Every class uses the restriction of the common box $[-0.11426128163399648E_G,0.11426128163399648E_G]^{36}$.
- Both channels use one shared energy reference and scale.
- A common witness must satisfy both thresholds without channel-specific refitting.

## Hierarchy conclusion

A minimum tested compatible class requires evidence about every smaller class.

- Retain one explicit common witness in the selected class.
- Establish channel emptiness or certified separation for every smaller class.
- Block minimality when any smaller nonempty class remains unresolved.
- Interpret the result only within the frozen finite hierarchy.

## Sources and references

The current method is project-derived from retained parent data and a draft calculation
protocol; literature references will be added at the implementing class when a sourced
numerical method is selected.

- [Maintained prospective protocol](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/protocol.md).
- [Projection and loss design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/projection-and-loss-design.md).
- [Sample-role design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/sample-role-design.md).
- [Threshold and resolution design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/threshold-design.md).
- [Historical draft protocol](../../../../../../../calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md).
- [Legacy scientific derivation](../../../../ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/scientific.md).
- [Shared evidence semantics](../../../../ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md).
- No material or universal minimal-range claim is sourced or made.
