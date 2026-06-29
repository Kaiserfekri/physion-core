"""
Physion Core
Metadata definitions for chemistry parameter sets.

Stores descriptive information only.
No numerical simulation parameters should be placed here.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class ChemistryMetadata:
    chemistry: str
    level: str

    version: str = "1.0.0"

    author: str = "Physion Team"

    organization: str = "Physion Core"

    description: str = ""

    source: str = ""

    created: str = str(date.today())

    units: str = "SI"

    validated: bool = False

    experimental: bool = False

    notes: str = ""


def build_metadata(**kwargs) -> ChemistryMetadata:
    """
    Create a metadata object.

    Example
    -------
    meta = build_metadata(
        chemistry="lithium_metal",
        level="industrial"
    )
    """
    return ChemistryMetadata(**kwargs)