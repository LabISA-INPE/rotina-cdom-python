# Rotina CDOM em Python

Rotina em Python convertida da rotina em MatLab para análise de CDOM

## Execução

Para executar o código é necessário instalar as seguintes tecnologias:

* [Python](https://www.python.org/downloads/)
* [Anaconda](https://www.anaconda.com/download)

Clone o repositório com o comando:

```console
git clone https://github.com/LabISA-INPE/rotina-cdom-python.git
```

Com o Anaconda Prompt e na raiz do projeto, instale as bibliotecas necessários no arquivo de ambiente:

Observações:
* Confire o nome e o caminho do arquivo de ambiente e, caso necessário, modifique na linha de comando abaixo.
* Caso seja necessário, também é possível modificar o nome do ambiente (neste caso está com o nome cdom).

```console
conda env create --name cdom --file cdom.yaml
```

Após isso, ative o ambiente:

```console
conda activate cdom
```

Por fim, rode o código em Python:

```console
python roda_CDOM_correto.py
```

Caso queira testar o código, há um diretório chamado input-example com um arquivo de entrada, que devem ser abertos ao rodar o código. Além disso, temos um exemplo de saída da entrada de exemplo na pasta output-example.
