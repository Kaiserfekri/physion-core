"""
mechanical_state.py
===================

Industrial Mechanical State for Physion Framework.

Purpose
-------
Owns every mechanical-related state variable used
throughout the Physion Framework.

Architecture
------------
• Owns mechanical variables only.
• Contains NO mechanics equations.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by MechanicalSolver.

Categories
----------
• Stress
• Strain
• Deformation
• Pressure
• Contact
• Crack
• Mechanical Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to MechanicalSolver.

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
class MechanicalState(BaseState):
    """
    Industrial Mechanical State.

    Stores every mechanical quantity required
    by Physion.

    No computation is performed here.
    """
    # =====================================================
    # Stress
    # =====================================================

    stress: float = 0.0

    axial_stress: float = 0.0

    radial_stress: float = 0.0

    tangential_stress: float = 0.0

    hydrostatic_stress: float = 0.0

    von_mises_stress: float = 0.0

    maximum_principal_stress: float = 0.0

    minimum_principal_stress: float = 0.0

    equivalent_stress: float = 0.0
    # =====================================================
    # Strain
    # =====================================================

    strain: float = 0.0

    axial_strain: float = 0.0

    radial_strain: float = 0.0

    tangential_strain: float = 0.0

    plastic_strain: float = 0.0

    elastic_strain: float = 0.0

    equivalent_strain: float = 0.0

    volumetric_strain: float = 0.0
    # =====================================================
    # Deformation
    # =====================================================

    displacement: float = 0.0

    axial_displacement: float = 0.0

    radial_displacement: float = 0.0

    thickness_change: float = 0.0

    volume_change: float = 0.0

    deformation_rate: float = 0.0
    # =====================================================
    # Pressure
    # =====================================================

    pressure: float = 0.0

    contact_pressure: float = 0.0

    internal_pressure: float = 0.0

    external_pressure: float = 0.0

    pore_pressure: float = 0.0

    pressure_gradient: float = 0.0
    # =====================================================
    # Crack
    # =====================================================

    crack_length: float = 0.0

    crack_width: float = 0.0

    crack_depth: float = 0.0

    crack_density: float = 0.0

    crack_growth_rate: float = 0.0

    fracture_index: float = 0.0

    fracture_detected: bool = False
    # =====================================================
    # Mechanical Diagnostics
    # =====================================================

    mechanical_warning: bool = False

    mechanical_fault: bool = False

    excessive_deformation: bool = False

    excessive_stress: bool = False

    excessive_strain: bool = False

    fracture_risk: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    