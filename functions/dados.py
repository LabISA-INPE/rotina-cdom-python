from functions import roda_CDOM_correto


def dados(num_grps_amos, amostra_agua, path_cdom, path_dados_finais, titulo_grafico, path_grafico, path_arquivo):
    # Write variables to configuration file "input.txt"
    with open("input.txt", "w") as arquivo:
        arquivo.write(f"num_grps_amos= {num_grps_amos}\n")
        arquivo.write(f"amostra_agua= {amostra_agua}\n")
        arquivo.write(f"path_cdom= {path_cdom}\n")
        arquivo.write(f"path_dados_finais= {path_dados_finais}\n")
        arquivo.write(f"titulo_grafico= {titulo_grafico}\n")
        arquivo.write(f"path_grafico= {path_grafico}\n")
        arquivo.write(f"path_arquivo= {path_arquivo}\n")
        
    print("Variables saved to input.txt file")

    # Call the function to start CDOM analysis routine
    roda_CDOM_correto()