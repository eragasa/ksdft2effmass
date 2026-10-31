# Scientific claim-use audit for unmatched donor surfaces

## Scope and decision boundary

This read-only audit traces the five-scale parent-family, truncation, and refinement
surfaces that remained unmatched after [`donor-parity-audit.md`](donor-parity-audit.md).
It asks whether active scientific claims still consume those surfaces before scientific
authority decides whether they remain maintained capabilities or become Git-recoverable
historical development records.

The audit is bound to repository revision
`6cdf9e787a923f5ea565c55afcf11b1514346bdf`. It does not rerun a calculation, import the
pandas-dependent donor diagnostics, alter a retained or development result, revise a
publication claim, authorize a new execution, or retire `workflow/`.

The audit distinguishes three evidence boundaries:

1. the donor tables and development figures support sampled development claims;
2. direct v2 authenticates its own typed parent-family and scale-one truncation values;
   and
3. neither boundary silently supplies the values absent from the other.

## Bound source identities

| Source | SHA-256 |
|---|---|
| `parent-family-continuum.csv` | `1ab9a26544f70f2f53ad798f6ab61aa9f72b7f065f5dc3fa67ff84f8b5557597` |
| `parent-family-summary.csv` | `aa249ec7b19b8126e906f10ee657e79998c81980e6531440d2da2c0359c1aeb9` |
| `truncation-consequences.csv` | `84c1769c98d737f2e65e53c1ea105cca9c01e7f36c39713112c6649a2f92c40c` |
| `truncation-refinement.csv` | `bf3b3c80cc7b9ee37da00ad02735368a9b1b5b281d5af56098f77a2cc0d09b20` |
| `truncation-summary.csv` | `5c18c4d8506f0a4e54b921cb7d508862c9ed8067bf879a1fe5e403a8a15a7575` |
| `band-equivalence-locality-scientific-story.pdf` | `191d8fff0dbc777a6268c0e1e3dd481f8160da11bc9b5797510919ca9e57b2a8` |
| `parent-family-robustness-exploratory.pdf` | `c33f88d42d774e6337698426c03aa2426c10065dbbecffdde5a6067ffc8a0c60` |
| `truncation-band-consequences.pdf` | `1c7bfcd9507ab1673237df7bb8b409113a6ee44c0d432bbc11efe0b724935d67` |
| Ragasa2026a v3 `manuscript.tex` | `02c20cf087cc7272ba45bb271d617a081582514c618bc6fe1c39d389d88d74` |
| Ragasa2026a v3 `supplementary.tex` | `8b43ec4cf5cad5ecbfffe5ccdba804c47e22775a1c56d9d1f8f94d2369709a1e` |
| Prospective `experimental-protocol.tex` | `202497e62584049f92a2e0b4f5b0b11c094ede2e3445193324af1aaec43f4ab4` |

These digests establish the audited byte identities, not scientific validity or
publication readiness.

## Claim-use graph

| Development surface | Direct consumers | Active claim use | Direct-v2 coverage |
|---|---|---|---|
| Five-scale `parent-family-continuum.csv` and `parent-family-summary.csv` | `plot_scientific_story.py`, `plot_parent_family.py`, the scientific-story figure, and the exploratory robustness figure | The Ragasa2026a v3 main parent-family figure and claim-ledger items N10, N11, and N22 report behavior across five parent scales and 33 amplitudes. The prospective protocol embeds the same scientific-story figure. | Direct v2 retains independently verified final-mesh family members for all five scales, but not the donor's five adjacent-mesh refinement summaries. |
| Five-scale `truncation-consequences.csv` and `truncation-summary.csv` | `plot_truncation.py`, `plot_range_inflation_preview.py`, `plot_error_channel_decomposition.py`, and diagnostic packaging | Ragasa2026a v3 main range-inflation and error-channel figures, main numerical claims N12--N19, and supplemental truncation figures use the five-scale by 33-amplitude inventory. The prospective protocol also embeds the truncation-consequence figure. | Direct v2 authenticates 561 scale-one rows. It does not retain the other 2,244 rows at scales `0.0`, `0.25`, `0.5`, and `0.75`. |
| `truncation-refinement.csv` | `run_14_truncation_mesh_stability.py` and the donor diagnostic bundle | Ragasa2026a v3 claim N20 and the claim--evidence table state that minimum tolerance-satisfying support decisions remain unchanged at construction meshes 128, 256, and 512. | No one-to-one retained direct-v2 successor covers the five-scale threshold-adjacent refinement table. |
| Donor diagnostic implementation | `run_16_diagnostic_packaging.py`, `test__DiagnosticBundle.py`, and development-only diagnostic compositions | Publication text cites diagnostic-ledger quantities, while the calculation README keeps the bundle development-only. | Installed authenticated visualizers cover the closed direct-v2 inventory, not every development diagnostic composition. The donor's pandas and dataframe interfaces are implementation details, not scientific parity requirements. |

