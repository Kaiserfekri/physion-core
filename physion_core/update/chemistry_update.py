"""
chemistry_update.py
===================

Industrial Chemistry Update Object
for Physion Framework.

Purpose
-------
Carries the final chemistry solution produced by
ChemistrySolver.

Architecture
------------
ChemistrySolver
        ↓
ChemistryUpdate
        ↓
Commit Manager
        ↓
ChemistryState

Contains
--------
Final chemistry values only.

Contains NO equations.

Contains NO solver logic.

Contains NO commit logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(frozen=True, slots=True, kw_only=True)
class ChemistryUpdate(BaseUpdate):
    """
    Immutable chemistry update.

    Produced exclusively by ChemistrySolver.
    """

    # =====================================================
    # Chemistry Solution
    # =====================================================

    electrolyte_concentration: float

    solid_concentration: float

    lithium_concentration: float

    lithium_surface_concentration: float

    reaction_rate: float

    exchange_current_density: float

    equilibrium_potential: float

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:

        if self.electrolyte_concentration < 0.0:
            return False

        if self.solid_concentration < 0.0:
            return False

        if self.lithium_concentration < 0.0:
            return False

        if self.lithium_surface_concentration < 0.0:
            return False

        if self.exchange_current_density < 0.0:
            return False

        return super().validate()