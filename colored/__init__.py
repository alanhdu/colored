from collections import Sequence

import numpy as np

from colored import util
from colored import data


def make_mapping_array(data, N=256, gamma=1.0):
    """ Create an *N*-element 1D array for a lookup table

    *data* should be a list of (x, y) correspondences. The list must
    start with x=0 and end w/ x=1. make_mapping_array will linearly 
    interpolate between the (x, y) correspondences to create the 
    lookup-table.

    For example, if we wanted y to increase from 0 to 1 when x increases
    from 0 to 0.5, and then to drop back to 0 when x goes to 1, we'd pass
    in:
        [(0, 0), (0.5, 1), (1, 0)]

    Alternatively, *data* can be a function mapping [0, 1] to [0, 1]
    """

    if callable(data):
        x = np.linspace(0, 1, N) ** gamma
        return np.clip(data(x), 0, 1).astype(np.float)
    try:
        data = np.array(data, dtype=np.float)
    except:
        msg = "data must be convertable to an array (got {})".format(data)
        raise TypeError(msg)

    x, y = data[:, 0], data[:, 1]

    if x[0] != 0 or x[-1] != 1:
        raise ValueError("Data points must start w/ x=1 and end w/ x=1")
    elif np.sometrue(np.sort(x) - x):
        raise ValueError("Data poisnt must have x in ascending order")

    x *= N - 1

    lookup = np.zeros(N, np.float)
    x_ind = (N - 1) * np.linspace(0, 1, N) ** gamma
    ind = np.searchsorted(x, x_ind)[1:-1]

    distance = (x_ind[1:-1] - x[ind - 1]) / (x[ind] - x[ind - 1])
    lookup[1:-1] = (y[ind] - y[ind - 1]) * distance + y[ind - 1]
    lookup[0], lookup[-1] = y[0], y[-1]

    return np.clip(lookup, 0, 1)


class Colormap(object):
    """ Map floats in [0, 1] to rgb tuples.
    """
    def __call__(self, value, clip=False):
        pass


class LinearColormap(Colormap):
    """ Colormap that uses linearly interpolates"""
    def __init__(self, colors, N=256, gamma=1.0):
        """Create color map from *colors*

        colors should either be a list of (x, (r, g, b)) tuples,
        or a dictionary of that maps ["red", "green", and "blue"]
        onto a format accepted by make_mapping_array
        """
        self.N = N
        if isinstance(colors, Sequence):
            xs, cs = zip(*colors)
            rs, gs, bs = zip(*cs)
            colors = {"red": tuple(zip(xs, rs)),
                      "green": tuple(zip(xs, gs)),
                      "blue": tuple(zip(xs, bs))}

        rs, gs, bs = colors["red"], colors["green"], colors["blue"]

        self.reds = make_mapping_array(rs, N=N, gamma=gamma)
        self.greens = make_mapping_array(gs, N=N, gamma=gamma)
        self.blues = make_mapping_array(bs, N=N, gamma=gamma)

    def __call__(self, value, clip=False):
        value = np.round(np.array(value) * (self.N - 1)).astype(np.uint)
        if np.isscalar(value):
            color = self.reds[value], self.greens[value], self.blues[value]
        else:
            color = zip(self.reds[value], self.greens[value], self.blues[value])
            color = tuple(color)

        return np.array(color)

cmaps = {key: LinearColormap(value)
         for key, value in data.data.items()}


# can't be replaced by lambda -- doesn't work well w/ closures
def reverser(f):
    def func(x):
        return f(1 - x)
    return func

cmaps.update({key + "_r": reverser(value)
              for key, value in cmaps.items()})
