"""A Python interface for CD-HIT package."""

from ._commands import *  # noqa: F403
from ._io import *  # noqa: F403

VERSION = "0.2.0"

__all__ = [  # noqa: F405
    "read_fasta",
    "read_clstr",
    "cd_hit",
    "cd_hit_2d",
    "cd_hit_est",
    "cd_hit_est_2d",
    "cd_hit_div",
    "cd_hit_454",
]
