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
Ao clonar o código e abrir em um editor de código (foi utilizado o VS Code), os seguintes arquivos estarão disponíveis: *driver_ag.py*, *least_squares.py*, *roda_CDOM_correto.py* e a rotina de interpolação *interpolacao_cdom.py*.

Com o Anaconda Prompt e na **raiz do projeto**, instale as bibliotecas necessários no arquivo de ambiente:

```console
cd path/rotina-cdom-python
```

Observações:
* Confira o nome e o caminho do arquivo de ambiente e, caso necessário, modifique na linha de comando abaixo.
* Caso seja necessário, também é possível modificar o nome do ambiente (neste caso está com o nome "cdom").

```console
conda env create --name cdom --file environment.yaml
```

Após isso, ative o ambiente:

```console
conda activate cdom
```

Rode o código em Python:

```console
python main.py
```

Caso queira testar o código, há um diretório chamado input-exemplo com um arquivo de entrada. 
Além disso, há um exemplo de saída da entrada de exemplo na pasta output-exemplo.

## Interface

Depois de executar o código main.py, uma interface gráfica irá aparecer para que o usuário entre com algumas informações.
Essas informações serão dadas de acordo com a organização da tabela dos dados de entrada.

## Preparando a tabela com as medidas

Antes de iniciar o processamento, é preciso que a tabela com os dados de saída do espectrofotômetro tenha 1 nm de resolução espectral, caso não esteja, é necessário interpolar. Esse ajuste pode ser feito ao executar o código em Python (script com o nome interpolacao_cdom.py) com a tabela original em formato ".xls" e a tabela interpolada será salva no formato ".csv".

Com a tabela já interpolada, ela deve ser organizada com as colunas na sequência: wavelength, branco, amostras, branco. Não é necessária a inclusão de uma coluna de leitura do ar. O branco se refere à leitura "água vs água" feita no espectrofotômetro.

É importante que a tabela seja dividida em grupos de amostras de mesmo tamanho entre os “brancos”. Por exemplo, se foram coletadas 15 amostras, poderão ser feitos 3 grupos de 5 amostras entre brancos ou 5 grupos de 3 amostras. É importante ter atenção à essa formatação, pois ela vai definir uma modificação essencial no código.

A amostra de branco deve ser escolhida pelo usuário, levando em consideração o dado mais estável. Se assim optar, também poderá utilizar uma média dos brancos entre os grupos de leituras que foram feitas no espectrofotômetro . Recomenda-se que se use o primeiro branco como “branco1”; o segundo branco pode ser uma média entre os grupos 2 e 3 ou somente 3; e o último branco uma média do grupo 4.

Um exemplo da tabela pode ser visto na figura abaixo em (a) - como a tabela sai do espectrofotômetro - e (b) - como ela deve ser organizada:

<img src="/docs/exemploa_tabela.jpg" alt="Exemplo da tabela antes (a).">
<img src="/docs/exemplob_tabela.jpg" alt="Exemplo da tabela depois de organizada (b).">

Mais detalhes sobre a organização das tabelas, podem ser encontrados no tutorial disponível na pasta [docs](/docs/Tutorial_CDOM.pdf).

**Número de grupo de amostras**: onde você deve colocar o número de amostras;

**Número de amostras de água**: Essa coluna se refere ao 'branco'. 
Coloque o número das colunas das amostras de água. Ex: coluna B: 0, coluna I: 7, coluna P: 14. Entrada: 0, 7, 14;  
*Atenção!!*: a coluna zero é a segunda coluna do arquivo de leitura, pois o código segue a lógica de que a coluna A(-1) é a "Wave".

**Caminho do output do arquivo CDOM**: selecione/crie o caminho e dê o nome do arquivo que será salvo com os dados do CDOM;

**Caminho do output do arquivo dos dados finais**: selecione/crie o caminho e dê o nome do arquivo que será salvo com os dados finais da rotina;

**Título do gráfico**: Digite o título do gráfico;

**Caminho do output do gráfico**: selecione/crie o caminho e dê o nome do arquivo para o gráfico gerado pela rotina;

**Selecione o Arquivo para ánalise**: selecione o arquivo com os dados a serem analisados;

**Iniciar rotina**: clique para começar a análise.

#

**Importante**: em caso de erro, confira o dado de entrada selecionado para análise. Possíveis erros podem estar atrelados a separadores decimais e tabuladores.

## Iniciando o processamento em Python

Para iniciar o processamento, execute o código "main.py". A seguinte janela interativa será apresentada:

<img src="/docs/primeira_tela_interativa.jpg" alt="Janela interativa para entrada de informações.">

**Atenção:** O dado de entrada deve ser selecionado corretamente, caso contrário, uma mensagem de "Arquivo não encontrado" será exibida no console. Também deve ser criada uma pasta "outputs", onde, por padrão, ficarão salvos os dados de saída do processamento (que podem ser alterados no arquivo "input.txt").

No mesmo txt, o usuário poderá alterar o título do gráfico, a pasta de saída do gráfico (com o nome do arquivo), dos dados do acdom e dados finais diretamente nas variáveis titulo_grafico, path_grafico, path_cdom e path_dados_finais respectivamente.

> *Fonte: Texto de Raianny Leite (autora do tutorial do código em Matlab) modificado por Gustavo Ando e Kauã Renó (Conversão para Python) e atualizado por Raianny Leite e Claudia Secco em 28/08/2024*