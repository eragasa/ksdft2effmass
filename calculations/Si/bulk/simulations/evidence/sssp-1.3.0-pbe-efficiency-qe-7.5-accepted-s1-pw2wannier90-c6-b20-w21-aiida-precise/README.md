# Accepted-S1 `C6-B20-W21` 20-band conversion evidence

This directory retains compact evidence for the separately authorized Quantum ESPRESSO
7.5 `pw2wannier90.x -in pw2wannier90.in` occurrence. The authorization-request SHA-256
was `fbd250691cd7b5836ac3ad3ecda038efd906379ed3c1527569dfafb27c44da5f`. The exact
230-byte native input SHA-256 was
`1e920e99e272598fa2364d3ae9185c748e7e17e5dc826db69367de448ab11b67`;
its lineage manifest binds the authenticated 20-band NSCF saved state and eligible
`C6-B20-W21` NNKP. Exactly one local process ran with a 300-second timeout, 256 MiB
ceiling, and zero retries.

Quantum ESPRESSO returned zero, emitted `JOB DONE`, and reported 26.41 seconds wall
time. The maintained bounded parsers and correlation checks confirmed:

- AMN shape: 216 k-points, 20 bands, 10 projections;
- MMN shape: 216 k-points, 20 bands, eight neighbors per point, and 1,728 records;
- exact MMN-to-NNKP neighbor-inventory agreement;
- EIG shape: 216 k-points and 20 bands;
- maximum absolute EIG-to-authenticated-QEXSD difference:
  `5.364597654988756e-13 eV`; and
- finite AMN and MMN Frobenius norms.

The external occurrence contains 238 files and 122,528,868 bytes, below the 256 MiB
bound. QE's terminal IEEE flag line is retained as a nonblocking diagnostic because
native completion, bounded parsing, finite interface norms, NNKP correlation, and QEXSD
correlation all passed. Conversion performs no disentanglement or Wannierisation.

The 2,894,499-byte AMN and 25,662,627-byte MMN remain outside Git as authenticated
interface artifacts; their exact identities are retained below and in the external
inventory and result records. The compact EIG and NNKP copies are retained here for
review. This avoids committing the larger dense interface matrices while preserving
lineage to the external occurrence required by a later localization preflight.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `b32bbd4edecb04ceaed2ab3871efadabecaf619ab749154ad6726b58bbbefe6c` |
| consumed authorization | `1fb9753041b5a5107a7e080be4fcc072580ec609eaa49c7150191aa2cf904243` |
| AMN (external) | `9186cd5b8802bede18f81b96188f0a2035eb97565c2f811f5ca7769f2ebefece` |
| MMN (external) | `f81833fe7476426c15b690774214b4d07acaa2ffa93b1facb8ceb78c44ab6074` |
| EIG | `a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2` |
| NNKP | `608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575` |
| converter result | `b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a` |
| campaign result | `9aded6afad54e636b3711aca7203d3cb5580a36bbed241982633696ce677a7e2` |
| diagnostic disposition | `15a13e6d820db5501434c3237690cbcf33c53c973b29e4499a8e20b16a461575` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1`.

## Scientific disposition

This is an eligible 20-band AMN/MMN/EIG handoff for a separately prepared and authorized
fresh `C6-B20-W21` localization occurrence. It is not a localization result, represented
operator, optimizer-convergence result, or intended-use result. The conversion
authorization is consumed. Localization, retries, `C6-B30`, `C8`, `C12`, confirmation,
component-operator construction, and Slater--Koster reduction remain unauthorized.
