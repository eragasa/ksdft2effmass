# `ksdft2effmass.simulations.abinit`

`ksdft2effmass.simulations.abinit` owns ABINIT-specific simulation composition above
the backend-neutral DFT catalog and ABINIT-native integration mechanics.

Its pseudopotential adapter admits only cataloged PSP8 artifacts for the accepted
common native-representation branch. Although ABINIT can parse some norm-conserving
UPF files, that capability does not override the project decision to pair native
PseudoDojo PSP8 and UPF2 representations under one source-entry identity.

The adapter returns the source-entry identity, independent PSP8 SHA-256, filename,
and content-addressed local path. It performs no current-byte verification, parser
smoke test, input rendering, workspace staging, process invocation, cross-format
comparison, or scientific acceptance. Those operations remain with their explicit
generic verifier, future simulation composition, integration boundary, or scientific
protocol owner.
