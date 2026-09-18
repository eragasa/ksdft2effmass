# Non-DFT Wannier90 convergence and embedding study preflight

## Execution outcome

All six authorized cases completed once, serially, without retry. Preprocessing
used at most 0.36 s and 22.8 MB; localization used at most 2.04 s and 31.6 MB.
Each case remained below 2.9 MB external output. The resulting spreads and
tails are nonmonotone, so the study does not establish cutoff, mesh, or
inactive-embedding independence. Detailed results are retained in
`wannier90-study-result.json` and `wannier90-study-report.md`.

## Authority and boundary

The human instruction `everything that doesn't require dft calculations` on
2026-09-18 authorizes the remaining non-DFT periodic-2D work. This preflight
narrows the protected executable work to six new local synthetic Wannier90
cases listed in `wannier90-study-input.json`. It does not authorize Quantum
ESPRESSO, another DFT code, a material calculation, remote execution, data
transmission, publication, release, successor activation, or an automatic
retry.

## Executable and input system

- Executable: `/Users/eugene/.local/bin/wannier90.x`
- Version: Wannier90 3.1.0
- Executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- Parent: the existing two-dimensional synthetic cosine plane-wave operator
- Retained group: the lowest three bands
- Trial family: the existing deterministic synthetic $s/p_x/p_y$ projections
- Processes: one local process per stage; cases run serially

The study changes one axis at a time around the retained reference
$(P,N,c)=(3,15,15)$:

| Axis | New cases |
|---|---|
| reciprocal mesh | $(3,11,11)$ and $(3,19,19)$ |
| plane-wave cutoff | $(2,15,15)$ and $(4,15,15)$ |
| inactive embedding | $(3,15,12)$ and $(3,15,18)$ |

Here $P$ is the plane-wave cutoff, $N^2$ is the active reciprocal mesh, and $c$
is the auxiliary inactive direct-lattice length. The mesh cases keep the three
reciprocal increments balanced by setting $c=N$. The embedding cases preserve
every active-plane input and vary only $c$.

## Expected scale, outputs, and limits

The largest parent diagonalization is 361 reciprocal points with an $81\times81$
plane-wave matrix. Every case has three bands and three Wannier functions.
Expected native outputs are `.nnkp`, `.mmn`, `.wout`, `.chk`, `.u.mat`,
`_hr.dat`, centers, spreads, and logs.

Each case has two executable stages: preprocessing and localization. Each stage
is limited to 300 seconds and 512 MiB resident memory; each case is limited to
50 MiB external output. Six new cases are permitted and run serially. Based on
the retained reference, the expected total runtime is under ten minutes and the
expected new output is under 15 MiB, but these are estimates rather than
results.

## Stop conditions

A case stops without retry if preprocessing or localization fails, fails to
converge, exceeds a limit, produces nonfinite values, or requires a scientific
or interface change. A failed case remains evidence and does not authorize a
replacement case. The study stops entirely if the observed scale materially
exceeds this preflight.

Only active-plane quantities are interpreted. Mesh, cutoff, inactive embedding,
native-spread discretization, common finite-supercell spread, hopping range,
and serialized-Hamiltonian errors remain separate. Passing these cases would be
synthetic numerical verification, not DFT, material validation, transferability,
a general localization theorem, or uncertainty quantification.
