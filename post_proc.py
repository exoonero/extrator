from bs4 import BeautifulSoup

in_file = open("diario-anadia-2022-08-29-extraido.txt", "r")
html = BeautifulSoup(in_file.read(), "html.parser")  

out_file = open("diario-anadia-2022-08-29-proc.txt", "w")
out_file.write(html.get_text())
out_file.close()