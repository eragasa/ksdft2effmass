# `ManuscriptSourceLocator`

Excerpt-free locator containing root-relative path, complete source content identity,
include-instance index, half-open UTF-8 byte span, and one-based line/column. Replay
correlates the locator to the exact source descriptor and include instance, checks span
containment, and bounds display integers against represented source size.
