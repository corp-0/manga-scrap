import unittest
import json
from manga_scrap.modelos import JsonSerializable, Manga, Capitulo, Imagen, Genero
from dataclasses import dataclass


@dataclass()
class ObjetoSimple(JsonSerializable):
    campo_str: str
    campo_int: int
    campo_bool: bool

    def __eq__(self, other):
        return (
                self.campo_int == other.campo_int and
                self.campo_str == other.campo_str and
                self.campo_bool == other.campo_bool)


class ObjetoSimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.obj = ObjetoSimple("string", 10, True)
        self.serializado = self.obj.to_json_string()
        self.deserializado = json.loads(self.serializado)

    def test_campo_str(self):
        self.assertEqual("string", self.deserializado.get("campo_str"))

    def test_campo_int(self):
        self.assertEqual(10, self.deserializado.get("campo_int"))

    def test_campo_bool(self):
        self.assertEqual(True, self.deserializado.get("campo_bool"))

    def test_de_json_a_objeto(self):
        self.assertEqual(self.obj, ObjetoSimple(**self.deserializado))


class MangaSerializacionTest(unittest.TestCase):
    esperado = {
        "nombre": "nombre",
        "imagen": "imagen",
        "enlace": "enlace",
        "capitulos": [{
            "nombre": "pepe",
            "enlace": "enlace_capitulo",
            "imagenes": [{
                "enlace": "enlace_imagen"
            }
            ]
        }
        ],
        "generos": [{
            "genero": "Hentai"
        }]
    }

    def setUp(self) -> None:
        img = Imagen("enlace_imagen")
        capitulo = Capitulo("pepe", "enlace_capitulo", [img])
        genero = Genero("Hentai")
        self.manga = Manga("nombre", "imagen", "enlace", [capitulo], [genero])

    def test_manga_serializacion(self):
        self.assertEqual(self.esperado, json.loads(self.manga.to_json_string()))


if __name__ == '__main__':
    unittest.main()
