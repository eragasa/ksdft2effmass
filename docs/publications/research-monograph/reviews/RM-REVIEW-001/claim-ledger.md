# RM-REVIEW-001 claim ledger

## Status and use

This is a preliminary planning ledger. Every row below is `SEEDED`: it identifies
a claim family that review must inventory, not a claim that has been accepted,
verified, validated, or completely located.

During packet preparation, each substantive claim receives an exact source
location, rendered page, class, evidence owner, conventions, reviewer, and
review state. Claims must be split when one sentence combines assertions with
different evidence owners or statuses.

## Claim classes

Use one primary class per ledger row:

- `DEFINITION`;
- `DERIVATION_OR_PROOF`;
- `LITERATURE_CLAIM`;
- `CALCULATED_RESULT`;
- `SYNTHETIC_OR_ILLUSTRATIVE_RESULT`;
- `SOFTWARE_CAPABILITY`;
- `PROPOSED_WORK`;
- `LIMITATION_OR_NONCLAIM`;
- `EDITORIAL_OR_PEDAGOGICAL_CLAIM`.

## Review states

- `SEEDED` — planning pointer, not fully inventoried;
- `INVENTORIED` — exact claim and owner recorded;
- `UNDER_REVIEW`;
- `REVISION_REQUIRED`;
- `HUMAN_DECISION_PENDING`;
- `SUPPORTED_FOR_STATED_SCOPE`;
- `INCONCLUSIVE`;
- `SUPERSEDED`.

`SUPPORTED_FOR_STATED_SCOPE` is a bounded review state. It does not upgrade the
scientific evidence class of the underlying claim.

## Seeded central claims

| Claim ID | Claim family to inventory | Primary class | Packet | Expected evidence owner | State |
|---|---|---|---|---|---|
| `RM-CL-001` | Operators are compared only after state spaces and applicable basis, gauge, geometry, spin, unit, and energy-reference conventions are identified. | `DEFINITION` | `RM-P01`, `RM-P04`, `RM-P08` | specification and mathematical derivation | `SEEDED` |
| `RM-CL-002` | Exact spectral retention, eliminated-space downfolding, block decoupling, localization, and finite-range truncation are distinct operations with distinct consequences. | `DERIVATION_OR_PROOF` | `RM-P02`, `RM-P03`, `RM-P08` | derivation plus cited literature | `SEEDED` |
| `RM-CL-003` | Exact retained spectral information does not generally imply exact finite hopping support after projection. | `DERIVATION_OR_PROOF` | `RM-P02`, `RM-P03` | explicit counterexample plus literature context | `SEEDED` |
| `RM-CL-004` | Model adequacy requires one common candidate satisfying declared spectral and operator criteria, rather than unrelated optima in the two channels. | `DEFINITION` | `RM-P04` | model-adequacy contract | `SEEDED` |
| `RM-CL-005` | Failure of an optimization search is not an infeasibility certificate; a separation claim requires an applicable global bound or certificate. | `LIMITATION_OR_NONCLAIM` | `RM-P04`, `RM-P09` | certificate contract and retained records | `SEEDED` |
| `RM-CL-006` | The historical M1 calculation provides bounded synthetic reconstruction and withheld-evaluation evidence under its retained maximum-error contract. | `SYNTHETIC_OR_ILLUSTRATIVE_RESULT` | `RM-P09` | `calculations/ICMSEP2026/conference/paper_1/isolated-band/` | `SEEDED` |
| `RM-CL-007` | The historical M3 calculation retains a bounded common witness and finite-family separation certificate under its frozen contract. | `SYNTHETIC_OR_ILLUSTRATIVE_RESULT` | `RM-P04`, `RM-P09` | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/` | `SEEDED` |
| `RM-CL-008` | The periodic and impurity controls are bounded synthetic or illustrative evidence and do not establish material validity for silicon. | `LIMITATION_OR_NONCLAIM` | `RM-P05`, `RM-P06`, `RM-P09`, `RM-P10` | retained calculations and evidence-boundary chapter | `SEEDED` |
| `RM-CL-009` | The project does not yet support the production material parent, Wannier operator, impurity operator, crossover, silicon validation, or uncertainty-quantification claims excluded by the current evidence boundary. | `LIMITATION_OR_NONCLAIM` | `RM-P05`, `RM-P06`, `RM-P07` | current evidence owners and calculation inventory | `SEEDED` |
| `RM-CL-010` | Prospective M1v2, M3v2, bulk-silicon, doped-silicon, and proof work remains proposed until separately specified, implemented, executed where authorized, retained, and reviewed. | `PROPOSED_WORK` | `RM-P05`, `RM-P06`, `RM-P07`, `RM-P09` | proposal text and owning future records | `SEEDED` |
| `RM-CL-011` | Passing manuscript, software, or standalone artifact checks does not establish exact original-producer replay when historical source bytes are unavailable. | `LIMITATION_OR_NONCLAIM` | `RM-P03`, `RM-P04`, `RM-P09` | source manifests and provenance records | `SEEDED` |
| `RM-CL-012` | The narrative is accessible to numerate undergraduate physics majors while preserving the mathematical and scientific distinctions needed by later specialist chapters. | `EDITORIAL_OR_PEDAGOGICAL_CLAIM` | all packets | human audience readers | `SEEDED` |

## Required row expansion

Before a packet enters `HUMAN_READING`, its seeded families must be expanded into
atomic claims with:

| Field | Required content |
|---|---|
| Claim identifier | Stable campaign-local identifier |
| Exact wording | One reviewable assertion |
| Location | Source path and line plus candidate PDF page |
| Class | One primary claim class |
| Scientific status | Calculated, literature, expected, illustrative, synthetic, placeholder, or proposed, as applicable |
| Evidence owner | Specification, paper, calculation, proof, software contract, or human audience observation |
| Conventions | State space, basis, gauge, units, energy reference, geometry, thresholds, and roles as applicable |
| Human reviewer | Identified reviewer and qualification role |
| Review state | One claim-ledger state |
| Findings | Stable finding identifiers |
| Revision candidate | Candidate version containing the reviewed wording |
