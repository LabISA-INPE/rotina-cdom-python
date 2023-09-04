import pandas as pd
from scipy.interpolate import interp1d

# Carregue os dados do arquivo CSV
tr15 = pd.read_csv(r"C:\Users\kauar\OneDrive\Documentos\INPE\Matlab\Python\Leituras_22_08_2022_organizado.csv", sep=";", decimal=",", na_values="")

# Renomeie a primeira coluna
tr15.columns.values[0] = "Wave"

# Crie um novo DataFrame com as colunas de comprimento de onda desejadas
tr15_completa = pd.DataFrame({"Wave": range(220, 801)})

print(tr15)

# Itere pelas colunas de dados
for col_name in tr15.columns[1:]:
    # Interpole os dados
    interpolator = interp1d(tr15["Wave"], tr15[col_name], kind="linear", fill_value="extrapolate")
    tr15_completa[col_name] = interpolator(tr15_completa["Wave"])

# Salve os resultados em um arquivo CSV
tr15_completa.to_csv(r"C:\Users\kauar\OneDrive\Documentos\INPE\Matlab\Python\Leituras_22_08_2022_organizado.txt", index=False)