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
            num_linhas_waves = len(dados.iloc[:, 0])

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

            # Calcule the difference between each row for acdom and the meam of row between p1 and p2
            for ii in range(acdom.shape[0]):
                acdom1[ii, :] = acdom[ii, :] - np.mean(acdom[p1:p2, :], axis=0)

            # Save ACDOM data to Excel
            df = pd.DataFrame(acdom1)
            df.to_excel(path_cdom, index=False)
            print(f"CDOM data saved to: {path_cdom}")
            
            # Optimization setup
            A = np.empty((len(wlg), 2))
            acdomcor = np.zeros((num_linhas_waves, num_colunas-1))
            A[:, 0] = wlg

            I = np.where((A[:, 0] < ultima_linha_wave+1) & (A[:, 0] > segunda_linha_wave-1))[0]

            x0 = [1.0, 0.03]

            # Optimization loop
            for iii in range(acdom1.shape[1]):
                # Fill the second column of matrix A with CDOM attenuation values
                A[:, 1] = acdom1[:, iii]

                wl = A[I, 0]
                a_g = A[I, 1]
                opts = {'maxiter': 4000, 'maxfun': 2000, 'xtol': 1e-9}
                x1 = fmin(least_squares, x0, args=(a_g, wl), disp=False, **opts)

                # Calculate corrected CDOM atenuation and store results in acdomcor
                acdomcor[:, iii] = a_g[np.where(wl == 440)[0][0] * np.exp(-x1[1] * (wl - 440))]

            # Prepare sample names
            nome = []
            for k in range(1, len(dados.columns[1:])+1):
                col_name = dados.columns[k]
                if "_" in col_name:
                    nome.append(col_name[col_name.find("_") +1:])
                else:
                    nome.append(col_name)
            
            acdom_df = pd.DataFrame(acdom)

            # Remove water sample columns
            nome = [nome[i] for i in range(len(nome)) if i not in amostra_agua]
            acdom_df = acdom_df.drop(acdom_df.columns[amostra_agua], axis=1)

            # Create the plot
            plt.figure(figsize=(12, 8))
            
            # Plot each sample
            for i, col in enumerate(acdom_df.columns):
                plt.plot(wl, acdom_df.iloc[:, i], linewidth=2, 
                        label=nome[i] if i < len(nome) else f'Sample {i+1}')
            
            # Plot configuration
            plt.title(titulo_grafico, fontname='Arial', fontweight='bold', fontsize=16)
            plt.xlabel('Comprimento de Onda (nm)', fontname='Arial', fontsize=14)
            plt.ylabel('a$_{cdom}$ (m$^{-1}$)', fontname='Arial', fontsize=14)
            plt.tick_params(labelsize=12)
            plt.xticks(np.arange(220, 801, step=50))

            # Set y-axis dynamically
            max_val = np.max(acdom_df.iloc[duzentos:oitocentos])
            if max_val > 0:
                step = max(1, int(max_val /10))
                plt.yticks(np.arange(0, max_val + step, step=step))
                plt.ylim(0, max_val * 1.05)

            plt.xlim(220, 800)
            plt.grid(True, which='both', linestyle='--', color=[0.3, 0.3, 0.3], alpha=0.7)
            plt.minorticks_off()
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().xaxis.set_tick_params(width=1)
            plt.gca().yaxis.set_tick_params(width=1)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()    

            # Save plot
            plt.savefig(path_grafico)
            plt.close()
            print(f"Plot saved to: {path_grafico}")

            # Prepare final data
            nome.insert(0, "Wave")

            # Save final data to Excel
            dados_final = pd.DataFrame(wl, columns=["Wave"])
            dados_final = pd.concat([dados_final, acdom_df], axis=1)
            dados_final.to_excel(path_dados_finais, header=nome, index=False)
            print(f"Final data saved to: {path_dados_finais}")

            print("CDOM analysis completed successfully!")
        
    except FileNotFoundError as e:
        error_msg = f"File not found: {str(e)}"
        print(f"Error: {error_msg}")
        raise

    except ValueError as e:
        error_msg = f"Data format error: {str(e)}"
        print(f"Error: {error_msg}")
        raise
    
    except Exception as e:
        error_msg = f"Unexpected error in CDOM analysis: {str(e)}"
        print(f"Error: {error_msg}")
        raise