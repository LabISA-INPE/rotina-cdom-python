import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from scipy.optimize import fmin
import matplotlib.pyplot as plt

def least_squares(x0, spec, l):
    y = np.sum((spec - x0[0] * np.exp(-x0[1] * (l - 532))) ** 2)
    return y

root = tk.Tk()
root.withdraw()

try:
    filename = filedialog.askopenfilename()
except FileNotFoundError:
    print("Arquivo não encontrado")

print("Arquivo aberto")

# delimit = '\t'

# with open(filename, 'r') as arquivo:
#     tline = arquivo.readline()  # Lê uma linha do arquivo

# numcols = tline.count(delimit) + 1

# del_repeated = '%t ' * numcols
# a = del_repeated.strip()

np.set_printoptions(suppress=True, precision=4)

dados = pd.read_csv(filename, delimiter='\t')

# Criação da matriz preenchida com NaN
matrix = np.full((dados.shape[0], dados.shape[1]), np.nan)

# Preenche a matriz com os valores convertidos
for i in range(dados.shape[1]):
    matrix[:,i] = dados.iloc[:, i]

# Inicializa ACDOM com NaNs
# ACDOM = np.empty((581,15))
ACDOM = np.empty_like(matrix)
ACDOM = ACDOM[:, :-1]

print(matrix.shape[1])

# Itera para cada grupo de 7 colunas
for i in range(1, ((matrix.shape[1] - 1) // 7) + 1):
    for ii in range(1, 8):
        ACDOM[:, 0] = matrix[:, 0]
        ACDOM[:, (ii + ((i - 1) * 7) + 1) - 1] = matrix[:, (ii + ((i - 1) * 7) + 2) - 1] - matrix[:, (7 * i - 5) - 1]

# np.savetxt('ACDOM3.txt', ACDOM, fmt='%f', delimiter='\t')

wlg = ACDOM[:, 0]

L = 0.1 # Comprimento da Cubeta em metro

acdom = ACDOM[:, 1:] * 2.303 / L

# np.savetxt('acdom4.txt', acdom, fmt='%f', delimiter='\t')

p1 = np.where(wlg == 750)[0][0]  # Encontra o índice do primeiro valor igual a 750
p2 = np.where(wlg == 800)[0][0]  # Encontra o índice do primeiro valor igual a 800

acdom1 = np.empty_like(acdom)

for ii in range(acdom.shape[0]):
    acdom1[ii, :] = acdom[ii, :] - np.mean(acdom[p1:p2, :], axis=0)

df = pd.DataFrame(acdom1)
df.to_excel('outputs/acdom1.xlsx', index = False)

A = np.empty((len(wlg), 2))
# var = np.zeros(acdom1.shape[1])
acdomcor = np.zeros((299, 14))

A[:, 0] = wlg

I = np.where((A[:, 0] < 700) & (A[:, 0] > 400))[0]

x0 = [1.0, 0.03]

for iii in range(acdom1.shape[1]):

    A[:, 1] = acdom1[:, iii]

    wl = A[I, 0]
    a_g = A[I, 1]

    opts = {'maxiter': 4000, 'maxfun': 2000, 'xtol': 1e-9}

    x1 = fmin(least_squares, x0, args=(a_g, wl), **opts)

    acdomcor[:, iii] = a_g[np.where(wl == 440)[0][0]] * np.exp(-x1[1] * (wl - 440))
    # var[iii] = x1[1]

# np.savetxt('A.txt', A, fmt='%f', delimiter='\t')

# np.savetxt('wl.txt', wl, fmt='%f', delimiter='\t')
# np.savetxt('a_g.txt', a_g, fmt='%f', delimiter='\t')

# np.savetxt('acdomcor.txt', acdomcor, fmt='%f', delimiter='\t')

# Crie o gráfico
figura = plt.figure()
plt.plot(wl, acdomcor, linewidth=2)

# Configuração do gráfico
plt.title('Coeficiente de Absorção do CDOM - Promissao (Ago/22)', fontname='AvantGarde', fontsize=20, fontweight='bold')
plt.xlabel('Comprimento de Onda (nm)', fontname='Helvetica', fontsize=18)
plt.ylabel('a$_{cdom}$ (m$^{-1}$)', fontname='Helvetica', fontsize=18)
plt.tick_params(labelsize=16)
plt.xticks(np.arange(400, 701, step=50))
plt.yticks(np.arange(0, np.max(acdomcor)+1, step=5))
plt.xlim(400, 700)
plt.ylim(0, np.max(acdomcor))
plt.grid(True, which='both', linestyle='--', color=[0.3, 0.3, 0.3])
plt.minorticks_on()
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().xaxis.set_tick_params(width=1)
plt.gca().yaxis.set_tick_params(width=1)

plt.savefig('outputs/grafico.jpg')

# Salvando dados no excel
dados_final = pd.DataFrame(wl)
dados_final = pd.concat([dados_final, pd.DataFrame(acdomcor)], axis=1)
dados_final.to_excel('outputs/dados_finais.xlsx', header=False, index=False)

plt.show()