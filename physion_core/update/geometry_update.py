"""
geometry_update.py
==================

Industrial Geometry Update Object
for Physion Framework.

Purpose
-------
Carries the final geometry solution produced by
GeometrySolver.

Architecture
------------
GeometrySolver
        ↓
GeometryUpdate
        ↓
CommitManager
        ↓
GeometryState

Mirror
------
This object is an exact mirror of GeometryState.

Contains
--------
• NO geometry equations
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
class GeometryUpdate(BaseUpdate):

    # =====================================================
    # Cell Geometry
    # =====================================================

    cell_thickness: float

    cell_width: float

    cell_height: float

    cell_volume: float

    cell_surface_area: float

    # =====================================================
    # Electrode Geometry
    # =====================================================

    anode_thickness: float

    cathode_thickness: float

    anode_volume: float

    cathode_volume: float

    anode_surface_area: float

    cathode_surface_area: float

    # =====================================================
    # Separator Geometry
    # =====================================================

    separator_thickness: float

    separator_volume: float

    separator_surface_area: float

    # =====================================================
    # Particle Geometry
    # =====================================================

    particle_radius: float

    particle_surface_area: float

    particle_volume: float

    particle_characteristic_length: float

    # =====================================================
    # Geometry Diagnostics
    # =====================================================

    geometry_warning: bool

    geometry_fault: bool

    geometry_valid: bool

    measurement_valid: bool

    solver_converged: bool

    validation_passed: bool