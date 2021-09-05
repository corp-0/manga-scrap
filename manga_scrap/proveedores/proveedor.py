from abc import ABC, abstractmethod
from ..modelos import MangaPreview, Manga, Capitulo, Genero
from typing import List


class Proveedor(ABC):
    """
    Clase base que define la interfaz para todas las implementaciones que representan a un proveedor de contenido,
    con sus detalles de implementación.
    """
    _catalogo: List[MangaPreview] = []
    _mangas: dict = {}

    @property
    @abstractmethod
    def nombre(self) -> str:
        """
        :return: Nombre del proveedor
        """

    @abstractmethod
    def generar_catalogo(self) -> List[MangaPreview]:
        """
        Scrapea la lista de mangas para generar un catálogo

        :return: un catálogo de tipo List[MangaPreview]
        """

    @property
    def catalogo(self) -> List[MangaPreview]:
        if not self._catalogo:
            self._catalogo = self.generar_catalogo()

        return self._catalogo

    @abstractmethod
    def construir_manga(self, preview: MangaPreview) -> Manga:
        """
        Scrapea y construye un objeto manga a partir de una preview.

        :param preview: MangaPreview que se usará para scrappear y llenar el resto de datos de un Manga
        :return: un manga
        """

    def obtener_manga(self, preview: MangaPreview) -> Manga:
        """
        Devuelve un manga, construyéndolo en memoria si es que no existía, a partir de una preview del catálogo.

        :param preview: preview del catálogo
        :return: un manga
        """
        if preview.enlace_manga not in self._mangas:
            self._mangas[preview.enlace_manga] = self.construir_manga(preview)

        return self._mangas[preview.enlace_manga]

    @abstractmethod
    def obtener_img(self, capitulo: Capitulo) -> None:
        """
        este metodo recibe un capitulo (enlace) y lo analiza buscando todas las imagenes del mismo
        para posteriormente añadirselas al capitulo en cuestion
        :return:
        """

    @abstractmethod
    def obtener_generos(self, preview: MangaPreview):
        """
        este metodo recibe un link del manga y obtiene todos los generos a los cuales pertenece
        y se los añade al manga
        :param preview: preview del catálogo
        :return:
        """
