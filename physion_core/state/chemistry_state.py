"""
chemistry_state.py
==================

Industrial Chemistry State for Physion Framework.

Purpose
-------
Owns every electrochemical variable used throughout the Physion
Framework.

Architecture
------------
• Owns chemistry variables only.
• Contains NO physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by ChemistrySolver.

Categories
----------
• Species Concentration
• Lithium Inventory
• Stoichiometry
• Electrolyte
• Solid Phase
• Diffusion
• Reaction
• Exchange Current
• Charge Transfer
• Thermodynamics
• Kinetics
• Transport
• SEI
• Lithium Plating
• Side Reactions
• Electrochemical Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to ChemistrySolver.

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
class ChemistryState(BaseState):
    """
    Industrial Chemistry State.

    Stores every electrochemical quantity required by
    Physion.

    This object owns the chemistry state of a cell.

    No computation is performed here.
    """