from pathlib import Path

import pandas as pd
import pytest

from pycdhit import _class


class TestCDHIT:
    cdhit_installed = Path("~/cd-hit/cd-hit-est").expanduser().exists()

    @pytest.fixture(autouse=True)
    def init_cdhit(self):
        self.cdhit = _class.CDHIT(prog="cd-hit-est", path="~/cd-hit")

    def test_invalid_name(self):
        with pytest.raises(ValueError):
            _class.CDHIT(prog="")

    @pytest.mark.skipif(not cdhit_installed, reason="FileNotFoundError")
    def test_help(self, capsys):
        self.cdhit.help()
        assert len(capsys.readouterr().out) > 0

    def test_set_options(self):
        self.cdhit.set_options(c=0.9, n=10)
        assert self.cdhit.options == {"c": 0.9, "n": 10}

    @pytest.mark.skipif(not cdhit_installed, reason="FileNotFoundError")
    def test_cluster_return_type(self):
        assert self.cdhit.options == {}
        fasta_in = pd.DataFrame(
            {
                "identifier": ["alpha", "beta", "gamma"],
                "sequence": ["ACGTA", "CGTC", "CCGCC"],
            }
        )
        fasta, clstr = self.cdhit.cluster(fasta_in)
        assert isinstance(fasta, pd.DataFrame)
        assert isinstance(clstr, pd.DataFrame)
