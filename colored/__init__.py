import numpy as np

from colored import util


def make_mapping_array(data, N=256, gamma=1.0):
    if callable(data):
        x = np.linspace(0, 1, N) ** gamma
        return np.clip(data(x), 0, 1).astype(np.float)
    try:
        data = np.array(data, dtype=np.float)
    except:
        raise TypeError("data must be convertable to an array")

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
    pass
