from manga_scrap.proveedores.nineMangaNet import NineMangaNet

if __name__ == "__main__":
    nine = NineMangaNet()
    for manga in nine.catalogo:
        if "Prison School" in manga.nombre:
            manga_buscado = nine.obtener_manga(manga)
            nine.obtener_img(manga_buscado.capitulos[0])
            print(manga_buscado)
