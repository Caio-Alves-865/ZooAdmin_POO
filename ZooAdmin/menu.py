from datetime import date
import sqlite3

from zoologico import Zoologico
from terminal import console, titulo, sucesso, erro as mostrar_erro, pausar_e_limpar, limpar_console
from models.especie import Especie
from models.mamiferos import Mamifero
from models.aves import Ave
from models.repteis import Reptil
from models.anfibios import Anfibio
from models.peixes import Peixe


CLASSES_POR_GRUPO = {
    "Mamífero": Mamifero,
    "Ave": Ave,
    "Réptil": Reptil,
    "Anfíbio": Anfibio,
    "Peixe": Peixe
}


class Menu:
    def __init__(self):
        self.zoologico = Zoologico()

    def executar(self):
        while True:
            titulo("ZOO ADMIN — SISTEMA ADMINISTRATIVO")
            console.print("""==================================================
  1. Visualizar animais
  2. Gerenciar animais
  3. Gerenciar espécies
  0. Sair do sistema
==================================================""")
            opcao = console.input("Selecione uma opção: ").strip()

            try:
                if opcao == "1":
                    self.visualizar_animais()
                elif opcao == "2":
                    self.menu_animais()
                elif opcao == "3":
                    self.menu_especies()
                elif opcao == "0":
                    sucesso("\nSistema encerrado. Até mais!")
                    break
                else:
                    mostrar_erro("\nOpção inválida. Tente novamente.")
                    self._pausar()
            except (ValueError, sqlite3.IntegrityError) as erro:
                mostrar_erro(f"\nNão foi possível concluir a operação: {erro}")
                self._pausar()
            except KeyboardInterrupt:
                mostrar_erro("\n\nOperação cancelada.")
                self._pausar()
                continue

    @staticmethod
    def _pausar():
        pausar_e_limpar()

    @staticmethod
    def _ler_inteiro(mensagem, minimo=0):
        while True:
            valor = console.input(mensagem).strip()
            try:
                numero = int(valor)
                if numero < minimo:
                    mostrar_erro(f"Informe um número igual ou maior que {minimo}.")
                    continue
                return numero
            except ValueError:
                mostrar_erro("Digite um número inteiro válido.")

    @staticmethod
    def _ler_real(mensagem, minimo=0.01):
        while True:
            valor = console.input(mensagem).strip().replace(",", ".")
            try:
                numero = float(valor)
                if numero < minimo:
                    mostrar_erro(f"Informe um valor igual ou maior que {minimo}.")
                    continue
                return numero
            except ValueError:
                mostrar_erro("Digite um número válido.")

    @staticmethod
    def _ler_data(mensagem, valor_padrao=None):
        while True:
            valor = console.input(mensagem).strip()
            if not valor and valor_padrao:
                return valor_padrao
            try:
                return date.fromisoformat(valor).isoformat()
            except ValueError:
                mostrar_erro("Data inválida. Utilize o formato AAAA-MM-DD.")

    @staticmethod
    def _escolher_sexo():
        opcoes = {"1": "Macho", "2": "Fêmea", "3": "Não informado"}
        while True:
            console.print("\n1. Macho\n2. Fêmea\n3. Não informado")
            escolha = console.input("Sexo: ").strip()
            if escolha in opcoes:
                return opcoes[escolha]
            mostrar_erro("Opção inválida.")

    def visualizar_animais(self):
        animais = self.zoologico.listar_animais()
        titulo("ANIMAIS CADASTRADOS")
        if not animais:
            mostrar_erro("Nenhum animal cadastrado.")
        else:
            for animal in animais:
                console.print("\n" + animal.apresentar_informacoes())
                console.print("-" * 50)
        self._pausar()

    def menu_animais(self):
        while True:
            titulo("GERENCIAR ANIMAIS")
            console.print("""  1. Cadastrar animal
  2. Atualizar animal
  3. Remover animal
  4. Consultar animal por ID
  5. Listar todos os animais
  0. Voltar""")
            opcao = console.input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.cadastrar_animal()
            elif opcao == "2":
                self.atualizar_animal()
            elif opcao == "3":
                self.remover_animal()
            elif opcao == "4":
                self.consultar_animal()
            elif opcao == "5":
                self.visualizar_animais()
            elif opcao == "0":
                limpar_console()
                return
            else:
                mostrar_erro("Opção inválida.")
                self._pausar()

    def _selecionar_especie(self):
        especies = self.zoologico.listar_especies()
        if not especies:
            mostrar_erro("\nNão há espécies cadastradas. Cadastre uma espécie primeiro.")
            return None

        titulo("ESPÉCIES DISPONÍVEIS")
        for especie in especies:
            console.print(f"{especie.id_especie}. {especie}")
        id_especie = self._ler_inteiro("ID da espécie: ", 1)
        especie = self.zoologico.buscar_especie(id_especie)
        if not especie:
            mostrar_erro("Espécie não encontrada.")
        return especie

    def _selecionar_habitat(self):
        habitats = self.zoologico.listar_habitats()
        titulo("HABITATS DISPONÍVEIS")
        for habitat in habitats:
            console.print(f"{habitat['id_habitat']}. {habitat['nome']}")
        id_habitat = self._ler_inteiro("ID do habitat: ", 1)
        if not any(h["id_habitat"] == id_habitat for h in habitats):
            mostrar_erro("Habitat não encontrado.")
            return None
        return id_habitat

    def cadastrar_animal(self):
        titulo("CADASTRAR ANIMAL")
        especie = self._selecionar_especie()
        if not especie:
            self._pausar()
            return

        nome = console.input("Nome do animal: ").strip()
        if not nome:
            mostrar_erro("O nome é obrigatório.")
            self._pausar()
            return

        idade = self._ler_inteiro("Idade (anos): ")
        sexo = self._escolher_sexo()
        peso = self._ler_real("Peso (kg): ")
        data_chegada = self._ler_data(
            "Data de chegada (AAAA-MM-DD, ENTER para hoje): ",
            date.today().isoformat()
        )
        id_habitat = self._selecionar_habitat()
        if id_habitat is None:
            self._pausar()
            return

        classe = CLASSES_POR_GRUPO[especie.grupo]
        animal = classe(
            nome=nome, idade=idade, sexo=sexo, peso=peso,
            data_chegada=data_chegada, especie=especie, habitat=""
        )
        novo_id = self.zoologico.adicionar_animal(animal, id_habitat)
        sucesso(f"\nAnimal cadastrado com sucesso! ID: {novo_id}")
        self._pausar()

    def consultar_animal(self):
        id_animal = self._ler_inteiro("\nID do animal: ", 1)
        animal = self.zoologico.buscar_animal(id_animal)
        if animal:
            console.print("\n" + animal.apresentar_informacoes())
        else:
            mostrar_erro("Animal não encontrado.")
        self._pausar()

    def atualizar_animal(self):
        id_animal = self._ler_inteiro("\nID do animal que deseja atualizar: ", 1)
        atual = self.zoologico.buscar_animal(id_animal)
        if not atual:
            mostrar_erro("Animal não encontrado.")
            self._pausar()
            return

        console.print("\nDeixe um campo vazio para manter o valor atual.")
        nome = console.input(f"Nome [{atual.nome}]: ").strip() or atual.nome
        idade_txt = console.input(f"Idade [{atual.idade}]: ").strip()
        idade = atual.idade if not idade_txt else self._validar_int_texto(idade_txt, 0)
        sexo_txt = console.input(f"Sexo [{atual.sexo}] (ENTER mantém): ").strip()
        sexo = atual.sexo
        if sexo_txt:
            mapa = {"1": "Macho", "2": "Fêmea", "3": "Não informado"}
            console.print("1. Macho | 2. Fêmea | 3. Não informado")
            sexo = mapa.get(sexo_txt, sexo_txt)
            if sexo not in mapa.values():
                mostrar_erro("Sexo inválido; mantendo o valor anterior.")
                sexo = atual.sexo

        peso_txt = console.input(f"Peso em kg [{atual.peso}]: ").strip().replace(",", ".")
        peso = atual.peso if not peso_txt else self._validar_float_texto(peso_txt, 0.01)
        data_chegada = self._ler_data(
            f"Data de chegada [{atual.data_chegada}]: ",
            atual.data_chegada
        )

        especie = atual.especie
        trocar = console.input("Deseja alterar a espécie? (s/n): ").strip().lower()
        if trocar == "s":
            nova_especie = self._selecionar_especie()
            if nova_especie:
                especie = nova_especie

        habitats = self.zoologico.listar_habitats()
        console.print("\nHabitats:")
        for h in habitats:
            console.print(f"{h['id_habitat']}. {h['nome']}")
        habitat_atual = next(
            (h for h in habitats if h["nome"] == atual.habitat), None
        )
        escolha_habitat = console.input(
            f"ID do habitat [{habitat_atual['id_habitat'] if habitat_atual else ''}] "
            "(ENTER mantém): "
        ).strip()
        id_habitat = (
            habitat_atual["id_habitat"] if not escolha_habitat
            else self._validar_int_texto(escolha_habitat, 1)
        )

        if not any(h["id_habitat"] == id_habitat for h in habitats):
            mostrar_erro("Habitat inválido; atualização cancelada.")
            self._pausar()
            return

        classe = CLASSES_POR_GRUPO[especie.grupo]
        atualizado = classe(
            id_animal=atual.id_animal, nome=nome, idade=idade, sexo=sexo,
            peso=peso, data_chegada=data_chegada, especie=especie,
            habitat=atual.habitat
        )
        self.zoologico.atualizar_animal(atualizado, id_habitat)
        sucesso("\nAnimal atualizado com sucesso!")
        self._pausar()

    def remover_animal(self):
        id_animal = self._ler_inteiro("\nID do animal que deseja remover: ", 1)
        animal = self.zoologico.buscar_animal(id_animal)
        if not animal:
            mostrar_erro("Animal não encontrado.")
            self._pausar()
            return
        console.print(animal)
        confirmar = console.input("Confirma a exclusão? (s/n): ").strip().lower()
        if confirmar == "s":
            self.zoologico.remover_animal(id_animal)
            sucesso("Animal removido com sucesso.")
        else:
            mostrar_erro("Exclusão cancelada.")
        self._pausar()

    @staticmethod
    def _validar_int_texto(texto, minimo):
        try:
            numero = int(texto)
            if numero < minimo:
                raise ValueError
            return numero
        except ValueError:
            mostrar_erro("Valor inválido. A operação foi cancelada.")
            raise ValueError("Entrada numérica inválida.")

    @staticmethod
    def _validar_float_texto(texto, minimo):
        try:
            numero = float(texto)
            if numero < minimo:
                raise ValueError
            return numero
        except ValueError:
            mostrar_erro("Valor inválido. A operação foi cancelada.")
            raise ValueError("Entrada numérica inválida.")

    def menu_especies(self):
        while True:
            titulo("GERENCIAR ESPÉCIES")
            console.print("""  1. Cadastrar espécie
  2. Atualizar espécie
  3. Remover espécie
  4. Consultar espécie por ID
  5. Listar todas as espécies
  0. Voltar""")
            opcao = console.input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.cadastrar_especie()
            elif opcao == "2":
                self.atualizar_especie()
            elif opcao == "3":
                self.remover_especie()
            elif opcao == "4":
                self.consultar_especie()
            elif opcao == "5":
                self.listar_especies()
            elif opcao == "0":
                limpar_console()
                return
            else:
                mostrar_erro("Opção inválida.")
                self._pausar()

    def _ler_dados_especie(self, especie_atual=None):
        atual = especie_atual
        nome = console.input(
            f"Nome popular [{atual.nome_popular}]: " if atual else "Nome popular: "
        ).strip() if atual else console.input("Nome popular: ").strip()
        cientifico = console.input(
            f"Nome científico [{atual.nome_cientifico}]: " if atual else "Nome científico: "
        ).strip() if atual else console.input("Nome científico: ").strip()
        descricao = console.input(
            f"Descrição [{atual.descricao}]: " if atual else "Descrição: "
        ).strip() if atual else console.input("Descrição: ").strip()
        alimentacao = console.input(
            f"Alimentação [{atual.alimentacao}]: " if atual else "Alimentação: "
        ).strip() if atual else console.input("Alimentação: ").strip()

        if atual:
            nome = nome or atual.nome_popular
            cientifico = cientifico or atual.nome_cientifico
            descricao = descricao or atual.descricao
            alimentacao = alimentacao or atual.alimentacao

        if not all([nome, cientifico, descricao, alimentacao]):
            raise ValueError("Todos os campos textuais são obrigatórios.")

        grupos = self.zoologico.listar_grupos()
        titulo("GRUPOS ZOOLÓGICOS")
        for grupo in grupos:
            console.print(f"{grupo['id_grupo']}. {grupo['nome']}")
        if atual:
            grupo_atual_id = next(
                g["id_grupo"] for g in grupos if g["nome"] == atual.grupo
            )
            texto = console.input(f"ID do grupo [{grupo_atual_id}] (ENTER mantém): ").strip()
            id_grupo = grupo_atual_id if not texto else self._validar_int_texto(texto, 1)
        else:
            id_grupo = self._ler_inteiro("ID do grupo: ", 1)

        grupo_escolhido = next(
            (g["nome"] for g in grupos if g["id_grupo"] == id_grupo), None
        )
        if not grupo_escolhido:
            raise ValueError("Grupo zoológico inválido.")

        if atual:
            minimo_txt = console.input(
                f"Expectativa mínima de vida [{atual.expectativa_vida_min}]: "
            ).strip()
            maximo_txt = console.input(
                f"Expectativa máxima de vida [{atual.expectativa_vida_max}]: "
            ).strip()
            minimo = atual.expectativa_vida_min if not minimo_txt else self._validar_int_texto(minimo_txt, 1)
            maximo = atual.expectativa_vida_max if not maximo_txt else self._validar_int_texto(maximo_txt, 1)
        else:
            minimo = self._ler_inteiro("Expectativa mínima de vida (anos): ", 1)
            maximo = self._ler_inteiro("Expectativa máxima de vida (anos): ", 1)

        if maximo < minimo:
            raise ValueError("A expectativa máxima não pode ser menor que a mínima.")

        return Especie(
            id_especie=atual.id_especie if atual else None,
            nome_popular=nome, nome_cientifico=cientifico,
            descricao=descricao, expectativa_vida_min=minimo,
            expectativa_vida_max=maximo, alimentacao=alimentacao,
            grupo=grupo_escolhido
        )

    def cadastrar_especie(self):
        titulo("CADASTRAR ESPÉCIE")
        especie = self._ler_dados_especie()
        novo_id = self.zoologico.adicionar_especie(especie)
        sucesso(f"\nEspécie cadastrada com sucesso! ID: {novo_id}")
        self._pausar()

    def listar_especies(self):
        especies = self.zoologico.listar_especies()
        titulo("ESPÉCIES CADASTRADAS")
        if not especies:
            mostrar_erro("Nenhuma espécie cadastrada.")
        for especie in especies:
            console.print(f"\nID: {especie.id_especie}")
            console.print(f"Nome: {especie.nome_popular}")
            console.print(f"Nome científico: {especie.nome_cientifico}")
            console.print(f"Grupo: {especie.grupo}")
            console.print(f"Expectativa de vida: {especie.expectativa_vida_min}-"
                  f"{especie.expectativa_vida_max} anos")
            console.print(f"Alimentação: {especie.alimentacao}")
            console.print(f"Descrição: {especie.descricao}")
            console.print("-" * 50)
        self._pausar()

    def consultar_especie(self):
        id_especie = self._ler_inteiro("\nID da espécie: ", 1)
        especie = self.zoologico.buscar_especie(id_especie)
        if especie:
            console.print(f"\nID: {especie.id_especie}")
            console.print(especie)
            console.print(f"Descrição: {especie.descricao}")
            console.print(f"Alimentação: {especie.alimentacao}")
        else:
            mostrar_erro("Espécie não encontrada.")
        self._pausar()

    def atualizar_especie(self):
        id_especie = self._ler_inteiro("\nID da espécie que deseja atualizar: ", 1)
        atual = self.zoologico.buscar_especie(id_especie)
        if not atual:
            mostrar_erro("Espécie não encontrada.")
            self._pausar()
            return
        especie = self._ler_dados_especie(atual)
        self.zoologico.atualizar_especie(especie)
        sucesso("\nEspécie atualizada com sucesso.")
        self._pausar()

    def remover_especie(self):
        id_especie = self._ler_inteiro("\nID da espécie que deseja remover: ", 1)
        especie = self.zoologico.buscar_especie(id_especie)
        if not especie:
            mostrar_erro("Espécie não encontrada.")
            self._pausar()
            return
        console.print(especie)
        confirmar = console.input("Confirma a exclusão? (s/n): ").strip().lower()
        if confirmar == "s":
            self.zoologico.remover_especie(id_especie)
            sucesso("Espécie removida com sucesso.")
        else:
            mostrar_erro("Exclusão cancelada.")
        self._pausar()
