# SUPERCLASSE Animal
# A classe Animal se relaciona por meio de Associação com a tabela Espécie. Uma relação unidirecional

class Animal:
    """Classe-base que representa um animal individual do zoológico."""

    grupo = "Não definido"

    def __init__(
        self, nome, idade, sexo, peso, data_chegada,
        especie, habitat, id_animal=None
    ):
        self.id_animal = id_animal
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.peso = peso
        self.data_chegada = data_chegada
        self.especie = especie
        self.habitat = habitat

    # método genérico que é necessário para o polimorfismo
    def realizar_acao(self):
        return f"{self.nome} não possui um comportamento específico definido."
    
    def apresentar_informacoes(self):
        return (
            f"ID: {self.id_animal}\n"
            f"Nome: {self.nome}\n"
            f"Espécie: {self.especie.nome_popular} "
            f"({self.especie.nome_cientifico})\n"
            f"Grupo: {self.especie.grupo}\n"
            f"Idade: {self.idade} anos\n"
            f"Sexo: {self.sexo}\n"
            f"Peso: {self.peso:.2f} kg\n"
            f"Data de chegada: {self.data_chegada}\n"
            f"Habitat: {self.habitat}\n"
            f"Expectativa de vida: {self.especie.expectativa_vida_min}-"
            f"{self.especie.expectativa_vida_max} anos\n"
            f"Alimentação: {self.especie.alimentacao}\n"
            f"Descrição da espécie: {self.especie.descricao}\n"
            f"Comportamento característico: {self.realizar_acao()}"
        )

    def __str__(self):
        return (
            f"[{self.id_animal}] {self.nome} — "
            f"{self.especie.nome_popular} ({self.especie.grupo})"
        )
