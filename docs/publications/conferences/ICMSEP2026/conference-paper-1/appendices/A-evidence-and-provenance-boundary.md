# Appendix A. Evidence, Provenance, and Controlled-Calculation Plan

## A.1 Purpose and status boundary

This appendix serves two purposes:

1. it identifies the retained evidence supporting the present manuscript; and
2. it distinguishes the completed M3 constrained-alignment bridge from the remaining
   prospective calculations needed to extend the framework.

The maintained evidence is retained under:

| Location | Present role | Status and claim boundary |
|---|---|---|
| `calculations/ICMSEP2026/conference/paper_1/isolated-band/` | Prospectively frozen M1 parent refinement, lowest-band extraction, complete hopping reconstruction, finite-range truncation, matched-route comparison, and withheld evaluation | Retained controlled numerical-verification evidence; its historical identity does not substitute for a gap or isolation result, it excludes historical stress channels, and it is not a thresholded admissible-set map |
| `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` | Prospectively frozen M2 gapped rank-two parent, known periodic gauge attack, pointwise and global-unitary alignment channels, block-hopping locality, and withheld evaluation | Retained controlled numerical-verification evidence; not a general alignment solver or thresholded admissible-set map |
| `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/` | Prospectively frozen M3 two-parameter rank-two admissible sets over nine one-global-rotation components, including a common witness and a finite-component separation certificate | Retained controlled numerical-verification evidence for the frozen finite family only; not an unrestricted alignment result, physical threshold calibration, or material validation |
| `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/` | Post-hoc analytic reanalysis of the sealed M3 quadratics at fixed spectral threshold | Exploratory sensitivity evidence only; not part of the prospective M3 confirmatory package |
| `calculations/research-monograph/periodic-2d/` | Coupling and shell hierarchy, projector/loop controls, gauge-locality comparison, and withheld-mesh diagnostics | Retained controlled numerical-verification evidence; not material or wavefunction validation |
| `calculations/ICMSEP2026/conference/paper_1/` | Minimal scalar admissible-set illustration with an exact witness and certified separation | Retained analytic/numerical evidence for the frozen two-parameter identity-alignment contract only |

Each retained directory contains, as applicable, its protocol, input and result records,
independent verification code, figures, report, software record, and checksum manifest.
The evidence is classified as controlled illustrative software and numerical
verification. It is not a public data deposit, DOI, material validation, statistical
uncertainty analysis, or evidence that a general alignment problem has been solved.
Historical external executions are not rerun by the manuscript.

The standalone M1, M2, and M3 retained verifiers decode the frozen JSON documents and
reconstruct their finite protocols without importing the corresponding producer
Actions. The separate threshold-sensitivity verifier reconstructs its analytic grid
from the source quadratics after checking both the source-result digest and its exact
entry in the source package manifest. These verifiers remain dependent on shared
numerical libraries, runtime behavior, and declared mathematical conventions; passing
establishes bounded reconstruction consistency rather than an independent physical
oracle. The checksum manifests bind
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
| A1 | Highest scientific priority | Completed as M3 | Add a rank-two admissible-set case with a nonidentity constrained alignment |
| A2 | Next | Planned | Extend the 1D matched/changed-route study to prospectively frozen admissible sets |
| A3 | Next | Planned | Extend the 2D coupling and shell hierarchy to thresholded operator/spectral sets |
| A4 | After A1 | Planned | Connect the composite gauge-locality attack to a constrained admissibility study |
| A5 | Final synthesis | Blocked by A0 and A2–A4 | Decide which remaining new evidence belongs in the main text and archival package |

The ordering is intentional. M2 supplies the multiband alignment and locality control,
and completed M3 supplies a prospectively thresholded rank-two admissible-set decision
with finite-component certification. A2–A4 remain planned extensions of the central
benchmarks rather than evidence already established by M3.

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

## A.5 Work package A1 — completed M3 constrained-alignment bridge

### Scientific question and disposition

A1 asked whether the admissible-set decision logic could be exercised in a small
multiband model when operator comparison requires a known nonidentity alignment, without
granting an unrestricted unitary. M3 answers that bounded question for a rank-two
synthetic baseline, a two-parameter candidate rectangle, and nine frozen one-global
real rotations. It does not solve a continuous or $k$-dependent alignment problem.

### Retained design and result

M3 composes the frozen M2 baseline rather than relabeling M2's pointwise recovery. Its
64 training points determine analytic spectral and operator-loss quadratics, while 257
disjoint staggered points are evaluation-only. The parameter order, compact domain,
energy scale, normalized losses, thresholds, locality ranges, separation resolution,
and finite alignment angles were prospectively frozen.

At spectral/operator thresholds `0.03/0.33`, the point `(0, 1)` with a nonidentity
selected rotation is a retained common witness. At thresholds `0.03/0.31`, the finite
component construction retains equal lower and upper separation bounds
`0.099467401027216296`, above the frozen resolution `0.05`. The certificate applies
only to the feasible components of the declared finite family and its unclipped
positive-definite quadratic ellipsoids.

### Artifacts and verification boundary

The completed package is
`calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/`. It contains
the editable configuration, deterministic input builder, prospective freeze, amendment
chain, producer, result, library and standalone verification records, figure data,
report, software record, source manifest, and package checksum manifest. The standalone
verifier reconstructs roles, controls, quadratics, evaluations, locality diagnostics,
and certificate quantities without importing the producer Actions. A separate post-hoc
package varies only the operator threshold and is not part of the confirmatory M3
protocol.

A1 is therefore complete as bounded synthetic numerical-verification evidence. It is
not physical threshold calibration, material validation, uncertainty quantification,
or evidence for unrestricted alignment families. Any future continuous or
$k$-dependent alignment study requires a new prospectively frozen protocol.

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
