# RM-REVIEW-001 packet map

## Status

All packets are `PLANNED`. Page ranges, human assignments, and candidate
identifiers remain pending until candidate freeze. The source boundaries below
follow the composition at proposed baseline `2f30d7a3`; they must be reconciled
against the selected candidate before any packet enters `BRIEF_READY`.

## Main-text packets

### RM-P01 — quantities, representations, eigensystems, and quantum operators

**Sources**

- `chapters/preface.tex`
- `chapters/computational-quantities.tex`
- `chapters/finite-representations.tex`
- `chapters/hermitian-eigensystems.tex`
- `chapters/quantum-states-and-operators.tex`

**Dependencies:** none within the manuscript.

**Primary review focus:** declared audience, notation foundations, continuum and
finite-operator separation, eigensystem reasoning, and the first complete
pedagogical progression.

### RM-P02 — dimensions, periodic geometry, discretization, and projection

**Sources**

- `chapters/particle-in-a-box-higher-dimensions.tex`
- `chapters/periodic-geometry.tex`
- `chapters/bloch-periodic-finite-differences.tex`
- `chapters/projection-and-retained-spaces.tex`

**Dependencies:** `RM-P01`.

**Primary review focus:** tensor products, geometry conventions, Bloch seams,
sparse representations, spectral restriction, eliminated-space downfolding,
block decoupling, and finite-range versus decay claims.

### RM-P03 — periodic reduction, composite gauges, and evidence vocabulary

**Sources**

- `chapters/isolated-band-fourier-reduction.tex`
- `chapters/composite-band-gauge-alignment.tex`
- `chapters/verification-and-evidence-vocabulary.tex`

**Dependencies:** `RM-P01`, `RM-P02`.

**Primary review focus:** isolated and composite retained spaces, Fourier
reconstruction and truncation, gauge transport and alignment, locality,
training and withheld roles, and evidence terminology.

### RM-P04 — model adequacy, common-space comparison, and certificates

**Sources**

- `chapters/model-adequacy.tex`
- `chapters/operator-comparison.tex`
- `chapters/admissible-sets-and-certificates.tex`
- `chapters/evidence-for-model-adequacy.tex`

**Dependencies:** `RM-P01`, `RM-P02`, `RM-P03`.

**Primary review focus:** state-space identification, spectral and operator
losses, candidate and alignment families, common witnesses, separation
certificates, threshold ownership, and the boundary between fitting precedent
and the manuscript's claimed contribution.

### RM-P05 — bulk-silicon representation program

**Sources**

- `chapters/bulk-silicon-program.tex`
- `chapters/first-principles-bulk-parent.tex`
- `chapters/bulk-representations.tex`
- `chapters/bulk-reduced-models.tex`
- `chapters/selecting-bulk-representation.tex`

**Dependencies:** `RM-P02`, `RM-P03`, `RM-P04`.

**Primary review focus:** parent-model assumptions, pseudopotential and
convergence boundaries, Bloch and Wannier representations, reduction routes,
model-class selection, and the distinction between completed controls and the
proposed silicon program.

### RM-P06 — doped-silicon and impurity program

**Sources**

- `chapters/doped-silicon-program.tex`
- `chapters/impurity-operator-extraction.tex`
- `chapters/lattice-impurity-models.tex`
- `chapters/continuum-effective-mass.tex`
- `chapters/structured-learning.tex`
- `chapters/dopant-transferability.tex`
- `chapters/current-evidence-boundary.tex`

**Dependencies:** `RM-P04`, `RM-P05`.

**Primary review focus:** defect-minus-bulk alignment, impurity model classes,
continuum transition, structured-learning claims, phosphorus-to-boron transfer,
and the current evidence boundary.

### RM-P07 — proof program, conclusions, and global claims

**Sources**

- the title-page status and abstract in `manuscript/manuscript.tex`
- `chapters/proof-architecture.tex`
- `chapters/finite-dimensional-foundations.tex`
- `chapters/mathematics-of-reduction.tex`
- `chapters/mechanization-status.tex`
- `chapters/conclusions.tex`

**Dependencies:** `RM-P01` through `RM-P06`, plus appendix packets where cited.

**Primary review focus:** proof obligations and status, analytical reduction
claims, mechanization boundaries, and agreement among the title, abstract,
evidence boundary, body, and conclusions.

## Appendix packets

### RM-P08 — notation and operator foundations

**Sources**

- `appendices/A-notation-and-status.tex`
- `appendices/B-hilbert-schmidt-and-frobenius.tex`
- `appendices/C-operator-spaces-compression-alignment.tex`

**Dependencies:** `RM-P01` through `RM-P04`.

**Primary review focus:** consistency with main-text definitions and conventions,
finite-dimensional operator geometry, compression, alignment, and downfolding.

### RM-P09 — controlled numerical and periodic reductions

**Sources**

- `appendices/D-particle-in-a-box-residuals.tex`
- `appendices/E-harmonic-oscillator-comparison.tex`
- `appendices/F-bulk-silicon-reduction-routes.tex`
- `appendices/G-one-dimensional-reduction.tex`
- `appendices/H-two-dimensional-wannier-reduction.tex`

**Dependencies:** `RM-P01` through `RM-P05`, `RM-P08`.

**Primary review focus:** numerical provenance, dimensional versus normalized
metrics, M1/M2/M3 historical contracts, witness and certificate semantics,
negative evidence, and route-comparison boundaries.

### RM-P10 — impurity, envelope theory, literature, and optional silicon status

**Sources**

- `appendices/I-impurity-effective-mass-models.tex`
- `appendices/J-two-dimensional-defect-extraction.tex`
- `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex`
- `appendices/L-candidate-contemporary-literature.tex`
- `appendices/M-preliminary-silicon-work.tex`, only if the candidate decision
  includes it

**Dependencies:** `RM-P04`, `RM-P05`, `RM-P06`, `RM-P08`, `RM-P09`.

**Primary review focus:** synthetic impurity controls, proposed two-dimensional
work, envelope-theory interpretation, unresolved literature review, and—if
included—the bounded status of preliminary silicon evidence.

## Cross-cutting surfaces

The following are not substitutes for packet review but support all packets:

- `references.bib` and `citation-audit.md`;
- `navigation-index.md`;
- `current-library-capability-crosswalk.md`;
- `extraction-map.md`;
- applicable specifications and proof packages;
- `calculations/README.md` and retained calculation packages; and
- applicable software contracts and verification records.

## Cross-cutting human gates

After packet review, named humans must complete:

1. notation and definition consistency review;
2. logical and pedagogical dependency review;
3. literature, novelty, and contribution-boundary review;
4. numerical, figure, and table provenance review;
5. evidence-status and current-capability review;
6. abstract/body/conclusion reconciliation;
7. adversarial central-claims review; and
8. a sequential whole-manuscript read of the final candidate.

## Assignment table

| Packet | State | Primary reader | Scientific reviewer | Mathematical/numerical reviewer | Audience reader | Candidate |
|---|---|---|---|---|---|---|
| `RM-P01` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P02` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P03` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P04` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P05` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P06` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P07` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P08` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P09` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
| `RM-P10` | `PLANNED` | unassigned | unassigned | unassigned | unassigned | not frozen |
