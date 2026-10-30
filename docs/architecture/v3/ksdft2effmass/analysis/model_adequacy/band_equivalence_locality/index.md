# `ksdft2effmass.analysis.model_adequacy.band_equivalence_locality`

## Purpose and status

This owner asks whether two finite rank-two represented Hamiltonian fields can preserve
their sampled ordered bands while exhibiting different complete Fourier-block locality
and different consequences under explicit metric-shell truncation.

The installed source implements a typed nominal calculation for the square,
graphene-inspired, simple-cubic, and silicon-inspired family identities. Direct
calculate → verify → render compositions are installed for the orthogonal periodic-2D
square, nonorthogonal periodic-2D triangular/honeycomb, orthogonal periodic-3D
simple-cubic, and nonorthogonal periodic-3D FCC/diamond cases at their calculation
roots. All are bounded synthetic lifecycles. The square root contains a **CALCULATED
RESULT — UNSEALED** execution; no nonorthogonal periodic-2D or periodic-3D execution is
created. No scientific convergence result, sealing decision, evidence promotion, or
publication acceptance is created. Refinement remains outside these nominal lifecycles.

## Module ownership

| Module | Responsibility |
|---|---|
| `definitions.py` | Immutable typed family, geometry, parent, gauge, mesh, amplitude, tolerance, and support requests. |
| `analysis.py` | Immutable scientific analysis and request-bound production analyzer with zero-argument `execute()`. |
| `results/` | Plain immutable scientific point, shell, decision, and case results with no serialization behavior. |
| `diagnostics.py` | Concrete constructor-bound diagnostic analyzers implementing `BaseDiagnosticAnalyzer`. |
| `calculation/` | Independent finite diagnostic reconstruction used only by verification. |
| `records/` | Retained point, shell, decision, case, and diagnostic `BaseTypedRecord` projections. |
| `shell_power.py` | Typed KSD aggregation of PhysKit-owned block powers by physical-metric shell, with retained-rank normalization. |
| `result.py` | Passive retained calculation result and the analysis-bound recorder that projects scientific results into retained records. |
| `verification.py` | Exact-result-byte ownership, independent checks, verification aggregate, and stored-value readmission. |
| `lifecycle.py` | Domain-owned typed execution, execution-verification, and rendering records using the final `BaseTypedRecord` JSON boundary. |
| `visualizations/` | Authenticated scalar projection, one closed plot name, figure composition, and visualizer. |

These symbols remain available from their concrete owning modules. This stage does not
add them to the package-root `__all__` inventory.

## Dependency boundary

- Project Koios Optimization owns unit-free finite-periodic meshes, multidimensional
  Fourier transforms and evaluation, Parseval arithmetic, and transform diagnostics.
- PhysKit owns direct-lattice metrics, reusable physical lattice semantics, and raw
  unit-aware squared Frobenius powers for individual hopping blocks.
- KSD owns the synthetic parent laws, retained-rank policy, gauge-amplitude meaning,
  physical-metric shell policy, diagnostic applicability, error-channel meaning,
  thresholds, family identities, result records, and evidence boundary.
- Calculation scripts own paths, exact file digests, no-overwrite gates, atomic stage
  publication, and the unsealed execution statement.

The installed package imports neither experiment nor calculation directories. Quantum
ESPRESSO and Wannier90 are not invoked and retain ownership of first-principles
calculation and Wannier localization.

## Architectural invariants

- Spatial dimension and retained rank are independent; this owner currently admits
  dimensions two and three while retaining rank two from a four-state parent.
- A case states its primitive basis, primitive-vector axis, positive bond inventory,
  basis offsets, metric scale, parent kind, and gauge normalization.
- Canonical bytes come from `BaseTypedRecord`; SHA-256 authenticates byte identity but
  does not establish scientific validity.
- The scientific lifecycle is request → bound analyzer → plain immutable analysis.
- The analysis recorder performs a separate retained-result projection and never reruns the producer.
- The passive retained result never reruns the producer during reconstruction.
- The verifier owns the exact immutable result bytes and does not call the bound
  production analyzer.
- Projection, alignment, Fourier reconstruction, ordinary-lattice conversion,
  truncation, and total comparison remain distinct operations.
- Interpolation, truncation, and total error channels are retained separately; their
  separately maximized norms are not added.
- Inapplicable transport and diagnostic values retain explicit reasons rather than
  fabricated zeros.
- Rendering consumes the independently readmitted verification and typed projection;
  it does not invoke the scientific producer.
- Direct scripts contain module-scope composition only and perform no sealing,
  publication, remote execution, or external scientific calculation.

## Detailed architecture

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Parent `analysis.model_adequacy` boundary](../index.md)
- [Periodic-1D direct-lifecycle guide](../../../periodic1d/index.md)
