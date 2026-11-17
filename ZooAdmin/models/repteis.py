from models.animal import Animal


class Reptil(Animal):
    grupo = "Réptil"

    def realizar_acao(self):
        """Apresenta uma característica fisiológica dos répteis."""
        return (
            f"{self.nome} é um réptil e como réptil, regula a temperatura corporal "
            "com auxílio de fontes externas de calor."
        )
