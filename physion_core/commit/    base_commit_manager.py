"""
base_commit_manager.py
======================

Industrial Base Commit Manager for Physion Framework.

Purpose
-------
Defines the common commit workflow for every
Physion state.

Architecture
------------
Solver
    ↓
Update
    ↓
CommitManager
    ↓
State

Responsibilities
----------------
• Commit immutable updates
• State validation
• Hook execution
• Timestamp update

Contains
--------
• NO physics
• NO numerical methods
• NO solver logic
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic
from typing import TypeVar

from physion_core.state.base_state import BaseState
from physion_core.update.base_update import BaseUpdate


StateT = TypeVar(
    "StateT",
    bound=BaseState,
)

UpdateT = TypeVar(
    "UpdateT",
    bound=BaseUpdate,
)

class BaseCommitManager(
    Generic[
        StateT,
        UpdateT,
    ],
    ABC,
):
    """
    Base class for every Physion Commit Manager.
    """

    def __init__(
        self,
        state: StateT,
    ) -> None:

        self._state = state

    @property
    def state(self) -> StateT:
        """
        Managed state.
        """

        return self._state
        
    # =====================================================
    # Commit
    # =====================================================

    def commit(
        self,
        update: UpdateT,
    ) -> None:
        """
        Commit an immutable update into the managed state.
        """

        if not update.validate():

            raise ValueError(
                f"Invalid {update.class_name}."
            )

        self.before_commit(
            update,
        )

        self.apply_update(
            update,
        )

        self.after_commit(
            update,
        )
        
    # =====================================================
    # Hooks
    # =====================================================

    def before_commit(
        self,
        update: UpdateT,
    ) -> None:
        """
        Hook executed before commit.
        """

        return

    def after_commit(
        self,
        update: UpdateT,
    ) -> None:
        """
        Hook executed after commit.
        """

        return
        
    # =====================================================
    # Apply Update
    # =====================================================

    @abstractmethod
    def apply_update(
        self,
        update: UpdateT,
    ) -> None:
        """
        Apply an immutable update to the managed state.

        Notes
        -----
        This method must modify the managed state
        using the supplied update.

        Validation is handled by BaseCommitManager.
        """
        raise NotImplementedError
