from models.animal import Animal


class Ave(Animal):
    grupo = "Ave"

    def realizar_acao(self):
        """Apresenta um comportamento associado a muitas espécies de aves."""
        return (
            f"{self.nome} é uma ave e como exemplo de comportamento das aves, "
            "pode utilizar as asas para voar."
        )
