# Numerical contract

The factory performs no numerical allocation or arithmetic. It delegates intrinsic
identity validation to `RepresentationIdentity`, whose `rank` is derived from the space
and whose `domain_id` is derived from the complete domain object.

Wrong nominal domain or role types raise `TypeError`; no string or integer is converted
into an enum member.
