# ruff: noqa: E501
"""Controlled reduced and exact external QEXSD fixtures for software verification."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

CONTROLLED_QEXSD = b"""<?xml version='1.0'?>
<qes:espresso xmlns:qes='http://www.quantum-espresso.org/ns/qes/qes-1.0' Units='Hartree atomic units'>
  <general_info><xml_format NAME='QEXSD' VERSION='23.03.10'>QEXSD_23.03.10</xml_format><creator NAME='PWSCF' VERSION='7.2'>fixture</creator></general_info>
  <output>
    <atomic_species ntyp='1'><species name='Si'><mass>28.086</mass><pseudo_file>Si.UPF</pseudo_file></species></atomic_species>
    <atomic_structure nat='2' alat='1.0'><atomic_positions><atom name='Si' index='1'>0 0 0</atom><atom name='Si' index='2'>1 1 1</atom></atomic_positions><cell><a1>1 0 0</a1><a2>0 1 0</a2><a3>0 0 1</a3></cell></atomic_structure>
    <basis_set><fft_grid nr1='4' nr2='5' nr3='6'/><fft_smooth nr1='4' nr2='5' nr3='6'/><fft_box nr1='4' nr2='5' nr3='6'/><reciprocal_lattice><b1>1 0 0</b1><b2>0 1 0</b2><b3>0 0 1</b3></reciprocal_lattice></basis_set>
    <total_energy><etot>-1.25</etot></total_energy>
    <band_structure><nbnd>2</nbnd><nks>2</nks>
      <ks_energies><k_point weight='0.25'>0 0 0</k_point><eigenvalues size='2'>-1 0</eigenvalues><occupations size='2'>1 1</occupations></ks_energies>
      <ks_energies><k_point weight='0.75'>0.5 0 0</k_point><eigenvalues size='2'>-0.5 0.5</eigenvalues><occupations size='2'>1 0</occupations></ks_energies>
    </band_structure>
  </output><exit_status>0</exit_status>
</qes:espresso>
"""

CONTROLLED_QEXSD_250521 = CONTROLLED_QEXSD.replace(
    b"VERSION='23.03.10'>QEXSD_23.03.10",
    b"VERSION='25.05.21'>QEXSD_25.05.21",
).replace(b"VERSION='7.2'>fixture", b"VERSION='7.5'>fixture")


def controlled_source_bytes(content: bytes = CONTROLLED_QEXSD) -> tuple[str, int]:
    """Return the independent digest and count for controlled fixture bytes."""
    return hashlib.sha256(content).hexdigest(), len(content)


def _configured_external_path(environment_variable: str) -> Path:
    """Return an explicitly configured external artifact path or skip."""
    configured_path = os.environ.get(environment_variable)
    if configured_path is None:
        pytest.skip(f"set {environment_variable} to run external-artifact evidence")
    return Path(configured_path)


def actual_qexsd_path() -> Path:
    """Return the configured accepted QE 7.2 QEXSD source path."""
    return _configured_external_path("KSDFT2EFFMASS_QE72_QEXSD_PATH")


def actual_qe75_qexsd_path() -> Path:
    """Return the configured QE 7.5 smoke-test QEXSD source path."""
    return _configured_external_path("KSDFT2EFFMASS_QE75_QEXSD_PATH")
