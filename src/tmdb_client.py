import requests 

class TMDBClient:
    def __init__(self, api_key):
        # Inicializa o cliente TMDB com a chave de API f
        self.api_key = 'cd54cd3d7a97a19dac6fc20dd8041a81' 
        self.base_url = 'https://api.themoviedb.org/3'     

    def get_top_series(self, page=1):
        # Obtém as séries de TV com as melhores avaliações da API do TMDB
        url = f"{self.base_url}/tv/top_rated"  # Endpoint para séries mais bem avaliadas
        params = {
            'api_key': self.api_key,   # Chave de API necessária para autenticação
            'language': 'pt-BR',       # Define o idioma da resposta como pt-BR
            'page': page               # Número da página dos resultados
        }
        response = requests.get(url, params=params)  # Faz a requisição GET com os parâmetros
        if response.status_code == 200:
            # Se a requisição for bem-sucedida, retorna a lista de resultados
            return response.json()['results']
        else:
            # Se houver um erro, exibe uma mensagem e retorna uma lista vazia
            print("Erro ao obter top séries")
            return []

    def get_serie_details(self, serie_id):
        # Obtém os detalhes de uma série específica usando seu ID
        url = f"{self.base_url}/tv/{serie_id}"  # Endpoint para detalhes da série
        params = {
            'api_key': self.api_key,   # Chave de API necessária para autenticação
            'language': 'pt-BR'       
        }
        response = requests.get(url, params=params)  # Faz a requisição GET com os parâmetros
        if response.status_code == 200:
            # Se a requisição for bem-sucedida, retorna os dados em formato JSON
            return response.json()
        else:
            # Se houver um erro, exibe uma mensagem e retorna um dicionário vazio
            print(f"Erro ao obter detalhes da série {serie_id}")
            return {}
