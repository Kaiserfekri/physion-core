"""
aging_update.py
===============

Industrial Aging Update Object
for Physion Framework.

Purpose
-------
Carries the final degradation solution produced by
AgingSolver.

Architecture
------------
AgingSolver
        ↓
AgingUpdate
        ↓
CommitManager
        ↓
AgingState

Mirror
------
This object is an exact mirror of AgingState.

Contains
--------
• NO degradation equations
• NO numerical methods
• NO solver logic
• NO commit logic
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AgingUpdate(BaseUpdate):

    # =====================================================
    # Capacity Fade
    # =====================================================

    capacity_fade: float
    relative_capacity_fade: float
    available_capacity_loss: float
    irreversible_capacity_loss: float
    capacity_retention: float

    # =====================================================
    # Resistance Growth
    # =====================================================

    resistance_growth: float
    relative_resistance_growth: float
    internal_resistance_growth: float
    interfacial_resistance_growth: float
    sei_resistance_growth: float

    # =====================================================
    # Loss of Lithium Inventory
    # =====================================================

    lithium_inventory_loss: float
    relative_lithium_inventory_loss: float
    cyclable_lithium_loss: float
    irreversible_lithium_loss: float
    lithium_inventory_retention: float

    # =====================================================
    # Loss of Active Material
    # =====================================================

    active_material_loss: float
    relative_active_material_loss: float
    anode_active_material_loss: float
    cathode_active_material_loss: float
    active_material_retention: float

    # =====================================================
    # Solid Electrolyte Interphase (SEI)
    # =====================================================

    sei_thickness: float
    sei_growth: float
    sei_growth_rate: float
    sei_volume_fraction: float
    sei_coverage: float

    # =====================================================
    # Cycle Aging
    # =====================================================

    cycle_count: float
    equivalent_full_cycles: float
    cycle_aging: float
    cycle_aging_rate: float

    # =====================================================
    # Calendar Aging
    # =====================================================

    calendar_time: float
    calendar_aging: float
    calendar_aging_rate: float

    # =====================================================
    # Mechanical and Thermal Aging
    # =====================================================

    mechanical_aging: float
    thermal_aging: float
    coupled_aging: float

    # =====================================================
    # Aging Diagnostics
    # =====================================================

    aging_warning: bool
    aging_fault: bool
    end_of_life_reached: bool
    replacement_recommended: bool
    measurement_valid: bool
    solver_converged: bool
    validation_passed: bool