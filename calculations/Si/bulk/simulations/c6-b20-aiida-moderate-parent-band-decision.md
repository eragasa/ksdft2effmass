# C6-B20 AiiDA-moderate parent-band decision

## Decision

The next selected target-space stage is `C6-B20`: a fresh Gamma-origin `6 x 6 x 6`
Davidson NSCF with 20 parent bands. Relative to the authenticated 12-band `C6` NSCF,
this stage changes only the calculated parent-band count from 12 to 20. The accepted
structure and SCF parent, pseudopotential, 42/336 Ry cutoffs, 216-point mesh and source
ordering, fixed occupations, `conv_thr = 1.0e-12 Ry`, full-accuracy Davidson
configuration, and symmetry controls remain fixed.

The prepared but unexecuted `C6-T1` localization request is no longer the selected next
execution. It remains retained as no-execution evidence of the narrower 12-band
outer-window proposal. Its authorization request has not been granted and must not be
interpreted as authority to run Wannier90.

## AiiDA workflow design prior

This campaign adopts the moderate *band-count heuristic*, not the complete protocol,
from [`aiida-wannier90-workflows` release 3.1.0, commit
`1c0115cb7c77541a0bd549bc05005df435d651b6`](https://github.com/aiidateam/aiida-wannier90-workflows/tree/1c0115cb7c77541a0bd549bc05005df435d651b6).
The pinned workflow's [moderate protocol sets
`num_bands_factor = 2.0`](https://github.com/aiidateam/aiida-wannier90-workflows/blob/1c0115cb7c77541a0bd549bc05005df435d651b6/src/aiida_wannier90_workflows/workflows/protocols/base/wannier90.yaml#L6-L25).
Its [band estimator](https://github.com/aiidateam/aiida-wannier90-workflows/blob/1c0115cb7c77541a0bd549bc05005df435d651b6/src/aiida_wannier90_workflows/utils/pseudo/__init__.py#L292-L342)
uses, for this non-spin-polarized case,

```text
max(
  int(0.5 * number_of_electrons * factor),
  int(0.5 * number_of_electrons + 4),
  int(number_of_projections * factor),
  int(number_of_projections + 4),
)
```

The exact two-atom Si cell has eight pseudopotential valence electrons and this campaign
has ten declared trial projections. Substitution with factor 2.0 gives

```text
max(8, 8, 20, 14) = 20 parent bands.
```

This is an explicit calculation-owned adaptation. The pinned AiiDA workflow derives
projection counts from its configured pseudo/projector machinery and its default
moderate protocol names `SSSP/1.3/PBEsol/efficiency`; this campaign instead retains its
already accepted SSSP 1.3 PBE efficiency pseudopotential and its declared
`Si:sp3` plus `Si:l=0:r=2` projection family. For this parent-band decision, the citation
supports the factor-two inventory heuristic only. A later, separately documented
[`AiiDA-precise convergence adaptation`](aiida-precise-convergence-adaptation-decision.md)
applies to prospective localization controls; it does not alter this 20-band derivation.
Neither adaptation establishes that AiiDA executed this campaign, that the complete
AiiDA protocol was adopted, or that 20 bands are scientifically adequate.

The workflow repository's requested scientific citations are listed in its pinned
[Support and citations](https://github.com/aiidateam/aiida-wannier90-workflows/tree/1c0115cb7c77541a0bd549bc05005df435d651b6#support-and-citations)
section. The software source and exact pinned implementation above remain the direct
authorities for the numerical derivation used here.

## Staged target-space review

Twenty calculated bands enlarge the available parent Bloch space; they do not change
the requested Wannier rank from 10 to 20. They also do not predetermine which states
belong in an outer window. After, and only after, a separately authorized `C6-B20` NSCF
produces authenticated finite eigenvalues:

1. inventory all 20 eigenvalues at all 216 construction points;
2. report the state-count distributions under both the inherited
   `[-5.85, 19.02] eV` window and the prepared `C6-T1` `[-6.0, 21.0] eV` window;
3. identify crossings or clipping at either boundary;
4. decide the outer window separately while retaining rank 10, the frozen window, and
   the projection family unless a later decision explicitly changes one of them; and
5. prepare distinct preprocessing/conversion/localization requests only after that
   target-space decision.

The current 12-band EIG, AMN, and MMN files cannot represent bands 13--20. Any selected
20-band route therefore requires new NSCF and converter artifacts. Existing failed or
12-band localization outputs are not eligible inputs to the new route.

## Completed inventory stage

One exact, separately authorized `C6-B20` NSCF subsequently completed successfully.
The QEXSD contains 216 points and 20 finite bands spanning
`[-5.8341319732, 30.2720123939] eV`; the saved state verifies. The ordered points and
weights match the 12-band occurrence exactly, and the first 12 eigenvalues agree within
`4.14e-11 eV`.

The inherited `[-5.85, 19.02] eV` window contains 10--14 states per point with
histogram `{10: 12, 11: 62, 12: 96, 13: 24, 14: 22}`. The prepared
`[-6.0, 21.0] eV` window contains 12--14 states with histogram
`{12: 48, 13: 108, 14: 60}`. Bands 13 and 14 enter both investigated windows, while
band 15 remains above `21.0 eV` everywhere. This completes the stipulated inventory;
it does not select either window. A separate target-space decision remains required
before preparing 20-band preprocessing or conversion.

## Bounds and stop rule

The 20-band moderate adaptation is the first broader-parent candidate. The AiiDA precise
factor of 3.0 would yield 30 bands for the same declared projection count, but `C6-B30`
is only a conditional upper diagnostic. It does not follow automatically from failure
of `C6-B20` and requires a separate scientific decision and bounded authorization.

Preparation and documentation did not authorize the completed `pw.x` occurrence; it
was executed only after the exact bounded request was separately granted and is now
consumed. This decision does not authorize `wannier90.x -pp`, `pw2wannier90.x`,
`wannier90.x`, `C6-B30`, any retry, or any other calculator occurrence. Each requires a
new exact authorization after the applicable scientific decision.
