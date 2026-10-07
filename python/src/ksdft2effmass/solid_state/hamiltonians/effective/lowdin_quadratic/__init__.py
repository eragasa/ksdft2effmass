"""Finite selected-space Löwdin quadratic effective Hamiltonians.

Scientific reference
--------------------
Per-Olov Löwdin, "A Note on the Quantum-Mechanical Perturbation Theory,"
*The Journal of Chemical Physics* 19(11), 1396--1401 (1951),
https://doi.org/10.1063/1.1748067. The bibliographic metadata was checked against the
Crossref DOI record on 2026-10-07.

The citation establishes the provenance of the class-partition construction. It does
not validate this implementation's derivative convention, tolerances,
kinetic/remainder decomposition, or material interpretation.

The reduction, model-evaluation, and directional-contraction modules remain explicit.
This initializer is reserved for a reviewed composite Löwdin-Hamiltonian facade.
"""
