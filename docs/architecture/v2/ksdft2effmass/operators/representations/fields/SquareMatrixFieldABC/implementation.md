# Implementation

The class inherits `MatrixFieldABC`, has empty slots, and implements `dimension` as a
read-only derived property. It remains abstract because it does not implement domain,
values, source dimension, or target dimension.

Shape validation belongs to concrete leaves rather than the abstract property getter.
