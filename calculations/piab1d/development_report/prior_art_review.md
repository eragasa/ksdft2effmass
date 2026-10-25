# Structured prior-art review for the PIAB1D draft preprint

- Status: working literature audit
- Search completed: 2026-10-21
- Manuscript: `development_report.tex`

## Review question

Does the prior literature already combine the following elements in one one-dimensional particle-in-a-box study?

1. a centered finite-difference Dirichlet Hamiltonian with an exact discrete eigensystem;
2. explicit separation of represented, computed, and continuum eigenpairs;
3. invariant-subspace spectral compression and exact finite reconstruction identities;
4. fixed-mode and full-spectrum dispersion diagnostics;
5. distinct semantics for matched-compression, unmatched-compression, and changed-boundary residuals;
6. model-class tests for the identifiability of an additive reduced-operator decomposition;
7. independently recomputed retained numerical evidence; and
8. a theorem-level crosswalk to machine-checked finite algebraic identities.

The question is intentionally about the combination. None of the individual ingredients is claimed to be new.

## Search protocol

### Sources searched

- Google Scholar, for relevance-ranked scholarly discovery;
- Crossref, for DOI resolution and bibliographic metadata;
- publisher landing pages, institutional repositories, author manuscripts, and arXiv, for abstracts or full text where available; and
- backward and forward citation chasing from the most relevant finite-difference, model-reduction, Hamiltonian-identification, dispersion, and formal-verification sources.

The topical search screened the first ten Google Scholar results for each query below. These are 110 result slots, not 110 unique records: duplicates occur across searches. Crossref was used as a metadata authority rather than counted as a second independent topical hit. Publisher pages that rejected automated access were not treated as negative evidence; their metadata were checked through Crossref and, where possible, an accessible repository or author copy.

### Search strings

| ID | Google Scholar query | Purpose |
|---|---|---|
| Q1 | `"particle in a box" "finite difference" eigenvalue` | Direct PIAB finite-difference studies |
| Q2 | `"Schrodinger" "finite difference" eigenvalue convergence residual` | Stationary Schrödinger discretization and solver diagnostics |
| Q3 | `"Hamiltonian" "projection-based model reduction" spectral` | Projection and structure-preserving reduction |
| Q4 | `"a posteriori error" "model order reduction" residual` | Residual-based reduced-model error estimation |
| Q5 | `"Hamiltonian identification" identifiability quantum` | Quantum-system identification and identifiability |
| Q6 | `"operator inference" Hamiltonian reduced` | Data-driven reduced-Hamiltonian inference |
| Q7 | `"finite difference" dispersion "high frequency" eigenvalue` | Nonuniform and high-frequency discrete dispersion |
| Q8 | `"formal proof" "finite difference" theorem prover Coq Lean` | Mechanized finite-difference results |
| Q9 | `"Lax equivalence theorem" Coq "finite difference"` | Formal convergence theory |
| Q10 | `"wave equation numerical resolution" mechanized proof` | End-to-end numerical-program verification |
| Q11 | `"quantum mechanics" formalization Lean Coq Isabelle` | Formal quantum-mechanics context |

The search was supplemented by an exact-title and DOI lookup when a relevant result had incomplete metadata.

### Inclusion criteria

A source was retained when it was scholarly and directly informed at least one of the eight elements, or when it established the closest identifiable neighboring research program. Journal versions were preferred over preprints. Books and surveys were retained when they supplied the standard mathematical or methodological baseline used in the manuscript.

### Exclusion criteria

The synthesis excluded results that were:

- about a physical system unrelated to the PIAB1D calibration problem;
- finite-difference applications without a relevant eigenvalue, dispersion, reduction, residual, or verification result;
- general quantum visualization resources with no bearing on the manuscript's methodological claim;
- generic machine-learning or model-reduction papers without Hamiltonian, projection, residual, or identifiability content;
- informal web explanations when a scholarly source was available; or
- duplicate preprint and journal records, for which only the journal version was retained.

A non-quantum finite-difference paper was retained only if it directly addressed the high-frequency dispersion or formal-verification boundary used in the manuscript.

