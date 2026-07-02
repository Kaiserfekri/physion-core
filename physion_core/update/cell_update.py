"""
cell_update.py
==============

Industrial Cell Update for Physion Framework.

Purpose
-------
Immutable snapshot update object for CellState.

Notes
-----
Carries immutable snapshots of CellState components
to be committed.

Contains NO physics.

Contains NO solver logic.

Contains NO state ownership.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from physion_core.update.base_update import BaseUpdate

from physion_core.state.cell_state import (
    CellIdentity,
    CellConfiguration,
    CellLimits,
    CellMetadata,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CellUpdate(BaseUpdate):
    """
    Immutable snapshot update object for CellState.
    """

    # =====================================================
    # Identity
    # =====================================================

    identity: CellIdentity = field(
        default_factory=CellIdentity
    )

    # =====================================================
    # Configuration
    # =====================================================

    configuration: CellConfiguration = field(
        default_factory=CellConfiguration
    )

    # =====================================================
    # Limits
    # =====================================================

    limits: CellLimits = field(
        default_factory=CellLimits
    )

    # =====================================================
    # Metadata
    # =====================================================

    metadata: CellMetadata = field(
        default_factory=CellMetadata
    )

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:
        """
        Validate immutable CellUpdate container.

        Notes
        -----
        Validates only the update container itself.

        State consistency is validated after commit
        by CellState.
        """

        return super().validate()