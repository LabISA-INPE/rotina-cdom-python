import numpy as np
from scipy.optimize import minimize

# Importa os dados de entrada, com o comprimento de onda na primeira coluna e absorção por cdom na segunda coluna
A = np.loadtxt('acdom.txt')

# Seleciona o intervalo de interesse
I = np.where((A[:, 0] < 700) & (A[:, 0] > 400))
wl = A[I, 0].flatten()
a_g = A[I, 1].flatten()

# Seleciona as opções para a função minimize (equivalente a fminsearch do MATLAB)
opts = {'maxiter': 4000, 'maxfev': 2000, 'ftol': 1e-9}

# Estima os parâmetros (amplitude em 532 e slope)
x0 = [1.0, 0.03]

# Função para minimização (least_squares)
def least_squares(x, a_g, wl):
    return np.sum((a_g - x[0] * np.exp(-x[1] * (wl - 440)))**2)

# Rotina de minimização
result = minimize(least_squares, x0, args=(a_g, wl), options=opts)
x1 = result.x

acdom = x1[0] * np.exp(-x1[1] * (wl - 440))
