from typing import List
from manga_scrap.modelos import MangaPreview, Manga, Capitulo, Imagen, Genero
from manga_scrap.proveedores.proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS, Tag

url_lista = "https://leermanga.net/biblioteca"

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


class MangaList(Proveedor):
    # segundo

    def construir_manga(self, preview: MangaPreview) -> Manga:
        pass

    def obtener_img(self, capitulo: Capitulo) -> None:
        pass

    def obtener_generos(self, enlace: str):
        pass

    @property
    def nombre(self) -> str:
        return "mangaList.com"

    # primero
    def contar_paginas(self):
        r = requests.get(url_lista)
        soup = BS(r.text, features='html.parser')
        paginas = soup.find('ul', attrs={'class': 'pagination'})
        numero_paginas = paginas.contents[-4].contents[0].contents[0]
        return int(numero_paginas)

    # segundo
    def generar_catalogo(self) -> List[MangaPreview]:
        numero_paginas = self.contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            previews = self._obtener_preview_mangas(i)
            previews_lista += previews
        return previews_lista

    def _obtener_preview_mangas(self, page: int):
        r = requests.get(f"{url_lista}?page={page}")
        soup = BS(r.text, features='html.parser')
        cosa = soup.find_all("div", {"class": "manga_biblioteca"})
        mangas_previews = []
        for resultado in cosa:
            # a_parsear = resultado.contents
            enlace = resultado.contents[3].attrs.get("href")
            imagen = resultado.contents[3].contents[1].attrs.get("src")
            nombre = resultado.contents[3].attrs.get("title")
            manga = MangaPreview(nombre, imagen, enlace, self.obtener_generos(enlace))
            mangas_previews.append(manga)
        return mangas_previews

