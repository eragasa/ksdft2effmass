# Sampled periodic-3D Bain-path scan

This directory receives replaceable 201-point plots and canonical JSON artifacts from
[`run_path_scan.py`](../../../run_path_scan.py). The scan reports sampled
operator-requirement envelopes, M0 geometry-only locality costs, retained-subspace and
frame qualification, approximation-channel extrema, M1 frozen response, M2 prescribed
radial response, and declared transition brackets. Every sampled extremum retains its
first sample location.

The request binds the complete scan grid and controls. The derived result binds canonical
geometry, witness, M1, and M2 source documents by SHA-256. A read-back verifier validates
every schema, reconstructs typed sources, recomputes the summary and transition brackets,
and rejects changed or mixed sources. This establishes artifact identity and
reconstruction agreement, not continuum convergence, a common path witness, material
validity, or scientific acceptance. Generated files remain outside integration commits.
