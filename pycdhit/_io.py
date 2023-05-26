"""A module parsing the output files of CD-HIT."""

import re
from pathlib import Path
from typing import Union

import pandas as pd

FilePath = Union[str, Path]


def read_fasta(file: FilePath) -> pd.DataFrame:
    """Parse file in fasta format.

    Args:
        file: A file path.

    Returns:
        The data of fasta file.

    """
    rows = []
    with open(file) as f:
        # skip text before the first record
        for line in f:
            if line[0] == ">":
                identifier = line[1:].rstrip()
                break
        seq = ""
        for line in f:
            if line[0] != ">":
                seq += line.rstrip()
            else:
                rows.append((identifier, seq))
                identifier = line[1:].rstrip()
                seq = ""
        rows.append((identifier, seq))
    return pd.DataFrame.from_records(rows, columns=["identifier", "sequence"])


def read_clstr(file: FilePath) -> pd.DataFrame:
    """Parse file in clstr format.

    Args:
        file: A file path.

    Returns:
        The data of clstr file.

    """
    # refer to PrintInfo
    identifier, cluster, size, is_representative, identity = [], [], [], [], []
    coverage, strand = [], []  # distance is not used
    with open(file) as f:
        for line in f:
            if line[0] == ">":
                idx = int(re.search(r">Cluster (\d+)", line).group(1))
                continue
            cluster.append(idx)
            line = line.split()
            size.append(int(re.search(r"(\d+)(aa|nt),", line[1]).group(1)))
            identifier.append(re.search(r">(.+)\.{3}", line[2]).group(1))
            if line[3] == "*":
                is_representative.append(True)
                identity.append(100.0)
                coverage.append(None)
                strand.append(None)
                continue
            is_representative.append(False)
            identity.append(float(re.search(r"([\d.]+)%", line[4]).group(1)))
            if match := re.search(r"(\d+):(\d+):(\d+):(\d+)\/", line[4]):
                coverage.append(tuple(map(int, match.groups())))
            else:
                coverage.append(None)
            if match := re.search(r"([+-])\/", line[4]):
                strand.append(match.group(1))
            else:
                strand.append(None)
    locals_ = locals()
    data = {
        col_name: lst
        for col_name in [
            "identifier",
            "cluster",
            "size",
            "is_representative",
            "identity",
            "coverage",
            "strand",
        ]
        if any(lst := locals_[col_name])
    }
    return pd.DataFrame(data)


__all__ = ["read_fasta", "read_clstr"]
