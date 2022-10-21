from cgitb import text
from os import pread
import unicodedata
import sys


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

    # Montagem da lista municípios
    lista_municipios = []
    lista_nomes_municipios = []
    num_linha = 0
    qtd_municipios = -1
    while num_linha < len(texto_diario_slice):
        linha = texto_diario_slice[num_linha].rstrip()

        if linha.startswith("ESTADO DE ALAGOAS"):
            nome, num_linhas_nome = extrai_nome(texto_diario_slice, num_linha)
            if nome != "":
                qtd_municipios += 1
                lista_municipios.append([])
                lista_nomes_municipios.append(nome)

                for i in range(num_linhas_nome):
                    linha = texto_diario_slice[num_linha].rstrip()
                    lista_municipios[qtd_municipios].append(linha)
                    num_linha += 1

                continue

        # Só começa, quando algum muncípio for encontrado.
        if qtd_municipios < 0:
            num_linha += 1
            continue

        # Conteúdo faz parte de um muncípio
        lista_municipios[qtd_municipios].append(linha)
        num_linha += 1

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


def extrai_nome(texto_diario_slice: slice, num_linha: int):
    nome_municipio = ""
    num_linhas_nome = 0
    while True:
        num_linha += 1
        num_linhas_nome += 1
        linha = texto_diario_slice[num_linha].rstrip()

        if linha.startswith("PREFEITURA MUNICIPAL DE") or linha == "": 
            nome_municipio += linha
        else:
            nome_municipio += " " + linha

        # Alarme falso. Não é o início de um diário.
        if linha.startswith("ESTADO DE ALAGOAS") or num_linhas_nome > 5:
            return "", num_linha

        if linha == "":
            proxima = texto_diario_slice[num_linha+1].rstrip()
            if proxima == "":
                nome_municipio = " ".join(nome_municipio.split(" ")[3::])
                return nome_municipio, num_linhas_nome + 2


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
