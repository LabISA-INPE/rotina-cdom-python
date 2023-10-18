import numpy as np
import pandas as pd
import tkinter as tk
import csv
# from tkinter import filedialog
from scipy.optimize import fmin
import matplotlib.pyplot as plt
from tkinter import messagebox

def roda_CDOM_correto():
    def least_squares(x0, spec, l):
        y = np.sum((spec - x0[0] * np.exp(-x0[1] * (l - 532))) ** 2)
        return y

    # Lendo txt com as variáveis
    with open('./input.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    # Adicionando as variáveis no código
    for linha in linhas:
        chave, valor = linha.strip().split('=')
        if chave == 'num_grps_amos': num_grps_amos = int(valor.strip())
        elif chave == 'path_cdom': path_cdom = valor.strip()
        elif chave == 'path_dados_finais': path_dados_finais = valor.strip()
        elif chave == 'titulo_grafico': titulo_grafico = valor.strip()
        elif chave == 'path_grafico': path_grafico = valor.strip()
        elif chave == 'path_arquivo': path_arquivo = valor.strip()
    x = num_grps_amos + 1
    y = num_grps_amos - 1

    root = tk.Tk()
    root.withdraw()

    np.set_printoptions(suppress=True, precision=4)

    try:
        dados = pd.read_csv(path_arquivo, sep=";") 
    except:
        messagebox.showerror(title="Formato de arquivo errado!!", message="O arquivo selecionado para ánalise não está no formato "".csv"" ")
        return

    try:
        # Criação da matriz preenchida com NaN
        matrix = np.full((dados.shape[0], dados.shape[1]), np.nan)

        # Preenche a matriz com os valores convertidos
        for i in range(dados.shape[1]):
            matrix[:,i] = dados.iloc[:, i]

        # Inicializa ACDOM com NaNs
        ACDOM = np.empty_like(matrix)
        ACDOM = ACDOM[:, :-1]

        ACDOM[:, 0] = matrix[:, 0]

        # Itera para cada grupo de 7 colunas
        for i in range(1, ((matrix.shape[1] - 1) // x) + 1):
            for ii in range(1, x + 1):
                ACDOM[:, (ii + ((i - 1) * x) + 1) - 1] = matrix[:, (ii + ((i - 1) * x) + 2) - 1] - matrix[:, (x * i - y) - 1]

        wlg = ACDOM[:, 0]

        L = 0.1 # Comprimento da Cubeta em metro

        acdom = ACDOM[:, 1:] * 2.303 / L

        p1 = np.where(wlg == 750)[0][0]  # Encontra o índice do primeiro valor igual a 750
        p2 = np.where(wlg == 800)[0][0]  # Encontra o índice do primeiro valor igual a 800

        acdom1 = np.empty_like(acdom)

        for ii in range(acdom.shape[0]):
            acdom1[ii, :] = acdom[ii, :] - np.mean(acdom[p1:p2, :], axis=0)

        df = pd.DataFrame(acdom1)
        df.to_excel(path_cdom, index = False)

        A = np.empty((len(wlg), 2))

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
    except:
        messagebox.showerror(title="Dado incorreto!!!", message="O arquivo selecionado para ánalise provavelmente não está organizado corretamente, certifique-se de que o arquivo está interpolado") 
        return

    # Criando o gráfico
    figura = plt.figure()
    plt.plot(wl, acdomcor, linewidth=2)

    # Configurações do gráfico
    plt.title(titulo_grafico, fontname='AvantGarde', fontsize=20, fontweight='bold')
    plt.xlabel('Comprimento de Onda (nm)', fontname='Helvetica', fontsize=18)
    plt.ylabel('a$_{cdom}$ (m$^{-1}$)', fontname='Helvetica', fontsize=18)
    plt.tick_params(labelsize=16)
    plt.xticks(np.arange(400, 701, step=50))
    plt.yticks(np.arange(0, np.max(acdomcor)+1, step=0.2))
    plt.xlim(400, 700)
    plt.ylim(0, np.max(acdomcor))
    plt.grid(True, which='both', linestyle='--', color=[0.3, 0.3, 0.3])
    plt.minorticks_on()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().xaxis.set_tick_params(width=1)
    plt.gca().yaxis.set_tick_params(width=1)

    plt.savefig(path_grafico)

    # Salvando dados no excel
    dados_final = pd.DataFrame(wl)
    dados_final = pd.concat([dados_final, pd.DataFrame(acdomcor)], axis=1)
    dados_final.to_excel(path_dados_finais, header=False, index=False)

    plt.show()

    return