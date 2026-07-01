"""
Physion Update Package
======================

Update objects are immutable containers that carry
solver results to the Commit Manager.

Architecture
------------
Solver
    ↓
Update
    ↓
Commit Manager
    ↓
State

This package contains every Update object used
inside the Physion Framework.

Principles
----------
• Immutable
• Type Safe
• No Physics
• No Solver Logic
• No State Ownership
"""

from .base_update import BaseUpdate

from .electrical_update import ElectricalUpdate
from .thermal_update import ThermalUpdate
from .chemistry_update import ChemistryUpdate
from .transport_update import TransportUpdate
from .mechanical_update import MechanicalUpdate
from .aging_update import AgingUpdate
from .geometry_update import GeometryUpdate
from .boundary_update import BoundaryUpdate

__all__ = [
    "BaseUpdate",
    "ElectricalUpdate",
    "ThermalUpdate",
    "ChemistryUpdate",
    "TransportUpdate",
    "MechanicalUpdate",
    "AgingUpdate",
    "GeometryUpdate",
    "BoundaryUpdate",
]