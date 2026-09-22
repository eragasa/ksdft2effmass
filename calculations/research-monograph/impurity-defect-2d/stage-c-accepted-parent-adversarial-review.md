# Accepted-parent Stage C adversarial design review

## Review intent and scope

This review challenges the proposed accepted-parent Stage C design, protocol,
and preflight. The definition of done is an exact, internally consistent,
resource-bounded design that preserves accepted parent identities, keeps error
classes separate, supports independent verification, and grants no implementation
or execution authority.

The review does not inspect an implementation or calculated Stage C result and
does not establish numerical verification, scientific validation, uncertainty
quantification, human acceptance, publication, or release status.

## Findings

### Anisotropic-parent reconstruction could silently become a new parent claim

Disposition: `NO_ACTION_REQUIRED`

Problem: The accepted periodic result retains anisotropy diagnostics but not the
compact anisotropic hopping inventory required by Stage C.

Evidence: The design now classifies construction of the $15\times15$, cutoff-5,
radius-18 inventory as explicit Stage C preprocessing and requires retention of
the pretruncation inventory, truncation residual, Hermiticity, $D_2$ closure,
and axis-swapped identity.

Consequence: Parent-representation error cannot be silently merged with the
defect-model residual or described as revalidation of the parent.

Next action: None for design adoption; implementation must preserve these
separate records.

### Model classes could be under-specified or selected using plant knowledge

Disposition: `NO_ACTION_REQUIRED`

Problem: Class names alone would permit implementations to choose different
basis vectors or use the expected planted class as a tie-breaker.

Evidence: `model_class_basis` now lists every basis vector, while
`selection_input_boundary` limits selection to the aligned defect, frozen bases,
and tolerances. Expected class identity is evaluated only afterward.

Consequence: A later implementation has one deterministic hierarchy and cannot
select a favorable class from plant metadata.

Next action: None.

### The anisotropic parent could be subjected to an invalid $D_4$ invariance claim

Disposition: `NO_ACTION_REQUIRED`

Problem: Diagonal reflection swaps the anisotropic axes and does not preserve the
$(0.3,0.7,0)$ parent.

Evidence: The design restricts same-parent covariance to $D_2$, identifies the
$(0.7,0.3,0)$ target separately, and uses one diagonal reflection as the frozen
$D_4/D_2$ coset representative. The invalid same-parent $D_4$ claim remains an
adverse control.

Consequence: Axis-swap agreement cannot be misreported as symmetry of one
anisotropic parent.

Next action: None.

### Fresh route-order processes could still share anisotropic preprocessing state

Disposition: `NO_ACTION_REQUIRED`

Problem: Precomputing the anisotropic hopping inventory in the parent process
would leave schedule-state contamination untested.

Evidence: The corrected inventory contract requires each fresh schedule process
to reconstruct the anisotropic hopping independently and requires exact hopping
digest and preprocessing-residual agreement.

Consequence: A clean schedule comparison now covers both preprocessing and route
order rather than only downstream matrices.

Next action: None.

### A normal-equation verifier could create avoidable conditioning disagreement

Disposition: `NO_ACTION_REQUIRED`

Problem: Normal equations square the condition number and are not an appropriate
independent oracle when the model basis is not exactly orthogonal.

Evidence: The corrected verifier contract requires direct orthogonal projections
for orthogonal classes and an independent QR factorization otherwise; normal
equations are forbidden.

Consequence: Verifier disagreement is less likely to be an avoidable numerical
artifact of the oracle method.

Next action: None.

### Adverse discrimination floors might be too aggressive before implementation

Disposition: `SAFE_TO_DEFER`

Problem: Matrix-level anisotropic $D_4$ and unswapped-parent residual floors are
proposed without an authored implementation measurement.

Evidence: The design lowers both proposed floors to $10^{-3}E_G$, while the
accepted periodic anisotropy control reports a much larger sampled $C_4$
energy residual. The resource and authorization boundary requires an authored
toy to demonstrate every floor before execution authority can be requested.

Consequence: If either floor is nondiscriminating in the exact finite-matrix
representation, implementation cannot advance to execution authorization.

Next action: Revisit only during the separately authorized execution-free
implementation; retain a failed floor rather than tune it after observing the
accepted parent.

### Spectral and bound-state observables remain outside this Stage C acceptance

Disposition: `SAFE_TO_DEFER`

Problem: The broader defect-2D program names spectral and state observables, but
this Stage C design is limited to operator model-class discrimination and
locality.

Evidence: The result contract explicitly excludes spectral, bound-state,
wavefunction, and physical-observable claims from Stage C acceptance.

Consequence: Stage C cannot be cited as bound-state or material-adequacy evidence.

Next action: Revisit only through a later separately authorized stage or design
that defines the corresponding parent, oracle, and acceptance criteria.

## Evidence digest

- immutable parent and prerequisite paths have explicit SHA-256 identities;
- isotropic, anisotropic, and axis-swapped parents are distinct;
- 52 cases per schedule produce exactly 208 route evaluations, 104 bridge
  records, 1,040 model fits, and 104 cross-schedule comparisons;
- ten adverse controls cover alignment, energy, model class, Hermiticity, gauge,
  twist, symmetry, axis swap, and route independence;
- route, schedule, parent preprocessing, representation, and model errors remain
  separate; and
- the proposed local envelope is dimension 64, 600 seconds, 2 GiB, and 20 MiB.

## Review outcome

`NO_BLOCKING_FINDINGS`

The bounded design is technically coherent after the deterministic corrections
above. This outcome does not adopt the design or authorize implementation or
execution.

## Operator request

`NONE`

HC12 human-adopts this exact accepted-parent Stage C design as the authoritative
proposed contract. No further action belongs to this design review.
Execution-free implementation and accepted-parent execution remain separate
later authorization boundaries.
