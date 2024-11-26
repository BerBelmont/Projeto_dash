from serie import Serie
from tmdb_client import TMDBClient
from data_analyzer import DataAnalyzer

def main():
    # Chave de API do TMDB
    API_KEY = 'sua-api-key'

    # Instanciar o cliente da API
    tmdb_client = TMDBClient(API_KEY)

    # Lista para armazenar objetos Serie
    series_list = []

    # IDs do Breaking Bad
    series_ids = [1396]  # ID do TMDB para "Breaking Bad"

    # Obter detalhes do Breaking Bad
    for serie_id in series_ids:
        detalhes = tmdb_client.get_serie_details(serie_id)

        serie = Serie(
            id=detalhes['id'],
            titulo=detalhes['name'],
            avaliacao=detalhes['vote_average'],
            generos=[genre['name'] for genre in detalhes['genres']],
            num_temporadas=detalhes['number_of_seasons'],
            num_episodios=detalhes['number_of_episodes'],
            data_lancamento=detalhes['first_air_date'],
            pais_origem=detalhes['origin_country']
        )

        # Adicionar à lista
        series_list.append(serie)

    # Obter as top séries
    for page in range(1, 6):  # Obter as 5 primeiras páginas
        top_series_data = tmdb_client.get_top_series(page=page)
        if not top_series_data:
            break

        # Processar cada série
        for serie_data in top_series_data:
            serie_id = serie_data['id']
            detalhes = tmdb_client.get_serie_details(serie_id)

            # Evitar duplicatas
            if any(s.id == serie_id for s in series_list):
                continue

            serie = Serie(
                id=detalhes['id'],
                titulo=detalhes['name'],
                avaliacao=detalhes['vote_average'],
                generos=[genre['name'] for genre in detalhes['genres']],
                num_temporadas=detalhes['number_of_seasons'],
                num_episodios=detalhes['number_of_episodes'],
                data_lancamento=detalhes['first_air_date'],
                pais_origem=detalhes['origin_country']
            )

            # Adicionar à lista
            series_list.append(serie)

    # Análise de dados
    analyzer = DataAnalyzer(series_list)
    # Salvar DataFrame em um arquivo CSV
    analyzer.df.to_csv('series_data.csv', index=False)

if __name__ == '__main__':
    main()
