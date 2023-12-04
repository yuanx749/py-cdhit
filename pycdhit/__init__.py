"""A Python interface for CD-HIT package."""

from ._class import *  # noqa: F403
from ._commands import *  # noqa: F403
from ._io import *  # noqa: F403

VERSION = "0.8.0"

__all__ = [  # noqa: F405
    "CommandBase",
    "CDHIT",
    "read_fasta",
    "write_fasta",
    "read_clstr",
    "cd_hit",
    "cd_hit_2d",
    "cd_hit_est",
    "cd_hit_est_2d",
    "cd_hit_div",
    "cd_hit_454",
    "cd_hit_dup",
    "cd_hit_lap",
]
