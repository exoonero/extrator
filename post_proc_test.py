import json
import unittest
import re
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        # Deve ser adicionado um arquivo -test.json para cada texto extraído (caso de teste)
        cases = ('test_data/diario-completo-2022-01-03-test.json',
                 'test_data/diario-completo-2022-08-29-test.json',
                 'test_data/diario-completo-2022-08-15-test.json',
                 'test_data/diario-completo-2022-07-20-test.json',
                 'test_data/diario-completo-2022-02-14-test.json',
                 'test_data/diario-completo-2021-04-01-test.json',
                 'test_data/diario-completo-2021-03-29-test.json',
                 'test_data/diario-completo-2020-06-29-test.json',
                 'test_data/diario-completo-2020-05-14-test.json',
                 'test_data/diario-completo-2019-08-14-test.json',
                 'test_data/diario-completo-2019-07-02-test.json',   
                 'test_data/diario-completo-2018-10-02-test.json',    
                 'test_data/diario-completo-2014-06-23-test.json',          
                 'test_data/test_eleitoral/diario-completo-2016-10-14-test.json',
                 )
        for case_path in cases:
            with open(case_path, 'r') as f:
                case = asobject(json.load(f))

            with self.subTest(case.desc):
                with open(case.path, "r") as diario:
                    # Teste Quantidade de Municípios
                    diario_extraido = diario.read()
                    diarios = extrai_diarios(diario_extraido)
                    municipios_esperados = list(case.cods.keys())
                    municipios_obtidos = list(diarios.keys())
                    self.assertListEqual(municipios_esperados, municipios_obtidos, f'Caso: {case.desc}\nEsperado:{municipios_esperados}\nObtido:{municipios_obtidos}')
                    for municipio, diario in diarios.items():
                        # Teste Cabeçalho
                        self.assertEqual(
                            case.cabecalho, diario.splitlines()[0])

                        # Verifica se todos os atos foram corretamente extraídos
                        expected_cods = case.cods.get(municipio, [])
                        cods_in_text = re.findall(
                            r'Código Identificador:(.*)', diario)
                        self.assertListEqual(
                            expected_cods, cods_in_text, f'Município: {municipio}\nDiário:{diario}')


class asobject(object):
    def __init__(self, d):
        self.__dict__ = d


if __name__ == '__main__':
    unittest.main()
