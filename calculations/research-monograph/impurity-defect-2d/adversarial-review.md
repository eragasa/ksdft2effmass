# Adversarial review of the defect-2D design

## Review intent and scope

This review attacks the execution-free design in `study-design.json`,
`protocol.md`, and `preflight.md`. The definition of done is a deterministic,
bounded proposal that cannot accidentally authorize execution, conflate
represented spaces, hide negative evidence, or support stronger claims than its
synthetic evidence class.

This is an adversarial design review, not independent verification of a future
implementation and not human acceptance.

## Threat model

| Attack | Plausible false conclusion | Required defense in the design |
|---|---|---|
| Runner and verifier share the same construction | Two agreeing implementations appear independent while reproducing one bug | Independent integer-enumeration, folding, symmetry, alignment, and eigensystem routes; verifier must not import runner |
| Subtract before compatibility is established | A basis, geometry, twist, or energy-zero mismatch appears as an impurity | Structured stops before subtraction and explicit negative controls |
| Use one eigenvector in a degenerate cluster | Arbitrary basis rotation appears as state error | Projectors, principal angles, fixed gap rule, and an individual-vector stop |
| Assume square-lattice symmetry everywhere | An anisotropic parent falsely passes or fails a $D_4$ claim | $D_4$ only for the isotropic parent; $D_2$ and explicit axis swap for the anisotropic parent |
| Wrap rotated coordinates by floating-point proximity | Site mapping changes with rounding or boundary location | Integer point-group actions followed by exact modular wrapping |
| Use the wrong seam phase or rotate a generic twist without transforming it | A boundary convention error masquerades as a defect, covariance failure, or finite-size effect | Four exact folding twists, an exact $9\times9$ twist formula, point-group action on twists, and mandatory wrong-phase/fixed-twist controls |
| Change area and aspect ratio together | Shape dependence is mislabeled as finite-area convergence | Separate square-area and fixed-area shape sequences |
| Tune the model class after observing residuals | The planted defect appears uniquely identified by construction | Frozen nested classes and first-passing-class rule |
| Select only cases with a bound state | A weak or adverse case disappears from evidence | No-bound-state is a retained outcome, distinct from process failure |
| Accept matching energies as operator recovery | Spectral agreement hides nonlocal or symmetry-breaking error | Operator, projector, spectral, state, shell, symmetry, and anisotropy metrics remain separate |
| Correct a blind-map tie using planted information | A nominally blind route becomes a known-map route | Exhaustive declared search, frozen tie tolerance, ambiguity record, and unresolved-map stop |
| Let a scalar energy shift leak into the defect | A global offset appears as a delocalized impurity | Known shift correction plus an intentionally uncorrected negative control |
| Reuse accepted spin evidence as new 2D evidence | Scope expands while duplicating a frozen prerequisite | Spin result is identity-only inherited context; no spin variant is in the study |
| Treat a parent file as mutable input | Results silently change after parent regeneration | Exact parent SHA-256 checks before execution |
| Interpret passing synthetic checks as material validation | The manuscript overstates silicon or dopant evidence | Explicit claim exclusions in every package surface |
| Permit stage authorization to cascade | A small null run silently authorizes the full study | Stage-specific authorization gates; each later stage requires a new request |

## Findings

### Representation and subtraction ordering

Disposition: NO_ACTION_REQUIRED
Problem: Direct subtraction could manufacture an impurity from incompatible
coordinates or boundary conventions.
Evidence: `protocol.md` requires compatibility checks and enumerates structured
stops before subtraction; `study-design.json` includes pre-alignment,
energy-shift, and wrong-seam negative controls.
Consequence: The identified attack is covered by the proposed contract.
Next action: None at design time; the future verifier must demonstrate each
stop.

### Degenerate-state ambiguity

Disposition: NO_ACTION_REQUIRED
Problem: Individual eigenvectors are not invariant inside a degenerate cluster.

Evidence: The design freezes a $10^{-8}E_G$ adjacent-gap rule, projector and
principal-angle metrics, and `DEFECT_2D.DEGENERATE_PROJECTOR_REQUIRED`.
Consequence: The future result cannot legitimately use individual-vector error
as the primary oracle.
Next action: None at design time.

### Area/shape and symmetry confounding

Disposition: NO_ACTION_REQUIRED
Problem: A single supercell sequence could confuse area, aspect ratio,
orientation, and broken rotational symmetry.
Evidence: The design separates square area refinement, area-144 shapes,
anisotropic orientation pairs, boundary twists, $D_4$, $D_2$, and axis-swap
comparisons.
Consequence: The major two-dimensional confounders have distinct result
channels.
Next action: None at design time.

### False independence

Disposition: SAFE_TO_DEFER
Problem: Textual separation cannot prove that a future verifier is genuinely
independent of a future runner that does not yet exist.
Evidence: `protocol.md` fixes different reconstruction algorithms and forbids
verifier imports from the runner, but no implementation can yet be inspected.
Consequence: Independence remains unestablished until implementation review;
this does not block an execution-free design.
Next action: Before any execution authorization, inspect imports and algorithms
and retain a dry verification report.

### Numerical conditioning and measured resources

Disposition: SAFE_TO_DEFER
Problem: Runtime, memory, eigensolver conditioning, and cluster behavior are
estimates until code exists.
Evidence: `preflight.md` labels the 20-minute and 2-GiB values as planning
estimates and requires a new implementation-aware preflight.
Consequence: The design can be reviewed now, but its resource estimate cannot
serve as execution evidence.
Next action: Recalculate the envelope and inspect representative matrix
conditioning before requesting Stage A execution.

## Adversarial conclusion

**ReviewOutcome: NO_BLOCKING_FINDINGS**

The recommendation survives the bounded adversarial review as an
**execution-free design package**, subsequently human-accepted for Stage A
implementation only. Its strongest defenses are subtraction only
after compatibility, independent reconstruction, exact integer symmetry maps,
projector treatment of degeneracy, separate area/shape/twist axes, frozen
negative controls, and noncascading stage gates.

**OperatorRequest: NONE**

No execution is requested or authorized. When Stage A implementation is ready,
the exact local invocation will require separate authorization after
implementation-aware preflight and review. A passing future Stage A will not
authorize later stages or establish material validation.
