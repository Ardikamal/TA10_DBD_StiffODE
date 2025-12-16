import numpy as np

def euler_explicit(f, t_span, y0, h):
    t0, tf = t_span
    t = np.arange(t0, tf, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0

    for i in range(len(t) - 1):
        y[i+1] = y[i] + h * f(t[i], y[i])
    return t, y
