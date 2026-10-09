# `Periodic1DSupercellOperatorProvenance`

**Defined in:** `ksdft2effmass.periodic1d.supercell_operators`

## Role

Closed structured provenance containing stable parent-model, source-record,
construction-record, and producer identities. It adapts to fixed `OperatorRecord`
provenance keys without claiming that the referenced records have been authenticated.

## Evidence boundary

`test__Periodic1DSupercellOperatorProvenance.py` checks exact retention and empty-value
rejection. A digest can establish content identity elsewhere but is not accepted as a
scientific identity substitute here.
