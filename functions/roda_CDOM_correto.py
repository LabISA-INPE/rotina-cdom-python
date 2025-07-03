import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import fmin
import os

def roda_CDOM_correto():
    def least_squares(x0, spec, l):
        y = np.sum((spec - x0[0] * np.exp(-x0[1] * (1 - 532))) ** 2)
        return y
    
    try:
        with open("./input.txt", "r") as arquivo:
            linhas = arquivo.readlines()

        # Add variables to the code
        for linha in linhas:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                chave = chave.strip()
                valor = valor.strip()

                if chave == "num_grps_amos":
                    num_grps_amos = int(valor)
                elif chave == "path_cdom":
                    path_cdom = valor
                elif chave == "path_dados_finais":
                    path_dados_finais = valor
                elif chave == "titulo_grafico":
                    titulo_grafico = valor
                elif chave == "path_grafico":
                    path_grafico = valor
                elif chave == "path_arquivo":
                    path_arquivo = valor
                elif chave == "amostra_agua":
                    amostra_agua = valor

            x = num_grps_amos + 1
            y = num_grps_amos - 1

            # Parse water sample values
            valores_amostra_agua = amostra_agua.strip().split(",")
            amostra_agua = [int(valor.strip()) for valor in valores_amostra_agua]

            # Check if the selected file is .csv
            if not path_arquivo.lower().endswith(".csv"):
                raise ValueError("The selected file for analysis is not in '.csv' format")
            
            # Load CSV data
            try:
                dados = pd.read_csv(path_arquivo, sep=";")
                print(f"Successfully loaded data with shape: {dados.shape}")
            except Exception as e:
                raise ValueError(f"Error reading CSV file: {str(e)}")
            
            # Check if data is properly organized
            num_colunas = len(dados.columns)
            num_linas_wave = len(dados.iloc[:, 0])

            segunda_linha_wave = dados.iloc[0, 0]
            duzentos = 220 - segunda_linha_wave

            ultima_linha_wave = dados.iloc[-1, 0]
            oitocentos = duzentos + 580

            # Create a matrix filled with NaN
            matrix = np.full((dados.shape[0], dados.shape[1]), np.nan)

            # Fill the matrix with converted values
            for i in range(dados.shape[1]):
                matrix[:, 1] = dados.iloc[:, i]

            # Initialize ACDOM WITH NaNs
            ACDOM = np.empty_like(matrix)
            ACDOM = ACDOM[:, :-1]
            ACDOM[:, 0] = matrix[:, 0]

            # Iterate for each group of columns
            for i in range(1, ((matrix.shape[1] - 1) // x ) +1 ):
                for ii in range(1, x + 1):
                    ACDOM[:, (ii + ((i - 1) * x) + 1) - 1] = matrix[:, (ii + ((i - 1) * x) + 2) - 1] - matrix[:, (x * i - y) - 1]
            
            wlg = ACDOM[:, 0]

            L = 0.1 # Cuvette length in meters

            acdom = ACDOM[:, 0:] * 2.303 / L

            # Find indices for basline correction
            p1 = np.where(wlg == 750)[0][0] # Find index of first value equal to 750
            p2 = np.where(wlg == 800)[0][0] # Find index of first value equal to 800

            acdom1 = np.empty_like(acdom)

            