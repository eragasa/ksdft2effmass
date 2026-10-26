# Legacy QHO1D disposition

## Status and scope

This page records the non-destructive maintenance disposition for the QHO1D surfaces
that predate the direct typed calculate → verify → render lifecycle. It does not
authorize deletion, byte rewriting, API removal, execution sealing, publication, or a
release.

The direct successor is authoritative for new calculations:

```text
calculations/qho1d/run_01_calculation.py
  → run_02_verification.py
  → run_03_render.py
```

The predecessor remains a historical reproduction and compatibility surface. It is not
an alternative architecture for new work.

## Audited surfaces

| Surface | Existing role | Current consumers | Disposition |
|---|---|---|---|
| `calculations/qho1d/input.json` | JSON-authored `qho1d.development.v1` sweep | `dev_analysis.py`, `dev_plots.py`, study tests | Retain exact bytes; frozen for historical reproduction; no new callers. |
| `dev_analysis.py`, `dev_verification.py`, `dev_plots.py` | Predecessor generation, verification, and plotting adapters | Development-report reproduction | Retain; maintenance-only; do not extend with successor behavior. |
| `analysis/development/.gitignore` | Keeps replaceable predecessor outputs untracked | Predecessor scripts | Retain. Generated files remain non-evidence and must not be committed implicitly. |
| `development_report/` | Buildable predecessor review snapshot | Historical review and provenance | Retain exact committed source, PDF, bibliography, and figures. Do not update it into the successor report. |
| `model_systems/qho1d/study/` | Closed version-one study records, JSON input, custom result wire, and retained-result verifier | Predecessor scripts, tests, root re-exports, research-monograph aliases | Keep supported for historical reproduction and compatibility; bug- and security-fix only. |
| QHO1D root re-exports | Historical public import compatibility | Tests and possible external consumers | Retain until an announced breaking release and caller audit authorize removal. |
| `campaigns.research_monograph` aliases | Historical locator compatibility | Research-monograph API and tests | Retain; do not add new aliases. |
| `study/` tests | Software evidence for the predecessor contract | Bounded test suite | Retain. Artifact-dependent tests may skip explicitly when the rejected historical calculation tree is absent. |

## Boundary between predecessor and successor

The predecessor and successor currently declare the same nondimensional parameters and
ordered sweep:

- `hbar = mass = omega = 1`;
- box half-widths `(4.0, 6.0, 8.0)`;
- requested grid spacings `(0.2, 0.1, 0.05)`; and
- retained dimensions `(2, 4, 6)`.

That equality does not make their records or wires interchangeable. The successor also
declares the selected state-resolved case, retains typed arrays and quantities through
the shared serialization boundary, records the full-space residual, independently
verifies 468 named comparisons, and authenticates the exact visualization projection.
The predecessor owns a repository-bound custom JSON wire with `.tolist()` matrix
transport and source-path identities. That wire is a historical exception, not a
pattern permitted for successor development.

No adapter shall translate a predecessor result into a successor result and present it
as newly calculated. Reproduction must run the owning calculation route or preserve the
original bytes and identity.

## Selected capability migration

The explicit adjacent-grid coarse-minus-fine Frobenius diagnostic is the only
predecessor capability selected for the direct successor. The successor implements it
from its own typed calculation results, uses the canonical PhysKit Frobenius norm, and
verifies the derived values without importing or adapting the legacy study package.

No other predecessor capability is selected for migration. In particular, the
JSON-authored scientific input, custom plain-JSON wire, repository-coupled result
verifier, executable request objects, replaceable fixed-path execution behavior, and
historical aliases remain predecessor-only compatibility or provenance surfaces.
Retention of those historical files does not make them maintained successor features.

## Exact-byte audit observations

At merge commit `0433d9c4e20eaa99afed40f14332e49301eaf9cc`, the principal predecessor
identities are:

| Path | SHA-256 |
|---|---|
| `calculations/qho1d/input.json` | `93d8d987bc18320402eb0a2beabde829a51a5f43f6aefdf291cfcf9fea03b9d9` |
| `calculations/qho1d/dev_analysis.py` | `def531aa1ad7c74e5879c7f476808ef9a04b813cc95041d3677e9c4805363913` |
| `calculations/qho1d/dev_verification.py` | `c164e92477147be955d36d91bfa9eafef030cd46063e5a8255f4ca9fed625fc6` |
| `calculations/qho1d/dev_plots.py` | `c6ea9c676100181080daabfe4cd782cbd39759c6bc27cf90436b86e3c06219d6` |
| `development_report/development_report.tex` | `11fa387a02342c1035cc051de15c5cb44501dadeab84202a9834b2417d2de9b5` |
| `development_report/development_report.pdf` | `b4bf3897aef9a9c5a2d57f4fa42eebe5a27afabe4485b56a43b8ae44903e232d` |

The ignored local predecessor result was read-only verified successfully during this
audit and had SHA-256
`1bc17c2911ede0d679af080442a7331a18972213f9ad464a4f6fb6937d2f961a`.
This observation identifies replaceable local development bytes only; it does not make
them retained evidence.

Two predecessor report-local figures are byte-identical to successor figures:
`qho1d-eigenstates.png` and `qho1d-eigenstate-distortion.png`. The diagnostics figures
are not byte-identical because the successor rendering changes the authenticated
projection and presentation. Figure identity does not establish result-wire identity.

## Known historical report qualification

The predecessor report source embeds result SHA-256
`e22e83398b7f77d1ad3717e6789da30847092af5eebf5af4ebe9c7f7d57ac25d`, while its
README associates the retained report-local figures with result SHA-256
`1bc17c2911ede0d679af080442a7331a18972213f9ad464a4f6fb6937d2f961a`.
The current ignored result has the latter identity and passes the predecessor verifier.

Therefore the retained predecessor PDF is a historical review snapshot whose embedded
result-digest statement must not be used as an exact correlation to the current ignored
result or report-local figures. This page is the additive qualification. The report
source, PDF, and figures are not silently rewritten because doing so would create new
bytes under an old review identity.

## Maintenance rules

1. New QHO1D calculations, documentation examples, and visualizations use the direct
   successor only.
2. Predecessor files remain readable and testable but receive no new scientific
   features, schemas, aliases, or generic serialization code.
3. Do not add deprecation warnings to predecessor execution paths. Warnings would alter
   retained reproduction behavior without removing ambiguity for external callers.
4. A necessary correctness or security fix must state which historical result hashes
   cease to verify and must not rewrite retained report bytes in place.
5. The predecessor custom serializer remains local to `study/`; it must not be imported
   by the successor or copied to another model system.
6. The absent `calculations/research-monograph/harmonic-oscillator/` tree remains absent.
   Do not restore it merely to execute one conditional historical-identity test.
7. No predecessor artifact is sealed, released, or scientifically validated by this
   disposition.

## Removal gates

Removal or relocation is not currently recommended. A future proposal must satisfy all
of the following before requesting destructive authorization:

1. inventory repository and known external consumers of every QHO1D root export and
   `campaigns.research_monograph` alias;
2. provide test-owned compact fixtures for any historical wire behavior still claimed;
3. announce the breaking public-import change in an appropriate versioned release plan;
4. identify every retained artifact or report whose provenance names a removed path;
5. provide an exact migration map or explicitly preserve the historical source at its
   existing path; and
6. obtain human authorization for deletion and any evidence-identity migration.

Until those gates are met, the correct action is retention plus clear documentation,
not compatibility wrappers, wire conversion, or deletion.
