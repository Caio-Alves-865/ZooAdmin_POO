from database.conexao import conectar


def criar_tabelas():
    """Cria as tabelas e cadastra dados iniciais de apoio."""
    with conectar() as conexao:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS grupos (
                id_grupo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS habitats (
                id_habitat INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            );

            CREATE TABLE IF NOT EXISTS especies (
                id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_popular TEXT NOT NULL,
                nome_cientifico TEXT NOT NULL UNIQUE,
                descricao TEXT NOT NULL,
                expectativa_vida_min INTEGER NOT NULL CHECK (expectativa_vida_min > 0),
                expectativa_vida_max INTEGER NOT NULL CHECK (expectativa_vida_max >= expectativa_vida_min),
                alimentacao TEXT NOT NULL,
                id_grupo INTEGER NOT NULL,
                FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS animais (
                id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL CHECK (idade >= 0),
                sexo TEXT NOT NULL CHECK (sexo IN ('Macho', 'Fêmea', 'Não informado')),
                peso REAL NOT NULL CHECK (peso > 0),
                data_chegada TEXT NOT NULL,
                id_especie INTEGER NOT NULL,
                id_habitat INTEGER NOT NULL,
                FOREIGN KEY (id_especie) REFERENCES especies(id_especie)
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                FOREIGN KEY (id_habitat) REFERENCES habitats(id_habitat)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
        """)

        grupos = ("Mamífero", "Ave", "Réptil", "Anfíbio", "Peixe") #tupla que define os grupos
        for grupo in grupos:
            conexao.execute(
                "INSERT OR IGNORE INTO grupos (nome) VALUES (?)",
                (grupo,)
            )

        habitats = [
            ("Savana", "Ambiente aberto com vegetação rasteira e árvores esparsas."),
            ("Floresta", "Ambiente com predominância de árvores e vegetação densa."),
            ("Aquático", "Ambiente com água doce ou salgada."),
            ("Terrário", "Recinto controlado para animais terrestres de pequeno porte."),
            ("Viveiro", "Recinto destinado principalmente a aves.")
        ]
        for nome, descricao in habitats:
            conexao.execute(
                "INSERT OR IGNORE INTO habitats (nome, descricao) VALUES (?, ?)",
                (nome, descricao)
            )
