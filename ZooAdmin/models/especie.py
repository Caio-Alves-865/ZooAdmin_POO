class Especie:
    """Representa uma espécie e suas características gerais."""

    def __init__(
        self, nome_popular, nome_cientifico, descricao,
        expectativa_vida_min, expectativa_vida_max, alimentacao,
        grupo, id_especie=None
    ):
        self.id_especie = id_especie
        self.nome_popular = nome_popular
        self.nome_cientifico = nome_cientifico
        self.descricao = descricao
        self.expectativa_vida_min = expectativa_vida_min
        self.expectativa_vida_max = expectativa_vida_max
        self.alimentacao = alimentacao
        self.grupo = grupo

    def __str__(self):
        return (
            f"{self.nome_popular} ({self.nome_cientifico}) | "
            f"{self.grupo} | Vida média: "
            f"{self.expectativa_vida_min}-{self.expectativa_vida_max} anos"
        )
