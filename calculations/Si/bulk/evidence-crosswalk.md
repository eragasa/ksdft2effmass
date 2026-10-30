# Bulk-silicon evidence crosswalk

This crosswalk links existing records without transferring their identity or evidence
status into this calculation root.

| Source | Evidence class | Permitted use | Excluded use |
|---|---|---|---|
| [`calculations/bulk-silicon/materials-project/`](../../bulk-silicon/materials-project/) | External reference snapshot | Structure/catalog correlation and provenance reference | Production input or project calculation |
| [`qe-example01-si-scf-davidson/`](../../bulk-silicon/qe-example01-si-scf-davidson/) | Human-accepted tutorial reproduction | QE execution, parsing, and compact-provenance precedent | Production convergence, material validation, or model selection |
| [`qe-example01-si-bands-davidson/`](../../bulk-silicon/qe-example01-si-bands-davidson/) | Tutorial band-path calculation awaiting review | Band-output and extraction precedent | Valley location, effective mass, Wannier, or production evidence |
| [`qe-7.5-si-scf-smoke-comparison/`](../../bulk-silicon/qe-7.5-si-scf-smoke-comparison/) | Bounded smoke comparison | Mechanical cross-version comparison | Accepted executable migration or physical validation |
| [`production-convergence-preflight/`](../../bulk-silicon/production-convergence-preflight/) | Audited provisional finite-setting numerical evidence | Labelled downstream development and exploratory analysis under the successor [provisional-use disposition](provisional-use-disposition.md), plus planning of an exact mixed-corner successor | Accepted production cutoff/mesh, infinite-basis convergence, publication-grade validation, valley or mass convergence |
| [`projectkoios-simulations@bbb9f1d` retained QE SCF grid](https://github.com/eragasa/projectkoios-simulations/tree/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/examples/projectkoios/integrations/quantumespresso/pw/scf/Si/primitive/convergence/joint/evidence) | External provider-software evidence on a different structure/pseudopotential/settings branch | Exact-byte authentication, parsing, replay, warning-inventory, and software-contract development | Transfer of convergence, lattice, pseudopotential, toolchain acceptance, valley, mass, or Wannier evidence into this calculation |
| [`silicon-wannier-kinetic-preview/` at historical revision `8d75f7ca`](https://github.com/eragasa/ksdft2effmass/tree/8d75f7ca6c590d9cd3c98fcbfc0a15579696b59b/calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview) | Read-only tutorial-scale extraction retained in repository history after removal of the superseded tree from the current branch | Wannier90 interface and presentation precursor | Production Wannier parent or membership in Paper D admissible sets |
| [`bulk-silicon-production-convergence-design.md`](../../../docs/computational/bulk-silicon-production-convergence-design.md) | Scientific design and source audit | Exact parameter rationale, artifact identities, criteria, and protected-execution gates | Evidence that proposed successors were executed |
| [`Ragasa2026d/v1/appendices/`](../../../docs/publications/papers/Ragasa2026d/v1/appendices/) | Pre-results publication planning | Claim/evidence requirements and manuscript crosswalk | Calculation authority or completed results |

## Retained-path policy

Historical repository-relative paths embedded in JSON, Markdown, scripts, manifests,
and provenance records remain unchanged. Moving or rewriting those bytes would create a
new evidence version rather than reorganize ownership. New work references the records
at their historical locations and receives a new identity under `calculations/Si/bulk/`
only after its own contract exists.

## Physical non-transfer rules

- The non-SOC ten-spatial-orbital bulk parent is not the direct subtraction reference
  for a later spinorial SOC defect program.
- The synthetic diamond-lattice controls used by Paper B are not silicon evidence.
- Literature and Materials Project values do not replace project convergence or parent
  qualification.
- Tutorial convergence or successful exit does not establish production adequacy.
