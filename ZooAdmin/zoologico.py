import sqlite3
from database.consultas import Animal_consult, Especie_consult


class Zoologico:

    def __init__(self):
        self.animais = Animal_consult()
        self.especies = Especie_consult()

    # Consultas e operações de animais
    def listar_animais(self):
        return self.animais.listar()

    def buscar_animal(self, id_animal):
        return self.animais.buscar_por_id(id_animal)

    def listar_habitats(self):
        return self.animais.listar_habitats()

    def adicionar_animal(self, animal, id_habitat):
        return self.animais.inserir(animal, id_habitat)

    def atualizar_animal(self, animal, id_habitat):
        return self.animais.atualizar(animal, id_habitat)

    def remover_animal(self, id_animal):
        return self.animais.excluir(id_animal)

    # Consultas e operações de espécies
    def listar_especies(self):
        return self.especies.listar()

    def buscar_especie(self, id_especie):
        return self.especies.buscar_por_id(id_especie)

    def listar_grupos(self):
        return self.especies.listar_grupos()

    def adicionar_especie(self, especie):
        return self.especies.inserir(especie)

    def atualizar_especie(self, especie):
        return self.especies.atualizar(especie)

    def remover_especie(self, id_especie):
        try:
            return self.especies.excluir(id_especie)
        except sqlite3.IntegrityError:
            raise ValueError(
                "Esta espécie possui animais cadastrados. "
                "Transfira ou remova esses animais antes de excluir a espécie."
            )
