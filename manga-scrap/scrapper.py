import requests
from bs4 import BeautifulSoup as BS, Tag
from manga import Manga, Capitulo, Imagen
from exceptions import CapituloInicialInvalido
from pprint import pprint
import time

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
        manga = Manga(nombre, imagen, enlace)
        mangas.append(manga)

    return mangas

def obtener_capitulos(manga: Manga):
    try:
        r_zero = requests.get(f"{manga.enlace}/0")
        r_uno = requests.get(f"{manga.enlace}/1")
        if r_zero.status_code == 500 and r_uno.status_code == 500:
            raise CapituloInicialInvalido(manga)
    except CapituloInicialInvalido:
        raise CapituloInicialInvalido(manga)

    enlace = f"{manga.enlace}/0" if r_zero.status_code != 500 else f"{manga.enlace}/1"
    r = requests.get(enlace, timeout=None)
    soup = BS(r.text, features="html.parser")
    select_capitulos = soup.find("select", {"id": "c_list"})
    capitulos = []
    for wea in select_capitulos:
        if type(wea) is Tag:
            enlace = wea.attrs.get("value")
            numero = float(enlace.split("/")[-1])
            c = Capitulo(numero, enlace)
            capitulos.append(c)
    capitulos.reverse()
    manga.capitulos = capitulos

def obtener_manga_por_pagina_y_index(pagina: int, index: int):
    try:
        manga = obtener_mangas(pagina)[index]
        obtener_capitulos(manga)
        for c in manga.capitulos:
            obtener_imagenes(c)
    except IndexError:
        return None
    else:
        return manga


def obtener_imagenes(capitulo: Capitulo):
    r = requests.get(capitulo.enlace, timeout=None)
    soup = BS(r.text, features="html.parser")
    imgs = soup.find_all("img", {"class": "img-responsive"})
    imagenes = [Imagen(img.attrs.get("data-src")) for img in imgs if img.attrs.get("data-src") is not None]
    capitulo.imagenes = imagenes


if __name__ == "__main__":
    # a = time.clock()
    pprint(obtener_manga_por_pagina_y_index(9, 18))
    b = time.clock()
    # print("tiempo total consulta: ", b - a)

