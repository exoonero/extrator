import re
import sys
import unicodedata
from cgitb import text
from os import pread

# No final do regex, existe uma estrutura condicional que verifica se o próximo match é um \s ou SECRETARIA. Isso foi feito para resolver um problema no diário de 2018-10-02, em que o município de Coité do Nóia não foi percebido pelo código.
re_nomes_municipios = (
    r"ESTADO DE ALAGOAS \n{0,2}PREFEITURA MUNICIPAL DE (.*\n{0,2}.*$)\n\s(?:\s|SECRETARIA)")


def extrai_diarios(texto_diario: str):
    texto_diario_slice = texto_diario.lstrip().splitlines()

    # Processamento
    linhas_apagar = []  # slice de linhas a ser apagadas ao final.
    ama_header = texto_diario_slice[0]
    ama_header_count = 0
    codigo_count = 0
    codigo_total = texto_diario.count("Código Identificador")

    for num_linha, linha in enumerate(texto_diario_slice):
        # Remoção do cabeçalho AMA, porém temos que manter a primeira aparição.
        if linha.startswith(ama_header):
            ama_header_count += 1
            if ama_header_count > 1:
                linhas_apagar.append(num_linha)

        # Remoção das linhas finais
        if codigo_count == codigo_total:
            linhas_apagar.append(num_linha)
        elif linha.startswith("Código Identificador"):
            codigo_count += 1

    # Apagando linhas do slice
    texto_diario_slice = [l for n, l in enumerate(
        texto_diario_slice) if n not in linhas_apagar]

    # Inserindo o cabeçalho no diário de cada município.
    diarios = {}
    nomes_municipios = re.findall(
        re_nomes_municipios, texto_diario, re.MULTILINE)
    for municipio in nomes_municipios:
        diarios[municipio.strip().replace('\n', '')] = ama_header + '\n'

    num_linha = 0
    municipio_atual = None
    while num_linha < len(texto_diario_slice):
        linha = texto_diario_slice[num_linha].rstrip()

        if linha.startswith("ESTADO DE ALAGOAS"):
            nome = nome_municipio(texto_diario_slice, num_linha)
            if nome is not None:
                municipio_atual = nome

        # Só começa, quando algum muncípio for encontrado.
        if municipio_atual is None:
            num_linha += 1
            continue

        # Conteúdo faz parte de um muncípio
        diarios[municipio_atual] += linha + '\n'
        num_linha += 1

    return diarios


def cria_arquivos(nome_arquivo_preffix: str, municipios: dict):
    for nome_municipio, diario in municipios.items():
        nome_arquivo = nome_municipio.strip().lower().replace(" ", "-")
        nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
        nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode("utf-8")
        nome_arquivo = f"{nome_arquivo_preffix}-proc-{nome_arquivo}.txt"
        with open(nome_arquivo, "w") as out_file:
            out_file.write(diario)


def nome_municipio(texto_diario_slice: slice, num_linha: int):
    texto = '\n'.join(texto_diario_slice[num_linha:num_linha+10])
    match = re.findall(re_nomes_municipios, texto, re.MULTILINE)
    if len(match) > 0:
        return match[0].strip().replace('\n', '')
    return None


if __name__ == "__main__":
    # Verificando argumentos passados para o programa.
    if len(sys.argv) < 2:
        print("Usage: python post_proc.py <caminho para arquivo texto extraído>", file=sys.stderr)
        sys.exit(1)

    path_texto_diario = sys.argv[1]
    texto_diario = ""
    with open(path_texto_diario, "r") as in_file:
        texto_diario = in_file.read()

    diarios = extrai_diarios(texto_diario)
    # Usando como chave os nomes dos arquivos gerados, que são  baseado no prefixo
    # extraído do arquivo extraído e nos nomes dos municípios.
    prefixo = "-".join(path_texto_diario.split("-")[:-1])
    cria_arquivos(prefixo, diarios)