The main paper is not a dormant historical consumer. Its
[README](../../../../docs/publications/papers/Ragasa2026a/v3/README.md) identifies this
calculation as the authoritative source for the working Physical Review B and arXiv
revision, and its
[manuscript](../../../../docs/publications/papers/Ragasa2026a/v3/manuscript.tex) imports
calculation-owned development PDFs directly. The
[claim-and-commitment inventory](../../../../docs/publications/papers/Ragasa2026a/v3/claim-and-commitment-inventory.md)
marks N10, N15, N20, and N22 as delivered development claims. Historicalizing the
unmatched donor surfaces without revising their evidence status, ownership, and
reproduction commitments would contradict the paper's declared evidence graph.

## Other reviewed consumers

### Technical report

The calculation [technical report](technical-report/README.md) uses authenticated
direct-v2 projections. Its
parent-family figures use the retained five final-mesh members, and its truncation figure
uses the retained scale-one channel. It does not require the missing four truncation
slices or the donor's five-scale adjacent-mesh summaries. The report therefore cannot be
used as a substitute evidence source for the broader publication figures.

### Prospective protocol

The [prospective protocol](protocol/README.md) embeds the development scientific-story
and truncation figures
and states five-scale sampled conclusions. It remains a prospective design snapshot, not
a frozen retained protocol, but it is a live rebuild consumer of the unmatched surfaces.

### Research monograph

The research monograph's
[composite-band chapter](../../../../docs/publications/research-monograph/chapters/composite-band-gauge-alignment.tex)
explicitly says that it reports no M2 numerical outcome. Repository searches found no
import of the audited development
figures or table names into the monograph. Its pedagogical derivation therefore does not
require the unmatched five-scale numerical surfaces.

### Maintained code and tests

At the audited revision, the six development entrypoints and four calculation-local tests
identified by the donor parity audit were live consumers. Their scientific behaviors
required replacement or explicit disposition before donor retirement, but their
pandas-specific interfaces did not require preservation. Deleting only `workflow/` then
would have left broken maintained files.

Subsequent source migration moved five scientific producer entrypoints and three producer
composition tests to installed owners through `rank2_control_analysis.py`, without executing
or modifying the audited artifacts. It also moved diagnostic packaging and its test to
`development_diagnostics.py`: immutable standard-library CSV projections feed canonical
typed catalog and separate spectral/Hamiltonian range-decision records, and plotting
consumes those validated projections without recomputation. No maintained Python
consumer now imports `workflow/`. No donor schema extraction, dataframe compatibility
layer, or competing wire representation was introduced. This migration status does not
change the claim-use findings or evidence identities above.

## Evidence conflicts requiring explicit treatment

### Momentum disposition

Ragasa2026a v3 claim N09 and the manuscript describe the nonflat momentum study as
converged, and the main parent-family caption says that all five momentum studies through
`N=256` are converged. Those statements follow the donor's narrower development
refinement diagnostic. The installed owner includes the primitive-link Frobenius
residual in the parent diagnostic and retains
`Periodic1DRank2MomentumRefinementUnresolved`.

These are different declared semantics. Ragasa2026a v3 now states both: it explicitly
attributes the `converged` summaries to the historical donor's narrower development
diagnostic and records the installed broader outcome as unresolved because of the
primitive-link Frobenius-residual channel. Tolerance widening or omission of the
installed channel is not used to force agreement.

### Retained-execution wording

The working paper and its README formerly said that no retained execution existed for
the active rank-two calculation. They now identify the passing unsealed direct-v2
execution and bound it to its declared aggregate, including scale-one truncation. They
also state that v2 does not retroactively authenticate the full five-scale development
figures. Failed v1 remains a distinct immutable execution, and neither execution is
sealed, promoted, or publication evidence.

## Decision alternatives

### Keep the unmatched studies maintained

This option preserves the current paper scope and its five-scale sampled claims. It
requires keeping the donor tree and current result bytes recoverable while named
maintained-scope parity and the missing retained refinement/truncation evidence are
established deliberately. Any new retained calculation must receive a new execution
identity and separate authorization; direct v2 must not be rerun, extended, or relabeled.

### Make the unmatched studies historical

This option requires an explicit scientific and editorial evidence decision. The paper
could either withdraw or reduce the five-scale claims, or retain them as fixed-byte
historical development claims after revising their status, maintained-source statement,
and reproduction commitments. The six development entrypoints and four tests no longer
import the donor, but either route still requires binding exact Git recovery identities
and a new reviewed retirement audit before separately authorized donor retirement. The
tracked figures and tables need not be deleted merely
because their producing capability becomes historical, but direct v2 cannot authenticate
them by implication.

## Recommendation and decision boundary

**Recommendation: keep the unmatched five-scale studies maintained while Ragasa2026a v3
retains its current maintained-source and reproduction commitments.** They support
active, named claims and figures, including the sampled range-inflation result that the
paper identifies as a central numerical headline. Historicalization would be a
scientific and editorial evidence-status change, not a software cleanup.

Scientific authority could instead choose historicalization and either withdraw the
claims or retain them under an explicit fixed-byte historical evidence contract.

## Scientific-authority disposition

Scientific authority selected maintenance on 2026-10-31. The durable scope and evidence
boundary are recorded in
[`five-scale-maintenance-disposition.md`](five-scale-maintenance-disposition.md). The
five-scale development tables and their producing and consuming sources remain maintained
under this calculation. `workflow/` remains tracked until named installed successors,
complete maintained-scope parity, and a new reviewed retirement audit support removal.
