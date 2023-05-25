# py-cdhit

A Python interface for CD-HIT package.

## Description

This package provides a Python interface for CD-HIT (Cluster Database at High Identity with Tolerance), which has programs for clustering biological sequences with a very fast speed. Specifically, it contains functions that run commands and read the output files, thus reducing the overhead of switching between languages and writing parsing code when using Python in the data analysis workflows.

## Usage

A simple example on Linux is provided below. See the [notebook](docs/examples/examples.ipynb) for more details.

```Python
from pycdhit import cd_hit, read_clstr

stdout = cd_hit(
    i="./docs/examples/APD.fasta",
    o="./docs/examples/out",
    c=0.7,
    d=0,
    sc=1,
)

df_clstr = read_clstr("./docs/examples/out.clstr")
```

Please visit CD-HIT's [documentations](https://github.com/weizhongli/cdhit/wiki) for its installation and the options of commands.

## Installation

### Install

First Install CD-HIT. Then install this package as follows.

Install from PyPI:

```bash
pip install py-cdhit
```

### Develop

Install from source after git clone:

```bash
cd py-cdhit
pip install -e '.[dev,doc]'
python -m pytest --cov-report term-missing --cov=pycdhit tests/
```
