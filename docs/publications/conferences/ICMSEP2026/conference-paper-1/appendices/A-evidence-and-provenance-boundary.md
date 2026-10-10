# Appendix A. Evidence, Provenance, and Controlled-Calculation Plan

## A.1 Purpose and status boundary

This appendix serves two purposes:

1. it identifies the retained evidence supporting the present manuscript; and
2. it defines the prospective controlled calculations needed to extend the framework
   beyond the minimal scalar illustration.

The maintained evidence is retained under:

| Location | Present role | Status and claim boundary |
|---|---|---|
| `calculations/ICMSEP2026/conference/paper_1/isolated-band/` | Prospectively frozen M1 parent refinement, lowest-band extraction, complete hopping reconstruction, finite-range truncation, matched-route comparison, and withheld evaluation | Retained controlled numerical-verification evidence; its historical identity does not substitute for a gap or isolation result, it excludes historical stress channels, and it is not a thresholded admissible-set map |
| `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` | Prospectively frozen M2 gapped rank-two parent, known periodic gauge attack, pointwise and global-unitary alignment channels, block-hopping locality, and withheld evaluation | Retained controlled numerical-verification evidence; not a general alignment solver or thresholded admissible-set map |
| `calculations/research-monograph/periodic-2d/` | Coupling and shell hierarchy, projector/loop controls, gauge-locality comparison, and withheld-mesh diagnostics | Retained controlled numerical-verification evidence; not material or wavefunction validation |
| `calculations/ICMSEP2026/conference/paper_1/` | Minimal scalar admissible-set illustration with an exact witness and certified separation | Retained analytic/numerical evidence for the frozen two-parameter identity-alignment contract only |

Each retained directory contains, as applicable, its protocol, input and result records,
independent verification code, figures, report, software record, and checksum manifest.
The evidence is classified as controlled illustrative software and numerical
verification. It is not a public data deposit, DOI, material validation, statistical
uncertainty analysis, or evidence that a general alignment problem has been solved.
Historical external executions are not rerun by the manuscript.

The standalone M1 and M2 retained verifiers decode the frozen JSON documents and
reconstruct their finite protocols without importing the corresponding producer
Actions. They remain dependent on shared numerical libraries, runtime behavior, and
declared mathematical conventions; passing establishes bounded reconstruction
consistency rather than an independent physical oracle. The checksum manifests bind
retained bytes to recorded SHA-256 digests and therefore detect inconsistency relative
to those manifests. A digest manifest alone is not an external trusted timestamp and
does not, without an independent commit or archival record, prove when the bytes were
created.

In this plan, **retained** means that artifacts and verification records already exist;
**planned** means that no result or scientific disposition is yet claimed; and
**blocked** means that a declared dependency or authorization is absent. Planned work
must never be cited as completed evidence.

## A.2 Planning and evidence rules

All new calculation packages must satisfy the following rules before their results can
enter the manuscript:

1. **Prospective freezing.** Freeze the parent, candidate class, parameter domain,
   alignment family, energy reference, units, training samples, withheld samples,
   scales, weights, thresholds, finite operator domain, and decision rule before
   evaluating the confirmatory evidence.
2. **No retrospective relabeling.** Preserve existing 1D and 2D artifacts byte-for-byte.
   Any thresholded extension is a new calculation package, not a reinterpretation of an
   earlier exploratory run.
3. **Separated evidence roles.** Training samples may define an admissible set. Guard and
   withheld samples diagnose conditioning or generalization only and may not update a
   threshold, witness, optimizer restart, or certificate.
4. **Bounded optimization claims.** A feasible point or multistart solution supplies an
   upper bound. Incompatibility requires a certified positive lower separation bound;
   otherwise the disposition is `INCONCLUSIVE`.
5. **Resolved operator diagnostics.** Report the global operator loss together with
   translation/block residuals, shell norms, and omitted-tail diagnostics. A global
   scalar may not conceal a weak block.
6. **Independent verification.** The verifier must reconstruct the decisive quantities
   without importing the result-producing script. It must fail closed on missing,
   malformed, or inconsistent evidence.
7. **Provenance completeness.** Retain software versions, repository revision, dirty
   state, input hashes, output hashes, figure inputs, and the exact verification
   command.
8. **Protected-action boundary.** The planned work below is synthetic and should require
   no Quantum ESPRESSO, Wannier90, remote, cluster, or cloud execution. Any later change
   that introduces protected execution requires separate human authorization.

## A.3 Work-package overview

| ID | Priority | Status | Purpose |
|---|---:|---|---|
| A0 | Immediate | Planned | Complete claim-to-artifact and figure provenance traceability |
| A1 | Highest scientific priority | Planned | Add a two-band admissible-set case with a nonidentity constrained alignment |
| A2 | Next | Planned | Extend the 1D matched/changed-route study to prospectively frozen admissible sets |
| A3 | Next | Planned | Extend the 2D coupling and shell hierarchy to thresholded operator/spectral sets |
| A4 | After A1 | Planned | Connect the composite gauge-locality attack to a constrained admissibility study |
| A5 | Final synthesis | Blocked by A0–A4 | Decide which new evidence belongs in the main text and archival package |

