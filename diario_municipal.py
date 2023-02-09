import re
import unicodedata
from datetime import date

import atos


class Municipio:

    def __init__(self, municipio):
        municipio = municipio.rstrip().replace('\n', '')  # limpeza inicial
        self.id = self._computa_id(municipio)
        self.nome = municipio

    def _computa_id(self, nome_municipio):
        ret = nome_municipio.strip().lower().replace(" ", "-")
        ret = unicodedata.normalize('NFKD', ret)
        ret = ret.encode('ASCII', 'ignore').decode("utf-8")
        return ret

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Diario:

    _mapa_meses = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12,
    }

    def __init__(self, municipio: Municipio, cabecalho: str, texto: str):
        self.municipio = municipio.nome
        self.id = municipio.id
        self.cabecalho = cabecalho
        self.texto = texto.rstrip()
        self.data_publicacao = self._extrai_data_publicacao(cabecalho)
        self.atos = []

    @classmethod
    def do_texto(self, texto: str):
        '''Constrói um objeto Diario, inferindo os campos a partir de um texto de um diário municipal.'''
        municipio = Diario._extrai_municipio(texto)
        cabecalho = texto.splitlines()[0]
        diario = Diario(municipio, cabecalho, texto)
        return diario

    def extrai_atos(self):
        self.atos = atos.extrair(self.texto)

    def _extrai_data_publicacao(self, ama_header: str):
        match = re.findall(
            r".*(\d{2}) de (\w*) de (\d{4})", ama_header, re.MULTILINE)[0]
        mes = Diario._mapa_meses[match[1]]
        return date(year=int(match[2]), month=mes, day=int(match[0]))

    @classmethod
    def _extrai_municipio(self, texto: str):
        re_nome_municipio = (
            r"ESTADO DE ALAGOAS\n{1,2}PREFEITURA MUNICIPAL DE (.*\n{0,2}.*$)\n\s(?:\s|SECRETARIA)")
        return Municipio(re.findall(re_nome_municipio, texto, re.MULTILINE)[0])

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
