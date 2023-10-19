import numpy as np
from functions.roda_CDOM_correto import roda_CDOM_correto

# Escreve as variáveis no arquivo de configuração "input.txt"
def dados(num_grps_amos, path_cdom, path_dados_finais, titulo_grafico, path_grafico, path_arquivo):
    with open("input.txt", "w") as arquivo:
        arquivo.write(f"num_grps_amos= {num_grps_amos}\n")
        arquivo.write(f"path_cdom= {path_cdom}\n")
        arquivo.write(f"path_dados_finais= {path_dados_finais}\n")
        arquivo.write(f"titulo_grafico= {titulo_grafico}\n")
        arquivo.write(f"path_grafico= {path_grafico}\n")
        arquivo.write(f"path_arquivo= {path_arquivo}\n")

    print("As variáveis foram salvas no arquivo input.txt.")

    # Chama a função para iniciar a rotina de análise de CDOM
    roda_CDOM_correto()
