from typing import List

from .proveedor import Proveedor
from ..modelos import MangaPreview, Manga, Capitulo, Imagen


class PruebaProveedor(Proveedor):
    """
    Proveedor de prueba que devuelve un catálogo de 3 mangas, cada uno con 3 capítulo y cada capítulo con 3 fotos.
    """

    def obtener_img(capitulo: Capitulo) -> None:
        pass

    @property
    def nombre(self) -> str:
        return "Proveedor Dummy"

    def generar_catalogo(self) -> List[MangaPreview]:
        preview: List[MangaPreview] = []
        for i in range(1, 4):
            p = MangaPreview(f"Manga Nº{i}", f"https://dummy.cl/portada/{i}", f"https://dummy.cl/manga/{i}")
            preview.append(p)
        return preview

    def construir_manga(self, preview: MangaPreview) -> Manga:
        imagenes: List[Imagen] = []
        for i in range(1, 4):
            img = Imagen(f"{preview.enlace_manga}/img/{i}")
            imagenes.append(img)

        capitulos: List[Capitulo] = []
        for i in range(1, 4):
            c = Capitulo(i, f"{preview.enlace_manga}/cap/{i}", imagenes)
            capitulos.append(c)

        manga = Manga(preview.nombre, preview.enlace_imagen, preview.enlace_manga, capitulos)

        return manga
