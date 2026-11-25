# Findings and limits

## Scientific question

Does the retained alignment fail because the ten trials are dependent in the
20-band parent, because the outer window removes a needed direction, or because
of the final retained-subspace selection? Can a narrowly extended window avoid
the demonstrated window obstruction while preserving the frozen states?

All energies below use the historical native S30 energy reference, not a VBM
shift. All conclusions are conditional on the authenticated source associations,
the assumed nearest decimal rounding (AMN/EIG: 12 places; U/U_dis: 10), and correctly
rounded binary64 parsing. Parent-model and DFT discretization errors are not
included in the native-input error bounds.

## Trial independence and normalized overlap

[Trial-subspace diagnosis](results/trial-subspace-diagnostic.json) resolves trial
independence at all 216 construction points. The smallest nominal parent-space
trial singular value is approximately `0.036249`; a conservative exact-residual
lower bound after native-input uncertainty is approximately `0.028939`.

[Whitening](results/trial-whitening.json) removes trial-coordinate scaling but
not subspace near-orthogonality. At `(0, 1/3, 0)`, the normalized minimum singular
value is approximately `4.76865e-6`, with a positive lower bound after uncertainty.
At Gamma it is approximately `6.06e-12` and remains input-limited. The original
raw gate, `5.890206739032098e-7`, still flags indices 0 and 12. There is no new
normalized acceptance criterion, and no exact physical nullspace is inferred.

## The Gamma loss is already present at the window

The [window diagnostic](results/gamma-window.json) finds:

| Trial representation at Gamma | Nominal minimum singular value |
|---|---:|
| All 20 parent bands | `0.0853637` |
| Current outer window, bands 1–14 | `1.2431e-12` |

Including the declared trial-input uncertainty, the windowed minimum has an upper
bound of approximately `1.12435e-11`. For any orthonormal retained frame inside
that window, `sigma_min(W† C) <= sigma_min(P_window C)`. Consequently the original
raw gate cannot be met for this trial family merely by changing the localization
or retained-subspace selection inside the same window. This is a resolved
fixed-window limitation, not proof of an exact zero or a symmetry-protected cause.

## The excluded response is concentrated in Gamma band 15

[Excluded-band attribution](results/gamma-excluded-bands.json) identifies band 15
at `21.257167314276 eV`, above the old `21 eV` ceiling. Its lower share bound is
approximately `0.9999999893` of the excluded squared response of the lost trial
combination. Algebraically including that band restores the Gamma trial minimum
to approximately `0.0853637`.

These shares describe a normalized trial combination's parent-band response,
not occupations, charges or physical orbital populations. The combination has
nominal trial-coordinate weights of about 19.49% s and 80.51% s-star; it is not
identified as a physical Si 4s state. No irrep is assigned, and the band index is
not a tracked branch across reciprocal space.

## Sampled candidate feasibility, not a selected construction

The [all-point preflight](results/window-feasibility.json) tests the first sampled
cap-membership interval admitting Gamma band 15. A representative outer window is
`[-6, 21.3378850145845] eV`; the frozen window remains `[-5.85, 8] eV`.

- It admits 49 additional parent states at 49 points, with band 15 admitted only
  at Gamma on this mesh. Outer counts are 12/13/14/15 at 48/60/107/1 points.
- All 216 windowed trial matrices are independent under the declared uncertainty.
  The smallest nominal trial singular value is about `0.00872139`, with a
  conservative lower bound after error of about `0.00870257`.
- Frozen counts remain 4/5/6 at 129/84/3 points. The frozen-to-trial overlap has
  full row rank everywhere; its smallest conservative lower singular bound is
  approximately `0.286057`.
- Thus, pointwise, a rank-ten subspace containing every frozen state and having
  nonsingular trial overlap exists. This is an existence statement, not an
  actual new retained frame or a proof of passage at the frozen raw threshold.
- All four valence bands remain frozen. The lowest conduction band is available
  in the outer space everywhere and frozen at 87 points. This is sampled state
  availability, not new band-edge interpolation fidelity.

For the existence statement, write F for the frozen frame and C for the windowed
trials. Full column rank of C and full row rank of F†C imply that
K=ker(F†C) has dimension 10-dim(F). Then W=F direct-sum span(CK) has dimension
ten and W†C is nonsingular. No such W or candidate Hamiltonian was constructed.

## What remains unestablished

No new localized operator, global smooth/periodic/symmetry-compatible frame,
off-mesh guarantee, band-edge fidelity, new raw-gate result, production-qualified
PseudoDojo parent, or accepted successor follows from these diagnostics. No
unobserved confirmation values were consumed. The current protocol sequence and
human branch-selection boundary remain unchanged.

The actionable next work is tracked under **Pending — qualify a window-remedy
Wannier candidate** in [the development plan](../../development-plan.md). The
[current protocol](../../research-protocol/controlled-reduction-protocol-hopping-first.tex)
continues to control progression; this report does not amend it.
