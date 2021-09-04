from typing import List
from manga_scrap.modelos import MangaPreview, Manga, Capitulo, Imagen
from .proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS

url_lista = "https://ninemanga.net/manga-list"


class NineMangaNet(Proveedor):
    @property
    def nombre(self) -> str:
        return "Nombre X"

    def generar_catalogo(self) -> List[MangaPreview]:
        numero_paginas = self._contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            previews = self._obtener_mangas(i)
            previews_lista += previews
        return previews_lista

    def construir_manga(self, preview: MangaPreview) -> Manga:
        capitulos = self._obtener_capitulos_menos_hard(preview.enlace_manga)
        manga = Manga(preview.nombre, preview.enlace_imagen, preview.enlace_manga, capitulos)
        return manga

    def _contar_paginas(self):
        r = requests.get(url_lista)
        soup = BS(r.text, features='html.parser')
        paginas = soup.find('ul', attrs={'class': 'pagination'})
        numero_paginas = paginas.contents[-4].contents[0].contents[0]
        return int(numero_paginas)

    def _obtener_mangas(self, page: int):

        r = requests.get(f"{url_lista}?page={page}")
        soup = BS(r.text, features='html.parser')
        cosa = soup.find_all("div", {"class": "thumbnail"})
        mangas_previews = []
        for resultado in cosa:
            a_parsear = resultado.contents
            enlace = a_parsear[1].attrs.get("href")
            imagen = a_parsear[1].contents[1].attrs.get("src")
            nombre = a_parsear[1].contents[1].attrs.get("alt")
            manga = MangaPreview(nombre, imagen, enlace)
            mangas_previews.append(manga)
        return mangas_previews

    def _obtener_capitulos_menos_hard(self, enlace: str):
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
