from collections import Sequence

import pytest

import matplotlib as mpl
from matplotlib import cm
import numpy as np

import colored as clrd

@pytest.mark.parametrize("col", ["#95Fa51", "#161ACA", "#FFFFFF"])
def test_hex2color(col):
    assert col is col and clrd.util.hex2color(col) == mpl.colors.hex2color(col)

@pytest.mark.parametrize("col", ["#95Fa51", "turquoise", "0.33", "b", "darkslategrey", "g"])
def test_to_rgb(col):
    ours = clrd.util.to_rgb(col)
    theirs = mpl.colors.colorConverter.to_rgb(col)
    assert col is col and ours == theirs
    assert ours == theirs

@pytest.mark.parametrize("col", [(0, 0, 0), (0.3, 0.7, 0.1), (1, 1, 1)])
def test_rgb2hex(col):
    assert col is col and clrd.util.rgb2hex(col) == mpl.colors.rgb2hex(col)

@pytest.mark.parametrize("name", ["flag", "gnuplot2"])
def test_make_mapping_array_funcs(name):
    data = clrd.data.data[name]

    for value in data.values():
        ours = clrd.make_mapping_array(data=value, N=256)
        theirs = mpl.colors.makeMappingArray(data=value, N=256)
        assert data is data and value is value and (ours == theirs).all()

@pytest.mark.parametrize("name", ["terrain", "pink", "binary"])
def test_make_mapping_array_tuple(name):
    data = clrd.data.data[name]
    xs, cs = zip(*data)
    rs, gs, bs = zip(*cs)
    data = {"red": tuple(zip(xs, rs)),
            "green": tuple(zip(xs, gs)),
            "blue": tuple(zip(xs, bs))}

    rs, gs, bs = data["red"], data["green"], data["blue"]

    for value in data.values():
        ours = clrd.make_mapping_array(data=value, N=256)
        # add 3rd value
        xs, cs = zip(*value)
        value = tuple(zip(xs, cs, cs))
        theirs = mpl.colors.makeMappingArray(data=value, N=256)

        assert data is data and value is value and (ours == theirs).all()

@pytest.mark.parametrize("name", clrd.cmaps.keys())
def test_cmaps(name):
    l = np.linspace(0, 1, 256)
    cmap = clrd.cmaps[name]
    other = getattr(cm, name)
    
    ours = cmap(l)
    theirs = other(l)[:, :3]              # ignore alpha
    diff = np.abs(ours - theirs).sum()    # allow floating point errors

    assert name is name and diff < 0.0001

if __name__ == "__main__":
    pytest.main()
