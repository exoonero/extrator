import unittest
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        cases = (
            {
                'desc': 'diario-completo-2022-08-29-extraido.txt',
                'path': 'test_data/diario-completo-2022-08-29-extraido.txt',
                'nomes_municipios': ['ANADIA', 'ARAPIRACA', 'ATALAIA', 'CACIMBINHAS', 'CAJUEIRO', 'CAMPO ALEGRE', 'CANAPI', 'COQUEIRO SECO', 'CRAÍBAS', 'DELMIRO GOUVEIA', 'ESTRELA DE ALAGOAS', 'IBATEGUARA', 'JEQUIÁ DA PRAIA', 'JUNQUEIRO', 'MARAVILHA', 'MARECHAL DEODORO', 'MARIBONDO', 'MESSIAS', 'NOVO LINO', 'OLHO D´AGUA DO CASADO', 'OURO BRANCO', 'PALESTINA', 'PARICONHA', 'PILAR', 'PIRANHAS', 'QUEBRANGULO', 'RIO LARGO', 'SANTANA DO MUNDAÚ', 'SÃO JOSÉ DA LAJE', 'SÃO LUIS DO QUITUNDE', 'TRAIPÚ', 'VIÇOSA', 'MARAGOGI'],
                'header': 'Alagoas , 29 de Agosto de 2022 • Diário Oficial dos Municípios do Estado de Alagoas • ANO IX | Nº 1869'
            },
            {
                'desc': 'diario-completo-2022-07-20-extraido.txt',
                'path': 'test_data/diario-completo-2022-07-20-extraido.txt',
                'nomes_municipios': ['ARAPIRACA', 'ATALAIA', 'BARRA DE SÃO MIGUEL', 'BRANQUINHA', 'CACIMBINHAS', 'CAMPO ALEGRE', 'CANAPI', 'CARNEIROS', 'COQUEIRO SECO', 'DELMIRO GOUVEIA', 'DOIS RIACHOS', 'FELIZ DESERTO', 'INHAPI', 'JOAQUIM GOMES', 'LAGOA DA CANOA', 'MARAGOGI', 'MARAVILHA', 'MARECHAL DEODORO', 'MATA GRANDE', 'MESSIAS', 'MINADOR DO NEGRÃO', "OLHO D´AGUA DO CASADO", "OLHO D'ÁGUA DAS FLORES", 'PÃO DE AÇÚCAR', 'PARICONHA', 'PILAR', 'PINDOBA', 'PIRANHAS', 'PORTO CALVO', 'PORTO REAL DO COLÉGIO', 'QUEBRANGULO', 'RIO LARGO', 'SANTA LUZIA DO NORTE', 'SANTANA DO MUNDAÚ', 'SÃO JOSÉ DA TAPERA', 'SÃO MIGUEL DOS MILAGRES', "TANQUE D'ARCA", 'TAQUARANA', 'TEOTÔNIO VILELA', 'VIÇOSA']
            },
        )

        for case in cases:
            case = asobject(case)
            with self.subTest(case.desc):
                with open(case.path, "r") as diario:
                    # Teste Quantidade de Municípios
                    diario_extraido = diario.read()
                    diarios = extrai_diarios(diario_extraido)
                    self.assertEqual(len(case.nomes_municipios), len(diarios))
                    # Teste Nome dos Municípios
                    for municipio in diarios.keys():
                        self.assertIn(municipio, case.nomes_municipios)
                    # Teste Cabeçalho
                    cabecalho_esperado = case.header.replace(" ", "")
                    for municipio in diarios.values():
                        cabecalho_extraido = municipio.lstrip().splitlines()[
                            0].replace(" ", "")
                        self.assertIn(cabecalho_esperado, cabecalho_extraido)


class asobject(object):
    def __init__(self, d):
        self.__dict__ = d


if __name__ == '__main__':
    unittest.main()
