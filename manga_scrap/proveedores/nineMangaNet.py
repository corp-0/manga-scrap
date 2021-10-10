import logging
from typing import List
from manga_scrap.modelos import MangaPreview, Manga, Capitulo, Imagen, Genero
from manga_scrap.proveedores.proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS, Tag

url_lista = "https://ninemanga.net/manga-list"
log = logging.getLogger("manga_scrap")

class NineMangaNet(Proveedor):

    @property
    def nombre(self) -> str:
        return "NineManga.net"

    def generar_catalogo(self) -> List[MangaPreview]:
        log.info("Generando catálogo...")
        numero_paginas = self._contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            previews = self._obtener_preview_mangas(i)
            previews_lista += previews
        return previews_lista

    def construir_manga(self, preview: MangaPreview) -> Manga:
        log.info(f"Construyendo manga desde preview {preview.nombre} ...")
        capitulos = self._obtener_capitulos(preview.enlace_manga)
        manga = Manga(preview.nombre, preview.enlace_imagen, preview.enlace_manga, capitulos, preview.generos)
        return manga

    def _contar_paginas(self):
        log.debug("Contando páginas...")
        r = requests.get(url_lista)
        soup = BS(r.text, features='html.parser')
        paginas = soup.find('ul', attrs={'class': 'pagination'})
        numero_paginas = paginas.contents[-4].contents[0].contents[0]
        return int(numero_paginas)

    def _obtener_preview_mangas(self, page: int):
        log.debug("Obteniendo previews...")
        r = requests.get(f"{url_lista}?page={page}")
        soup = BS(r.text, features='html.parser')
        cosa = soup.find_all("div", {"class": "thumbnail"})
        mangas_previews = []
        for resultado in cosa:
            a_parsear = resultado.contents
            enlace = a_parsear[1].attrs.get("href")
            imagen = a_parsear[1].contents[1].attrs.get("src")
            nombre = a_parsear[1].contents[1].attrs.get("alt")
            manga = MangaPreview(nombre, imagen, enlace, self.obtener_generos(enlace))
            mangas_previews.append(manga)
        return mangas_previews

    def _obtener_capitulos(self, enlace: str):
        log.debug(f"Obteniendo capítulos desde enlace {enlace}...")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        table = soup.find('table', attrs={'class': 'table-hover'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        capitulos = []
        for row in rows:
            enlace_capitulo = (row.contents[1].contents[3].attrs.get("href"))
            nombre = row.contents[1].contents[3].contents[0]
            capitulos.append(Capitulo(nombre, enlace_capitulo))
        return capitulos

    def obtener_img(self, capitulo: Capitulo):
        log.info(f"Obteniendo imágenes de capítulo {capitulo.nombre}...")
        r = requests.get(capitulo.enlace)
        soup = BS(r.text, features="html.parser")
        images = soup.find_all("img", {"class": "img-responsive"})
        lista_images = []
        for img in images:
            enlace_bruto = img.attrs.get("data-src")
            if "None" not in str(enlace_bruto):
                # evita espacios no manejados
                lista_images.append(Imagen(enlace_bruto.strip()))
        capitulo.imagenes = lista_images

    def obtener_generos(self, enlace):
        log.info(f"Obteniendo géneros para manga con enlace {enlace}")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        # contiene la reseña, autor, generos, el estado de publicacion
        datos_interesantes = soup.find_all('span', attrs={'class': 'list-group-item'})
        lista__categorias = datos_interesantes[5].contents
        if lista__categorias is None:
            return [Genero("Desconocido")]
        categorias = []
        for c in lista__categorias:
            if type(c) is Tag and "None" not in str(c.attrs.get("href")):
                genero = c.contents[0]
                categorias.append(Genero(genero))
        return categorias
