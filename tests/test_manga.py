import unittest
from manga_scrap.modelos import Manga, Capitulo, Imagen
from manga_scrap.excepciones import NoExisteCapitulo

class TestManga(unittest.TestCase):
    def setUp(self) -> None:
        img = Imagen("enlace_imagen")
        capitulo = Capitulo("pepe", "enlace_capitulo", [img])
        self.manga = Manga("nombre", "imagen", "enlace", [capitulo])


    def test_contador_capitulos(self):
        self.assertEqual(1, self.manga.n_capitulos)

    def test_contador_imagenes(self):
        self.assertEqual(1, self.manga.n_imagenes)

    def test_consulta_cap_no_levanta_NoExisteCapitulo(self):
        try:
            self.manga.obtener_capitulo(0)
        except NoExisteCapitulo:
            self.fail()

    def test_consulta_cap_fuera_de_lista_levanta_NoExisteCapitulo(self):
        with self.assertRaises(NoExisteCapitulo):
            self.manga.obtener_capitulo(10)


if __name__ == '__main__':
    unittest.main()
