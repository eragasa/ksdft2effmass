# Accepted-S1 `C6` pw2wannier90 preflight

This directory retains the no-execution preflight for the distinct `C6` Quantum ESPRESSO
7.5 `pw2wannier90.x` conversion occurrence. It binds the verified 216-point/12-band
Davidson NSCF saved state to the authenticated rank-10 Wannier90 NNKP topology.

The maintained ProjectKoios projector and runner produced
[`rendered/pw2wannier90.in`](rendered/pw2wannier90.in) in dry-run mode. The declaration
uses prefix `system`, staged outdir `./tmp/`, seed `silicon`, scalar spin component
`none`, standalone mode, AMN and MMN output enabled, and UNK and SPN output disabled.
Required outputs are `silicon.amn`, `silicon.mmn`, and `silicon.eig`.

The verified parent state contains 219 files totaling 58,433,245 bytes. The NNKP contains
216 points, eight neighbors per point, 1,728 neighbor records, ten projections, and no
excluded bands. No artifact was copied into a proposed occurrence and no calculator was
invoked.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-lower-energy-frozen-v1`
- command: `pw2wannier90.x -in pw2wannier90.in`
- executable SHA-256:
  `61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c`
- one process, one invocation, zero retries
- timeout: 300 seconds
- retained-byte ceiling: 256 MiB

Required success evidence includes return code zero, native `JOB DONE`, regular nonempty
AMN/MMN/EIG artifacts, finite values, AMN rank and 216-point shape, MMN rank and exact
NNKP-neighbor correlation, and EIG 12-band by 216-point shape.

## Identities

| Artifact | SHA-256 |
|---|---|
| `rendered/pw2wannier90.in` | `1e920e99e272598fa2364d3ae9185c748e7e17e5dc826db69367de448ab11b67` |
| rendered input manifest | `f48d8082674b4f8c3ad5b101ac7fa07a3522be99b23eea447eb12d0fd9b8206c` |
| campaign preflight | `48a719fb43dbd2415286f6c1085c67fc1493914f3225d3a3214079d4125ff0cb` |
| authorization request | `8cdd7bd14c95ebc516b844c7819f3b08af0b62f37b781f40a377c34c9b3b5e9f` |
| parent NSCF manifest | `28df04c1bf314371d6138bfe41b564147354253c6d609b465c7ebd4778c617b8` |
| parent NNKP | `f367195dcc42a72244104e8149bbc75b4ce623c67a6acc1d169c68b33aeffead` |

## Authorization boundary

Status: **authorization required**.

The consumed preprocessing authorization does not authorize `pw2wannier90.x`. The
request retains `authorization_granted: false`. Conversion, localization, retries, `C8`,
`C12`, and confirmation-parent evaluation remain separately controlled.
