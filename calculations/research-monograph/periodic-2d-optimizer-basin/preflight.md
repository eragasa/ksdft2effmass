# Periodic-2D optimizer-basin and convergence preflight

## Authorization and status

Human authorization is retained at
`RM-PERIODIC-2D-OPTIMIZER-BASIN-EXECUTION-HC07`. This is a separate non-DFT
follow-up. It does not reopen or alter the accepted periodic-2D controlled
exercise.

## Executable and input system

- executable: Wannier90 3.1.0;
- resolved path:
  `/Users/eugene/projects/wannier90-3.1.0-local/bin/wannier90.x`;
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`;
- parent: the frozen synthetic coupled periodic-2D rank-three continuum
  representation from `../periodic-2d/composite-input.json`;
- execution: local and serial; no DFT, remote, cloud, or cluster work.

The exact nine configurations, eight deterministic smooth reciprocal-periodic
initial gauges, gauge formula, generators, convergence rules, limits, and claim
boundary are frozen in `study-input.json`.

## Scale and outputs

The study performs nine interface preparations and at most 72 serial Wannier90
localizations. Parent eigensystems range from 25 to 121 plane-wave basis states
on meshes from $11^2$ through $23^2$. Expected normal runtime is below 30
minutes. Hard limits are two total hours, 300 seconds per stage, 512 MiB resident
memory per stage, 8 MiB per localization, and 400 MiB total external output.

Native files and logs will remain under
`/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/optimizer-basin-20260918T110000Z`.
The repository will retain compact inputs, manifests, summaries, figures,
reports, verifier code, and checksums rather than the native working set.

## Initialization and basin policy

Each initial gauge right-multiplies the same baseline trial-overlap matrix by a
deterministic smooth periodic unitary. The Hamiltonian, eigenspaces, energy
window, rank, mesh, cutoff, and embedding for a configuration are therefore
unchanged. The identity and all seven perturbed starts are retained. A failed,
timed-out, or higher-spread run is evidence and will not be retried, removed, or
silently replaced.

Basins are classified by total spread and unordered periodic center set using
the frozen tolerances. The best observed basin is not called a proven global
minimum. Convergence is evaluated for both the best observed basin and the
across-start median on the two finest mesh and cutoff pairs. A supporting
classification additionally requires that the best basin be reached by at least
two independent starts. Embedding dependence is reported separately and is not
interpreted as numerical convergence.

A $512^2$ common finite-supercell estimator is used so that the largest declared
$P=5,N=23$ represented modes do not alias. Native Berry-link spread remains a
separate Wannier90 diagnostic.

## Stop conditions and claim boundary

Execution stops without retry if a hard bound is exceeded or an unexpected
scientific ambiguity invalidates the declared comparison. Software completion
cannot establish material adequacy, scientific validation, uncertainty
quantification, production robustness, a global optimum, or a general
localization-convergence theorem.
