# FCC/diamond bounded nominal calculation

Status: **replaceable diagnostics; not retained evidence, silicon validation, or
scientific validation**.

The canonical JSON outputs are intentionally excluded from source integration. Rerun
[`run_nominal_calculation.py`](../../../run_nominal_calculation.py) to recreate
replaceable artifacts. The bounded request compares a matched simple-cubic Bravais
control, FCC Bravais control, and synthetic diamond-basis connectivity control. It uses
an `8 x 8 x 8` construction mesh, shifted `17 x 17 x 17` evaluation mesh, parent scales
`0` and `1`, gauge amplitudes through `pi/(4*sqrt(12))`, complete FCC metric shells
through index `7`, and provisional band thresholds `1e-3` and `1e-5`.

The historical bounded run reported independent verification passing with maximum stored
identity defect about `4.5e-15`. Several first-passing decisions remained unresolved at
the declared shell cap. Those values are historical replaceable observations; they were
not rerun by the context migration and are not retained execution evidence.

The diamond-basis control is not an `sp3s*`, valley, effective-mass, first-principles, or
bulk-silicon model. The maintained action does not establish convergence or publication
evidence.
