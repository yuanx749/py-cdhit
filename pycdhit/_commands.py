"""A module wraps the programs of CD-HIT."""

import os
import subprocess
from itertools import chain
from pathlib import Path

PROGS = [
    "cd-hit",
    "cd-hit-2d",
    "cd-hit-est",
    "cd-hit-est-2d",
    "cd-hit-div",
    "cd-hit-454",
]


def _create_function(name: str):
    def function(**kwargs) -> str:
        dir_ = Path(os.environ.get("CD_HIT_DIR", "~/cd-hit")).expanduser()
        keys = (f"-{k.replace('_', '-')}" for k in kwargs)
        values = map(str, kwargs.values())
        command = [dir_ / name] + list(chain(*zip(keys, values)))
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                check=True,
                text=True,
            )
            return proc.stdout
        except subprocess.CalledProcessError as err:
            print(err.stderr)
            raise
        except FileNotFoundError:
            print(command)
            raise

    function.__doc__ = f"""Run command {name}.

        Args:
            kwargs: Options and arguments of the command.

        Returns:
            The stdout of the command.

        Raises:
            `~subprocess.CalledProcessError`: If command returns
                non-zero exit status.
            `FileNotFoundError`: If program is not installed.

        """

    return function


functions = [prog.replace("-", "_") for prog in PROGS]
for prog, fun in zip(PROGS, functions):
    globals()[fun] = _create_function(prog)

__all__ = functions
