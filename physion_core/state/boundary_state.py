"""
boundary_state.py
=================

Industrial Boundary State for Physion Framework.

Purpose
-------
Owns every boundary-condition variable used
throughout the Physion Framework.

Architecture
------------
• Owns boundary conditions only.
• Contains NO physics equations.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by BoundarySolver.

Categories
----------
• Electrical Boundary
• Thermal Boundary
• Mechanical Boundary
• Chemical Boundary
• Transport Boundary

Notes
-----
This class is intentionally passive.

It stores boundary conditions only.

All calculations are delegated to BoundarySolver.

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
class BoundaryState(BaseState):
    """
    Industrial Boundary State.

    Stores every boundary condition required
    by Physion.

    No computation is performed here.
    """
    # =====================================================
    # Electrical Boundary
    # =====================================================

    applied_current: float = 0.0

    applied_voltage: float = 0.0

    applied_power: float = 0.0

    load_resistance: float = 0.0
    # =====================================================
    # Thermal Boundary
    # =====================================================

    ambient_temperature: float = 298.15

    ambient_pressure: float = 101325.0

    heat_flux_boundary: float = 0.0

    convective_heat_transfer_coefficient: float = 0.0

    radiative_heat_transfer_coefficient: float = 0.0
    # =====================================================
    # Mechanical Boundary
    # =====================================================

    applied_force: float = 0.0

    applied_pressure: float = 0.0

    displacement_constraint: float = 0.0

    fixed_constraint: bool = False
    # =====================================================
    # Chemical Boundary
    # =====================================================

    concentration_boundary: float = 0.0

    species_flux_boundary: float = 0.0
    # =====================================================
    # Transport Boundary
    # =====================================================

    diffusion_flux_boundary: float = 0.0

    migration_flux_boundary: float = 0.0
    # =====================================================
    # Boundary Diagnostics
    # =====================================================

    boundary_warning: bool = False

    boundary_fault: bool = False

    boundary_valid: bool = True

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    