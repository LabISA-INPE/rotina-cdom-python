import pandas as pd
from scipy.interpolate import interp1d

# Carrega os dados do arquivo CSV
tr15 = pd.read_csv("input-exemplo/Leituras_22_08_2022_organizado.csv", sep=";", decimal=",", na_values="")

# Renomeia a primeira coluna
tr15.columns.values[0] = "Wave"

# Cria um novo DataFrame com as colunas de comprimento de onda desejadas
tr15_completa = pd.DataFrame({"Wave": range(220, 801)})

# Itera pelas colunas de dados
for col_name in tr15.columns[1:]:
    # Interpola os dados
    interpolator = interp1d(tr15["Wave"], tr15[col_name], kind="linear", fill_value="extrapolate")
    tr15_completa[col_name] = interpolator(tr15_completa["Wave"])

# df = pd.DataFrame(tr15_completa)

# Salva os resultados em um arquivo CSV
tr15_completa.to_csv("input-exemplo/Leituras_22_08_2022_organizado2.csv", sep=";", index=False)