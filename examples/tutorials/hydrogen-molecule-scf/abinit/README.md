# ABINIT hydrogen-molecule SCF backend

**Status: partially materialized; one tutorial execution observed.**

ABINIT basic1 stage 1 supplies the upstream H$_2$ SCF case. The exact input and bundled
PseudoDojo PSP8 were staged externally by verified identity and executed once with
ABINIT 10.8.3 after the decision recorded by checkpoint `ABINIT-BASIC1-RUN-HC01`.
The execution used one process and one OpenMP thread; no MPI launcher was used.

The compact [calculated observation](expected/basic1-stage1-calculated-observation.json)
records useful values extracted from the `.abo`, GSR, EIG, and OUT outputs. The native
NetCDF, density, wavefunction, derivative-database, stdout, and stderr files remain in
the external run area and are not repository fixtures.

The calculation exited successfully and ABINIT reported satisfaction of the tutorial's
`toldfe = 1.0e-6` Hartree criterion at SCF step 6. ABINIT also emitted one warning that
the density fell below `xc_denpos` at 1,275 points and was clipped. The unchanged
upstream settings were not adjusted to suppress the warning. Completion and this
input-specific stopping report do not establish production convergence, numerical
verification, scientific validation, uncertainty quantification, or acceptance.

The exact upstream tutorial input has no file-specific license notice. It is therefore
not copied into this Apache-2.0 repository. The PseudoDojo pseudopotential is attributed
as CC BY 4.0 but is also not committed because the maintained example does not require
redistributing it. Consequently this backend does not yet provide a self-contained run
command; another scientific execution requires its own authorization.

The exact preflight and execution boundary are documented in
[`docs/computational/abinit-basic1-stage1-preflight.md`](../../../../docs/computational/abinit-basic1-stage1-preflight.md).
