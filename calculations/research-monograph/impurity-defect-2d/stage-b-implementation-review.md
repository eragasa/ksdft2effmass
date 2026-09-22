# Adversarial review of the Stage B multi-route implementation

## Scope and authority

This review covers only the authorized execution-free Stage B implementation:
`run_stage_b.py`, `verify_stage_b.py`, `plot_stage_b.py`,
`stage-b-result.schema.json`, and the maintained authored-toy software tests. It
does not read or execute the accepted scalar parent, create a calculated Stage B
result, authorize execution, or assess material validity.

The review applies adversarial, assumption-busting, and trust-but-verify checks
to route independence, gauge orientation, process isolation, retained-data
completeness, verifier independence, authority binding, path confinement, and
resource bounds.

## Findings and dispositions

### F1 — route schedules originally shared one Python process

- FindingDisposition: `FIXED`
- Evidence: the first implementation evaluated A-then-B and B-then-A through
  sequential method calls in one process, so it could not enforce the adopted
  fresh-process contract.
- Correction: each schedule now uses the multiprocessing `spawn` context, a
  byte-serialized process boundary, immutable inputs, a 120-second process
  timeout, and no route output shared with the other schedule.
- Verification: the clean authored toy has exact zero route-local schedule
  difference; retained execution-order metadata remains distinct from canonical
  serialization order.

### F2 — route-order adverse control was described but not retained

- FindingDisposition: `FIXED`
- Evidence: the implementation initially tested only clean schedule agreement.
- Correction: the toy record now includes a deliberately invalid shared-twist
  cache mutation separately from clean evidence.
- Verification: Route A schedule difference is
  `0.7653668647301796`, the B-then-A bridge mismatch is
  `0.7653668647301798`, and the seam-route difference is
  `2.7755575615628914e-17`; clean schedule differences remain zero.
- Interpretation: this is synthetic mutation discrimination, not a physical
  order effect.

### F3 — future authority did not bind every final implementation surface

- FindingDisposition: `FIXED`
- Evidence: the first exact-authority parser bound the design, runner, parent,
  Stage A result, output, and checkpoint but omitted the verifier, plotter,
  result schema, and parent input.
- Correction: future authority must now bind canonical repository-relative paths
  and SHA-256 identities for all of those surfaces. The execution checkpoint
  must also carry the exact normalized decision
  `AUTHORIZE_EXACT_STAGE_B_MULTIROUTE_EXECUTION`; resolved implementation
  authority is insufficient.
- Verification: isolated tests reject stale source identity, path escape, a
  wrong resolved checkpoint decision, and resource expansion before parent
  parsing or result creation.

### F4 — the parent hopping class was selected too weakly

- FindingDisposition: `FIXED`
- Evidence: selecting only `lambda_xy=0` did not prove the frozen
  `(lambda_x,lambda_y,lambda_xy)=(0.5,0.5,0)` parent or retained-hopping
  symmetry.
- Correction: the parser now requires both diagonal coefficients to equal
  `0.5`. A separate action validates unique displacements, Hermitian partners,
  and exact retained-inventory $D_4$ closure before either schedule starts.
  The verifier reconstructs those checks independently.

### F5 — no closed persistence schema owned the complete retained record

- FindingDisposition: `FIXED`
- Evidence: typed Python serialization alone did not provide a versioned wire
  contract.
- Correction: `stage-b-result.schema.json` closes the top-level record,
  provenance variants, controls, inventory, all 2,304 candidate rows, known
  cases, bridges, blind dispositions, order comparisons, criteria, and the
  execution-free adverse record. `stage-b-native-evidence-manifest.json` freezes
  the post-execution artifact inventory, identity algorithm, exact counts,
  dense-matrix disposition, and deterministic finalization rule while remaining
  explicitly non-evidentiary before execution.
- Verification: the complete toy validates under JSON Schema Draft 2020-12.

### F6 — verifier independence could have become tautological

