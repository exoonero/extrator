in_file = open("diario-anadia-2022-08-29-extraido.txt", "r")
#Mudei o nome da variável out_text para in_text, pois ela não será mais usada como texto de saída.
in_text = in_file.read().lstrip()
in_text = in_text.splitlines()

#Acha o índice da primeira palavra do preâmbulo
def find_initial_id():
    initial_id = 0

    for index, line in enumerate(in_text):
        if "Expediente" in line:
            initial_id = index

    return initial_id             

def generate_text():
    final_text = ""
    for linha in range(len(in_text)):
        if in_text[linha] != "":
            final_text += in_text[linha] + "\n"
    return final_text

def delete_lines(min,max):
    for linha in range(len(in_text)):
        if linha >= min and linha <=max:
            in_text[linha] = in_text[linha].replace(in_text[linha], "")

def create_file(final_text):
    out_file = open("diario-anadia-2022-08-29-proc.txt", "w")
    out_file.write(final_text)
    out_file.close()

#chamadas
delete_lines(find_initial_id(), 53)
create_file(generate_text())
print(generate_text().splitlines())