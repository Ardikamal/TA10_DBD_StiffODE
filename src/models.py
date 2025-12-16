import numpy as np

def sir_model(t, y, beta=5.0, gamma=0.1):
    S, I, R = y
    dS = -beta * S * I
    dI = beta * S * I - gamma * I
    dR = gamma * I
    return np.array([dS, dI, dR])
