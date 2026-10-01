# `ManuscriptBibliographyEntrySnapshot`

Immutable bibliography entry in file order. It retains owner entry identity, literal
case-sensitive key, entry type, exact bibliography locator, entry-level content
identity, and a nullable independent References observation binding. The owner emits
that binding as `None`; complete replay checks key uniqueness, locator lineage, span
size, entry identity, and citation bindings.
