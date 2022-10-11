import unicodedata

in_file = open("diario-completo-2022-08-29-extraido.txt", "r")
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
for municipio in lista_nomes_municipios:
    municipio_proc = municipio.strip().lower().replace(" ", "-")
    municipio_proc = unicodedata.normalize('NFKD', municipio_proc).encode('ASCII', 'ignore').decode("utf-8")
    nomes_arquivos.append(
        f"diario-completo-2022-08-29-proc-{municipio_proc}.txt")

# Inserindo o cabeçalho em cada município
for municipio in lista_municipios:
    municipio.insert(0, ama_header + "\n")
# Escrevendo resultado
for id, linhas in enumerate(lista_municipios):
    fname = nomes_arquivos[id]
    with open(fname, "w") as out_file:
        out_file.write('\n'.join(linhas))
