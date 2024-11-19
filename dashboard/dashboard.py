import os
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import requests

# Configurações da página do Streamlit
st.set_page_config(
    page_title='Dashboard Interativo das Top Séries de TV',
    page_icon='📺',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Chave de API do TMDB 
API_KEY = 'cd54cd3d7a97a19dac6fc20dd8041a81'

# Determinar o diretório base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir o caminho para o arquivo CSV na pasta 'src'
csv_path = os.path.join(BASE_DIR, '..', 'src', 'series_data.csv')

@st.cache  # Decorador para cachear a função e evitar recarregamentos desnecessários
def load_data():
    # Carrega os dados do arquivo CSV
    df = pd.read_csv(csv_path)
    # Converte as colunas de strings para listas usando 'eval'
    df['generos'] = df['generos'].apply(lambda x: eval(x))
    df['pais_origem'] = df['pais_origem'].apply(lambda x: eval(x))
    # Converte a coluna 'data_lancamento' para datetime, lidando com erros
    df['data_lancamento'] = pd.to_datetime(df['data_lancamento'], errors='coerce')
    # Remove linhas com 'data_lancamento' nulo
    df = df.dropna(subset=['data_lancamento'])
    # Extrai o ano de lançamento
    df['ano_lancamento'] = df['data_lancamento'].dt.year
    return df

# Carrega os dados e armazena em 'df'
df = load_data()

# Título do dashboard
st.title('Dashboard Interativo das Top Séries de TV')

# Sidebar para filtros
st.sidebar.title('Opções de Filtro')

# Filtro por Gênero
# Obtém uma lista única de todos os gêneros disponíveis
generos_disponiveis = sorted(set([genre for sublist in df['generos'] for genre in sublist]))
# Cria um multiselect na sidebar para os gêneros
genero_selecionado = st.sidebar.multiselect('Filtrar por Gênero:', generos_disponiveis)

# Filtro por Ano de Lançamento
# Obtém uma lista única de anos disponíveis
anos_disponiveis = sorted(df['ano_lancamento'].dropna().unique())
# Cria um slider de seleção de intervalo de anos
ano_min, ano_max = st.sidebar.select_slider(
    'Selecione o intervalo de anos:',
    options=anos_disponiveis,
    value=(min(anos_disponiveis), max(anos_disponiveis))
)

# Filtro por Avaliação
# Cria um slider para selecionar a faixa de avaliação
avaliacao_min, avaliacao_max = st.sidebar.slider(
    'Selecione a faixa de avaliação:',
    float(df['avaliacao'].min()),
    float(df['avaliacao'].max()),
    (float(df['avaliacao'].min()), float(df['avaliacao'].max()))
)

# Aplicar filtros
df_filtrado = df.copy()

# Filtra por gênero, se selecionado
if genero_selecionado:
    df_filtrado = df_filtrado[df_filtrado['generos'].apply(lambda x: any(genero in x for genero in genero_selecionado))]

# Filtra pelo intervalo de anos
df_filtrado = df_filtrado[(df_filtrado['ano_lancamento'] >= ano_min) & (df_filtrado['ano_lancamento'] <= ano_max)]

# Filtra pela faixa de avaliação
df_filtrado = df_filtrado[(df_filtrado['avaliacao'] >= avaliacao_min) & (df_filtrado['avaliacao'] <= avaliacao_max)]

# Função para obter o poster da série usando a API do TMDB
def get_poster_url(api_key, serie_id):
    base_url = 'https://api.themoviedb.org/3/tv/{}'
    poster_base_url = 'https://image.tmdb.org/t/p/w500'
    url = base_url.format(serie_id)
    params = {
        'api_key': api_key,
        'language': 'pt-BR'
    }
    response = requests.get(url, params=params)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return poster_base_url + poster_path
    else:
        return None

# Cria abas para organizar os gráficos e análises
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    'Avaliações', 
    'Gêneros', 
    'Temporadas x Avaliação', 
    'Avaliação por Ano', 
    'Séries por País', 
    'Destaque: Breaking Bad'
])

