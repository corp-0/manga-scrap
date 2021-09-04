from pprint import pprint
import requests
from bs4 import BeautifulSoup as BS
from modelos import Manga, Capitulo

url_lista = "https://ninemanga.net/manga-list"


def obtener_mangas(page: int = 1):
    r = requests.get(f"{url_lista}?page={page}")
    soup = BS(r.text, features='html.parser')
    cosa = soup.find_all("div", {"class": "thumbnail"})
    mangas = []
    for resultado in cosa:
        a_parsear = resultado.contents
        enlace = a_parsear[1].attrs.get("href")
        imagen = a_parsear[1].contents[1].attrs.get("src")
        nombre = a_parsear[1].contents[1].attrs.get("alt")
        capitulos = obtener_capitulos_menos_hard(enlace)
        manga = Manga(nombre, imagen, enlace, capitulos)
        mangas.append(manga)
    return mangas


# se obtinen los mangas desde la pagina principal del manga, menos hardcore si son 0 o 1, o incluso alguna wuea 0.0.0.01 xd
def obtener_capitulos_menos_hard(enlace: str):
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


def obtener_manga_por_pagina_y_index(pagina: int, index: int):
    manga = obtener_mangas(pagina)[index]
    obtener_capitulos_menos_hard(manga)
    obtener_img(manga.capitulos[0])


# existen espacios en los links de las images y los deja como 'link base (espacio)' '(espacio) resto de link'
# por eso recree este metodo
# falta añadirlos al capitulo, por alguna razon no puedo añadirlo al capitulo
def obtener_img(capitulo: Capitulo):
    r = requests.get(capitulo)
    soup = BS(r.text, features="html.parser")
    images = soup.find_all("img", {"class": "img-responsive"})
    enlace_sin_espacios = []
    for img in images:
        enlace_bruto = img.attrs.get("data-src")
        if "None" not in str(enlace_bruto):
            # evita espacios no manejados
            enlace_sin_espacios.append(enlace_bruto.strip())

    pprint(enlace_sin_espacios)
    # por algun motivo caga, no se puede añadir al capitulo
    # capitulo.imagenes = enlace_sin_espacios


if __name__ == "__main__":
    obtener_manga_por_pagina_y_index(5, 10)