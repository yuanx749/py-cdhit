from pathlib import Path

import pandas as pd
import pandas.testing as tm
import pytest

from pycdhit import _io

FASTA = """
>alpha
ACGTA

>beta
CG
TC
>gamma
CCGCC
"""


CLSTR = """>Cluster 0
0	2799aa, >PF04998.6|RPOC2_CHLRE/275-3073... *
>Cluster 1
0	2202aa, >PF06317.1|Q6UY61_9VIRU/8-2209... at 60%
1	2208aa, >PF06317.1|Q6IVU4_JUNIN/1-2208... *
2	2207aa, >PF06317.1|Q6IVU0_MACHU/1-2207... at 73%
3	2208aa, >PF06317.1|RRPO_TACV/1-2208... at 69%"""


@pytest.fixture
def temp_file():
    test_dir = Path(__file__).resolve().parent
    file = test_dir / "example"
    yield file
    file.unlink()


def test_read_fasta(temp_file):
    temp_file.write_text(FASTA)
    result = _io.read_fasta(temp_file)
    expected = pd.DataFrame(
        {
            "identifier": ["alpha", "beta", "gamma"],
            "sequence": ["ACGTA", "CGTC", "CCGCC"],
        }
    )
    tm.assert_frame_equal(result, expected)


def test_read_clstr(temp_file):
    temp_file.write_text(CLSTR)
    result = _io.read_clstr(temp_file)
    expected = pd.DataFrame(
        {
            "identifier": [
                "PF04998.6|RPOC2_CHLRE/275-3073",
                "PF06317.1|Q6UY61_9VIRU/8-2209",
                "PF06317.1|Q6IVU4_JUNIN/1-2208",
                "PF06317.1|Q6IVU0_MACHU/1-2207",
                "PF06317.1|RRPO_TACV/1-2208",
            ],
            "cluster": [0, 1, 1, 1, 1],
            "size": [2799, 2202, 2208, 2207, 2208],
            "is_representative": [True, False, True, False, False],
            "identity": [100.0, 60.0, 100.0, 73.0, 69.0],
        }
    )
    tm.assert_frame_equal(result, expected)
