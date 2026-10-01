# `ManuscriptCitationTodo`

Immutable prospective editorial marker with marker and priority locators, closed
priority, and ordered generated call/occurrence IDs. A marker may generate multiple
calls. Replay derives those tuples from all records carrying the same marker index and
rejects fabricated, missing, duplicated, or reordered links.
