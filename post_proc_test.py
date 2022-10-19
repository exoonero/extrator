import unittest
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_qtd_municipios_2022_08_29(self):
        self.assertEqual(33, len(extrai_diarios(
            'diario-completo-2022-08-29/diario-completo-2022-08-29-extraido.txt')))


if __name__ == '__main__':
    unittest.main()
