import numpy as np

def least_squares(x0, spec, l):
    y = np.sum((spec - x0[0] * np.exp(-x0[1] * (l - 532))) ** 2)
    return y