from manga_scrap.proveedores import mangaStream, mangaList

if __name__ == "__main__":
    manga_list = mangaStream
    manga_list.generar_catalogo(1)