The ordering is intentional. M2 now supplies a current multiband alignment and locality
control. A1 addresses the remaining gap between that calculation and a prospectively
thresholded multiband admissible-set decision with certification. A2–A4 deepen
the existing central benchmarks rather than allowing the minimal direct example to
dominate the paper.

## A.4 Work package A0 — claim and figure traceability

### Inputs

- the LaTeX and Markdown manuscripts and appendices;
- all retained `result.json`, report, protocol, software, and checksum records; and
- every manuscript figure and its generating data or script.

### Actions and deliverables

- Create a numerical-claim ledger with one row per reported value, including manuscript
  location, quantity, retained source path, exact field or table row, unit, formatting
  rule, and verifier.
- Create a figure ledger recording source data, generation command, plotting script,
  output path, and SHA-256 digest.
- Record the repository revision and runtime environment for every retained calculation;
  where historical metadata are incomplete, mark the field unresolved rather than
  reconstructing an identity by inference.
- Re-run independent verifiers and checksum checks that do not invoke external
  calculators.
- Classify each item as calculated result, analytic result, diagnostic, illustrative
  plot, literature value, or proposed work.

### Completion gate

A0 is complete only when every numerical statement and figure in the paper has an
unambiguous retained source, every verifier passes, and every unresolved provenance
field is explicitly listed. Completion improves traceability but does not change the
scientific evidence class.

## A.5 Work package A1 — thresholded multiband nonidentity-alignment bridge

### Scientific question

Can the admissible-set decision logic be exercised in a small multiband model when the
operator comparison requires a known nonidentity alignment, without granting an
unrestricted unitary that can erase physically meaningful differences?

### Proposed design to freeze

The protocol should either compose the frozen M2 rank-two parent or define a new gapped
periodic two-band parent with authenticated $2\times2$ hopping blocks containing at
least two noncommuting Pauli components. It must not relabel M2's pointwise recovery or
one-global-unitary diagnostic as a completed admissible-set result. The candidate class
should retain a small number of physical hopping parameters on the same state space. A cell-local alignment family should be declared explicitly, for example

$$
C(\alpha)=\exp\!\left(-\frac{i\alpha}{2}\sigma_y\right),
\qquad \alpha\in[\alpha_{\min},\alpha_{\max}],
$$

with a frozen bounded interval and a constructed nonidentity witness in its interior.
This is a proposed design family, not a reported result. A $k$-dependent gauge is a
separate extension and must not be conflated with this cell-local coordinate alignment.
If a $k$-dependent family is later adopted, its reciprocal-boundary sewing and induced
real-space range must be specified in a new protocol.

The frozen design must include:

- a complete reciprocal mesh sufficient to distinguish every retained translation;
- disjoint training and withheld points;
- canonical physical parameters separated from the alignment parameter;
- a bounded physical-parameter box and bounded alignment interval;
- explicit spectral and globally normalized operator losses;
- translation/block and omitted-tail diagnostics;
- prospectively declared thresholds and parameter scales; and
- one compatible construction plus one controlled perturbation for which the outcome is
  allowed to be compatible, separated, or inconclusive.

### Numerical and certification strategy

1. Derive analytic invariants and exact controls where possible.
2. Use deterministic gridding or multistart local optimization only to obtain feasible
   witnesses and upper bounds.
3. Construct a rigorous lower bound with analytic inequalities, interval arithmetic, or
   branch-and-bound over the frozen parameter/alignment domain.
4. Verify spectral gauge invariance, operator covariance under the known alignment, and
   sensitivity to inadmissible rotations.
5. Evaluate withheld points only after the sets and thresholds are frozen.

### Required artifacts

Create a new package under
`calculations/ICMSEP2026/conference/paper_1/two-band-nonidentity-alignment/` containing:

- `README.md`, `input.json`, and `protocol.md`;
- a result-producing script and a separately implemented verifier;
- `result.json`, `report.md`, and machine-readable boundary/certificate data;
- at least one figure showing the physical-parameter sets and the role of the alignment
  variable without projecting away an unresolved dimension;
- `software.json` and `SHA256SUMS`.

### Completion and manuscript gate

A1 is complete only if the known nonidentity witness is recovered within the frozen
contract, block-resolved diagnostics pass, withheld results remain independent, and any
separation claim has a certified lower bound. Failure to certify a lower bound is a
valid `INCONCLUSIVE` outcome. Only after independent verification may the manuscript
claim an admissible-set instantiation with nonidentity alignment. Even then, the result
remains a two-band controlled model, not a material-relevant validation.

## A.6 Work package A2 — prospective 1D route and truncation sets

The retained 1D route comparison is a central result, but its original protocol did not
freeze admissibility thresholds. A2 should create a new package rather than modifying
that evidence.

