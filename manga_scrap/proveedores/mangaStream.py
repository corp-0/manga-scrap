from typing import List
from manga_scrap.modelos import MangaPreview, Imagen, Genero, CapituloPreview, CapituloDetalle, MangaDetalle
from manga_scrap.proveedores.proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS, Tag
import logging

log = logging.getLogger("manga_scrap")
url_catalogo = "http://mangastream.mobi/latest-manga"


class MangaList(Proveedor):

    def generar_catalogo(self, pagina: int = None) -> List[MangaPreview]:
        pass

    def obtener_manga_detalle(self, preview: MangaPreview) -> MangaDetalle:
        pass

    def obtener_capitulo_detalle(self, capitulo: CapituloPreview) -> CapituloDetalle:
        pass

    @property
    def url_catalogo(self) -> str:
        return "http://mangastream.mobi/latest-manga"

    @property
    def nombre(self) -> str:
        return "mangastream.mobi"


def contar_paginas():
    log.debug("Contando paginas")
    r = requests.get(url_catalogo)
    soup = BS(r.text, features='html.parser')
    paginas = soup.find('ul', attrs={'class': 'pagination'})
    numero_paginas = paginas.contents[-4].contents[0].contents[0]
    log.debug(f'Número de paginas {numero_paginas}')
    return int(numero_paginas)


def obtener_preview_mangas(page: int):
    log.debug("Generando previews")
    r = requests.get(f"{url_catalogo}?page={page}")
    soup = BS(r.text, features='html.parser')
    cosa = soup.find_all("div", {"class": "media mainpage-manga"})
    mangas_previews = []
    genero = []
    for resultado in cosa:
        enlace = resultado.contents[3].contents[1].attrs.get("href")
        imagen = resultado.contents[1].contents[1].contents[1].attrs.get("src")
        nombre = resultado.contents[3].contents[1].attrs.get("title")
        genero_bruto = resultado.contents[3].contents[3]
        genero_menos_bruto = genero_bruto.contents[2]
        genero.append(genero_menos_bruto.split(';'))
        manga = MangaPreview(nombre, imagen, enlace, genero)
        log.debug(f'Nombre manga: {nombre}')
        mangas_previews.append(manga)
        # test
        obtener_manga_detalle(manga)
    return mangas_previews


def obtener_manga_detalle(preview: MangaPreview) -> MangaDetalle:
    capitulos = obtener_capitulos(preview.enlace_manga)
    return MangaDetalle(
        nombre=preview.nombre,
        imagen=preview.enlace_imagen,
        enlace=preview.enlace_manga,
        contenido_adulto=preview.contenido_adulto,
        generos=preview.generos,
        capitulos=capitulos
    )


def obtener_capitulos(enlace: str):
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
        #test
        obtener_capitulo_detalle(capitulo)
    return capitulos


def obtener_capitulo_detalle(capitulo: CapituloPreview) -> CapituloDetalle:
    log.debug(f"Obteniendo todo el contenido de capítulo {capitulo}...")
    r = requests.get(capitulo.enlace)
    soup = BS(r.text, features="html.parser")
    images_bruto = soup.find_all('div', attrs={'class': 'chapter-content-inner text-center image-auto'})
    images = images_bruto[0].contents[1].contents[0]
    lista_images = []
    lista_images.append(images.split(','))
    return CapituloDetalle(capitulo.nombre, capitulo.enlace, lista_images)


def generar_catalogo(pagina: int = None) -> List[MangaPreview]:
        log.debug("Generando catalogo")
        numero_paginas = pagina if pagina else contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            log.debug(f'Número de pagina actual: {i}')
            previews = obtener_preview_mangas(i)
            previews_lista += previews
        return previews_lista
