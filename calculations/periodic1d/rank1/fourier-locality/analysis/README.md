# Analysis

Architecture v3 does not assign this directory a runtime analysis stage. Reusable
Fourier, fit, truncation, error, and diagnostic behavior belongs to installed source
owners. `Periodic1DFourierLocalityAnalyzer` writes each authoritative value once, and
the byte-owning `Periodic1DFourierLocalityVerifier` independently reconstructs the
finite calculation before deriving authenticated visualization data.

The implemented channels include scalar Fourier coefficients,
interpolation/truncation/total errors, hopping-tail quantities, ordered scalar-spectrum
diagnostics, adjacent-mesh refinement, the attained range table, per-mesh finite
error--complexity and near-tie masks, and threshold/first-passage decisions. Rendering
consumes only the authenticated projection and calculates no new scientific values.

No calculation-local analysis or plotting entrypoint is supported. The direct stage
scripts live at the calculation root, and rank-one phase-alignment channels are not
manufactured as duplicate results. No retained execution has been produced.
