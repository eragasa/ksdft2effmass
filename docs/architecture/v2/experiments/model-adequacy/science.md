# Model-adequacy scientific method

## Scientific construction

A model-adequacy experiment identifies one candidate space and asks whether a single
candidate can satisfy two independently motivated scientific channels.

- Let `X` be the frozen candidate-parameter space.
- Let `L_A` and `L_B` be the declared channel losses.
- Let `tau_A` and `tau_B` be the declared thresholds.
- Define `A = {x in X : L_A(x) <= tau_A}`.
- Define `B = {x in X : L_B(x) <= tau_B}`.

## Compatibility method

Compatibility is established constructively by evaluating both channels at one retained
parameter vector.

- Retain one candidate `x_w` with a stable identity in `X`.
- Reconstruct `L_A(x_w)` and compare it with `tau_A`.
- Reconstruct `L_B(x_w)` and compare it with `tau_B`.
- Retain any finite component or alignment identity used for membership.
- Reject nearby channel-specific points as a substitute for a common witness.

## Separation method

For nonempty channel sets, separation is evaluated in one declared metric rather than by
failed witness search.

- Define `delta* = inf {d(a,b) : a in A, b in B}`.
- Retain a conservative lower bound `delta_lower <= delta*`.
- Declare separation only when `delta_lower` exceeds the frozen resolution.
- Retain every convexity, containment, enumeration, and arithmetic premise.
- Report nonempty cases without decisive evidence as unresolved.

## Scientific interpretation

The outcome describes one finite model family under one protocol and does not become a
general validation statement.

- A common witness supports joint adequacy only for the declared channels.
- A separation certificate excludes joint adequacy only in the tested candidate family.
- Channel emptiness identifies failure of one criterion rather than positive inter-set distance.
- Evaluation and locality diagnostics describe retained candidates without redefining the sets.
- Material, continuum, and uncertainty claims require separate evidence.

## Sources and references

The method is derived and interpreted through maintained project sources, with external
references added by each child when it adopts a literature-owned numerical method.

- [Shared admissible-set evidence semantics](../../ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md).
- [Dimensionality and anisotropy ladder](dimensional-anisotropy-ladder.md).
- Child `science.md` files bind the exact parent, geometry, channels, and scientific provenance.
- Child `numerics.md` files cite external numerical methods when the implementation depends on them.
