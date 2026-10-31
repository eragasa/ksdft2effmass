# Wannier90 disentanglement convergence tolerance note

## Native criterion

Wannier90 3.1.0 prints the disentanglement convergence quantity as `Delta (frac.)` and
computes it in `disentangle.F90` as

\[
\delta_i = \frac{\Omega_I(i-1)}{\Omega_I(i)} - 1.
\]

It declares convergence only when

\[
|\delta_i| < \mathtt{dis\_conv\_tol}
\]

for every entry in the declared convergence window. Therefore `dis_conv_tol` is a
dimensionless relative/fractional tolerance in the executed implementation. It must not
be interpreted as an absolute spread tolerance in square angstroms. This differs from
Wannierisation `conv_tol`, which applies to an absolute spread change and is expressed
in square angstroms.

Some earlier campaign records and the Wannier90 3.1.0 user-guide prose label
`dis_conv_tol` as having square-angstrom units. Those exact historical records remain
retained for provenance, but this note governs their scientific interpretation.

## Equivalent absolute tolerance

For one iteration, the native condition is exactly equivalent to the scale-dependent
absolute condition

\[
|\Omega_I(i-1)-\Omega_I(i)|
< \mathtt{dis\_conv\_tol}\,|\Omega_I(i)|.
\]

At the conditioned occurrence's final reported value
\(\Omega_I(i)=15.09162945\ \text{angstrom}^2\), the declared fractional tolerance
`1.0e-10` corresponds to

\[
\mathrm{atol}_{\Omega_I}
= 1.0\times10^{-10}\times15.09162945
= 1.509162945\times10^{-9}\ \text{angstrom}^2.
\]

The appropriate local equivalent absolute tolerance is therefore **approximately
`1.51e-9 angstrom^2`**. It is not a universal fixed tolerance: it must be recomputed as
`dis_conv_tol * abs(current Omega_I)` if the spread scale changes.

At iteration 1000, the printed absolute spread change was
`5.757e-5 angstrom^2`, corresponding to the native fractional delta `3.815e-6`. That
change was about `3.81e4` times the declared threshold.

## Verification consequence

The WOUT table prints \(\Omega_I\) to eight decimal places, giving an absolute display
resolution of order `1e-8 angstrom^2`, which is coarser than the `1.51e-9 angstrom^2`
equivalent threshold. Independent checks based only on the printed spread columns
cannot reproduce the native `1.0e-10` decision reliably. Retained assessment must use
the native fractional-delta field and convergence message; higher-precision internal
values would be required for an independent absolute comparison at the exact threshold.

ProjectKoios currently types the rendered disentanglement tolerance as a
square-angstrom quantity. That typing is retained as an implementation follow-up and
must not be used to infer the native criterion's physical dimension.
