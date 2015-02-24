import pytest

import matplotlib as mpl
from matplotlib import cm
import numpy as np

import colored as clrd

@pytest.mark.parametrize("col", ["#95Fa51", "#161ACA", "#FFFFFF"])
def test_hex2color(col):
    ours = (col, clrd.util.hex2color(col))
    theirs = (col, mpl.colors.hex2color(col))
    assert ours == theirs

@pytest.mark.parametrize("col", ["#95Fa51", "turquoise", "0.33", "b"])
def test_to_rgb(col):
    ours = (col, clrd.util.to_rgb(col))
    theirs = (col, mpl.colors.colorConverter.to_rgb(col))
    assert ours == theirs



if __name__ == "__main__":
    pytest.main()
