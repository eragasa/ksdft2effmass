# `ksdft2effmass` package scientific interpretation

`ksdft2effmass` constructs and evaluates reduced semiconductor Hamiltonians from declared
first-principles or controlled-model inputs. Quantum ESPRESSO owns electronic-structure
calculation and Wannier90 owns Wannier localization; this package does not reimplement
either.

Scientific contracts distinguish physical models, mathematical operators, and finite
matrix representations. Operators are compared only after their state spaces, bases,
gauges, energy references, units, and geometry are aligned. Projection,
disentanglement, basis transformation, alignment, fitting, and truncation remain
different operations.

Controlled models support software and bounded numerical questions. They do not by
themselves validate a material model. Retained calculations, provenance records, and
publication bindings remain separate from reusable source behavior.

Passing tests or independent numerical verification does not establish scientific
validation, continuum convergence, uncertainty quantification, evidence sealing,
publication acceptance, or release. Those conclusions require their own explicit
contracts and authority.
