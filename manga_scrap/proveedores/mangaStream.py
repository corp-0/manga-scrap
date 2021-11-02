from typing import List
from manga_scrap.modelos import MangaPreview, Imagen, Genero, CapituloPreview, CapituloDetalle, MangaDetalle
from manga_scrap.proveedores.proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS, Tag
import logging

log = logging.getLogger("manga_scrap")


class MangaStream(Proveedor):
    @property
    def url_catalogo(self) -> str:
        return "http://mangastream.mobi/latest-manga"

    @property
    def nombre(self) -> str:
        return "mangastream.mobi"

    def generar_catalogo(self, pagina: int = None) -> List[MangaPreview]:
        log.debug("Generando catalogo")
        numero_paginas = pagina if pagina else self._contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            log.debug(f'Número de pagina actual: {i}')
            previews = self._obtener_preview_mangas(i)
            previews_lista += previews
        return previews_lista

    def obtener_manga_detalle(self, preview: MangaPreview) -> MangaDetalle:
        capitulos = self._obtener_capitulos(preview.enlace_manga)
        return MangaDetalle(
            nombre=preview.nombre,
            imagen=preview.enlace_imagen,
            enlace=preview.enlace_manga,
            contenido_adulto=preview.contenido_adulto,
            generos=preview.generos,
            capitulos=capitulos
        )

    def obtener_capitulo_detalle(self, capitulo: CapituloPreview) -> CapituloDetalle:
        log.debug(f"Obteniendo todo el contenido de capítulo {capitulo}...")
        r = requests.get(capitulo.enlace)
        soup = BS(r.text, features="html.parser")
        images_bruto = soup.find_all('div', attrs={'class': 'chapter-content-inner text-center image-auto'})
        images = images_bruto[0].contents[1].contents[0]
        lista = [images.split(',')]
        lista_img = []
        for img in lista:
            imagen = Imagen(img)
            lista_img.append(imagen)
        return CapituloDetalle(capitulo.nombre, capitulo.enlace, lista_img)

    def _obtener_preview_mangas(self, page: int):
        log.debug("Generando previews")
        r = requests.get(f"{self.url_catalogo}?page={page}")
        soup = BS(r.text, features='html.parser')
        cosa = soup.find_all("div", {"class": "media mainpage-manga"})
        mangas_previews = []
        lista = []
        lista_genero = []
        for resultado in cosa:
            enlace = resultado.contents[3].contents[1].attrs.get("href")
            imagen = resultado.contents[1].contents[1].contents[1].attrs.get("src")
            nombre = resultado.contents[3].contents[1].attrs.get("title")
            genero_bruto = resultado.contents[3].contents[3]
            genero_menos_bruto = genero_bruto.contents[2]
            lista.append(genero_menos_bruto.split(';'))
            for g in lista:
                lista_genero.append(Genero(g))
            manga = MangaPreview(nombre, imagen, enlace, lista_genero)
            log.debug(f'Nombre manga: {nombre}')
            mangas_previews.append(manga)
            return mangas_previews

    def _obtener_capitulos(self, enlace: str):
        log.debug(f"Obteniendo capítulos desde enlace {enlace}...")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        table = soup.find_all('div', attrs={'class': 'col-xs-12 chapter'})
        capitulos = []
        for row in table:
            enlace_capitulo = (row.contents[1].contents[1].attrs.get("href"))
            nombre = (row.contents[1].contents[1].attrs.get("title"))
            capitulo = CapituloPreview(nombre, enlace_capitulo)
            capitulos.append(capitulo)
        return capitulos

    def _contar_paginas(self):
        log.debug("Contando paginas")
        r = requests.get(self.url_catalogo)
        soup = BS(r.text, features='html.parser')
        paginas = soup.find('ul', attrs={'class': 'pagination'})
        numero_paginas = paginas.contents[-4].contents[0].contents[0]
        log.debug(f'Número de paginas {numero_paginas}')
        return int(numero_paginas)
