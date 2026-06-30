"""
simulation_state.py
===================

Simulation execution state.

This module stores only the execution status of the
simulation.

It never performs numerical calculations.

Physion Core Principle
----------------------
SimulationState owns only simulation execution data.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import copy


@dataclass(slots=True)
class SimulationState:
    """
    Simulation execution state.

    Notes
    -----
    Stores only execution-related variables.
    """

    # =====================================================
    # Time
    # =====================================================

    time: float = 0.0

    dt: float = 0.0

    # =====================================================
    # Cycle information
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
    # Status
    # =====================================================

    running: bool = False

    paused: bool = False

    finished: bool = False

    aborted: bool = False

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:
        """
        Reset simulation state.
        """

        self.time = 0.0
        self.dt = 0.0

        self.cycle = 0
        self.step = 0
        self.iteration = 0

        self.converged = True
        self.solver_iterations = 0

        self.running = False
        self.paused = False
        self.finished = False
        self.aborted = False

    # =====================================================
    # Copy
    # =====================================================

    def copy(self) -> "SimulationState":
        """
        Return a deep copy.
        """

        return copy.deepcopy(self)

    # =====================================================
    # Dictionary conversion
    # =====================================================

    def to_dict(self) -> dict:
        """
        Convert state to dictionary.
        """

        return asdict(self)

    # =====================================================
    # Restore
    # =====================================================

    def from_dict(
        self,
        data: dict,
    ) -> None:
        """
        Restore state from dictionary.
        """

        for key, value in data.items():

            if hasattr(self, key):

                setattr(self, key, value)

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> None:
        """
        Validate simulation state.
        """

        if self.time < 0:

            raise ValueError(
                "Simulation time cannot be negative."
            )

        if self.dt < 0:

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