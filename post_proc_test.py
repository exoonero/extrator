import json
import unittest
import re
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        # Deve ser adicionado um arquivo -test.json para cada texto extraído (caso de teste)
        cases = (
            'test_data/diario-completo-2022-08-29-test.json',
            'test_data/diario-completo-2022-07-20-test.json',
        )

        for case_path in cases:
            with open(case_path, 'r') as f:
                case = asobject(json.load(f))

            with self.subTest(case.desc):
                with open(case.path, "r") as diario:

                    # Teste Quantidade de Municípios
                    diario_extraido = diario.read()
                    diarios = extrai_diarios(diario_extraido)
                    self.assertListEqual(list(case.cods.keys()), list(diarios.keys()))

                    for municipio, diario in diarios.items():
                        # Teste Cabeçalho
                        self.assertEqual(
                            case.cabecalho, diario.splitlines()[0])

                        # Verifica se todos os atos foram corretamente extraídos
                        expected_cods = case.cods.get(municipio, [])
                        cods_in_text = re.findall(
                            r'Código Identificador:(.*)', diario)
                        self.assertListEqual(
                            expected_cods, cods_in_text, f'Município: {municipio}')


class asobject(object):
    def __init__(self, d):
        self.__dict__ = d


if __name__ == '__main__':
    unittest.main()