### Planned calculation

- Freeze one finite-range candidate hierarchy and the complete-mesh parent.
- Define separate spectral sets for the matched complete-mesh objective, changed
  reciprocal weights, and restricted training region.
- Define the operator set from the same complete hopping representation over a frozen
  translation domain.
- Predeclare scales and thresholds from analytic/numerical floors plus a stated design
  resolution; do not tune them to reproduce the known coefficient defects.
- Preserve the original guard and withheld points and add new withheld points if needed
  without moving them into training.
- Map intersections or compute bounded separations for each route. Report
  `INCONCLUSIVE` wherever only an optimizer-derived upper bound is available.

### Required outputs and gate

Retain coefficient-space maps, training and withheld losses, complete-versus-truncated
hopping diagnostics, route-specific witnesses, separation bounds, and an independent
verifier. Completion should establish how objective changes alter admissibility within
the same 1D hierarchy; it must not be described as evidence that arbitrary reductions
commute or fail to commute.

## A.7 Work package A3 — 2D coupling, shells, and admissibility

A3 should preserve the two-dimensional shell hierarchy as a central result while adding
a prospectively thresholded layer.

### Planned calculation

- Treat the existing coupling sweep as pilot evidence only.
- Freeze selected coupling values and at least one new confirmatory coupling value before
  running the extension.
- Compare a declared sequence of onsite, axial, mixed-direction, and fuller shell
  classes on a complete mesh.
- Keep the $15\times15$ construction mesh and the separately evaluated withheld mesh
  logically distinct, or freeze a revised pair before execution.
- Report global spectral/operator losses, mixed-direction blocks, shell-resolved norms,
  omitted tails, symmetries, principal curvatures/masses, and conditioning.
- Map or bound admissible sets only in dimensions for which the domain and certification
  strategy are computationally explicit.

### Completion gate

A3 is complete when at least one nonseparable coupled case has independently verified
training, withheld, shell, and tail records, with no interpolation error mislabeled as
truncation error. A positive separation claim requires a certificate over the frozen
parameter box; otherwise the set relation remains `INCONCLUSIVE`.

## A.8 Work package A4 — constrained gauge-locality admissibility

The retained smooth/rough composite-frame comparison already establishes that identical
spectra and loop invariants can coexist with substantially different spread and
finite-range tails. A4 should connect that finding to the formal losses without
retrospectively converting the existing endpoints into confirmatory evidence.

### Planned calculation

- Treat the retained smooth and rough gauges as pilot cases.
- Freeze a finite, symmetry-compatible gauge family with explicit reciprocal-boundary
  sewing and no unrestricted pointwise rotations.
- Separate gauge-invariant spectral and projector diagnostics from gauge-dependent
  spread, complete hopping blocks, truncated blocks, and omitted tails.
- Declare the operator comparison domain and threshold before evaluating new gauge
  parameters; reserve at least one gauge parameter or constructed frame as withheld.
- Test whether spectral admissibility alone accepts frames that fail the declared
  operator/locality criteria, and whether an admissible alignment restores a known
  coordinate-equivalent case.
- Report the result as compatible, separated only with certification, or
  `INCONCLUSIVE`.

### Completion gate

A4 is complete only when periodicity, sewing, projector rank, and loop invariants pass;
when spread and tail conventions are fixed; and when the global operator loss is
accompanied by block/shell diagnostics. This calculation tests a controlled gauge
family, not complete space-group fidelity or material wavefunction validity.

## A.9 Work package A5 — synthesis and archival decision

After A0–A4, perform a claim-level review before changing the paper:

1. determine whether A1 merits a compact main-text subsection or remains appendix-only;
2. keep the direct scalar example as the minimal analytic illustration regardless of
   A1's outcome;
3. preserve the 1D/2D route, truncation, shell, and gauge-locality results as coequal
   central evidence;
4. update the evidence-summary table with only completed, independently verified work;
5. decide which machine-readable records and figure inputs belong in a public archive;
6. verify the intended conference or journal format and data policy; and
7. obtain explicit authorization before submission, publication, or deposition.

## A.10 Standard artifact and review contract

Every new work package should use the following minimum artifact set without moving or
rewriting existing retained files:

```text
README.md
input.json
protocol.md
run.py
result.json
verify_result.py
report.md
software.json
SHA256SUMS
```

Additional CSV/JSON certificate records and figures should be listed in the checksum
manifest. The protocol must include the exact reproduction and verification commands,
expected laptop-scale resource envelope when known, deterministic seed policy if any,
and failure dispositions. Code formatting, JSON parsing, local-link checks, checksum
verification, and independent scientific/editorial review are required before a result
is cited.

These practices follow general reproducible-computation guidance. Completing the plan
would broaden the controlled evidence and improve publication readiness; it would not,
by itself, validate silicon, establish uncertainty quantification, or authorize any
protected calculation or publication action.
