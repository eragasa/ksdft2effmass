# FCC/diamond replaceable analysis

[`render_nominal_analysis.py`](../../render_nominal_analysis.py) constructs typed
diagnostics from the bounded `N=8`, `N=16`, and `N=32` records and writes the
family-owned figure inventory in vector PDF and 600-dpi PNG form. The inventory includes
the scientific story, mesh-refinement summary, three-channel error decomposition, shell
locality profiles, first-passing-shell stability, and constrained-Bessel-tail diagnostic.

Generated figures are intentionally excluded from source integration and can be recreated
from typed diagnostics. The diamond-basis label denotes synthetic geometry and
connectivity only. The plots are not convergence, silicon validation, formal interval
certification, or retained evidence.
