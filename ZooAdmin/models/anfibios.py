from models.animal import Animal


class Anfibio(Animal):
    grupo = "Anfíbio"

    def realizar_acao(self):
        """Apresenta uma etapa característica do ciclo de vida de muitos anfíbios."""
        return (
            f"{self.nome} é um anfíbio e como exemplo do ciclo de vida dos anfíbios, "
            "pode passar por metamorfose."
        )
