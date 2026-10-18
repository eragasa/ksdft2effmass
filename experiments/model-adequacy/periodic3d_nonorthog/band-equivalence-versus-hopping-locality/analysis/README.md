# Silicon-inspired-family development figures

`plot_development.py` constructs typed diagnostics for the unchanged `N=8`, `N=16`,
and `N=32` requests and writes the following family-owned diagnostics in vector PDF and 600-dpi PNG form:

- `band-equivalence-locality-scientific-story`: withheld interpolation, external
  retained-subspace isolation, cumulative omitted hopping power, withheld spectral
  consequence, and tail-power/consequence separation;
- `mesh-refinement-summary`: all three mesh levels by case;
- `three-channel-error-decomposition`: interpolation, deliberate truncation, and total
  matrix and sorted-band errors on the refined endpoint comparison;
- `shell-locality-profiles`: matrix, spectral, and omitted-power shell profiles;
- `first-passing-shell-stability`: smoke-to-final-refinement sampled shell decisions; and
- `constrained-bessel-tail-certificate`: bounded binary64 evaluation of the FCC
  constrained-series certificate with its declared coefficient margin.

Generated figure files are intentionally excluded from this source integration and can
be recreated from the typed diagnostics. The inspired label denotes geometry and
connectivity only. The plots are not convergence, silicon validation, formal interval
certification, or retained evidence.
