# Descrição do Projeto
Este projeto é um dashboard interativo desenvolvido em Python utilizando a biblioteca Streamlit. O dashboard analisa dados das top séries de TV obtidas da API do TMDB (The Movie Database), apresentando visualizações interativas sobre avaliações, gêneros, países de origem e outros insights relevantes. Além disso, há um destaque especial para a série "Breaking Bad", explorando seus detalhes e destacando por que ela se sobressai no contexto das séries analisadas.


##### Pré-requisitos
Python 3.7 ou superior instalado em sua máquina.
Chave de API do TMDB para acessar os dados das séries. Você pode obter uma chave gratuita cadastrando-se no site do TMDB.


##### Instruções de Instalação e Execução
1. Clonar o Repositório
Clone este repositório em sua máquina local:

```
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Substitua seu-usuario e seu-repositorio pelo nome de usuário e nome do repositório correspondentes.

2. Navegar até o Diretório do Projeto
Entre no diretório do projeto:

```
cd seu-repositorio
```

3. Remover o Ambiente Virtual Existente
Caso exista uma pasta env no diretório do projeto, é recomendado excluí-la para evitar conflitos com ambientes virtuais anteriores:

No Windows:

```
rmdir /S /Q env
```

No Linux ou macOS:

```
rm -rf env
```

4. Criar um Novo Ambiente Virtual
Crie um novo ambiente virtual chamado env:


```
python -m venv env
```
5. Ativar o Ambiente Virtual
Ative o ambiente virtual recém-criado:

No Windows:

```
env\Scripts\activate
```
No Linux ou macOS:

```
source env/bin/activate
```

6. Instalar as Dependências
Com o ambiente virtual ativado, instale as dependências necessárias:

```
pip install -r libs.txt
```
###### Nota: Se o arquivo requirements.txt não estiver disponível, instale manualmente as seguintes bibliotecas:

```
pip install numpy scipy pandas matplotlib seaborn streamlit requests plotly
```
7. Configurar a Chave de API do TMDB
Para que o projeto acesse os dados do TMDB, é necessário configurar sua chave de API.

Para isso acesse o site do TMDB, crie uma conta e em configurações selecione API e faça um request para uma KEY.

Com a chave criada substitua os espaços nos códigos do src e do dashboard em que está escrito 'sua-api-key' pela sua chave de API real.


8. Executar o Script para Coletar os Dados
Antes de iniciar o dashboard, é necessário coletar os dados das séries executando o script main.py:

```
python main.py
```
Este script irá:

Utilizar a API do TMDB para obter dados das top séries de TV.
Salvar os dados em um arquivo CSV chamado series_data.csv dentro da pasta src.

9. Executar o Dashboard
Inicie o dashboard utilizando o Streamlit:

```
streamlit run dashboard/dashboard.py
```
Se o arquivo dashboard.py estiver em outro diretório, ajuste o caminho conforme necessário.

O Streamlit abrirá automaticamente o dashboard em seu navegador padrão. Caso não abra, acesse http://localhost:8501 em seu navegador.

10. Explorar o Dashboard
Utilize os filtros na barra lateral para interagir com os dados:

Filtrar por Gênero: Selecione um ou mais gêneros para visualizar séries correspondentes.

Intervalo de Anos de Lançamento: Defina o período dos anos de lançamento das séries.

Faixa de Avaliação: Ajuste a faixa de avaliação das séries que deseja analisar.

Explore as diferentes abas disponíveis:

Avaliações: Visualize a distribuição das avaliações das séries.

Gêneros: Descubra os gêneros mais populares entre as séries selecionadas.

Temporadas x Avaliação: Analise a relação entre o número de temporadas e a avaliação das séries.

Avaliação por Ano: Observe como a avaliação média das séries evoluiu ao longo dos anos.

Séries por País: Veja quais países mais produzem séries entre as selecionadas.

Destaque: Breaking Bad: Explore em detalhes a série "Breaking Bad" e entenda por que ela se destaca.

# Observações Importantes

Segurança da Chave de API: Não compartilhe sua chave de API publicamente ou em repositórios públicos. Utilize variáveis de ambiente ou arquivos de configuração não versionados para manter sua chave segura.

Atualização dos Dados: Para obter dados atualizados das séries, execute novamente o script main.py.

Dependências Adicionais: Caso encontre erros relacionados a dependências, instale as bibliotecas necessárias utilizando pip install.

Compatibilidade: Certifique-se de que está utilizando a versão correta do Python e das bibliotecas para evitar incompatibilidades.

