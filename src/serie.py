class Serie:
    def __init__(self, id, titulo, avaliacao, generos, num_temporadas, num_episodios, data_lancamento, pais_origem):
        # Inicializa um objeto Serie com os atributos fornecidos
        self.id = id
        self.titulo = titulo
        self.avaliacao = avaliacao
        self.generos = generos  # Lista de gêneros
        self.num_temporadas = num_temporadas
        self.num_episodios = num_episodios
        self.data_lancamento = data_lancamento
        self.pais_origem = pais_origem  # Lista de países de origem

    def exibir_informacoes(self):
        # Método para exibir as informações da série no console
        print(f"Título: {self.titulo}")
        print(f"Avaliação: {self.avaliacao}")
        print(f"Gêneros: {', '.join(self.generos)}")
        print(f"Número de Temporadas: {self.num_temporadas}")
        print(f"Número de Episódios: {self.num_episodios}")
        print(f"Data de Lançamento: {self.data_lancamento}")
        print(f"País(es) de Origem: {', '.join(self.pais_origem)}")
