"""Finite Wigner--Seitz represented-operator capabilities.

Scientific reference
--------------------
E. Wigner and F. Seitz, "On the Constitution of Metallic Sodium," *Physical Review*
43(10), 804--810 (1933), https://doi.org/10.1103/PhysRev.43.804. The bibliographic
metadata was checked against the Crossref DOI record on 2026-10-07.

The citation preserves the provenance of the Wigner--Seitz name and cell construction.
It does not validate this implementation's finite-mesh representatives, replica
selection, normalization, interpolation accuracy, or scientific application.

This package initializer intentionally does not re-export the implementation classes
from :mod:`.interpolation`. Package-level exports are reserved for a reviewed composite
facade rather than a flat aggregation of requests, results, and numerical actions.
"""
