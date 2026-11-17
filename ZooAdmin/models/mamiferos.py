from models.animal import Animal


class Mamifero(Animal):
    grupo = "Mamífero"

    def realizar_acao(self):
        """Apresenta um comportamento característico dos mamíferos."""
        return (
            f"{self.nome} é um mamífero e como exemplo de comportamento dos mamíferos, "
            "a fêmea amamenta suas crias por meio das glândulas mamárias."
        )
