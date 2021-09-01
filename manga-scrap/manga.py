from dataclasses import dataclass, field
from typing import List

@dataclass()
class Imagen:
    enlace: str

@dataclass()
class Capitulo:
    numero: float
    enlace: str
    imagenes: List[Imagen] = field(default_factory=list)

@dataclass()
class Manga:
    nombre: str
    imagen: str
    enlace: str
    capitulos: List[Capitulo] = field(default_factory=list)

    def __str__(self):
        return \
            f"{self.nombre}: {self.enlace} \n" \
            f"{self.capitulos}"


@dataclass()
class ListaMangas:
    mangas: List[Manga]
    pagina: int = 1


