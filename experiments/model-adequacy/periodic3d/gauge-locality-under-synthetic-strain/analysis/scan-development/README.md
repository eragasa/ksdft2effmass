# Sampled 3-D Bain strain scan

This directory receives replaceable 201-point development plots and canonical JSON
artifacts from [`../../scan_development.py`](../../scan_development.py). The scan reports
sampled witness-requirement envelopes, geometry-only locality costs, retained-subspace
and frame qualification, approximation-channel extrema, response-mechanism extrema, the
frozen-parent null response, and the prescribed radial response. Every extremum retains
its first sampled strain location.

The request binds the complete scan grid and controls. The derived result binds canonical
geometry, witness, frozen-response, and radial-response source documents by SHA-256. A
read-back verifier validates every schema, reconstructs the typed sources, recomputes the
summary and transition brackets, and rejects changed or mixed sources. This verification
establishes artifact identity and reconstruction agreement, not continuum convergence,
material validity, or scientific acceptance. Generated files remain outside integration
commits.
