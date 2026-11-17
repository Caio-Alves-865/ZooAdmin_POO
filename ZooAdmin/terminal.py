# Utilizando a biblioteca rich e a 'os' para melhor visualização do console

import os
from rich.console import Console


console = Console()

#títulos em azul
def titulo(mensagem):
    console.print(f"\n{mensagem}", style="bold blue")

#ação feita com sucesso em verde
def sucesso(mensagem):
    console.print(mensagem, style="green")

#erros ou falhas em vermelho
def erro(mensagem):
    console.print(mensagem, style="bold red")

#limpa o console com base no sistema operacional (cls para windows e clear para linux)
def limpar_console():
    os.system("cls" if os.name == "nt" else "clear")


def pausar_e_limpar():
    console.input("\n[dim]Pressione ENTER para continuar...[/dim]")
    limpar_console()
