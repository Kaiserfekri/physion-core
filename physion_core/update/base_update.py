"""
base_update.py
==============

Industrial Base Update Object for Physion Framework.

Purpose
-------
Defines the immutable contract for every Physion
Update Object.

Architecture
------------
Solver
    ↓
Update Object
    ↓
Commit Manager
    ↓
State

Responsibilities
----------------
• Immutable update container
• Metadata
• Validation hooks
• Lightweight diagnostics

Contains
--------
• NO physics
• NO numerical methods
• NO state ownership
• NO commit logic

Physion Principles
------------------
✔ Immutable
✔ Type Safe
✔ Passive Object
✔ Single Responsibility
✔ High Performance
✔ Industrial Readability
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC

import uuid


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseUpdate(ABC):
    """
    Base class for every Physion Update Object.

    Update objects are immutable.

    They transport solver results to the
    Commit Manager.
    """

    # =====================================================
    # Framework Version
    # =====================================================

    VERSION: str = "2.0.0"

    # =====================================================
    # Metadata
    # =====================================================

    update_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
        repr=False,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
        init=False,
        repr=False,
    )

    # =====================================================
    # Diagnostics
    # =====================================================

    valid: bool = True

    # =====================================================
    # Information
    # =====================================================

    @property
    def class_name(self) -> str:
        """
        Return update class name.
        """
        return self.__class__.__name__

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:
        """
        Validate update object.

        Child classes may override.
        """
        return self.valid

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (
            f"{self.class_name}"
            "("
            f"id={self.update_id[:8]}"
            ")"
        )