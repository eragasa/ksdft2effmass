# Meeting notes — 2026-08-14

These notes preserve agenda items and self-reported progress for graduate-student
coordination. Checked items do not by themselves establish retained calculation
provenance, numerical convergence, scientific validation, or project acceptance.

## TODO RAGASA
- [x] workflow automation engine complete
- [ ] write automation schemes for QE
	- [x] SCF with relaxation
	- [x] SCF without relaxation
	- [x] NSCF from SCF
	- [ ] SCF convergence workflows
- [ ] write automation scheme for Wannier90
- [ ] Systems silicon bulk
## TODO LLENARIZAS

- [ ] Start powerpoint slides (ksdft2effmass/slides/\*.ppt)
	- [ ] kpoints converence on conventional unit cell
		- [ ] table,
		- [ ] simulations/conventionalcell/convergence/kpoints/2x2x2
		- [ ] simulations/conventionalcell/convergence/kpoints/3x3x3
		- [ ] ...
		- [ ] graph, script to create the graph
	- [ ] encut convergence on conventional unit cell
		- [ ] table,
		- [ ] simulations/conventionalcell/encut/xxx_eV/
	- [ ] wannier process
		- [ ] PBE-PAW flowchart
		- [ ] simulations/conventionalcell/wannier/scf
		- [ ] simulations/conventionalcell/wannier/nscf
		- [ ] simulations/conventionalcell/wannier/wannier90
		- [ ] simulations/conventioanlcell/wannier/analysis
- [ ] start looking at tight binding
	- [ ] Traditional Multi-Orbital Matrix approach to TB. https://github.com/deepmodeling/tbplas
	- [ ] Kittel, (tight binding).   Simon (tight binding, 2 chapters)
	- [ ] If we need to go custom, PythTB + SciPy
- [ ] Start paper outline/LaTeX (ksdft2effmass/paper/)
- [ ] Familiarize yourself with the project
	- [ ] Conference Abstract: https://github.com/eragasa/ksdft2effmass/blob/dev/docs/publications/conferences/ICMSEP2026/ksdft2effmass.ICMEP2026.abstract.md
	- [ ] Computational Tasks: https://github.com/eragasa/ksdft2effmass/blob/dev/docs/computational/ksdft2effmass.computational.00.md
	- [ ] https://github.com/eragasa/ksdft2effmass/blob/dev/docs/research/ksdft2effmass.00.md
- [ ] Tight-binding
- [ ] 2 atom, primitive unit cell of Si
		- [ ] make an image of the primitive cell inside the the conventional cell (https://jp-minerals.org/vesta/en/)

## Tasks Completed
- [x] QE, running, Si, PBE-GGA
	- [x] kpoint convergence.
	- [x] energy cutoff convergence.
- [x] Wannier90.x
	- [x] https://wannier.org/  (this is the original wannier library)
	- [x] https://www.quantum-espresso.org/Doc/INPUT_pw2wannier90.html (dft2wannier
	- [x] https://www.youtube.com/watch?v=8sxAr0Rtp2k&list=PLcGOxeoscxDBYKFJAUQhk
- [X] AUGUST 1, 2026: Submit enhanced abstract for conference.  https://www.imep-inc.org/icmsep-2026?fbclid=IwZXh0bgNhZW0CMTAAYnJpZBEyZUJyUWlMdWk2ZnJraFRzaHNydGMGYXBwX2lkEDIyMjAzOTE3ODgyMDA4OTIAAR6Q8IFLNKSMxYdy2PU95Y7KbOG3vlGChfs3ER6-ivi31PXDi0-ZKOAu9sl0mg_aem_ysxR0H3ThAT7kA8Gb2HJ3w
