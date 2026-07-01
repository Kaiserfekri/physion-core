"""
simulation_update.py
====================

Industrial Simulation Update Object
for Physion Framework.

Purpose
-------
Carries immutable simulation execution updates from
SimulationSolver to CommitManager.

Architecture
------------
SimulationSolver
        │
        ▼
SimulationUpdate
        │
        ▼
CommitManager
        │
        ▼
SimulationState

Notes
-----
This object is immutable.

It contains NO solver logic.

It contains NO execution logic.

It contains NO validation logic other than
BaseUpdate generic validation.

Mirror Rule
-----------
Every public data field of SimulationState is mirrored
here one-to-one.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class SimulationUpdate(BaseUpdate):
    """
    Immutable snapshot of SimulationState.
    """

    # =====================================================
    # Time
    # =====================================================

    time: float

    dt: float

    # =====================================================
    # Cycle Information
    # =====================================================

    cycle: int

    step: int

    iteration: int

    # =====================================================
    # Solver
    # =====================================================

    converged: bool

    solver_iterations: int

    # =====================================================
    # Execution Status
    # =====================================================

    running: bool

    paused: bool

    finished: bool

    aborted: bool