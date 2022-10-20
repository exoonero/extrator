import unittest
from post_proc import extrai_diarios


class PostProcTest(unittest.TestCase):
    def setUp(self):
        global texto_diario
        path_2022_08_29 = 'test_data/diario-completo-2022-08-29-extraido.txt'
        with open(path_2022_08_29, "r") as in_file:
            texto_diario = in_file.read()

    def test_qtd_municipios_2022_08_29(self):
        self.assertEqual(33, len(extrai_diarios(
            texto_diario)))

    def test_nomes_municipios_2022_08_29(self):
        nomes = [
            'Anadia', 'Arapiraca', 'Atalaia', 'Cacimbinhas', 'Cajueiro', 'Campo Alegre', 'Canapi', 'Coqueiro Seco', 'Craíbas', 'Delmiro Gouveia', 'Estrela de Alagoas', 'Ibateguara', 'Jequiá da Praia', 'Junqueiro', 'Maravilha', 'Marechal Deodoro', 'Maribondo', 'Messias', 'Novo Lino', 'Olho D´agua do Casado', 'Ouro Branco', 'Palestina', 'Pariconha', 'Pilar', 'Piranhas', 'Quebrangulo', 'Rio Largo', 'Santana do Mundaú', 'São José da Laje', 'São Luis do Quitunde', 'Traipú', 'Viçosa', 'Maragogi'
        ]
        for nome, chave in zip(nomes, extrai_diarios(texto_diario).keys()):
            nome = nome.upper()
            self.assertEqual(nome, chave.rstrip())


if __name__ == '__main__':
    unittest.main()
