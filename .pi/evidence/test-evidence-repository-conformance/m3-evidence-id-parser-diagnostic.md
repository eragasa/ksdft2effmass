# M3 evidence-ID parser diagnostic

The production `AuditEvidenceIdentifiers` action reports 59 `PIH.EVIDENCE.ID_INVALID` findings and zero occurrences for the 59 M3 modules even though focused structural validation finds 346 unique owners.

Cause: `python/src/ksdft2effmass/harness/pi/evidence.py::_declaration` searches `ast.get_docstring(node, clean=False)` with `^Evidence ID$`. Function docstring continuation lines contain their source indentation, so the multiline anchor does not match. The fallback examines the first line, which is the heading `Evidence ID`, not its following identifier. This is a deterministic multiline-dedent parser defect, not an M3 ownership gap.

A read-only strict diagnostic using `ast.get_docstring(node, clean=True)`, the same exact field block, and the loaded local namespace profile passed with 346 owners, 346 unique IDs, and zero field, namespace, width, range, or duplicate findings. Structural validation independently returned the same 346 unique-owner count.

Production source and harness tests are outside M3 mutation scope, so this defect was diagnosed but not repaired. It remains a required later harness correction and prevents treating the generic action's current result as a valid strict audit of indented maintained docstrings.
