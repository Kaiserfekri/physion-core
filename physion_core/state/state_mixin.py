"""
state_mixin.py
==============

Reusable infrastructure for every Physion state-like object.

StateMixin contains only generic utilities.

No battery physics.

No solver logic.

No simulation logic.
"""

from __future__ import annotations

import copy
import hashlib
import json

from dataclasses import asdict
from typing import Any


class StateMixin:
    """
    Reusable utilities for Physion objects.
    """

    VERSION = "1.0.0"

    # =====================================================
    # Deep Copy
    # =====================================================

    def clone(self):

        return copy.deepcopy(self)

    def copy(self):

        return self.clone()

    # =====================================================
    # Dictionary
    # =====================================================

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)

    # =====================================================
    # JSON
    # =====================================================

    def to_json(
        self,
        indent: int = 4,
    ) -> str:

        return json.dumps(

            self.to_dict(),

            indent=indent,

            sort_keys=True,

            default=str,

        )

    # =====================================================
    # Checksum
    # =====================================================

    def checksum(self) -> str:
        """
        Stable SHA256 checksum of the current object.
        """

        payload = json.dumps(

            self.to_dict(),

            sort_keys=True,

            default=str,

        ).encode("utf-8")

        return hashlib.sha256(

            payload

        ).hexdigest()

    # =====================================================
    # Equality
    # =====================================================

    def equals(

        self,

        other: object,

    ) -> bool:

        if not isinstance(

            other,

            self.__class__,

        ):

            return False

        return (

            self.checksum()

            ==

            other.checksum()

        )

    # =====================================================
    # Difference
    # =====================================================

    def diff(

        self,

        other,

    ) -> dict[str, tuple[Any, Any]]:

        if not isinstance(

            other,

            self.__class__,

        ):

            raise TypeError(

                "Objects must have identical type."

            )

        changes = {}

        mine = self.to_dict()

        yours = other.to_dict()

        for key in mine:

            if mine[key] != yours[key]:

                changes[key] = (

                    mine[key],

                    yours[key],

                )

        return changes

    # =====================================================
    # Reflection
    # =====================================================

    def field_names(self):

        return list(

            self.to_dict().keys()

        )

    def field_values(self):

        return list(

            self.to_dict().values()

        )

    def field_count(self):

        return len(

            self.to_dict()

        )

    # =====================================================
    # Version
    # =====================================================

    @classmethod
    def version(cls):

        return cls.VERSION

    # =====================================================
    # Representation
    # =====================================================

    def __str__(self):

        return self.to_json()

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(version={self.VERSION})"

        )