# Accepted-S1 `C6-B20-W21` 20-band conversion preflight

This directory retains the consumed deterministic no-execution recommendation and
preflight for the distinct Quantum ESPRESSO 7.5 `pw2wannier90.x` conversion occurrence.
It binds the
verified 216-point/20-band `C6-B20` Davidson saved state to the authenticated
`C6-B20-W21` rank-10 NNKP topology produced by the completed AiiDA-precise preprocessing
occurrence.

The maintained ProjectKoios projector and runner produced
[`rendered/pw2wannier90.in`](rendered/pw2wannier90.in) in dry-run mode. The declaration
uses prefix `system`, staged outdir `./tmp/`, seed `silicon`, scalar spin component
`none`, standalone mode, AMN and MMN output enabled, and UNK and SPN output disabled.
Required outputs are `silicon.amn`, `silicon.mmn`, and `silicon.eig`.

The native input is byte-identical to the earlier 12-band C6 converter input because
parent band count and NNKP identity are carried by the staged saved state and lineage
manifest rather than additional INPUTPP fields. The new input manifest binds the
20-band saved-state manifest SHA-256
`24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` and NNKP SHA-256
`608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575`.
The verified parent state contains 219 files totaling 93,658,989 bytes. The NNKP contains
216 points, eight neighbors per point, 1,728 neighbor records, ten projections, and no
excluded bands.

No occurrence root was created, no saved state or NNKP was copied, and no calculator
was invoked.

## Recommendation

Use the unchanged standalone converter configuration and require fresh 20-band
AMN/MMN/EIG artifacts. Reuse the previously successful C6 bounds:

- one process and one invocation;
- zero retries and stop on failure;
- 300-second timeout; and
- 256 MiB retained-byte ceiling.

The verified 20-band saved state is 93,658,989 bytes. The MMN payload scales
approximately with the square of band count; scaling the earlier 12-band C6 MMN size by
`(20/12)^2` gives about 25.8 MB (24.6 MiB), leaving substantial margin below the retained-byte
ceiling after saved-state staging. This is a resource recommendation, not an execution
result.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1`
- command: `pw2wannier90.x -in pw2wannier90.in`
- executable SHA-256:
  `61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c`
- one process, one invocation, zero retries
- timeout: 300 seconds
- retained-byte ceiling: 256 MiB

Required success evidence includes return code zero, native `JOB DONE`, regular nonempty
AMN/MMN/EIG artifacts, finite values, AMN 20-band/rank-10/216-point shape, MMN
20-band/216-point shape with exact NNKP-neighbor correlation, and EIG 20-band by
216-point shape correlated with the authenticated QEXSD spectrum.

## Identities

| Artifact | SHA-256 |
|---|---|
| `rendered/pw2wannier90.in` | `1e920e99e272598fa2364d3ae9185c748e7e17e5dc826db69367de448ab11b67` |
| rendered input manifest | `d200386e26e8dea5af974cf8a10fad3ece5e84617ff70b049e683b91ef089f1a` |
| campaign preflight | `fae31ab6e9f20c11b21211f50d661df33b699c508216b86518ed742e0d9ab3a7` |
| authorization request | `fbd250691cd7b5836ac3ad3ecda038efd906379ed3c1527569dfafb27c44da5f` |
| parent NSCF manifest | `24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` |
| parent NNKP | `608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575` |
| preprocessing result | `ca73c8e0384e5f8b3bccffbe1ab1b2e58d636876f802b380a06eec74f8c50e93` |

## Authorization boundary

Status: **consumed by one completed occurrence**.

[`authorization-request.json`](authorization-request.json) remains the immutable
ungranted preflight request, while its exact identity was authorized separately and
consumed by one occurrence. Compact authenticated result evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise/).
The request cannot authorize a retry. Localization, `C6-B30`, `C8`, `C12`,
confirmation-parent evaluation, component-operator construction, and Slater--Koster
reduction remain separately controlled.
