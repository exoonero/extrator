from os import pread
import unicodedata
import sys

# Verificando argumentos passados para o programa.
if len(sys.argv) < 2:
    print("Usage: python post_proc.py <caminho para arquivo texto extraído>", file=sys.stderr)
    sys.exit(1)

in_file_name = sys.argv[1]
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
            lista_nomes_municipios.append(in_text_slice[num_linha + 1][24::])
            qtd_municipios += 1
            municipio = True
        if in_text_slice[num_linha + 2].startswith("PREFEITURA MUNICIPAL"):
            lista_municipios.append([])
            lista_nomes_municipios.append(in_text_slice[num_linha + 2][24::])
            qtd_municipios += 1
            municipio = True

    if municipio:
        lista_municipios[qtd_municipios-1].append(linha)
nomes_arquivos = []
preffix = "-".join(in_file_name.split("-")[:-1])
for municipio in lista_nomes_municipios:
    municipio_proc = municipio.strip().lower().replace(" ", "-")
    municipio_proc = unicodedata.normalize(
        'NFKD', municipio_proc).encode('ASCII', 'ignore').decode("utf-8")
    if f"{preffix}-proc-{municipio_proc}.txt" not in nomes_arquivos:
        nomes_arquivos.append(
            f"{preffix}-proc-{municipio_proc}.txt")
dicionario_municipios = {}
for (nome, municipio) in zip(lista_nomes_municipios, lista_municipios):
    chave = nome.strip().lower().replace(" ", "-")
    chave = unicodedata.normalize('NFKD', chave).encode(
        'ASCII', 'ignore').decode("utf-8")

    if chave in dicionario_municipios.keys():
        dicionario_municipios[chave] = dicionario_municipios.get(
            chave) + municipio
    else:
        dicionario_municipios[chave] = municipio
# Inserindo o cabeçalho em cada município
for municipio in lista_municipios:
    municipio.insert(0, ama_header + "\n")

# Escrevendo resultado
for id, chave in zip(nomes_arquivos, dicionario_municipios.keys()):
    fname = id
    with open(fname, "w") as out_file:
        out_file.write('\n'.join(dicionario_municipios.get(chave)))
