from subprocess import CalledProcessError

import pandas as pd
import pytest

from pycdhit import _class


class TestCDHIT:
    @pytest.fixture(autouse=True)
    def init_cdhit(self):
        self.cdhit = _class.CDHIT(prog="cd-hit-est", path="~/cd-hit")

    def test_invalid_name(self):
        with pytest.raises(ValueError):
            _class.CDHIT(prog="")

    def test_help(self, capsys):
        try:
            self.cdhit.help()
            assert len(capsys.readouterr().out) > 0
        except FileNotFoundError:
            pass

    def test_set_options(self):
        self.cdhit.set_options(c=0.9, n=10)
        assert self.cdhit.options == {"c": 0.9, "n": 10}

    def test_cluster_return_type(self):
        assert self.cdhit.options == {}
        fasta_in = pd.DataFrame(
            {
                "identifier": ["alpha", "beta", "gamma"],
                "sequence": ["ACGTA", "CGTC", "CCGCC"],
            }
        )
        try:
            fasta, clstr = self.cdhit.cluster(fasta_in)
            assert isinstance(fasta, pd.DataFrame)
            assert isinstance(clstr, pd.DataFrame)
        except (CalledProcessError, FileNotFoundError):
            pass
