# Periodic calculation record extraction

**Status:** Software-verification record from the accepted external QEXSD artifact;
not numerical verification, scientific validation, convergence acceptance, or UQ.

The retained canonical JSON was mechanically parsed from
`/Users/eugene/projects/q-e-qe-7.2/tempdir/silicon.save/data-file-schema.xml`
(SHA-256 `2ad68bf1f16d6fda3873f5967677a81e81f16a9f88a797701134c0e5fecdd1d9`,
55,068 bytes) and then separately constructed as periodic-calculation semantics.
The parser supports only namespace `http://www.quantum-espresso.org/ns/qes/qes-1.0`
and observed QEXSD version `23.03.10`; the producer is PWSCF 7.2.

The record contains one ordered species, two ordered atoms, $3\times3$ direct and
reciprocal lattice arrays, ten ordered $k$ points with unnormalized represented
weights summing to 2.0, $10\times4$ eigenvalue and occupation arrays, total energy
`-7.922263630348509` in the native declared `Hartree atomic units`, three
`(20, 20, 20)` FFT grids, and exit status 0. Record and parser schema versions are
1 and `23.03.10`, respectively.

Absolute energy reference, Fermi-level alignment convention, retained subspace,
gauge, phase convention, basis identity, and spin convention remain typed as
unavailable. No Wannier functions, localized orbitals, physical band identities,
or convergence-sufficiency claim is inferred.

As a separate consistency observation, the XML energy converts using exactly
$1\ \mathrm{Ha}=2\ \mathrm{Ry}$ to `-15.844527260697017 Ry`. The retained tutorial
stdout reports `-15.84452726 Ry`; `E_XML(converted) - E_stdout` is
`-6.970175547849067e-10 Ry`. The native XML value remains unchanged in JSON.
