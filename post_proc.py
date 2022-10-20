from os import pread
import unicodedata
import sys


def extrai_diarios(texto_diario: str):
    texto_diario_slice = pegar_texto_diario_slice(texto_diario)

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

    # Montagem da lista municípios
    lista_municipios = []
    lista_nomes_municipios = []
    qtd_municipios = 0
    municipio = False
    for num_linha, linha in enumerate(texto_diario_slice):
        if linha.startswith("ESTADO DE ALAGOAS"):
            if texto_diario_slice[num_linha + 1].startswith("PREFEITURA MUNICIPAL"):
                lista_municipios.append([])
                lista_nomes_municipios.append(
                    texto_diario_slice[num_linha + 1][24::])
                qtd_municipios += 1
                municipio = True
            if texto_diario_slice[num_linha + 2].startswith("PREFEITURA MUNICIPAL"):
                lista_municipios.append([])
                lista_nomes_municipios.append(
                    texto_diario_slice[num_linha + 2][24::])
                qtd_municipios += 1
                municipio = True

        if municipio:
            lista_municipios[qtd_municipios-1].append(linha)

    # Consolidando partes dos diários onde o texto que faz referência ao município
    # aparece mais de uma vez.
    diarios = {}
    for (nome_municipio, diario) in zip(lista_nomes_municipios, lista_municipios):
        nome_municipio = nome_municipio.strip()
        diarios[nome_municipio] = diarios.get(nome_municipio, []) + diario

    # Inserindo o cabeçalho no diário de cada município.
    for diario in diarios.values():
        diario.insert(0, ama_header + "\n")

    # Transformando o slice diãrio em texto e retornando.
    return {nome_municipio: '\n'.join(diario).rstrip() for nome_municipio, diario in diarios.items()}


def cria_arquivos(nome_arquivo_preffix: str, municipios: dict):
    for nome_municipio, diario in municipios.items():
        nome_arquivo = nome_municipio.strip().lower().replace(" ", "-")
        nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
        nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode("utf-8")
        nome_arquivo = f"{nome_arquivo_preffix}-proc-{nome_arquivo}.txt"
        with open(nome_arquivo, "w") as out_file:
            out_file.write(diario)


def pegar_texto_diario_slice(texto_diario: str):
    texto_diario_slice = texto_diario.lstrip().splitlines()
    return texto_diario_slice


def pegar_cabecalho(texto_diario: str):
    texto_diario_slice = pegar_texto_diario_slice(texto_diario)
    ama_header = texto_diario_slice[0]
    return ama_header


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
