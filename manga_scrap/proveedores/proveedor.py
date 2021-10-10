import logging
from abc import ABC, abstractmethod
from ..modelos import MangaPreview, Manga, Capitulo
from typing import List
from requests import get
from ..excepciones import ServidorRespondeContenidoProhibido

log = logging.getLogger("manga_scrap")

class Proveedor(ABC):
    """
    Clase base que define la interfaz para todas las implementaciones que representan a un proveedor de contenido,
    con sus detalles de implementación.
    """
    _catalogo: List[MangaPreview] = []
    _mangas: dict = {}

    def check_respuesta(self):
        log.debug(f"Haciendo check de disponibilidad para proveedor {self.nombre}...")
        respuesta = get(self.url_catalogo)
        if respuesta.status_code == 403:
            log.error(f"El proveedor {self.nombre} con url {self.url_catalogo} ha prohibido el acceso a su contenido.")
            raise ServidorRespondeContenidoProhibido(self.url_catalogo)
        if respuesta.status_code != 200:
            log.warning(f"El proveedor {self.nombre} con url {self.url_catalogo} ha respondido con código diferente a 200: {respuesta.status_code}")

    @property
    @abstractmethod
    def url_catalogo(self) -> str:
        """
        :return: URL correspondiente al catálogo del proveedor.
        """

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
    def obtener_generos(self, enlace: str):
        """
        este metodo recibe un link del manga y obtiene todos los generos a los cuales pertenece
        y se los añade al manga
        :param enlace: preview del catálogo
        :return:
        """
