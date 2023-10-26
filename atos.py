import json
import re


def extrair(texto_diario: str):
    atos = []
    matches = re.findall(
        r"^[\s\S]*?Código Identificador:.*$(?:\n|)", texto_diario, re.MULTILINE)
    for match in matches:
        atos.append(AtoNormativo(match.strip()))
    return atos


class AtoNormativo:
    # Exceções notáveis (nomeações):
    # String: "Ficam nomeados", município Santa Luzia do Norte, 04/01/2021, ato 8D9E57A4
    # String: "nomeação do Conselho", município Piranhas, 04/01/2021, ato F12265E5
    # String: "nomear,", município Coruripe, 15/01/2021, ato EC041157
    re_nomeacoes = r"(Nomear|NOMEAR|nomear,|nomeação do Conselho|Ficam nomeados|CONVOCA os candidatos aprovados e nomeados|APROVADO e NOMEADO|Art.1º. NOMEAÇÃO|ficam nomeados)( |,|)"

    # Exceções notáveis (exonerações):
    # String: "Ficam exonerados", município São José da Taoera, 02/01/2023, ato 49D56711
    # String: "^Exonera", município Inhapi, 27/04/2020, ato 1BFBFDDB
    re_exoneracoes = r"(Exonerar|EXONERAR|Exonera|Ficam exonerados|RESOLVE EXONERAR)( |,|)"

    # Exceções notáveis:
    # Possui um CPF inválido, município Maragogi, 10/02/2018, ato 7C2C6663
    # Possui um CPF inválido, 060-478.934-30, município Maragogi, 02/01/2023, ato 99658F02
    # String: \*\*\*, município Maragogi, 15/08/2022, ato 2E57C952
    # String: –, município Pão de Açúcar, 02/01/2023, ato C7917E25
    # Erro de digitação do padrão cpf: 616.676668 – 00, município Pão de Açúcar, 02/01/2023, ato C7917E25. Solução na regex: (?:.|)
    # Erro de digitação do padrão cpf: 030-969-544-96, município Jacaré dos Homens, 29/01/2021, ato 31EA193A.
    re_cpf = r"((?:\*{3}|\d{3}(?:-|))(?:\d{3}|\*{3})(?:\*{3}|(?:-|)\d{3})-\d{2})"

    def __init__(self, texto: str):
        self.texto = texto
        self.cod = self._extrai_cod(texto)
        self.possui_nomeacoes = self._possui_nomeacoes()
        self.cpf_nomeacoes = []
        self.cpf_exoneracoes = []
        self.possui_exoneracoes = self._possui_exoneracoes()
        if self.possui_exoneracoes or self.possui_nomeacoes:
            self._extrai_cpf()

    def _extrai_cod(self, texto: str):
        matches = re.findall(r'Código Identificador:(.*)', texto)
        return matches[0].strip()

    def _possui_nomeacoes(self):
        return re.search(self.re_nomeacoes, self.texto) is not None

    def _possui_exoneracoes(self):
        return re.search(self.re_exoneracoes, self.texto) is not None

    def _extrai_cpf(self):
        # Limpeza do texto. Removemos quebras de linha, espaços, pontos e a parte final do texto.
        novo_texto = re.sub(
            r"\n|\s|\.|\,|(Registre-se, publique-se e cumpra-se.[\s\S]*)", "", self.texto)
        
        # 2023-01-02, ato C7917E25, município Pão de Açúcar usou caracter U+2013 ("En Dash") ao invés de hifen
        novo_texto = novo_texto.replace("–", "-")

        # Dividimos o texto de nomeações e exonerações a partir das regexps. Daí buscamos os CPFs de cada uma das partes.
        # Essa estratégia é muito importante para resolver os casos de municípios que possuem nomeações e
        # exonerações no mesmo ato.
        texto_nomeacoes = ""
        texto_exoneracoes = ""
        for texto in re.split(self.re_nomeacoes, novo_texto):
            if re.search(self.re_exoneracoes, texto) is not None:
                texto_exoneracoes += texto
            else:
                texto_nomeacoes += texto

        # Buscando e limpando os CPFs.
        cpf_nomeacoes = re.findall(self.re_cpf, texto_nomeacoes)
        cpf_exoneracoes = re.findall(self.re_cpf, texto_exoneracoes)

        # Aplicando a regex para remover hifens extras nos CPFs encontrados
        regexhifen = r'(\d{3})-?(\d{3})-?(\d{3})-?(\d{2})'
        substitution = r'\1\2\3-\4'
        
        self.cpf_nomeacoes = [re.sub(regexhifen, substitution, cpf) for cpf in cpf_nomeacoes]
        self.cpf_exoneracoes = [re.sub(regexhifen, substitution, cpf) for cpf in cpf_exoneracoes]
        for i in range(len(self.cpf_nomeacoes)):
            self.cpf_nomeacoes[i] = f"{self.cpf_nomeacoes[i][0:3]}.{self.cpf_nomeacoes[i][3:6]}.{self.cpf_nomeacoes[i][6:8]}{self.cpf_nomeacoes[i][8:12]}"
        for i in range(len(self.cpf_exoneracoes)):
            self.cpf_exoneracoes[i] = f"{self.cpf_exoneracoes[i][0:3]}.{self.cpf_exoneracoes[i][3:6]}.{self.cpf_exoneracoes[i][6:8]}{self.cpf_exoneracoes[i][8:12]}"

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)
