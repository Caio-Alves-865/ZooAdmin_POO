from models.animal import Animal


class Peixe(Animal):
    grupo = "Peixe"

    def realizar_acao(self):
        """Apresenta características comuns aos peixes."""
        return (
            f"{self.nome} é um peixe e como exemplo de comportamento dos peixes, "
            "utiliza as nadadeiras para se locomover na água e, em geral, "
            "as brânquias para realizar trocas gasosas."
        )