with tab1:
    st.header('Distribuição das Avaliações das Séries')
    st.write('Este gráfico mostra como as avaliações estão distribuídas entre as séries selecionadas.')
    # Cria um histograma das avaliações usando Plotly
    fig = px.histogram(
        df_filtrado,
        x='avaliacao',
        nbins=20,
        labels={'avaliacao': 'Avaliação'},
        title='Distribuição das Avaliações'
    )
    # Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header('Gêneros Mais Populares')
    st.write('Este gráfico apresenta os gêneros mais frequentes entre as séries selecionadas.')
    # Lista todos os gêneros presentes nas séries filtradas
    all_genres = [genre for sublist in df_filtrado['generos'] for genre in sublist]
    # Conta a frequência de cada gênero
    genre_counts = Counter(all_genres)
    # Cria um DataFrame com os gêneros e suas contagens
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Gênero', 'Contagem'])
    # Ordena os gêneros por contagem decrescente e seleciona os top 10
    genre_df = genre_df.sort_values('Contagem', ascending=False).head(10)
    # Cria um gráfico de barras horizontal usando Plotly
    fig = px.bar(
        genre_df,
        x='Contagem',
        y='Gênero',
        orientation='h',
        labels={'Contagem': 'Número de Séries', 'Gênero': 'Gênero'},
        title='Top 10 Gêneros Mais Populares'
    )
    # Ajusta a ordem das categorias no eixo y
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    # Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header('Relação entre Número de Temporadas e Avaliação')
    st.write('Este gráfico explora a possível correlação entre o número de temporadas de uma série e sua avaliação média.')
    # Cria um gráfico de dispersão usando Plotly
    fig = px.scatter(
        df_filtrado,
        x='num_temporadas',
        y='avaliacao',
        hover_data=['titulo'],  # Mostra o título da série ao passar o mouse
        labels={
            'num_temporadas': 'Número de Temporadas',
            'avaliacao': 'Avaliação',
            'titulo': 'Título da Série'
        },
        title='Número de Temporadas vs. Avaliação'
    )
    # Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header('Avaliação Média por Ano de Lançamento')
    st.write('Este gráfico mostra como a avaliação média das séries evoluiu ao longo dos anos.')
    # Agrupa as séries por ano de lançamento e calcula a média das avaliações
    ano_avaliacao = df_filtrado.groupby('ano_lancamento')['avaliacao'].mean().reset_index()
    # Cria um gráfico de linha usando Plotly
    fig = px.line(
        ano_avaliacao,
        x='ano_lancamento',
        y='avaliacao',
        markers=True,
        labels={'ano_lancamento': 'Ano de Lançamento', 'avaliacao': 'Avaliação Média'},
        title='Avaliação Média por Ano'
    )
    # Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header('Número de Séries por País de Origem')
    st.write('Este gráfico destaca os países que mais produzem séries entre as selecionadas.')
    # Lista todos os países de origem das séries filtradas
    all_countries = [country for sublist in df_filtrado['pais_origem'] for country in sublist]
    # Conta a frequência de cada país
    country_counts = Counter(all_countries)
    # Cria um DataFrame com os países e suas contagens
    country_df = pd.DataFrame(country_counts.items(), columns=['País', 'Número de Séries'])
    # Ordena os países por contagem decrescente e seleciona os top 10
    country_df = country_df.sort_values('Número de Séries', ascending=False).head(10)
    # Cria um gráfico de barras horizontal usando Plotly
    fig = px.bar(
        country_df,
        x='Número de Séries',
        y='País',
        orientation='h',
        labels={'Número de Séries': 'Número de Séries', 'País': 'País'},
        title='Top 10 Países com Mais Séries'
    )
    # Ajusta a ordem das categorias no eixo y
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    # Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.header('Destaque: Breaking Bad')
    st.write('Analisando os dados, percebemos que o gênero **Crime** não está entre os mais frequentes nas séries com altas avaliações. No entanto, **Breaking Bad** é a série com a maior avaliação, mesmo sendo do gênero Crime. Vamos explorar esta série em detalhes.')
    
    # Encontrar Breaking Bad no DataFrame usando o ID 
    breaking_bad = df[df['id'] == 1396]

    if not breaking_bad.empty:
        # Obtém a primeira linha 
        serie = breaking_bad.iloc[0]
        st.subheader(serie['titulo'])
        
        # Obter o poster da série usando a função get_poster_url
        poster_url = get_poster_url(API_KEY, serie['id'])
        if poster_url:
            # Exibe a imagem do poster
            st.image(poster_url, width=300)
        
        # Mostrar detalhes da série
        st.write(f"**Avaliação:** {serie['avaliacao']}")
        st.write(f"**Gêneros:** {', '.join(serie['generos'])}")
        st.write(f"**Número de Temporadas:** {int(serie['num_temporadas'])}")
        st.write(f"**Número de Episódios:** {int(serie['num_episodios'])}")
        st.write(f"**Data de Lançamento:** {serie['data_lancamento'].strftime('%d/%m/%Y')}")
        st.write(f"**País(es) de Origem:** {', '.join(serie['pais_origem'])}")
        
        st.write('**Sinopse:**')
        # Função para obter a sinopse da série usando a API do TMDB
        def get_overview(api_key, serie_id):
            base_url = 'https://api.themoviedb.org/3/tv/{}'
            url = base_url.format(serie_id)
            params = {
                'api_key': api_key,
                'language': 'pt-BR'
            }
            response = requests.get(url, params=params)
            data = response.json()
            overview = data.get('overview')
            return overview
        
        # Obtém a sinopse da série
        overview = get_overview(API_KEY, serie['id'])
        if overview:
            st.write(overview)
        
        st.write('**Por que Breaking Bad se destaca?**')
        st.write('Mesmo pertencendo ao gênero Crime, que não é o mais frequente entre as séries com altas avaliações, Breaking Bad se destaca por sua narrativa envolvente, desenvolvimento profundo dos personagens e produção de alta qualidade. Isso mostra que, embora alguns gêneros possam ser menos representados, séries excepcionais dentro desses gêneros podem alcançar grande sucesso e reconhecimento.')
    else:
        # Mensagem caso Breaking Bad não seja encontrada nos dados
        st.write('Breaking Bad não foi encontrada nos dados.')

