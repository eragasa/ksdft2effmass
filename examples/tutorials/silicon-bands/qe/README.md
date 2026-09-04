# Quantum ESPRESSO realization

This backend uses the Quantum ESPRESSO 7.5 `PW/examples/example01` silicon
SCF-and-bands tutorial:

1. `pw.x < si.scf.in` creates the self-consistent density and native `si.save`
   state;
2. `pw.x < si.band.in` reads that state and evaluates eight fixed-density
   bands; and
3. `bands.x < si.bands.in` reads the bands state and writes plottable bands and
   raw `.rap` symmetry-representation indices.

The calculated result is summarized in
[qe75-calculated-observation.json](expected/qe75-calculated-observation.json).
All three processes exited successfully, and the SCF output reported convergence
in six iterations. The 72-point fixed-density path contains eight represented
eigenvalues at each point. Postprocessing also retained all 72 `.rap` coordinate,
boolean-flag, and eight-integer representation-index entries, using an absolute
`5e-7` coordinate tolerance for the file's six-decimal precision. No mapping from
those raw indices to irrep names is asserted. The plain and GNU plotting files
were also parsed into 72 path-coordinate entries with eight eigenvalues each and
cross-checked at their printed precision.

The final bands-mode invocation overwrote the run-local QEXSD produced by SCF.
Its represented total-energy field is `0.0`; it is not the SCF energy. All three
stderr streams also reported the same IEEE floating-point exception flags.
Both facts are retained diagnostics rather than silently normalized away.

The native inputs, pseudopotential, QEXSD, density, wavefunctions, streams, and
complete band files are not redistributed here. The compact observation records
a parse, continuation-consumption, duplicate-copy, or diagnostic disposition for
every generated output category. Use the exact upstream source
and identities in the
[paired execution preflight](../../../../docs/computational/paired-silicon-scf-bands-preflight.md).
The compact record is a calculated tutorial observation, not numerical
verification or scientific validation.
