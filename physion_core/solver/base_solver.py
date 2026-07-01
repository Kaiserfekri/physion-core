"""
base_solver.py
==============

Industrial Base Solver for Physion Framework.

Purpose
-------
Defines the standard lifecycle for every Physion solver.

Responsibilities
----------------
• Initialization
• Validation
• Preparation
• Numerical Solution
• State Update
• Convergence Check
• Finalization

Contains NO battery physics.

Contains NO equations.

Contains NO material models.

Physion Principles
------------------
✔ Passive State
✔ Solver Ownership
✔ Single Write Rule
✔ Snapshot State
✔ Separation of Concerns
✔ High Performance
✔ Industrial Readability
✔ Extensibility
"""
from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Any

class BaseSolver(ABC):
    """
    Industrial abstract base class
    for every Physion solver.
    """
    
        @abstractmethod
    def initialize(self) -> None:
        """
        Allocate resources.

        Called once before solving starts.
        """
        
            @abstractmethod
    def validate(self) -> None:
        """
        Validate required inputs
        before solving.
        """
        
            @abstractmethod
    def prepare(self) -> None:
        """
        Prepare internal structures
        required for numerical solution.
        """
        
        