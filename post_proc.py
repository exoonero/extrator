in_file = open("diario-anadia-2022-08-29-extraido.txt", "r")
# Mudei o nome da variável out_text para in_text, pois ela não será mais usada como texto de saída.
in_text = in_file.read().lstrip()
in_text = in_text.splitlines()

# Função que remove o preâmbulo a partir dos índices da primeira e última palavra contida no preâmbulo


def remove_preamble():
    initial_id = 0
    last_id = 0
    for index, line in enumerate(in_text):
        if "Expediente" in line:
            initial_id = index
            break
    for index, line in enumerate(in_text):
        if "gestão municipal" in line:
            last_id = index
            break
    for line in range(len(in_text)):
        if line >= initial_id and line <= last_id:
            in_text[line] = in_text[line].replace(in_text[line], "")

# Função que gera o texto linha a linha


def generate_text():
    final_text = ""
    for linha in range(len(in_text)):
        if in_text[linha] != "":
            final_text += in_text[linha] + "\n"
    return final_text


# Função que escreve em um arquivo de saída a partir do texto final


def create_file(final_text):
    out_file = open("diario-anadia-2022-08-29-proc.txt", "w")
    out_file.write(final_text)
    out_file.close()


# chamada das funções
remove_preamble()
create_file(generate_text())
print(generate_text().splitlines())
