"""
simulation_state.py
===================

Industrial Simulation State for Physion Framework.

Purpose
-------
Owns every simulation execution variable used
throughout the Physion Framework.

Architecture
------------
• Owns execution state only.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by SimulationSolver.

Categories
----------
• Time
• Cycle Information
• Solver Status
• Execution Status

Notes
-----
This class is intentionally passive.

All execution logic belongs to SimulationSolver.

Physion Principles
------------------
✔ Separation of Concerns
✔ Single Source of Truth
✔ Passive State
✔ Solver Ownership
✔ Explicit Validation
✔ Industrial Readability
✔ High Performance
✔ Future Extensibility
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.state.base_state import BaseState


@dataclass(slots=True, kw_only=True)
class SimulationState(BaseState):
    """
    Industrial Simulation State.

    Stores every execution-related quantity required
    by Physion.

    No computation is performed here.
    """

    # =====================================================
    # Time
    # =====================================================

    time: float = 0.0

    dt: float = 0.0

    # =====================================================
    # Cycle Information
    # =====================================================

    cycle: int = 0

    step: int = 0

    iteration: int = 0

    # =====================================================
    # Solver
    # =====================================================

    converged: bool = True

    solver_iterations: int = 0

    # =====================================================
    # Execution Status
    # =====================================================

    running: bool = False

    paused: bool = False

    finished: bool = False

    aborted: bool = False

    # =====================================================
    # Validation
    # =====================================================

    def validate_impl(self) -> None:
        """
        Validate simulation execution state.
        """

        if self.time < 0.0:
            raise ValueError(
                "Simulation time cannot be negative."
            )

        if self.dt < 0.0:
            raise ValueError(
                "Time step cannot be negative."
            )

        if self.cycle < 0:
            raise ValueError(
                "Cycle number cannot be negative."
            )

        if self.step < 0:
            raise ValueError(
                "Step number cannot be negative."
            )

        if self.iteration < 0:
            raise ValueError(
                "Iteration number cannot be negative."
            )

        if self.solver_iterations < 0:
            raise ValueError(
                "Solver iterations cannot be negative."
            )

        # ---------------------------------------------
        # Time Consistency
        # ---------------------------------------------

        if self.running and self.dt <= 0.0:
            raise ValueError(
                "Running simulation requires dt > 0."
            )

        # ---------------------------------------------
        # Execution State Consistency
        # ---------------------------------------------

        if self.finished and self.paused:
            raise ValueError(
                "Finished simulation cannot be paused."
            )

        if self.aborted and self.paused:
            raise ValueError(
                "Aborted simulation cannot be paused."
            )
            
        active_states = (
            int(self.running)
            + int(self.paused)
            + int(self.finished)
            + int(self.aborted)
        )

        if active_states > 1:
            raise ValueError(
                "Simulation execution states are mutually exclusive."
            )

        if self.finished and self.running:
            raise ValueError(
                "Finished simulation cannot be running."
            )

        if self.aborted and self.running:
            raise ValueError(
                "Aborted simulation cannot be running."
            )