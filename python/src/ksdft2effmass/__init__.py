"""Python reference package for ksdft2effmass research software.

The package contains maintained first-party Python implementations for finite
operator records used in controlled reduction of represented Kohn-Sham operator
matrices.  The root package intentionally does not re-export scientific objects:
the supported finite operator-record public API is
:mod:`ksdft2effmass.operators`.

This module has no numerical algorithm, unit convention, validation tolerance,
or scientific pass/fail criterion of its own.  Software verification occurs in
the package tests and Sphinx build; scientific validation of a represented
Hamiltonian or reduced model requires separate physical reference calculations
and is outside this package initializer.
"""

__all__: list[str] = []