## Screened evidence matrix

`Include` means the source supports the related-work synthesis. `Context` means it establishes an adjacent literature but does not support a claim that the manuscript's calculation has already been performed.

| Source | Cluster | What it establishes | Disposition |
|---|---|---|---|
| Magalhães and Vasconcelos (2006), DOI [10.1088/0143-0807/27/6/016](https://doi.org/10.1088/0143-0807/27/6/016) | PIAB education | Software-assisted visualization of infinite and finite boxes is established pedagogical practice. | Context |
| Halpern, Ge, and Glendening (2022), DOI [10.1021/acs.jchemed.2c00557](https://doi.org/10.1021/acs.jchemed.2c00557) | Schrödinger finite differences | A one-dimensional finite-difference solver can be used to obtain and visualize energies and wavefunctions for the box and other potentials. | Include |
| Strikwerda (2004), DOI [10.1137/1.9780898717938](https://doi.org/10.1137/1.9780898717938) | Finite differences | Standard consistency, stability, and convergence framework for finite-difference schemes. | Include |
| Horn and Johnson (2013), DOI [10.1017/CBO9781139020411](https://doi.org/10.1017/CBO9781139020411) | Matrix analysis | Standard finite-dimensional spectral and projector identities. | Include |
| Golub and Van Loan (2013), ISBN 978-1-4214-0794-4 | Numerical linear algebra | Standard symmetric-eigensolver and residual context. | Include |
| Benner, Gugercin, and Willcox (2015), DOI [10.1137/130932715](https://doi.org/10.1137/130932715) | Projection-based reduction | Projection-based model reduction is a mature field with explicit trial/test spaces and error questions. | Include |
| Peng and Mohseni (2016), DOI [10.1137/140978922](https://doi.org/10.1137/140978922) | Hamiltonian reduction | Structure preservation is a central concern in reduced Hamiltonian dynamics. | Include |
| Feng, Chellappa, and Benner (2024), DOI [10.1186/s40323-024-00260-8](https://doi.org/10.1186/s40323-024-00260-8) | Residual error estimation | Reduced-model residuals can support a posteriori error estimators when accompanied by the required analytical assumptions. | Include |
| Sharma, Wang, and Kramer (2022), DOI [10.1016/j.physd.2021.133122](https://doi.org/10.1016/j.physd.2021.133122) | Hamiltonian operator inference | Reduced Hamiltonian operators can be inferred nonintrusively while preserving declared structure. | Include |
| Kramer, Peherstorfer, and Willcox (2024), DOI [10.1146/annurev-fluid-121021-025220](https://doi.org/10.1146/annurev-fluid-121021-025220) | Operator inference | Operator inference connects learned reduced operators to projection-based reduction theory. | Context |
| Le Bris, Mirrahimi, Rabitz, and Turinici (2007), DOI [10.1051/cocv:2007013](https://doi.org/10.1051/cocv:2007013) | Quantum Hamiltonian identification | Hamiltonian identification is an inverse problem with explicit well-posedness and numerical questions. | Include |
| Zhang and Sarovar (2014), DOI [10.1103/PhysRevLett.113.080401](https://doi.org/10.1103/PhysRevLett.113.080401) | Quantum Hamiltonian identification | Measurement time traces can be used to identify parameters under declared observability conditions. | Context |
| Sone and Cappellaro (2017), DOI [10.1103/PhysRevA.95.022335](https://doi.org/10.1103/PhysRevA.95.022335) | Quantum identifiability | Probe design and accessible measurements constrain Hamiltonian identifiability. | Context |
| Wang et al. (2020), DOI [10.1109/TAC.2020.2973582](https://doi.org/10.1109/TAC.2020.2973582) | Quantum identifiability | Similarity transformations characterize identifiability in a dynamical system-identification setting. | Include |
| Zuazua (2005), DOI [10.1137/S0036144503432862](https://doi.org/10.1137/S0036144503432862) | Discrete dispersion | Finite-difference convergence need not be uniform over high-frequency modes; spurious discrete behavior can survive mesh refinement. | Include |
| Boldo et al. (2013), DOI [10.1007/s10817-012-9255-4](https://doi.org/10.1007/s10817-012-9255-4) | Formal numerical verification | A finite-difference PDE solver can be mechanized from mathematical error analysis through a C program. | Include |
| Boldo et al. (2014), DOI [10.1016/j.camwa.2014.06.004](https://doi.org/10.1016/j.camwa.2014.06.004) | Formal numerical verification | End-to-end trust requires additional reasoning beyond exact mathematical identities. | Include |
| Tekriwal, Duraisamy, and Jeannin (2021), DOI [10.1007/978-3-030-76384-8_20](https://doi.org/10.1007/978-3-030-76384-8_20) | Formal convergence theory | The Lax equivalence theorem for finite-difference schemes has been formalized in Coq. | Include |

## Synthesis by claim boundary

### Standard material

The continuum PIAB spectrum, the centered three-point stencil, the sine eigenvectors of the Dirichlet tridiagonal matrix, orthogonal spectral projection, and second-order fixed-mode convergence are standard. The manuscript must not present any of these as new mathematics. The educational PIAB literature and the one-dimensional finite-difference literature already cover computation and visualization of box eigenstates.

### Closest model-reduction literature

Projection-based reduction and Hamiltonian structure preservation are mature topics. Residual-based error estimation is also mature, but those estimators rely on a governing problem and analytical constants that give a residual norm an error-bound meaning. In the manuscript's invariant-eigenspace case, spectral compression is exact for the finite matrix. Its residual matrices are therefore used primarily to distinguish the operators being compared, not advertised as general a posteriori error bounds.

### Closest identification literature

Quantum Hamiltonian identification normally asks whether unknown dynamical parameters can be recovered from specified controls and measurements. Hamiltonian operator inference learns reduced dynamics from data under structural constraints. The manuscript asks a narrower and different question: whether a known finite reduced matrix uniquely determines an additive decomposition when the admissible component classes are varied. The exact nonuniqueness result is algebraic and does not establish or refute dynamical identifiability in the cited inverse-problem literature.

### Closest dispersion literature

High-frequency nonuniformity under finite-difference refinement is well known. The manuscript specializes that general warning to the exact stationary PIAB1D eigenvalue formula and displays fixed-index convergence beside fractional-index nonconvergence. The contribution is the role this contrast plays in the integrated calibration, not discovery of numerical dispersion.

### Closest formal-verification literature

The formal numerical-analysis literature includes proofs of convergence theorems and end-to-end verification from PDE discretization to executable code. The manuscript's Lean artifact has a smaller boundary: it checks exact finite algebraic identities used by the diagnostic interpretation. It does not verify the Python implementation, binary64 execution, plots, JSON files, or continuum limit. This narrower claim must remain explicit.

## Bounded novelty conclusion

No source in the screened record combines all eight review elements in a single PIAB1D calibration study. The defensible contribution is therefore the **integration and evidence separation**: a reproducible reference calculation that puts exact finite spectral algebra, continuum dispersion, residual semantics, model-class identifiability, independent numerical recomputation, and a machine-checked theorem crosswalk into one audit trail.

This search does **not** justify an unqualified priority claim such as “the first treatment.” It is a relevance-ranked structured search rather than an exhaustive multilingual or citation-index export, and negative search results cannot prove absence. The manuscript should say that the combination was not found in the screened literature and should identify its contribution as methodological integration, not new PIAB mathematics, a new projection algorithm, a new convergence theorem, or a general solution to Hamiltonian identification.

## Residual limitations

- Google Scholar relevance ranking is dynamic and not independently reproducible byte-for-byte.
- Several publisher pages rejected automated retrieval; DOI metadata and accessible repository copies were used instead.
- Search strings were English-language and therefore do not establish global priority.
- The review did not include a cited-reference database export suitable for a PRISMA flow diagram.
- The 2026 search cutoff includes recent preprints that may later receive revised titles or journal versions; journal versions were preferred whenever already available.
