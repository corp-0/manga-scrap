from manga import Manga

class BaseError(Exception):
    pass

class CapituloInicialInvalido(BaseError):
    def __init__(self, manga: Manga):

        super(CapituloInicialInvalido, self).__init__(
            f"Manga: {manga.nombre} no parte por capítulo 0 ni 1"
        )

