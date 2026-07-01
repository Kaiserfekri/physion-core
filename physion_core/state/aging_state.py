"""
aging_state.py
==============

Industrial Aging State for Physion Framework.

Purpose
-------
Owns every degradation-related state variable used
throughout the Physion Framework.

Architecture
------------
• Owns aging variables only.
• Contains NO degradation equations.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by AgingSolver.

Categories
----------
• Capacity Fade
• Resistance Growth
• Lithium Inventory Loss
• SEI
• Active Material Loss
• Mechanical Aging
• Thermal Aging
• Cycle Aging
• Calendar Aging
• Aging Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to AgingSolver.

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
class AgingState(BaseState):
    """
    Industrial Aging State.

    Stores every degradation quantity required
    by Physion.

    No computation is performed here.
    """
    # =====================================================
    # Capacity Fade
    # =====================================================

    capacity_fade: float = 0.0

    relative_capacity_fade: float = 0.0

    available_capacity_loss: float = 0.0

    irreversible_capacity_loss: float = 0.0

    capacity_retention: float = 1.0
    # =====================================================
    # Resistance Growth
    # =====================================================

    resistance_growth: float = 0.0

    relative_resistance_growth: float = 0.0

    internal_resistance_growth: float = 0.0

    interfacial_resistance_growth: float = 0.0

    sei_resistance_growth: float = 0.0
    # =====================================================
    # Loss of Lithium Inventory
    # =====================================================

    lithium_inventory_loss: float = 0.0

    relative_lithium_inventory_loss: float = 0.0

    cyclable_lithium_loss: float = 0.0

    irreversible_lithium_loss: float = 0.0

    lithium_inventory_retention: float = 1.0
    # =====================================================
    # Loss of Active Material
    # =====================================================

    active_material_loss: float = 0.0

    relative_active_material_loss: float = 0.0

    anode_active_material_loss: float = 0.0

    cathode_active_material_loss: float = 0.0

    active_material_retention: float = 1.0
    # =====================================================
    # Solid Electrolyte Interphase (SEI)
    # =====================================================

    sei_thickness: float = 0.0

    sei_growth: float = 0.0

    sei_growth_rate: float = 0.0

    sei_volume_fraction: float = 0.0

    sei_coverage: float = 0.0
    # =====================================================
    # Cycle Aging
    # =====================================================

    cycle_count: float = 0.0

    equivalent_full_cycles: float = 0.0

    cycle_aging: float = 0.0

    cycle_aging_rate: float = 0.0
    # =====================================================
    # Calendar Aging
    # =====================================================

    calendar_time: float = 0.0

    calendar_aging: float = 0.0

    calendar_aging_rate: float = 0.0
    # =====================================================
    # Mechanical and Thermal Aging
    # =====================================================

    mechanical_aging: float = 0.0

    thermal_aging: float = 0.0

    coupled_aging: float = 0.0
    # =====================================================
    # Aging Diagnostics
    # =====================================================

    aging_warning: bool = False

    aging_fault: bool = False

    end_of_life_reached: bool = False

    replacement_recommended: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    