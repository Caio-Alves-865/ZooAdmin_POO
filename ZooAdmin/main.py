from database.tabelas import criar_tabelas
from menu import Menu
from terminal import console, erro as mostrar_erro


def main():
    try:
        criar_tabelas()
        Menu().executar()
    except KeyboardInterrupt:
        console.print("\n\nSistema encerrado pelo usuário.", style="bold red")
    except Exception as erro:
        mostrar_erro(f"\nNão foi possível iniciar o ZooAdmin: {erro}")


if __name__ == "__main__":
    main()

# DESENVOLVIDO POR CAIO ALVES DE VASCONCELOS
# BP3081702
