from bs4 import BeautifulSoup

file1 = open("diario-anadia-2022-08-29-extraido.txt", "r")
file2 = open("diario-anadia-2022-08-29-proc.txt", "w")

HTML_DOC = file1.read()
  
def remove_tags(html):
  
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):
        data.decompose()
  
    return ' '.join(soup.stripped_strings)

file2.write(remove_tags(HTML_DOC))