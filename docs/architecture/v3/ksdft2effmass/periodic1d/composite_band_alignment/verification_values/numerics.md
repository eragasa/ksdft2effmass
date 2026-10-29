# Independent reconstruction numerics

The verifier uses direct NumPy formulas and singular-value decompositions, with SciPy Schur decomposition for closure phases. Shared BLAS/LAPACK lineage is not algorithmic independence. Comparisons use declared absolute software tolerances and record maximum discrepancies without interpreting them as uncertainty.