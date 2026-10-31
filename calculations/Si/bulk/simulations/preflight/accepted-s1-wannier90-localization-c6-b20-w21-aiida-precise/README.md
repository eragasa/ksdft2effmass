# Accepted-S1 `C6-B20-W21` precise-profile localization preflight

This directory retains the consumed deterministic no-execution recommendation and
preflight for one fresh Wannier90 3.1.0 localization occurrence. It binds the
authenticated 20-band AMN/MMN/EIG interface and NNKP to the selected rank-10 `C6-B20-W21` target space and
the complete pinned AiiDA precise convergence-derived tuple.

This is not a retry of either blocked 12-band C6 localization. It has a distinct
20-band parent inventory, outer window, interface artifacts, convergence tuple, input
manifest, and proposed occurrence identity. It consumes no checkpoint, HR, `u`,
`u_dis`, or other failed output.

## Exact optimizer profile

```text
num_iter       = 40000
conv_tol       = 2.0e-9 angstrom^2
conv_window    = 6
num_cg_steps   = 200

dis_num_iter   = 40000
dis_conv_tol   = 2.0e-9  # dimensionless
dis_conv_window = 3
dis_mix_ratio  = 0.2
```

The fresh input retains rank 10, 20 parent bands, outer window `[-6.0, 21.0] eV`,
frozen window `[-5.85, 8.0] eV`, `Si:sp3` plus `Si:l=0:r=2`, the ordered 216-point C6
mesh, enabled preconditioning, native-default `trial_step = 2.0`, unset `fixed_step`,
and disabled `guiding_centres`. It explicitly requests HR, `u`, and `u_dis` outputs.
The 40000 values are ceilings, not required iteration counts or evidence of convergence.

The maintained ProjectKoios localization input preparer authenticated the 216-point,
20-band, rank-10, eight-neighbor interface. The input manifest binds 28,795,489 bytes
of fresh NNKP/EIG/AMN/MMN and construction-input artifacts. No proposed occurrence root
was created, no interface artifact was copied into the worktree, and no calculator was
invoked.

## Resource recommendation

The blocked 12-band C6 occurrence using 4000-step ceilings required 359.302 seconds on
one local process. Scaling its measured per-iteration cost by `(20/12)^2` and allowing
both precise 40000-step ceilings gives a conservative four-hour bound. The recommended
execution limits are:

- one process and one invocation;
- zero retries and stop on failure;
- 14,400-second timeout; and
- 128 MiB retained-byte ceiling.

This is a bounded resource estimate, not a runtime prediction. If the occurrence reaches
the timeout or either iteration ceiling without both native convergence phrases, it is
ineligible and no automatic retry or extension follows.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1`
- command: `wannier90.x silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- one process, one invocation, zero retries
- timeout: 14,400 seconds
- retained-byte ceiling: 128 MiB

Provider eligibility requires return code zero, native completion, converged
disentanglement and Wannierisation messages, no maximum-iteration warning, declared HR
and unitary outputs, gauge-unitarity and disentanglement-isometry residuals at most
`1.0e-8`, k-point agreement within `1.0e-10`, and Hamiltonian Hermiticity residual at
most `1.0e-8 eV`. Passing establishes provider eligibility only, not a global minimum or
scientific adequacy.

## Identities

| Artifact | SHA-256 |
|---|---|
| prepared `silicon.win` | `6a6fe1b3193455038a0c4a14038f174f3c0e6244113ee9fb17ff1f42a145a2f3` |
| localization input manifest | `523515dffc883abf1bc0ff3e1427eea13e85a12774a5ce2040e3dd43c396568e` |
| input transformation | `76d1bba6f54888b7b3ef4998ff7840bc35365326abdffc5e46917903bee77b0f` |
| campaign preflight | `b7e6b150e28e4ae79eadffbc8799eb593554ccd4f9792347fbd6852ca9a1977d` |
| authorization request | `02375507dbe487f1ad5dee2569151faf04c2e5a5fa3aadd9b0007d977bc26aa7` |
| preprocessing result | `ca73c8e0384e5f8b3bccffbe1ab1b2e58d636876f802b380a06eec74f8c50e93` |
| converter result | `b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a` |
| AMN | `9186cd5b8802bede18f81b96188f0a2035eb97565c2f811f5ca7769f2ebefece` |
| MMN | `f81833fe7476426c15b690774214b4d07acaa2ffa93b1facb8ceb78c44ab6074` |
| EIG | `a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2` |
| NNKP | `608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575` |

## Authorization boundary

Status: **consumed by one provider-eligible occurrence**.

[`authorization-request.json`](authorization-request.json) remains the immutable
ungranted preflight request, while its exact identity was authorized separately and
consumed by one occurrence. Wannier90 converged disentanglement at iteration 1517 and
Wannierisation at iteration 378. An initial provider false negative compared matrix
coordinates with lossy NNKP presentation values. No-calculator reverification against
the canonical WIN block measured `3.300004713935323e-11`, passing the unchanged
`1.0e-10` fractional gate. Compact evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-b20-w21-aiida-precise-eligible/`](../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-b20-w21-aiida-precise-eligible/).
The request cannot authorize a retry. The HR, `u`, and `u_dis` artifacts are now eligible
for the separately gated S30 full untruncated characterization. Confirmation, spatial
truncation, and Slater--Koster reduction remain blocked.
