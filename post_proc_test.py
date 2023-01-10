import json
import unittest
import re
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        # Deve ser adicionado um arquivo -test.json para cada texto extraído (caso de teste)
        cases = (
            'test_data/diario-completo-2022-01-03-test.json',
            'test_data/diario-completo-2022-08-15-test.json',
            'test_data/diario-completo-2022-08-29-test.json',
            'test_data/diario-completo-2022-07-20-test.json',
            'test_data/diario-completo-2022-02-14-test.json',
            'test_data/diario-completo-2021-04-01-test.json',
            'test_data/diario-completo-2021-03-29-test.json',
            'test_data/diario-completo-2020-12-16-test.json',
            'test_data/diario-completo-2020-10-30-test.json',
            'test_data/diario-completo-2020-10-15-test.json',
            'test_data/diario-completo-2020-10-01-test.json',
            'test_data/diario-completo-2020-06-29-test.json',
            'test_data/diario-completo-2020-05-14-test.json',
            'test_data/diario-completo-2020-04-27-test.json',
            'test_data/diario-completo-2019-08-14-test.json',
            'test_data/diario-completo-2019-07-05-test.json',
            'test_data/diario-completo-2019-07-02-test.json',
            'test_data/diario-completo-2018-09-28-test.json',
            'test_data/diario-completo-2018-10-02-test.json',
            'test_data/diario-completo-2017-12-28-test.json',
            'test_data/diario-completo-2017-11-13-test.json',
            'test_data/diario-completo-2017-10-25-test.json',
            'test_data/diario-completo-2016-10-14-test.json',
            'test_data/diario-completo-2016-10-28-test.json',
            'test_data/diario-completo-2016-02-15-test.json',
            'test_data/diario-completo-2016-01-04-test.json',
            'test_data/diario-completo-2015-04-02-test.json',
            'test_data/diario-completo-2015-03-26-test.json',
            'test_data/diario-completo-2014-06-23-test.json',
            'test_data/diario-completo-2014-05-20-test.json',
        )
        for case_path in cases:
            with open(case_path, 'r') as f:
                case = json.load(f, object_hook=asobject)

            with self.subTest(case.desc):
                with open(case.path, "r") as diario_ama:
                    diarios_extraidos = extrai_diarios(diario_ama.read())

                # Verifica se os municípios foram extraídos corretamente.
                municipios_esperados = [
                    diario.municipio for diario in case.diarios]
                municipios_obtidos = [
                    diario.municipio for diario in diarios_extraidos]
                self.assertListEqual(
                    municipios_esperados,
                    municipios_obtidos,
                    f'Caso: {case.desc}\nEsperado:{municipios_esperados}\nObtido:{municipios_obtidos}')

                # Checando diários e atos.
                for diario_esperado in case.diarios:
                    diario_obtido = get_diario(
                        diario_esperado.municipio, diarios_extraidos)

                    # Teste Cabeçalho
                    self.assertEqual(case.cabecalho, diario_obtido.cabecalho)

                    # Verifica se todos os atos foram corretamente extraídos
                    self.assertListEqual(
                        [ato.cod for ato in diario_esperado.atos],
                        [ato.cod for ato in diario_obtido.atos],
                        f'Caso: {case.desc}\nMunicípio: {diario_esperado.municipio}')


def get_diario(municipio: str, diarios: slice):
    for diario in diarios:
        if diario.municipio == municipio:
            return diario
    return None


class asobject(object):
    def __init__(self, d):
        self.__dict__.update(d)


if __name__ == '__main__':
    unittest.main()
