from database.conexao import conectar
from models.especie import Especie
from models.animal import Animal
from models.mamiferos import Mamifero
from models.aves import Ave
from models.repteis import Reptil
from models.anfibios import Anfibio
from models.peixes import Peixe


class Especie_consult:
    """Responsável exclusivamente pelas operações SQL relacionadas a espécies."""

    @staticmethod
    def _linha_para_especie(linha):
        return Especie(
            id_especie=linha["id_especie"],
            nome_popular=linha["nome_popular"],
            nome_cientifico=linha["nome_cientifico"],
            descricao=linha["descricao"],
            expectativa_vida_min=linha["expectativa_vida_min"],
            expectativa_vida_max=linha["expectativa_vida_max"],
            alimentacao=linha["alimentacao"],
            grupo=linha["grupo"]
        )

    def listar(self):
        with conectar() as conexao:
            linhas = conexao.execute("""
                SELECT e.*, g.nome AS grupo
                FROM especies e
                JOIN grupos g ON g.id_grupo = e.id_grupo
                ORDER BY e.nome_popular
            """).fetchall()
            return [self._linha_para_especie(linha) for linha in linhas]

    def buscar_por_id(self, id_especie):
        with conectar() as conexao:
            linha = conexao.execute("""
                SELECT e.*, g.nome AS grupo
                FROM especies e
                JOIN grupos g ON g.id_grupo = e.id_grupo
                WHERE e.id_especie = ?
            """, (id_especie,)).fetchone()
            return self._linha_para_especie(linha) if linha else None

    def listar_grupos(self):
        with conectar() as conexao:
            return conexao.execute(
                "SELECT id_grupo, nome FROM grupos ORDER BY nome"
            ).fetchall()

    def inserir(self, especie):
        with conectar() as conexao:
            grupo = conexao.execute(
                "SELECT id_grupo FROM grupos WHERE nome = ?",
                (especie.grupo,)
            ).fetchone()
            if not grupo:
                raise ValueError("Grupo zoológico inválido.")

            cursor = conexao.execute("""
                INSERT INTO especies (
                    nome_popular, nome_cientifico, descricao,
                    expectativa_vida_min, expectativa_vida_max,
                    alimentacao, id_grupo
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                especie.nome_popular, especie.nome_cientifico,
                especie.descricao, especie.expectativa_vida_min,
                especie.expectativa_vida_max, especie.alimentacao,
                grupo["id_grupo"]
            ))
            return cursor.lastrowid

    def atualizar(self, especie):
        with conectar() as conexao:
            grupo = conexao.execute(
                "SELECT id_grupo FROM grupos WHERE nome = ?",
                (especie.grupo,)
            ).fetchone()
            if not grupo:
                raise ValueError("Grupo zoológico inválido.")

            cursor = conexao.execute("""
                UPDATE especies
                SET nome_popular = ?, nome_cientifico = ?, descricao = ?,
                    expectativa_vida_min = ?, expectativa_vida_max = ?,
                    alimentacao = ?, id_grupo = ?
                WHERE id_especie = ?
            """, (
                especie.nome_popular, especie.nome_cientifico,
                especie.descricao, especie.expectativa_vida_min,
                especie.expectativa_vida_max, especie.alimentacao,
                grupo["id_grupo"], especie.id_especie
            ))
            return cursor.rowcount > 0

    def excluir(self, id_especie):
        with conectar() as conexao:
            cursor = conexao.execute(
                "DELETE FROM especies WHERE id_especie = ?",
                (id_especie,)
            )
            return cursor.rowcount > 0

class Animal_consult:
    """Responsável exclusivamente pelas operações SQL relacionadas a animais."""

    CLASSES_POR_GRUPO = {
        "Mamífero": Mamifero,
        "Ave": Ave,
        "Réptil": Reptil,
        "Anfíbio": Anfibio,
        "Peixe": Peixe
    }

    @staticmethod
    def _consulta_base():
        return """
            SELECT a.*, h.nome AS habitat,
                   e.id_especie, e.nome_popular, e.nome_cientifico,
                   e.descricao AS descricao_especie,
                   e.expectativa_vida_min, e.expectativa_vida_max,
                   e.alimentacao, g.nome AS grupo
            FROM animais a
            JOIN especies e ON e.id_especie = a.id_especie
            JOIN grupos g ON g.id_grupo = e.id_grupo
            JOIN habitats h ON h.id_habitat = a.id_habitat
        """

    def _linha_para_animal(self, linha):
        especie = Especie(
            id_especie=linha["id_especie"],
            nome_popular=linha["nome_popular"],
            nome_cientifico=linha["nome_cientifico"],
            descricao=linha["descricao_especie"],
            expectativa_vida_min=linha["expectativa_vida_min"],
            expectativa_vida_max=linha["expectativa_vida_max"],
            alimentacao=linha["alimentacao"],
            grupo=linha["grupo"]
        )
        classe = self.CLASSES_POR_GRUPO.get(linha["grupo"], Animal)
        return classe(
            id_animal=linha["id_animal"],
            nome=linha["nome"],
            idade=linha["idade"],
            sexo=linha["sexo"],
            peso=linha["peso"],
            data_chegada=linha["data_chegada"],
            especie=especie,
            habitat=linha["habitat"]
        )

    def listar(self):
        with conectar() as conexao:
            linhas = conexao.execute(
                self._consulta_base() + " ORDER BY a.nome"
            ).fetchall()
            return [self._linha_para_animal(linha) for linha in linhas]

    def buscar_por_id(self, id_animal):
        with conectar() as conexao:
            linha = conexao.execute(
                self._consulta_base() + " WHERE a.id_animal = ?",
                (id_animal,)
            ).fetchone()
            return self._linha_para_animal(linha) if linha else None

    def listar_habitats(self):
        with conectar() as conexao:
            return conexao.execute(
                "SELECT id_habitat, nome FROM habitats ORDER BY nome"
            ).fetchall()

    def inserir(self, animal, id_habitat):
        with conectar() as conexao:
            cursor = conexao.execute("""
                INSERT INTO animais (
                    nome, idade, sexo, peso, data_chegada,
                    id_especie, id_habitat
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                animal.nome, animal.idade, animal.sexo, animal.peso,
                animal.data_chegada, animal.especie.id_especie, id_habitat
            ))
            return cursor.lastrowid

    def atualizar(self, animal, id_habitat):
        with conectar() as conexao:
            cursor = conexao.execute("""
                UPDATE animais
                SET nome = ?, idade = ?, sexo = ?, peso = ?,
                    data_chegada = ?, id_especie = ?, id_habitat = ?
                WHERE id_animal = ?
            """, (
                animal.nome, animal.idade, animal.sexo, animal.peso,
                animal.data_chegada, animal.especie.id_especie,
                id_habitat, animal.id_animal
            ))
            return cursor.rowcount > 0

    def excluir(self, id_animal):
        with conectar() as conexao:
            cursor = conexao.execute(
                "DELETE FROM animais WHERE id_animal = ?",
                (id_animal,)
            )
            return cursor.rowcount > 0
