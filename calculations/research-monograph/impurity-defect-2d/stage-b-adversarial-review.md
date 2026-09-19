# Adversarial review of the proposed Stage B design

**Subsequent disposition:** the reviewed single-route design was superseded after
implementation exposed the retained twist-gauge blocker. HC04 adopted the
multi-route replacement. This review remains historical design evidence.

## Scope and definition of done

This review stress-tests `stage-b-design.json`, `stage-b-protocol.md`, and
`stage-b-preflight.md` as an execution-free design. The design is ready for a
human implementation-authorization decision only if it fixes all coordinate,
symmetry, twist, identifiability, energy-reference, information-boundary,
criterion, and scope conventions without relying on a future calculation.

No Stage B implementation or numerical result was reviewed. The Stage A result,
periodic-2D parent, and earlier prerequisites were treated as immutable inputs
by identity rather than rerun.

## Findings

### Homogeneous-host symmetry cannot identify an absolute defect site

FindingDisposition: NO_ACTION_REQUIRED

Problem: The accepted high-level blind objective uses only off-diagonal host
blocks. For a translation- and $D_4$-symmetric scalar parent, that objective
cannot uniquely identify the authored translation and, at Gamma, cannot identify
the point-group operation.

Evidence: An onsite plant changes no off-diagonal block. The frozen search has
64 translations and eight $D_4$ operations at Gamma, while generic twist
metadata removes the point-group ambiguity but not the 64 translations.

Consequence: A design expecting unique blind recovery would either fail or leak
the planted site into inference.

Next action: None. The corrected design makes non-identifiability the expected
control: it requires exact 512- and 64-candidate ambiguity sets,
`DEFECT_2D.SITE_MAP_UNRESOLVED`, and null selected-map and extracted-operator
fields.

### Defect-only covariance cannot test boundary-twist transformation

FindingDisposition: NO_ACTION_REQUIRED

Problem: A scalar onsite operator has no twist dependence, so its covariance can
pass even when a generic twist is incorrectly kept fixed under rotation.

Evidence: $\Delta_p=-0.25|p\rangle\langle p|$ depends on site but not on the
boundary fiber. Rotating only this operator cannot distinguish $\phi$ from
$M\phi$.

Consequence: A nominal symmetry pass could leave the two-dimensional seam and
fiber convention untested.

Next action: None. The corrected design assigns twist covariance to the full
pristine-defect Hamiltonian, keeps defect covariance as a separate metric, and
requires the wrong-fixed-twist control to exceed a frozen discrimination floor.

### Point-group names conceal composition and wrapping ambiguities

FindingDisposition: NO_ACTION_REQUIRED

Problem: Names such as `reflection_x_after_quarter_turn` do not determine matrix
multiplication order, vector convention, permutation orientation, or whether
periodic wrapping occurs before or after the integer action.

Evidence: Reversing composition or using row vectors can produce a different but
internally consistent orbit and attacked support.

Consequence: Runner and verifier could agree on the wrong convention while
claiming to implement the accepted design.

Next action: None. The corrected design supplies all eight matrices, column-vector
and unitary conventions, operation order, exact orbit sites, action-before-wrap
rule, and group/composition checks.

### A trace mean biases the hidden energy-shift estimate

FindingDisposition: NO_ACTION_REQUIRED

Problem: The onsite defect contributes to the trace, so averaging all diagonal
differences estimates $c-0.25/64$ rather than $c$.

Evidence: Exactly one of 64 diagonal entries contains the planted onsite term;
the other 63 contain only the scalar reference shift after alignment.

Consequence: The blind route could report a deterministic energy error and then
misattribute it to map recovery.

Next action: None. The corrected design uses the median real diagonal difference
as a diagnostic and forbids the trace mean. The diagnostic does not override the
site-map stop.

### Blind inference can be contaminated by oracle fields

FindingDisposition: NO_ACTION_REQUIRED

Problem: A shared record or callable could expose the planted site, strength,
authored map, or known-map errors to the blind search and silently break ties.

Evidence: The known-map and blind routes operate on the same authored candidate,
so accidental field reuse is a credible implementation failure.

Consequence: Apparent blind success would be circular and would invalidate the
identifiability conclusion.

Next action: None. The design closes the blind input representation, explicitly
lists visible and withheld fields, prohibits plant-based tie-breaking, and
requires mutation tests that inject forbidden fields and expect rejection.

### A favorable spectrum can hide an operator covariance error

FindingDisposition: NO_ACTION_REQUIRED

Problem: Unitary conjugation preserves eigenvalues even when the wrong operator
fiber is compared.

Evidence: A spectrum-only check cannot establish entrywise full-Hamiltonian
covariance or the correct twist map.

Consequence: Stage B could pass a physically different represented comparison.

Next action: None. Maximum-entry and Frobenius operator covariance are primary;
symmetry-related eigenvalues are retained only as supplementary diagnostics.

### Stage B could absorb later-stage questions

FindingDisposition: NO_ACTION_REQUIRED

Problem: The program design lists model classes, finite-size controls,
observables, and composite alignment that could be pulled into the first planted
defect stage.

Evidence: Directional and nonlocal classes belong to Stage C, area/shape/twist
meshes to Stage D, and composite degeneracy to Stage E.

Consequence: Scope expansion would obscure whether scalar onsite alignment and
$D_4$ covariance work and would increase execution authority implicitly.

Next action: None. The corrected design limits model assessment to the exact
point-scalar-onsite projection, one $8\times8$ shape, two twists, and scalar
operators. Later stages remain excluded and unauthorized.

### Numerical failure could be mistaken for verifier disagreement

FindingDisposition: NO_ACTION_REQUIRED

Problem: A frozen adverse or covariance criterion may fail even when the
independent verifier reproduces it.

Evidence: Stage A already established the need to separate reconstruction
agreement from criterion disposition.

Consequence: Valid negative evidence could be discarded as a process failure or
tuned away.

Next action: None. Stage B retains exact failed-criterion identifiers and reports
criterion status separately from reconstruction status. The preflight forbids
post-execution changes to twists, floors, inventories, or tolerances.

### Resource and runtime estimates are unmeasured

FindingDisposition: SAFE_TO_DEFER

Problem: The proposed 180-second, 2-GiB, and 10-MiB bounds have not been measured
against a Stage B implementation.

Evidence: No Stage B source or execution exists. The largest declared matrix is
only $64\times64$, but the blind search includes up to 512 candidates.

Consequence: An inefficient implementation could exceed a future authorization
envelope.

Next action: Reassess with execution-free toy benchmarks after implementation
and before requesting calculation execution. Do not increase a bound silently.

## Review conclusion

ReviewOutcome: NO_BLOCKING_FINDINGS

The adversarial review found no unresolved technical blocker in the corrected
execution-free design. Its central conclusion is intentionally negative: the
homogeneous scalar host cannot uniquely identify an absolute onsite-defect map
without an external anchor. Stage B therefore tests known-map recovery and $D_4$
covariance while retaining blind-map ambiguity as a structured stop.

This outcome does not accept the design, authorize implementation or execution,
or establish numerical or scientific evidence.

OperatorRequest: AUTHORIZATION_REQUIRED

The immediate next operation, if desired, is execution-free implementation of
the exact proposed design: runner, independent verifier, and toy behavioral
tests only. That operation would add no dependencies and perform no Stage B
calculation. A later, separately bound human decision would still be required
before executing the accepted scalar parent.
