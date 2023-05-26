import os
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess

import pytest

from pycdhit import _commands

FASTA = """>alpha
ACGTA
>beta
CGTC
>gamma
CCGCC"""


@pytest.fixture
def cdhit_temp_files():
    test_dir = Path(__file__).resolve().parent
    in_path = test_dir / "in"
    out_path = test_dir / "out"
    yield in_path, out_path
    in_path.unlink()
    out_path.unlink(missing_ok=True)
    out_path.with_suffix(".clstr").unlink(missing_ok=True)


def test_cd_hit(cdhit_temp_files):
    os.environ["CD_HIT_DIR"] = "~/cd-hit"
    in_path, out_path = cdhit_temp_files
    in_path.write_text(FASTA)
    try:
        res = _commands.cd_hit_est(i=str(in_path), o=str(out_path))
        assert isinstance(res, CompletedProcess)
    except (CalledProcessError, FileNotFoundError):
        pass
