in_file = open("diario-2-municipios-2022-08-29-extraido.txt", "r")
in_text = in_file.read().lstrip()
in_text_slice = in_text.splitlines()
listaMunicipios = []
linhas_apagar = []  # slice de linhas a ser apagadas ao final.
ama_header = in_text_slice[0].split()[0]
ama_header_count = 0
codigo_count = 0
codigo_total = in_text.count("Código Identificador")
preambulo = False
verificaMunicipio = linha.startswith("ESTADO DE ALAGOAS") and in_text_slice[num_linha+1].startswith("PREFEITURA MUNICIPAL")
for num_linha, linha in enumerate(in_text_slice):
    if verificaMunicipio:
        #Arrumar uma forma de que para cada município presente no texto extraído, crie-se uma nova lista.
        pass


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


# Escrevendo resultado
out_file = open("diario-anadia-2022-08-29-proc.txt", "w")

out_file.write(out_text)
out_file.close()
