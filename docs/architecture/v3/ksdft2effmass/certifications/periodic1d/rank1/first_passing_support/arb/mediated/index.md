# Mediated maximum-error Arb enclosure

`mediated.py` constructs the frozen 256-point parent sample, retains Fourier coefficients
inside one requested ordinary support, evaluates the candidate on all 1025 staggered
points, and encloses the finite maximum total error.

- [`MediatedMaximumErrorArbEncloser`](MediatedMaximumErrorArbEncloser/index.md)

The module does not enclose the direct-fit route or assemble a certification result.

[Back to the Arb capability](../index.md)
