import unittest

from manga_scrap.modelos import MangaPreview, Genero
from manga_scrap.proveedores.prueba import PruebaProveedor

#TODO probar todos los métodos de Proovedor!
class ProveedorTest(unittest.TestCase):
    proveedor: PruebaProveedor

    def setUp(self) -> None:
        self.proveedor = PruebaProveedor()
        self.catalogo = self.proveedor.catalogo

    def test_nombre_es_el_esperado(self):
        self.assertEqual(self.proveedor.nombre, "Proveedor Dummy")

    def test_al_obtener_catalogo_no_es_none(self):
        self.assertIsNotNone(self.catalogo)

    def test_catalogo_tiene_3_entradas(self):
        self.assertEqual(3, len(self.catalogo))

    def test_cada_entrada_de_catalogo_tiene_datos(self):
        for preview in self.catalogo:
            self.assertIsNotNone(preview.nombre)
            self.assertIsNotNone(preview.enlace_manga)
            self.assertIsNotNone(preview.enlace_imagen)

    def test_al_generar_un_manga_no_es_none(self):
        manga = self.proveedor.obtener_manga_detalle(
            self.catalogo[0])  # generar un manga a partir de la primera entrada de catálogo
        self.assertIsNotNone(manga)

    def test_obtener_manga_fuera_de_catalogo_lo_agrega_a_catalogo(self):
        preview = MangaPreview(nombre="nombre", enlace_manga="enlace_manga", enlace_imagen="enlace_imagen",
                               generos=[Genero("Hentai")], contenido_adulto=True)
        manga = self.proveedor.obtener_manga_detalle(preview)
        self.assertEqual(preview.nombre, manga.nombre)
        self.assertEqual(preview.enlace_manga, manga.enlace)
        self.assertEqual(preview.enlace_imagen, manga.imagen)

    def test_generos_anidadas_al_manga(self):
        manga = self.proveedor.obtener_manga_detalle(self.catalogo[0])
        self.assertEqual(Genero("Hentai"), manga.generos[0])

if __name__ == '__main__':
    unittest.main()