- FindingDisposition: `FIXED`
- Evidence: cross-route agreement is not independent verification when one
  route or verifier consumes runner matrices.
- Correction: the verifier imports neither runner nor dynamic loader. It
  independently reconstructs uniform-link and quotient-seam matrices, site
  maps, gauge bridges, candidate objectives, ambiguity identities, parent
  checks, criteria, and order comparisons from retained compact inputs.
- Verification: bridge, ambiguity-identity, and schedule-order mutations are
  rejected. The clean toy reports reconstruction and criteria `PASS`, with
  maximum reconstructed difference `6.8397475661999700e-14`.

### F7 — retained output had no enforced byte limit

- FindingDisposition: `FIXED`
- Evidence: the authorization represented a 30 MiB ceiling but serialization
  did not enforce it.
- Correction: the future accepted-parent path serializes to bytes, checks the
  authorized ceiling, and writes only if the complete result fits. Overwrite is
  refused.
- Verification: the complete toy JSON occupies 3,090,150 bytes and its SVG
  occupies 63,729 bytes.

### F8 — not every conceivable gauge mutation has a dedicated named test

- FindingDisposition: `ACCEPTED_LIMITATION`
- Evidence: maintained tests directly cover clean inventory, ambiguity,
  independent reconstruction, bridge corruption, ambiguity-identity corruption,
  schedule corruption, deterministic plotting, overwrite, shared-cache order
  sensitivity, fail-closed invocation, stale identity, traversal, wrong
  checkpoint scope, resource expansion, schema conformance, and verifier import
  independence. Some algebraic mistakes listed during design review, such as
  every separate $D/D^\dagger$ or $U_M/W_M$ substitution, are represented by
  the independently reconstructed bridge rather than one named test per typo.
- Rationale: the independent verifier computes the correct objects without
  importing the runner, so these substitutions affect retained bridge or
  route-local data and fail existing reconstruction checks. A future
  execution-authority review may add named mutation cases without changing the
  scientific contract.
- Boundary: this limitation is acceptable for execution-free implementation; it
  is not evidence of accepted-parent correctness.

## Resource reassessment

The complete authored nearest-neighbour toy ran in 1.66 seconds with a measured
maximum resident set size of 56,229,888 bytes on the development machine. It
retained 72 known-map route evaluations, 36 bridge records, 2,304 blind
candidate rows, 36 known-case order comparisons, 18 bridge order comparisons,
and six blind-summary comparisons. These measurements remain synthetic software
evidence and do not predict production scientific cost.

## Check disposition

The following checks pass at this implementation boundary:

- Ruff formatting and lint;
- strict mypy for runner, verifier, plotter, and maintained tests;
- Python bytecode compilation;
- 16 maintained software-verification tests;
- maintained Python test-evidence conformance;
- independent toy reconstruction and criteria;
- closed-schema validation; and
- deterministic retained-data-only SVG generation.

## Review outcome

- TechnicalReviewOutcome: `NO_BLOCKING_FINDINGS`
- FindingDisposition summary: seven `FIXED`, one `ACCEPTED_LIMITATION`
- OperatorRequest: `DECISION_REQUIRED`

This outcome means only that the authorized execution-free implementation has no
remaining blocking technical finding in the reviewed scope. It is not human
acceptance, execution authority, a calculated Stage B result, numerical
verification of the accepted parent, scientific validation, uncertainty
quantification, publication authority, or release authority. HC05 subsequently
authorized one attempt, which stopped at fail-closed path resolution before
accepted-input access. HC06 then authorized a corrected-path retry, which
stopped at an exact parent-field ownership mismatch before hopping or matrix
construction. The parser is corrected and bounded read-only checks pass. Pending
checkpoint `RM-IMPURITY-DEFECT-2D-STAGE-B-SCHEMA-CORRECTED-RETRY-HC07`
subsequently authorized one schema-corrected attempt. That attempt completed;
runner criteria and independent reconstruction pass. HC08 later human-accepted
the exact bounded result and authorized managed closeout only.
