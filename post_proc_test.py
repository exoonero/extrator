import unittest
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):

    def test_extrai_diarios(self):
        # Novos casos de teste devem ser adicionados na tupla abaixo.
        cases = (
            {
                'desc': 'diario-completo-2022-08-29-extraido.txt',
                'path': 'test_data/diario-completo-2022-08-29-extraido.txt',
                'nomes_municipios': ['ANADIA', 'ARAPIRACA', 'ATALAIA', 'CACIMBINHAS', 'CAJUEIRO', 'CAMPO ALEGRE', 'CANAPI', 'COQUEIRO SECO', 'CRAÍBAS', 'DELMIRO GOUVEIA', 'ESTRELA DE ALAGOAS', 'IBATEGUARA', 'JEQUIÁ DA PRAIA', 'JUNQUEIRO', 'MARAVILHA', 'MARECHAL DEODORO', 'MARIBONDO', 'MESSIAS', 'NOVO LINO', 'OLHO D´AGUA DO CASADO', 'OURO BRANCO', 'PALESTINA', 'PARICONHA', 'PILAR', 'PIRANHAS', 'QUEBRANGULO', 'RIO LARGO', 'SANTANA DO MUNDAÚ', 'SÃO JOSÉ DA LAJE', 'SÃO LUIS DO QUITUNDE', 'TRAIPÚ', 'VIÇOSA', 'MARAGOGI']
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
                    diarios = extrai_diarios(diario.read())
                    self.assertEqual(len(case.nomes_municipios), len(diarios))
                    for municipio in diarios.keys():
                        self.assertIn(municipio, case.nomes_municipios)


class asobject(object):
    def __init__(self, d):
        self.__dict__ = d

if __name__ == '__main__':
    unittest.main()
