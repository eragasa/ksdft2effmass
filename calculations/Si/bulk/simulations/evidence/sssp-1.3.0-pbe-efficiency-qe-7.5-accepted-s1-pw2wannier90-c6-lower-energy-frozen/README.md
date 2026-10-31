# Accepted-S1 `C6` pw2wannier90 evidence

This directory retains compact evidence for the separately authorized `C6` Quantum
ESPRESSO 7.5 `pw2wannier90.x` occurrence. The request SHA-256 was
`8cdd7bd14c95ebc516b844c7819f3b08af0b62f37b781f40a377c34c9b3b5e9f`; the exact
input SHA-256 was
`1e920e99e272598fa2364d3ae9185c748e7e17e5dc826db69367de448ab11b67`.
Exactly one local process ran with a 300-second timeout, 256 MiB ceiling, and zero
retries.

QE returned zero, printed `JOB DONE`, and reported 25.55 seconds wall time. The
maintained bounded interface parsers and correlation checks confirmed:

- AMN shape: 216 k-points, 12 bands, ten projections;
- MMN shape: 216 k-points, 12 bands, eight neighbors and 1,728 records;
- exact MMN-to-NNKP normalized neighbor correlation;
- EIG shape: 216 k-points by 12 bands;
- finite AMN/MMN matrix norms; and
- maximum absolute EIG-to-QEXSD difference
  `5.222489107836736e-13 eV`.

The external occurrence contains 238 files and 69,709,679 bytes, including its staged
copy of the authenticated NSCF state. QE reported IEEE invalid, divide-by-zero,
overflow, and underflow flags at termination; they remain diagnostics because native
completion, finite bounded parsing, and cross-artifact correlations succeeded.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `e319f722c377abc358bb888b89324ee3ff2bee93d7a086949e28097074b8fa76` |
| consumed authorization | `f4f4d3df66cb55fc94f62bd56104b5f7737409c415c8dd467d1479584a7791fe` |
| `silicon.amn` | `efda4f7d101eb5ed5c7d871c3b5a9c14a2343bc09e86188dbf48dca5731355eb` |
| `silicon.mmn` | `f2db3539f36fb2a5c8174c503326e56726553593ec0609f96e66186db488e1a1` |
| `silicon.eig` | `94d759c2906c041a14adc12bd6d740f1f5499c7c85aeea20b06752536f25c463` |
| converter result | `ebb9352aa1184be665ef8021bf26feea466ef1f0ce701d071546a19e934f7769` |
| campaign result | `1206904008e5baebef9266d903567a96b914d1232c0be069c133ee12dc52c424` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-lower-energy-frozen-v1`.

## Scientific disposition

This is an eligible `C6` AMN/MMN/EIG handoff, not a localized or accepted Wannier
operator. Localization, retries, `C8`, `C12`, and confirmation-parent evaluation require
separate authorization.
