"""
geometry_state.py
=================

Industrial Geometry State for Physion Framework.

Purpose
-------
Owns every geometry-related state variable used
throughout the Physion Framework.

Architecture
------------
• Owns geometry variables only.
• Contains NO geometry equations.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by GeometrySolver.

Categories
----------
• Cell Geometry
• Electrode Geometry
• Separator Geometry
• Particle Geometry
• Surface Areas
• Volumes
• Characteristic Lengths

Notes
-----
This class is intentionally passive.

It stores simulation geometry only.

All calculations are delegated to GeometrySolver.

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
class GeometryState(BaseState):
    """
    Industrial Geometry State.

    Stores every geometry quantity required
    by Physion.

    No computation is performed here.
    """
    # =====================================================
    # Cell Geometry
    # =====================================================

    cell_thickness: float = 0.0

    cell_width: float = 0.0

    cell_height: float = 0.0

    cell_volume: float = 0.0

    cell_surface_area: float = 0.0
    # =====================================================
    # Electrode Geometry
    # =====================================================

    anode_thickness: float = 0.0

    cathode_thickness: float = 0.0

    anode_volume: float = 0.0

    cathode_volume: float = 0.0

    anode_surface_area: float = 0.0

    cathode_surface_area: float = 0.0
    # =====================================================
    # Separator Geometry
    # =====================================================

    separator_thickness: float = 0.0

    separator_volume: float = 0.0

    separator_surface_area: float = 0.0
    # =====================================================
    # Particle Geometry
    # =====================================================

    particle_radius: float = 0.0

    particle_surface_area: float = 0.0

    particle_volume: float = 0.0

    particle_characteristic_length: float = 0.0
    # =====================================================
    # Geometry Diagnostics
    # =====================================================

    geometry_warning: bool = False

    geometry_fault: bool = False

    geometry_valid: bool = True

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    