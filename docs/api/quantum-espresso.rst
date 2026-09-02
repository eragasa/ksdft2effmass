Quantum ESPRESSO integration
============================

The primary implemented Quantum ESPRESSO boundary is the loose ``pw.x`` input
representation and writer. It preserves upstream-selected grouping tags and body
lines; it does not model every Quantum ESPRESSO variable, apply scientific defaults,
own provenance, execute the calculator, or interpret output artifacts. QEXSD parsing
is a separate downstream output-side capability.

.. currentmodule:: ksdft2effmass.integration.quantumespresso

.. autoclass:: QePwInputFile
   :members:

.. autoclass:: QePwInputFileWriter
   :members:

The retained silicon SCF software example is available at
``examples/tutorials/silicon-scf/qe``. It introduces no provenance schema; the
existing retained calculation record remains authoritative for the earlier QE 7.2
execution.
