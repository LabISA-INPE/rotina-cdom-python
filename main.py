from tkinter import *
from tkinter import filedialog
import os

from functions.dados import dados

path_arquivo_output_cdom = ''
path_arquivo_output_dados = ''
selected_file_path = ''
path_arquivo_caminho = ''

# Especifique o nome da pasta que você deseja criar
nome_pasta = "outputs"

# Verifique se a pasta já existe antes de tentar criá-la
if not os.path.exists(nome_pasta):
    os.mkdir(nome_pasta)
    print(f'A pasta "{nome_pasta}" foi criada com sucesso.\n')
else:
    print(f'A pasta "{nome_pasta}" já existe.\n')

def start():

    def upload_file():
        global path_arquivo_caminho  # Declare path_arquivo como uma variável global
        try:
            filename = filedialog.askopenfilename()
            filename_text["text"] = filename.split('/')[-1]
            path_arquivo_caminho = filename  # Atribui o valor a path_arquivo
            print(path_arquivo_caminho)
        except FileNotFoundError:
            print("Arquivo não encontrado")

    def path_output_excel(file_type):
        global path_arquivo_output_cdom
        global path_arquivo_output_dados
        try:
            if file_type == "cdom":
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
                path_arquivo_output_cdom = file_path
                print(path_arquivo_output_cdom)
            elif file_type == "dados":
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
                path_arquivo_output_dados = file_path
                print(path_arquivo_output_dados)
        except FileNotFoundError:
            print("Arquivo não foi criado")

    def path_output_jpg():
        global selected_file_path
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Files", "*.jpg")])
            selected_file_path = file_path
            print(selected_file_path)
        except FileNotFoundError:
            print("Arquivo não foi criado")
    
    root = Tk()

    root.title("CDOM routine")
    root.geometry("500x550")

    font_titulo = ("Arial", "18")
    
    font = ("Arial", "11")
    
    first_container = Frame(root, padx=10, pady=12)
    first_container.pack()

    second_container = Frame(root, padx=12, pady=12)
    second_container.pack()

    third_container = Frame(root, padx=12, pady=12)
    third_container.pack()

    fourth_container = Frame(root, padx=12, pady=12)
    fourth_container.pack()

    fifth_container = Frame(root, padx=12, pady=12)
    fifth_container.pack()

    sixth_container = Frame(root, padx=12, pady=12)
    sixth_container.pack()

    seventh_container = Frame(root, padx=12, pady=12)
    seventh_container.pack()

    eighth_container = Frame(root, padx=12, pady=12)
    eighth_container.pack()
    
    column_names = Label(first_container, text="Rotina para Análise de CDOM", font=font_titulo, padx=20)
    column_names.pack()
    
    column_names = Label(second_container, text="Número de grupos de amostra:", font=font, padx=20)
    column_names.pack()

    numero_grupos_amostras = Entry(second_container, font=font, width=7, justify=CENTER)
    numero_grupos_amostras.insert(10, 6)
    numero_grupos_amostras.pack()
    
    column_names = Label(third_container, text="Caminho do output do arquivo CDOM:", font=font, padx=20)
    column_names.pack()

    path_cdom = Button(third_container, text="Selecione o Arquivo", font=font, command=lambda: path_output_excel("cdom"))
    path_cdom.pack()
    
    column_names = Label(fourth_container, text="Caminho do output do arquivo dos dados finais:", font=font, padx=20)
    column_names.pack()

    path_dados_finais = Button(fourth_container, text="Selecione o local", font=font, command=lambda: path_output_excel("dados"))
    path_dados_finais.pack()

    column_names = Label(fifth_container, text="Título do gráfico:", font=font, padx=20)
    column_names.pack()

    titulo_grafico = Entry(fifth_container, font=font, width=70, justify=CENTER)
    titulo_grafico.insert(10, "Coeficiente de Absorvência do CDOM - Promissao (Ago/22)")
    titulo_grafico.pack()

    column_names = Label(sixth_container, text="Caminho do output do gráfico", font=font, padx=20)
    column_names.pack()

    path_grafico = Button(sixth_container, text="Selecione o Arquivo", font=font, command=path_output_jpg)
    path_grafico.pack()

    column_names = Label(seventh_container, text="Selecione o Arquivo para ánalise", font=font, padx=20)
    column_names.pack()

    path_arquivo = Button(seventh_container, text="Selecione o arquivo", font=font, command=upload_file)
    path_arquivo.pack()

    filename_text = Label(seventh_container, text='', font=font)
    filename_text.pack()

    global path_arquivo_output_cdom
    global path_arquivo_output_dados
    global selected_file_path
    global path_arquivo_caminho
    save_button = Button(eighth_container, text="Iniciar rotina", font=font, command=lambda: dados(num_grps_amos=numero_grupos_amostras.get(), path_cdom=path_arquivo_output_cdom, path_dados_finais=path_arquivo_output_dados, titulo_grafico=titulo_grafico.get(), path_grafico=selected_file_path, path_arquivo=path_arquivo_caminho))
    save_button.pack()

    root.mainloop()

start()