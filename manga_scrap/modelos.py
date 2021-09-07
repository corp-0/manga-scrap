import json
from dataclasses import dataclass, field
from typing import List
from .excepciones import NoExisteCapitulo


class JsonSerializable:
    def to_json_string(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False).encode("utf-8").decode()


@dataclass()
class Genero(JsonSerializable):
    """
    Representacion de un único genero para un manga
    """
    genero: str


@dataclass()
class MangaPreview(JsonSerializable):
    """
    Representación de un manga sin contenido, visto desde el catálogo.

    :param: nombre: str
    :param: enlace_imagen: str
    :param: enlace_manga: str
    """
    nombre: str
    enlace_imagen: str
    enlace_manga: str
    generos: List[Genero]


@dataclass()
class Imagen(JsonSerializable):
    """
    Representación de una única imagen/hoja de un manga
    """
    enlace: str


@dataclass()
class Capitulo(JsonSerializable):
    """
    Representación de un único capítulo de un manga. Las imágenes de un capítulo se van poblando en la medida
    que el capítulo es consultado.
    """
    nombre: str
    enlace: str
    imagenes: List[Imagen] = field(default_factory=list)


@dataclass()
class Manga(JsonSerializable):
    """
    Representación de un manga, con toda su información.

    :param: nombre: str
    :param: imagen: str
    :param: enlace: str
    :param: capitulos: List[Capitulo]
    """
    nombre: str
    imagen: str
    enlace: str
    capitulos: List[Capitulo]
    generos: List[Genero]
    contenido_adulto: bool = False

    @property
    def n_capitulos(self) -> int:
        return len(self.capitulos)

    @property
    def n_imagenes(self) -> int:
        total = 0
        for c in self.capitulos:
            total += len(c.imagenes)

        return total

    @property
    def n_generos(self) -> int:
        return len(self.generos)

    def obtener_capitulo(self, index: int):
        try:
            capitulo = self.capitulos[index]
        except IndexError:
            raise NoExisteCapitulo(self, index)
        else:
            return capitulo

    def __str__(self):
        return \
            f"*** Manga *** \n" \
            f"nombre: {self.nombre} \n" \
            f"enlace: {self.enlace} \n" \
            f"Generos: {self.generos} \n" \
            f"imagen: {self.imagen} \n" \
            f"nº caps: {self.n_capitulos} \n" \
            f"nº imágenes: {self.n_imagenes}"
