"""A module containing high-level interface for the programs of CD-HIT."""

from pathlib import Path
from subprocess import CalledProcessError
from typing import Tuple
from uuid import uuid4

import pandas as pd

from ._commands import _format_options, _format_program, _run
from ._io import read_clstr, read_fasta, write_fasta

__all__ = ["CommandBase", "CDHIT"]


class CommandBase:
    """Base class for command-line programs.

    Args:
        prog: Name of the program.
        path: Path of the program. Default `None`.

    Attributes:
        options (dict): Parameters and arguments.
        subprocess (`~subprocess.CompletedProcess`): The finished process.
            Default `None`.

    """

    def __init__(self, prog: str, path: str = None):
        self.prog = prog
        self.path = path
        self.options = {}
        self._prog = _format_program(prog, path)
        self.subprocess = None

    def help(self):
        """Print help message."""
        res = _run([self._prog, "--help"])
        print(res.stdout)

    def set_options(self, **kwargs) -> "CommandBase":
        """Set and update options and arguments.

        Args:
            **kwargs: Options and arguments of the command.

        Returns:
            Instance of self with `options` updated.

        """
        self.options.update(kwargs)
        return self

    def run(self):
        """Run the program.

        Returns:
            The `~subprocess.CompletedProcess`.

        """
        command = [self._prog] + list(_format_options(self.options))
        self.subprocess = _run(command)
        return self.subprocess


class CDHIT(CommandBase):
    """Class for CD-HIT programs.

    Args:
        prog: Name of the program.
            {'cd-hit', 'cd-hit-2d', 'cd-hit-est', 'cd-hit-est-2d'},
            default 'cd-hit'.
        path: Path of the program. Default `None`.

    Attributes:
        options (dict): Parameters and arguments.
        subprocess (`~subprocess.CompletedProcess`): The finished process.
            Default `None`.

    """

    def __init__(self, prog: str = "cd-hit", path: str = None):
        if prog not in {"cd-hit", "cd-hit-2d", "cd-hit-est", "cd-hit-est-2d"}:
            raise ValueError(
                f"'{prog}' not in {{'cd-hit', 'cd-hit-2d', 'cd-hit-est', 'cd-hit-est-2d'}}"  # noqa: E501
            )
        super().__init__(prog, path)

    def help(self):
        try:
            super().help()
        except CalledProcessError:
            pass

    def set_options(self, **kwargs) -> "CDHIT":
        return super().set_options(**kwargs)

    def cluster(
        self,
        input1: pd.DataFrame,
        input2: pd.DataFrame = None,
    ) -> Tuple[pd.DataFrame, ...]:
        """Run the program with `~pandas.DataFrame` input.

        Args:
            input1: Input fasta data.
            input2: Input fasta data. Required for 2D programs.

        Returns:
            The output fasta and clstr data, as tuple of `~pandas.DataFrame`.

        Note:
            Specifiy the option 'o' to keep the output files.

        """
        options = self.options.copy()
        in_file = Path.cwd() / str(uuid4())
        options["i"] = str(in_file)
        write_fasta(in_file, input1)
        if "o" not in self.options:
            out_file = Path.cwd() / str(uuid4())
            options["o"] = str(out_file)
        else:
            out_file = Path(options["o"])
        if isinstance(input2, pd.DataFrame):
            in_file_2 = Path.cwd() / str(uuid4())
            options["i2"] = str(in_file_2)
            write_fasta(in_file_2, input2)
        command = [self._prog] + list(_format_options(options))
        try:
            self.subprocess = _run(command)
            fasta = read_fasta(out_file)
            clstr = read_clstr(out_file.with_suffix(".clstr"))
        finally:
            in_file.unlink()
            if "o" not in self.options:
                out_file.unlink(missing_ok=True)
                out_file.with_suffix(".clstr").unlink(missing_ok=True)
            if isinstance(input2, pd.DataFrame):
                in_file_2.unlink()
        return fasta, clstr
