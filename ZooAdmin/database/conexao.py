import sqlite3
from pathlib import Path

# O banco fica na pasta database, independentemente de onde o programa for iniciado.
CAMINHO_BANCO = Path(__file__).resolve().parent / "zoo_admin.db"


def conectar():
    """Abre e configura uma conexão com o banco SQLite."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao
