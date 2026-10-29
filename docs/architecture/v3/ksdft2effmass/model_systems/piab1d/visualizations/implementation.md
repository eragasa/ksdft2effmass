# Implementation

`Piab1dVisualizationData` remains one immutable typed projection derived by
`Piab1dVerifier` from independently reconstructed result values. Moving it to `data.py`
must preserve its field inventory, typed mapping, canonical JSON bytes, validation, and
projection digest exactly.

`Piab1dVisualizationPlotEnum` moves unchanged to `inventory.py`. The aggregate
`Piab1dVisualizer` binds `Piab1dVisualizationData` and `Piab1dVerification`, authenticates
them before constructing Matplotlib objects, composes one renderer per enum member, and
requires exact inventory equality.

Figure ownership is grouped as follows:

| Figure module | Existing presentation responsibility |
|---|---|
| `spectrum.py` | Spectrum, retained states, spectrum-and-states summary, and residual matrices. |
| `ladders.py` | Continuum and discrete wavefunction ladders and retained-dimension selection. |
| `convergence.py` | Convergence series, mode sweep, higher-eigenpair sweep, and higher-mode convergence. |
| `diagnostics.py` | Operator residuals, eigensolver residuals, and finite algebraic diagnostics. |
| `decomposition.py` | Kinetic-potential decomposition under declared model classes. |

Private plot and subplot actions stay with the smallest cohesive figure family that uses
them. No generic plotting helper, registry, or caller-defined figure is introduced.
Public family imports remain deliberate exports from `model_systems.piab1d`; the old
singular source module is deleted rather than retained as a forwarding facade.
