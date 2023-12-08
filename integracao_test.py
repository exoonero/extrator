import json
import re
import unittest

from diario_ama import extrair_diarios_municipais
import atos

# Combinando duas partes importantes desse projeto em apenas um teste para
# simplificar as coisas. Nesse teste checamos se os diários municipais são
# extraídos corretamente e se os atos são extraídos de cada diário corretamente.


class IntegracaoTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        # Deve ser adicionado um arquivo -test.json para cada texto extraído (caso de teste)
        cases = (
            'test_data/diario-completo-2019-09-11-test.json',
            'test_data/diario-completo-2020-08-14-test.json',
            'test_data/diario-completo-2022-10-07-test.json',
            'test_data/diario-completo-2019-11-08-test.json',
            'test_data/diario-completo-2020-11-30-test.json',
            'test_data/diario-completo-2020-07-22-test.json',
            'test_data/diario-completo-2023-09-08-test.json',
            'test_data/diario-completo-2023-10-20-test.json',
            'test_data/diario-completo-2022-03-31-test.json',
            'test_data/diario-completo-2023-08-02-test.json',
            'test_data/diario-completo-2023-07-20-test.json',
            'test_data/diario-completo-2023-03-17-test.json',
            'test_data/diario-completo-2023-10-04-test.json',
            'test_data/diario-completo-2023-03-16-test.json',
            'test_data/diario-completo-2023-01-26-test.json',
            'test_data/diario-completo-2023-01-02-test.json',
            'test_data/diario-completo-2022-01-03-test.json',
            'test_data/diario-completo-2022-03-22-test.json',
            'test_data/diario-completo-2022-10-31-test.json',
            'test_data/diario-completo-2022-08-15-test.json',
            'test_data/diario-completo-2022-08-29-test.json',
            'test_data/diario-completo-2022-07-20-test.json',
            'test_data/diario-completo-2023-08-28-test.json',
            'test_data/diario-completo-2022-02-14-test.json',
            'test_data/diario-completo-2022-01-06-test.json',
            'test_data/diario-completo-2021-04-01-test.json',
            'test_data/diario-completo-2021-03-29-test.json',
            'test_data/diario-completo-2021-01-29-test.json',
            'test_data/diario-completo-2021-04-27-test.json',
            'test_data/diario-completo-2021-12-01-test.json',
            'test_data/diario-completo-2021-01-15-test.json',
            'test_data/diario-completo-2020-12-16-test.json',
            'test_data/diario-completo-2020-10-30-test.json',
            'test_data/diario-completo-2020-10-15-test.json',
            'test_data/diario-completo-2020-10-01-test.json',
            'test_data/diario-completo-2020-01-21-test.json',
            'test_data/diario-completo-2020-06-29-test.json',
            'test_data/diario-completo-2020-05-14-test.json',
            'test_data/diario-completo-2020-04-27-test.json',
            'test_data/diario-completo-2019-11-14-test.json',
            'test_data/diario-completo-2019-10-25-test.json',
            'test_data/diario-completo-2019-10-15-test.json',
            'test_data/diario-completo-2019-08-14-test.json',
            'test_data/diario-completo-2019-07-05-test.json',
            'test_data/diario-completo-2019-07-02-test.json',
            'test_data/diario-completo-2019-05-16-test.json',
            'test_data/diario-completo-2018-09-05-test.json',
            'test_data/diario-completo-2019-11-28-test.json',
            'test_data/diario-completo-2018-09-28-test.json',
            'test_data/diario-completo-2018-10-26-test.json',
            'test_data/diario-completo-2018-10-17-test.json',
            'test_data/diario-completo-2018-10-03-test.json',
            'test_data/diario-completo-2018-10-02-test.json',
            'test_data/diario-completo-2018-03-02-test.json',
            'test_data/diario-completo-2018-02-20-test.json',
            'test_data/diario-completo-2017-12-28-test.json',
            'test_data/diario-completo-2017-11-13-test.json',
            'test_data/diario-completo-2017-10-25-test.json',
            'test_data/diario-completo-2017-05-26-test.json',
            'test_data/diario-completo-2016-10-14-test.json',
            'test_data/diario-completo-2016-10-28-test.json',
            'test_data/diario-completo-2016-08-02-test.json',
            'test_data/diario-completo-2016-02-15-test.json',
            'test_data/diario-completo-2016-01-04-test.json',
            'test_data/diario-completo-2015-09-10-test.json',
            'test_data/diario-completo-2015-04-02-test.json',
            'test_data/diario-completo-2015-03-26-test.json',
            'test_data/diario-completo-2014-06-23-test.json',
            'test_data/diario-completo-2014-05-20-test.json',
            'test_data/diario-completo-2021-04-23-test.json',
        )
        for case_path in cases:
            with open(case_path, 'r') as f:
                try:
                    case = json.load(f, object_hook=asobject)
                except json.decoder.JSONDecodeError as err:
                    self.fail(f'Erro ao carregar o arquivo {case_path}: {err}')

            with self.subTest(case.desc):
                with open(case.path, "r") as diario_ama:
                    diarios_extraidos = extrair_diarios_municipais(
                        diario_ama.read())

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

                    diario_obtido.atos = atos.extrair(diario_obtido.texto)

                    # Teste Cabeçalho
                    self.assertEqual(case.cabecalho, diario_obtido.cabecalho)

                    # Verifica se todos os atos foram corretamente extraídos
                    for ato_esperado, ato_obtido in zip(diario_esperado.atos, diario_obtido.atos):
                        try:
                            self.assertEqual(ato_esperado.cod, ato_obtido.cod,
                                             f'Caso: {case.desc}\nMunicípio: {diario_esperado.municipio}')
                            self.assertEqual(ato_esperado.nomeacoes > 0, ato_obtido.possui_nomeacoes,
                                             f'Caso: {case.desc}\nMunicípio: {diario_esperado.municipio}\nAto: {ato_obtido.cod}\nTexto:{ato_obtido.texto}')
                            self.assertEqual(ato_esperado.cpf_nomeacoes, ato_obtido.cpf_nomeacoes,
                                             f'Caso: {case.desc}\nMunicípio: {diario_esperado.municipio}\nAto: {ato_obtido.cod}\nTexto:{ato_obtido.texto}')
                            self.assertEqual(ato_esperado.exoneracoes > 0, ato_obtido.possui_exoneracoes,
                                             f'Caso: {case.desc}\nMunicípio: {diario_esperado.municipio}\nAto: {ato_obtido.cod}\nTexto:{ato_obtido.texto}')
                            self.assertEqual(ato_esperado.cpf_exoneracoes, ato_obtido.cpf_exoneracoes,
                                             f'Caso: {case.desc}\nMunicípio: {diario_esperado.municipio}\nAto: {ato_obtido.cod}\nTexto:{ato_obtido.texto}')
                        except AttributeError as err:
                            self.fail(
                                f'Erro ao acessar objeto {case_path} ato {ato_obtido.cod}: {err}')


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
