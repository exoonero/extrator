import unittest
import re
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        cases = (
            {
                'desc': 'diario-completo-2022-08-29-extraido.txt',
                'path': 'test_data/diario-completo-2022-08-29-extraido.txt',
                'nomes_municipios': ['ANADIA', 'ARAPIRACA', 'ATALAIA', 'CACIMBINHAS', 'CAJUEIRO', 'CAMPO ALEGRE', 'CANAPI', 'COQUEIRO SECO', 'CRAÍBAS', 'DELMIRO GOUVEIA', 'ESTRELA DE ALAGOAS', 'IBATEGUARA', 'JEQUIÁ DA PRAIA', 'JUNQUEIRO', 'MARAVILHA', 'MARECHAL DEODORO', 'MARIBONDO', 'MESSIAS', 'NOVO LINO', 'OLHO D´AGUA DO CASADO', 'OURO BRANCO', 'PALESTINA', 'PARICONHA', 'PILAR', 'PIRANHAS', 'QUEBRANGULO', 'RIO LARGO', 'SANTANA DO MUNDAÚ', 'SÃO JOSÉ DA LAJE', 'SÃO LUIS DO QUITUNDE', 'TRAIPÚ', 'VIÇOSA', 'MARAGOGI'],
                'cabecalho': 'Alagoas , 29 de Agosto de 2022   •   Diário Oficial dos Municípios do Estado de Alagoas   •    ANO IX | Nº 1869 ',
                'cods': {
                    'ANADIA': ['8D821A99', '9AB247D4', '3AE50C8E'],
                    'ARAPIRACA': ['3731993F', '64A3F55C', 'D784B299'],
                    'ATALAIA': ['E03D1FD1'],
                    'CACIMBINHAS': ['E6F5EDF8', '078D352E'],
                    'CAJUEIRO': ['C51B4AA5'],
                    'CAMPO ALEGRE': ['A9F1CC02',
                                     '812AF7A3',
                                     '46C01B82',
                                     '7BB0DCCD',
                                     '84C8A919',
                                     '5426CF94',
                                     'ADADC4D8',
                                     'ADFAE3F4',
                                     '1F46C28F',
                                     '213A26A4'],
                    'CANAPI': [],
                    'COQUEIRO SECO': [],
                    'CRAÍBAS': [],
                    'DELMIRO GOUVEIA': [],
                    'ESTRELA DE ALAGOAS': [],
                    'IBATEGUARA': [],
                    'JEQUIÁ DA PRAIA': [],
                    'JUNQUEIRO': [],
                    'MARAVILHA': [],
                    'MARECHAL DEODORO': [],
                    'MARIBONDO': [],
                    'MESSIAS': [],
                    'NOVO LINO': [],
                    'OLHO D´AGUA DO CASADO': [],
                    'OURO BRANCO': [],
                    'PALESTINA': [],
                    'PARICONHA': [],
                    'PILAR': [],
                    'PIRANHAS': [],
                    'QUEBRANGULO': [],
                    'RIO LARGO': [],
                    'SANTANA DO MUNDAÚ': [],
                    'SÃO JOSÉ DA LAJE': [],
                    'SÃO LUIS DO QUITUNDE': [],
                    'TRAIPÚ': [],
                    'VIÇOSA': [],
                    'MARAGOGI': [],
                },
            },
            {
                'desc': 'diario-completo-2022-07-20-extraido.txt',
                'path': 'test_data/diario-completo-2022-07-20-extraido.txt',
                'nomes_municipios': ['ARAPIRACA', 'ATALAIA', 'BARRA DE SÃO MIGUEL', 'BRANQUINHA', 'CACIMBINHAS', 'CAMPO ALEGRE', 'CANAPI', 'CARNEIROS', 'COQUEIRO SECO', 'DELMIRO GOUVEIA', 'FELIZ DESERTO', 'INHAPI', 'JOAQUIM GOMES', 'LAGOA DA CANOA', 'MARAGOGI', 'MARAVILHA', 'MARECHAL DEODORO', 'MATA GRANDE', 'MESSIAS', 'MINADOR DO NEGRÃO', "OLHO D'ÁGUA DAS FLORES", "OLHO D´AGUA DO CASADO", 'PÃO DE AÇÚCAR', 'PARICONHA', 'PILAR', 'PINDOBA', 'PIRANHAS', 'PORTO CALVO', 'PORTO REAL DO COLÉGIO', 'QUEBRANGULO', 'RIO LARGO', 'SANTA LUZIA DO NORTE', 'SANTANA DO MUNDAÚ', 'SÃO JOSÉ DA TAPERA', 'SÃO MIGUEL DOS MILAGRES', "TANQUE D´ARCA", 'TAQUARANA', 'TEOTONIO VILELA', 'VIÇOSA', 'DOIS RIACHOS'],
                'cabecalho': 'Alagoas , 20 de Julho de 2022   •   Diário Oficial dos Municípios do Estado de Alagoas   •    ANO IX | Nº 1841 ',
                'cods': {

                },
            },
        )

        for case in cases:
            case = asobject(case)
            with self.subTest(case.desc):
                with open(case.path, "r") as diario:
                    # Teste Quantidade de Municípios
                    diario_extraido = diario.read()
                    diarios = extrai_diarios(diario_extraido)
                    self.assertEqual(len(case.nomes_municipios),
                                     len(list(diarios.keys())))

                    for municipio, diario in diarios.items():
                        # Teste Nome dos Municípios
                        self.assertIn(municipio, case.nomes_municipios)

                        # Teste Cabeçalho
                        self.assertEqual(
                            case.cabecalho, diario.splitlines()[0])

                        # Verifica se todos os atos foram corretamente extraídos
                        expected_cods = case.cods.get(municipio, [])
                        cods_in_text = re.findall(
                            r'Código Identificador:(.*)', diario)
                        self.assertListEqual(expected_cods, cods_in_text, f'Município: {municipio}')


class asobject(object):
    def __init__(self, d):
        self.__dict__ = d


if __name__ == '__main__':
    unittest.main()
