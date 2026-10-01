# `AuthorSuppliedPublisherAbstractEvidence`

`AuthorSuppliedPublisherAbstractEvidence` binds one explicitly authorized APS abstract
URL, DOI, title, authors, publication date, abstract text, exact source-page SHA-256,
a bound `ProjectedCitationIdentity`, a separately local proposed candidate label, and
any source or extraction warnings. Its provenance is always
`AUTHOR_SUPPLIED_AD_HOC` and scope always `PUBLISHER_ABSTRACT`.

Status and canonical citekey are derived only from the bound References projection;
they are not constructor assertions. The abstract work ID must match that projection.
Only candidate status may carry a local proposed noncanonical label. The record makes
no full-paper, rights, scientific-validation, publication, or human-acceptance claim.
