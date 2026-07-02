"""
cell_update.py
==============

Industrial Cell Update Object
for Physion Framework.

Purpose
-------
Carries immutable cell-level updates from
CellSolver to CommitManager.

Architecture
------------
CellSolver
      │
      ▼
CellUpdate
      │
      ▼
CommitManager
      │
      ▼
CellState

Notes
-----
This object is immutable.

It contains NO solver logic.

It contains NO battery physics.

It contains NO validation logic other than
BaseUpdate generic validation.

Mirror Rule
-----------
Every public data field of CellState
is mirrored here one-to-one.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CellUpdate(BaseUpdate):
    """
    Immutable snapshot of CellState.
    """

    # =====================================================
    # Identity
    # =====================================================

    cell_name: str

    cell_type: str

    chemistry: str

    manufacturer: str

    serial_number: str

    # =====================================================
    # Configuration
    # =====================================================

    parallel_cells: int

    series_cells: int

    nominal_capacity: float

    nominal_voltage: float

    nominal_energy: float

    # =====================================================
    # Operating Mode
    # =====================================================

    charging: bool

    discharging: bool

    resting: bool

    balancing: bool

    # =====================================================
    # Operating Limits
    # =====================================================

    maximum_voltage: float

    minimum_voltage: float

    maximum_current: float

    maximum_temperature: float

    minimum_temperature: float

    # =====================================================
    # Diagnostics
    # =====================================================

    cell_warning: bool

    cell_fault: bool

    measurement_valid: bool

    solver_converged: bool

    validation_passed: bool
    