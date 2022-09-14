# Pra remover os espaços em branco, lstript

in_file = open("diario-anadia-2022-08-29-extraido.txt", "r")
out_file_text = in_file.read().lstrip()
out_file = open("diario-anadia-2022-08-29-proc.txt", "w")
out_file.write(out_file_text)
out_file.close()
    