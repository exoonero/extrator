in_file = open("diario-2-municipios-2022-08-29-extraido.txt", "r")
in_text = in_file.read().lstrip()
in_text_slice = in_text.splitlines()
# Montagem da lista municípios
listaMunicipios = []
qtdMunicipios = 0
aux = 0
municipio = False
for num_linha, linha in enumerate(in_text_slice):
    if linha.startswith("ESTADO DE ALAGOAS") and in_text_slice[num_linha+1].startswith("PREFEITURA MUNICIPAL"):
        listaMunicipios.append([])
        qtdMunicipios += 1
        municipio = True
    if municipio:
        listaMunicipios[qtdMunicipios-1].append(linha)
print(listaMunicipios)
# Processamento
linhas_apagar = []  # slice de linhas a ser apagadas ao final.
ama_header = in_text_slice[0]
ama_header_count = 0
codigo_count = 0
codigo_total = in_text.count("Código Identificador")
preambulo = False

# TODO(alex): O código está desatualizado
# Precisamos corrigir esse código para lidar com a matriz de conteúdo de arquivos
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

    # Remoção das linhas do preâmbulo
    if "Expediente" in linha:
        preambulo = True
    if preambulo:
        linhas_apagar.append(num_linha)
    if "gestão municipal" in linha:
        preambulo = False


# Apagando linhas do slice
out_text_slice = [l for n, l in enumerate(
    in_text_slice) if n not in linhas_apagar]
out_text = '\n'.join(out_text_slice)
qtdArquivos = 0
# Escrevendo resultado
for id, linhas in enumerate(listaMunicipios):
    fname = f"diario-2-municipios-arquivo{id}-2022-08-29-proc.txt"
    with open(fname, "w") as out_file:
        out_file.write('\n'.join(linhas))
