# `C6-B20-W21` gated full-operator-to-reduction series

This directory defines the branched series from the authenticated 20-band interface
through structural qualification of the fixed full source, controlled spatial and
Slater--Koster reduction, diagnostic prediction freeze, and hidden-parent confirmation.
[`series-plan.json`](series-plan.json) is generated
deterministically by [`prepare_series.py`](prepare_series.py).

The series is a plan and set of stage contracts, not blanket execution authority.
Automatic execution and automatic stage advancement are both forbidden. Every
calculator occurrence still requires a new exact artifact-bound request and separate
human authorization. A failed operational gate stops its dependent branch rather than
activating a retry, iteration extension, new band inventory, new window, mesh
escalation, truncation, or reduction. Parent-oracle criteria are evaluation labels, not
operational gates for the controlled-reduction branch.

## Stage sequence

| Stage | Kind | Current status | Gate |
|---|---|---|---|
| S00 | retained interface evidence | complete | authenticated NNKP and finite shape-correct 20-band AMN/MMN/EIG |
| S10 | Wannier90 localization calculator | complete | authorization consumed; disentanglement 1517, Wannierisation 378 |
| S20 | provider eligibility | complete after verifier reference correction | unchanged `1.0e-10` gate; canonical-WIN residual `3.300004713935323e-11` |
| S30 | full untruncated characterization | complete; structurally verified, scientifically unassessed | exact HR, `u`, `u_dis`, WS, EIG, and result identities bound |
| S40 | revealed 408-point development-oracle comparison | complete; oracle labels recorded | gap and mass criteria fail; valley-position criterion passes; none gates controlled reduction |
| S90 | controlled spatial-truncation design | complete; 18-shell family and diagnostics frozen | no radius selected and no 402-point values consumed |
| S100 | complete-family spatial-truncation evaluation | complete; every shell reported without selection | exact full-support control; no parent-oracle values consumed |
| S105 | spatial-truncation disposition | complete; full support retained | `H_T = H_W`; no nontrivial radius or post-observation threshold accepted |
| S110 | Slater--Koster definition and fit | blocked at common-space gate; no fit | projected ten-orbital `sp3s*` frame is rank deficient at two C6 points |
| S50 | reduction and diagnostic prediction freeze | blocked by S110 | no Slater--Koster parameter vector exists to freeze |
| S60 | hidden 402-point parent calculation | blocked by S50 | confirmation values remain unobserved |
| S70 | prospective hidden-oracle comparison | blocked by S60 | tests frozen diagnostic predictions without refitting |
| S120 | Slater--Koster diagnostic validation | blocked by S70 | separates parent, truncation, and parameterization error channels |
| S80 | optional full-operator physical-fidelity disposition | not required for controlled reduction | parent agreement limits physical claims only |

Exact downstream artifact bindings cannot be generated before their upstream outputs
exist. Those stages are therefore conditional templates rather than misleading runnable
preflights. Parent-fidelity errors are controlled-study oracle labels, not operational
reduction diagnostics. The 402-point confirmation geometry remains frozen at SHA-256
`51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8`; its direct-parent
values are not present in this plan and remain unobserved.

## Current actionable stage

S10 and S20 are complete. The initial provider rejection was a false negative caused by
using lossy eight-decimal NNKP coordinates as the reference for ten-decimal matrix
outputs. The corrected provider compares `u` and `u_dis` with the canonical WIN block.
Both residuals are `3.300004713935323e-11`, below the unchanged `1.0e-10` gate. No
calculator ran during reverification.

S30 is complete. It verified exact source reconstruction under an authenticated
native-serialization bound, zero pair-Hermiticity residual, six Delta-family minima,
positive curvature, and the full locality curve without applying spatial truncation.
S40 is complete without a calculator invocation. All six valley positions pass, while
the indirect-gap criterion, all six longitudinal-mass criteria, and 11 of 12
transverse-mass criteria fail. These are revealed development-oracle labels: they limit
physical-fidelity claims but do not invalidate S30 as the controlled reduction source.
The separately authorized no-calculator S90 design is complete. It freezes all 18
complete shells, pair closure, tail bounds, direct operator and spectrum diagnostics,
and full-source valley and mass changes without selecting a radius. The separately
authorized S100 evaluation is also complete: every mask was reported, pair closure and
Hermiticity pass, and the full-support control is exact. S100 selected no radius. The
separately authorized S105 disposition retains full support, defining `H_T = H_W` and
zero selected spatial-truncation error. It does not create a post-observation threshold
or repurpose parent numerical-convergence tolerances. The separately authorized S110
attempt stopped at the mandatory common-space gate: the projected ten-orbital `sp3s*`
frame has resolved rank 9 at Gamma and one additional C6 point. No fit ran, no parameter
vector exists, and S50 remains blocked. Stopping remains the default. The current
[post-S110 protocol](../../../research-protocol/controlled-reduction-protocol-post-s110.tex)
defines separately authorized foundation, spectral-only, global-unitary, rank-9, and
new-source continuation levels; it authorizes no automatic progression. Reduction
choices, calibration, fits, and oracle-error predictions must be frozen before the 402-point
parent values are observed. Any
`C6-B30`, `C8`, or `C12` source-fidelity route remains a separate scientific decision
and authorization sequence, not a prerequisite for controlled reduction.

