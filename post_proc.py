from os import pread
import unicodedata
import sys
# Verificando argumentos passados para o programa.
if len(sys.argv) < 2:
    print("Usage: python post_proc.py <caminho para arquivo texto extraído>", file=sys.stderr)
    sys.exit(1)


def processar(path: str, gerarArquivos: bool):

    in_file_name = path
    in_file = open(in_file_name, "r")
    in_text = in_file.read().lstrip()
    in_text_slice = in_text.splitlines()

    # Processamento
    linhas_apagar = []  # slice de linhas a ser apagadas ao final.
    ama_header = in_text_slice[0]
    ama_header_count = 0
    codigo_count = 0
    codigo_total = in_text.count("Código Identificador")

    for num_linha, linha in enumerate(in_text_slice):
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
    in_text_slice = [l for n, l in enumerate(
        in_text_slice) if n not in linhas_apagar]
    out_text = '\n'.join(in_text_slice)

    # Montagem da lista municípios
    lista_municipios = []
    lista_nomes_municipios = []
    qtd_municipios = 0
    municipio = False
    for num_linha, linha in enumerate(in_text_slice):
        if linha.startswith("ESTADO DE ALAGOAS"):
            if in_text_slice[num_linha + 1].startswith("PREFEITURA MUNICIPAL"):
                lista_municipios.append([])
                lista_nomes_municipios.append(
                    in_text_slice[num_linha + 1][24::])
                qtd_municipios += 1
                municipio = True
            if in_text_slice[num_linha + 2].startswith("PREFEITURA MUNICIPAL"):
                lista_municipios.append([])
                lista_nomes_municipios.append(
                    in_text_slice[num_linha + 2][24::])
                qtd_municipios += 1
                municipio = True

        if municipio:
            lista_municipios[qtd_municipios-1].append(linha)

    # Consolidando partes dos diários onde o texto que faz referência ao município
    # aparece mais de uma vez.
    # Usando como chave os nomes dos arquivos gerados, que são  baseado no prefixo
    # extraído do arquivo extraído e nos nomes dos municípios.
    nome_arquivo_preffix = "-".join(in_file_name.split("-")[:-1])
    diarios = {}
    # Diário que será retornado a partir dessa função
    diarioSaida = {}
    for (nome_municipio, diario) in zip(lista_nomes_municipios, lista_municipios):
        nome_arquivo = nome_municipio.strip().lower().replace(" ", "-")
        nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
        nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode("utf-8")
        diarioSaida[nome_arquivo] = diarioSaida.get(nome_arquivo, []) + diario
        nome_arquivo = f"{nome_arquivo_preffix}-proc-{nome_arquivo}.txt"
        diarios[nome_arquivo] = diarios.get(nome_arquivo, []) + diario

    # Inserindo o cabeçalho no diário de cada município.
    for (diariosElemento, diarioSaidaElemento) in zip(diarios.values(), diarioSaida.values()):
        diariosElemento.insert(0, ama_header + "\n")
        diarioSaidaElemento.insert(0, ama_header + "\n")
    if gerarArquivos == True:
        # Escrevendo resultado.
        for arquivo, diario in diarios.items():
            with open(arquivo, "w") as out_file:
                out_file.write('\n'.join(diario))
    return diarioSaida


processar(sys.argv[1], True)
