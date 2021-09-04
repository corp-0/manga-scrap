from manga_scrap.proveedores.nineMangaNet import NineMangaNet

if __name__ == "__main__":
    nine = NineMangaNet()
    for manga in nine.catalogo:
        if ("Dagashi Kashi" in manga.nombre):
            manga_buscado = nine.obtener_manga(manga)
            print(manga_buscado.capitulos)