## Identities

| Artifact | SHA-256 |
|---|---|
| S90-through-S110 controlled-reduction protocol | `80cf67acf00d6b906a64471ed06379a321bca71ed5b6636174c634a30d8b2380` |
| current post-S110 controlled-reduction protocol | `3ec2902a94ebe78eba1e223a0ee4ef99075f4bd86238398b67d370fa88224653` |
| series plan | `6dca2bfcbb0b00259a2ddf7d8630b82ee693f325ade0aedaabc70d4dcbc67eb7` |
| localization campaign preflight | `b7e6b150e28e4ae79eadffbc8799eb593554ccd4f9792347fbd6852ca9a1977d` |
| localization authorization request | `02375507dbe487f1ad5dee2569151faf04c2e5a5fa3aadd9b0007d977bc26aa7` |
| localization campaign result | `5727bb294590868e28a1fb57e0b847863c6b02b7ab669a8d71ac2a12bd5b9d3c` |
| localization structural diagnostic | `95553e74ffe50177f859b5ec56627ffafeadc0b5c02a8e1745e9852938030618` |
| provider reverification | `23a0a6fe182abd0b5d2f7dcd142f27f81d6d6cca4fe9852be1950b5b622548b6` |
| reconciled provider eligibility | `0b2a0e6bab52574c353d780f562afe11d07bb1400bf149fa1178ddb5e8504e4c` |
| S30 implementation | `985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e` |
| S30 initial fixed-gate result | `f038459542ab2d7801ce83630274fd27db60275c6694b53fbcb904980a22ef89` |
| S30 serialization-bound correction | `680cf0aeaa25c85915e8315ce06d1a821c9172333b43e5046dc8f75ba06a3ef9` |
| S30 characterization result | `37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18` |
| S40 corrected implementation | `c555f690fb0d6a7517bd61bcc3abee5acc30fc337e0bd3add358593f9b8f2952` |
| S40 initial linear-gate disposition | `fbd9ab474328323f43d03754d01a0a9be115ea30739c1a4ac65ca47767d99459` |
| S40 hidden-oracle role correction | `29e58f90c40ec428e12d087b4d6b6b70bfcd18d9c539bdcd9f17aa3dd36f333d` |
| S40 corrected development result | `bb1a6d0fab5d08fecaa0d86cbfe00e8670e7f089e289c6fabc59c32c6f76991d` |
| S90 design implementation | `687ed568e392ea1c3ac333c543313cc57206d5a92903b7e3e015b5103224cc1d` |
| S90 frozen truncation design | `6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531` |
| S100 final implementation | `5e2779945974c4c9cbdf702236d3686d937964be3bb4ff480fe7c476d582436f` |
| S100 initial incomplete result | `4a2e18d889ffc682acc2dc04cf37760aa1d662ac945d0ea8452eae814eb186de` |
| S100 final complete-family evaluation | `1ac8bb59137e8dc7217df52f89c18a84e8599bcf82ec59f40a361929d4322a52` |
| S105 disposition implementation | `6613d234b7e084baede6d9cfef9d34be7e14360b23ccc296e6adacfe24f422e0` |
| S105 full-support disposition | `519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68` |
| S110 implementation | `64459edf6f03161d30c6b6beec3361fa5ad7085417ab2a038d4f6c7c632925b3` |
| S110 blocked alignment result | `b9b8403dfc8b24df01e1671f582697440e1a211d60e0e70c9b0f621dfa086e98` |
| preprocessing result | `ca73c8e0384e5f8b3bccffbe1ab1b2e58d636876f802b380a06eec74f8c50e93` |
| converter result | `b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a` |
| revealed 408-point parent result | `29d3c50f70b9faa0eed24acf5f0673d43eb666d1216327fdf74e53cdd6176b51` |
| frozen 402-point geometry | `51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8` |

No calculator was invoked while preparing the series itself. One later localization
occurrence was separately authorized; its authorization is consumed. Provider
eligibility was later reconciled without another calculator invocation.
