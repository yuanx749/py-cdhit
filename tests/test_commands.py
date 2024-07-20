import os
from pathlib import Path
from subprocess import CompletedProcess

import pytest

from pycdhit import _commands

FASTA = """>alpha
ACGTA
>beta
CGTC
>gamma
CCGCC"""


os.environ["CD_HIT_DIR"] = "~/cd-hit"


@pytest.fixture
def cdhit_temp_files():
    test_dir = Path(__file__).resolve().parent
    in_path = test_dir / "in"
    out_path = test_dir / "out"
    yield in_path, out_path
    in_path.unlink()
    out_path.unlink(missing_ok=True)
    out_path.with_suffix(".clstr").unlink(missing_ok=True)


@pytest.mark.skipif(
    not Path("~/cd-hit/cd-hit-est").expanduser().exists(),
    reason="FileNotFoundError",
)
def test_cd_hit(cdhit_temp_files):
    in_path, out_path = cdhit_temp_files
    in_path.write_text(FASTA)
    res = _commands.cd_hit_est(i=in_path, o=out_path)
    assert isinstance(res, CompletedProcess)


@pytest.mark.skipif(
    not Path("~/cd-hit/cd-hit-div").expanduser().exists(),
    reason="FileNotFoundError",
)
def test_warning(cdhit_temp_files):
    in_path, out_path = cdhit_temp_files
    in_path.write_text(FASTA)
    with pytest.warns(UserWarning, match="Warning"):
        _commands.cd_hit_div(i=in_path, o=out_path, div=1)
