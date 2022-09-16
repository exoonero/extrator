in_file = open("diario-anadia-2022-08-29-extraido.txt", "r")
#Mudei o nome da variável out_text para in_text, pois ela não será mais usada como texto de saída.
in_text = in_file.read().lstrip()
in_text = in_text.splitlines()

#Função que retorna o índice da primeira palavra do preâmbulo
def find_initial_id():
    initial_id = 0
    for index, line in enumerate(in_text):
        if "Expediente" in line:
            initial_id = index
    return initial_id        

#Função que retorna o índice da última palavra do preâmbulo
def find_last_id():
    last_id = 0
    for index, line in enumerate(in_text):
        if "gestão municipal" in line:
            last_id = index
    return last_id        

#Função que gera o texto linha a linha
def generate_text():
    final_text = ""
    for linha in range(len(in_text)):
        if in_text[linha] != "":
            final_text += in_text[linha] + "\n"
    return final_text

#Função responsável por remover o preâmbulo
#a função recebe como parâmetro o índice da primeira palavra
#e o índice da última palavra. Por fim, substitui as linhas do preâmbulo por strings vazias
def delete_lines(min, max):
    for linha in range(len(in_text)):
        if linha >= min and linha <= max:
            in_text[linha] = in_text[linha].replace(in_text[linha], "")

#Função que escreve em um arquivo de saída a partir do texto final
def create_file(final_text):
    out_file = open("diario-anadia-2022-08-29-proc.txt", "w")
    out_file.write(final_text)
    out_file.close()

#chamada das funções
delete_lines(find_initial_id(), find_last_id())
create_file(generate_text())
print(generate_text().splitlines())
    
