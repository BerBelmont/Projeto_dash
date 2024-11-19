import pandas as pd
from collections import Counter

class DataAnalyzer:
    def __init__(self, series_list):
        self.series_list = series_list
        # Cria um DataFrame a partir da lista de séries
        self.df = self.create_dataframe()

    def create_dataframe(self):
        data = []
        # Itera sobre cada objeto Serie e extrai seus atributos para um dicionário
        for serie in self.series_list:
            data.append({
                'id': serie.id,
                'titulo': serie.titulo,
                'avaliacao': serie.avaliacao,
                'generos': serie.generos,
                'num_temporadas': serie.num_temporadas,
                'num_episodios': serie.num_episodios,
                'data_lancamento': serie.data_lancamento,
                'pais_origem': serie.pais_origem
            })
        # Cria um DataFrame a partir da lista de dicionários
        df = pd.DataFrame(data)
        # Garante que a coluna 'generos' é uma lista
        df['generos'] = df['generos'].apply(lambda x: x if isinstance(x, list) else [])
        # Garante que a coluna 'pais_origem' é uma lista
        df['pais_origem'] = df['pais_origem'].apply(lambda x: x if isinstance(x, list) else [])
        # Converte a coluna 'avaliacao' para tipo numérico
        df['avaliacao'] = pd.to_numeric(df['avaliacao'])
        # Converte 'num_temporadas' para numérico
        df['num_temporadas'] = pd.to_numeric(df['num_temporadas'])
        # Converte 'num_episodios' para numérico
        df['num_episodios'] = pd.to_numeric(df['num_episodios'])
        # Converte 'data_lancamento' para datetime
        df['data_lancamento'] = pd.to_datetime(df['data_lancamento'])
        return df

    def average_rating(self):
        # Calcula a média das avaliações das séries
        avg_rating = self.df['avaliacao'].mean()
        print(f"A média das avaliações é {avg_rating:.2f}")
        return avg_rating

    def most_common_genres(self, top_n=5):
        # Cria uma lista com todos os gêneros das séries
        all_genres = [genre for sublist in self.df['generos'] for genre in sublist]
        # Conta a frequência de cada gênero
        genre_counts = Counter(all_genres)
        # Obtém os 'top_n' gêneros mais comuns
        most_common = genre_counts.most_common(top_n)
        print("Gêneros mais comuns:")
        for genre, count in most_common:
            print(f"{genre}: {count} séries")
        return most_common

    def ratings_over_time(self):
        # Extrai o ano de lançamento das séries
        self.df['ano_lancamento'] = self.df['data_lancamento'].dt.year
        # Agrupa por ano e calcula a média das avaliações
        ratings_by_year = self.df.groupby('ano_lancamento')['avaliacao'].mean()
        return ratings_by_year

    def series_by_country(self):
        # Cria uma lista com todos os países de origem das séries
        all_countries = [country for sublist in self.df['pais_origem'] for country in sublist]
        # Conta a frequência de cada país
        country_counts = Counter(all_countries)
        return country_counts

    def correlation_between_seasons_and_rating(self):
        # Calcula a correlação entre o número de temporadas e a avaliação
        correlation = self.df['num_temporadas'].corr(self.df['avaliacao'])
        print(f"Correlação entre número de temporadas e avaliação: {correlation:.2f}")
        return correlation
