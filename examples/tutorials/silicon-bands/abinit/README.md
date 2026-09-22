# ABINIT realization

This backend uses the ABINIT 10.8.3 basic3 `tbase3_5.abi` silicon tutorial in
one process with two datasets:

1. dataset 1 constructs the self-consistent density; and
2. dataset 2 uses `getden2=-1` to read dataset 1's density and evaluates eight
   fixed-density bands.

The calculated result is summarized in
[abinit1083-calculated-observation.json](expected/abinit1083-calculated-observation.json).
The process exited successfully, dataset 1 reported energy convergence at SCF
step 5, and dataset 2 produced a 39-point spectrum with eight eigenvalues per
point.

ABINIT warned that its default two buffer bands might be insufficient for the
last bands to satisfy the fixed-density tolerance. The reported
`9.9726e-13` maximum residual excludes those two buffer bands and applies to the
six convergence-checked bands; no all-eight convergence claim is made. The
dataset-2 GSR also
repeated the dataset-1 SCF energy and used `9.9999999999e99` force sentinels;
those values are not a separately minimized energy or physical forces. The
warnings appeared in ABINIT's stdout log while process stderr was empty. The
compact observation records a disposition for every native-output category,
including explicit bounded-processor limitations for dataset-2 density,
wavefunction, DDB, plain-EIG, and AGR files.

The native input, PseudoDojo pseudopotential, NetCDF, density, wavefunction,
streams, and complete band files are not redistributed here. Use the exact
upstream source and identities in the
[paired execution preflight](../../../../docs/computational/paired-silicon-scf-bands-preflight.md).
The compact record is a calculated tutorial observation, not numerical
verification or scientific validation.
