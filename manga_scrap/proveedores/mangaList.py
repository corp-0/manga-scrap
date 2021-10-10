from typing import List
from manga_scrap.modelos import MangaPreview, Manga, Capitulo, Imagen, Genero
from manga_scrap.proveedores.proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS, Tag
import logging

log = logging.getLogger("manga_scrap")


class MangaList(Proveedor):

    @property
    def url_catalogo(self) -> str:
        return "https://leermanga.net/biblioteca"

    @property
    def nombre(self) -> str:
        return "mangaList.com"

    def contar_paginas(self):
        log.debug("Contando paginas")
        r = requests.get(self.url_catalogo)
        soup = BS(r.text, features='html.parser')
        paginas = soup.find('ul', attrs={'class': 'pagination'})
        numero_paginas = paginas.contents[-4].contents[0].contents[0]
        log.debug(f'Número de paginas {numero_paginas}')
        return int(numero_paginas)

    def generar_catalogo(self) -> List[MangaPreview]:
        log.debug("Generando catalogo")
        numero_paginas = self.contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            log.debug(f'Número de pagina actual: {i}')
            previews = self._obtener_preview_mangas(i)
            previews_lista += previews

        return previews_lista

    def _obtener_preview_mangas(self, page: int):
        log.debug("Generando previews")
        r = requests.get(f"{self.url_catalogo}?page={page}")
        soup = BS(r.text, features='html.parser')
        cosa = soup.find_all("div", {"class": "manga_biblioteca"})
        mangas_previews = []
        for resultado in cosa:
            enlace = resultado.contents[3].attrs.get("href")
            imagen = resultado.contents[3].contents[1].attrs.get("src")
            nombre = resultado.contents[3].attrs.get("title")
            manga = MangaPreview(nombre, imagen, enlace, self.obtener_generos(enlace))
            log.debug(f'Nombre manga: {nombre}')
            mangas_previews.append(manga)
        return mangas_previews

    def obtener_generos(self, enlace: str):

        log.info(f"Obteniendo géneros para manga con enlace {enlace}")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        datos_interesantes = soup.findAll("i", {"class": "fas fa-tag"})
        categorias = []
        for i in datos_interesantes:
            genero = Genero(i.next.strip())
            categorias.append(genero)
        return categorias

    def construir_manga(self, preview: MangaPreview) -> Manga:
        log.info(f"Construyendo manga desde preview {preview.nombre} ...")
        capitulos = self._obtener_capitulos(preview.enlace_manga)
        manga = Manga(preview.nombre, preview.enlace_imagen, preview.enlace_manga, capitulos, preview.generos)
        return manga

    def _obtener_capitulos(self, enlace: str):
        log.debug(f"Obteniendo capítulos desde enlace {enlace}...")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        table = soup.findAll('li', attrs={'class': 'wp-manga-chapter'})
        capitulos = []
        for row in table:
            enlace_capitulo = (row.contents[1].attrs.get("href"))
            nombre = row.contents[1].next.strip()
            capitulo = Capitulo(nombre, enlace_capitulo)
            self.obtener_img(capitulo)
            capitulos.append(capitulo)
        return capitulos

    def obtener_img(self, capitulo: Capitulo) -> None:
        log.info(f"Obteniendo imágenes de capítulo {capitulo.nombre}...")
        r = requests.get(capitulo.enlace)
        soup = BS(r.text, features="html.parser")
        images = soup.find_all("div", {"id": "images_chapter"})
        lista_images = []
        img = images[0].contents
        for enlace_img in img:
            if type(enlace_img) is Tag:
                imagen = Imagen(enlace_img.attrs.get("data-src"))
                lista_images.append(imagen)
        capitulo.imagenes = lista_images
