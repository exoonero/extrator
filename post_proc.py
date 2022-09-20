in_file = open("diario-anadia-2022-08-29-extraido.txt", "r")
in_text = in_file.read().lstrip()
in_text = in_text.splitlines()
ama_header_words = in_text[0].split()
ama_header_id = ama_header_words[0]


def generate_text():
    final_text = ""
    for linha in range(len(in_text)):
        final_text += in_text[linha] + "\n"
    return final_text


def delete_header():
    for linha in range(len(in_text)):
        if linha == 0:
            continue
        if in_text[linha].startswith(ama_header_id):
            in_text[linha] = in_text[linha].replace(in_text[linha], "")


def create_file(final_text):
    out_file = open("diario-anadia-2022-08-29-proc.txt", "w")
    out_file.write(final_text)
    out_file.close()


# chamadas
delete_header()
create_file(generate_text())
