# Extrai atos a partir de um arquivo de texto com o texto de um diário municipal.

import sys
import json

import diario_municipal


if __name__ == "__main__":
    # Verificando argumentos passados para o programa.
    if len(sys.argv) < 2:
        print("Usage: python extrair_atos.py <caminho para arquivo texto com diário municipal>", file=sys.stderr)
        sys.exit(1)

    path_texto_diario = sys.argv[1]
    with open(path_texto_diario, "r") as in_file:
        texto_diario = in_file.read()

    diario = diario_municipal.Diario.do_texto(texto_diario)
    diario.extrai_atos()
    diario_serializado = json.dumps(diario.__dict__, indent=2, ensure_ascii=False, default=str)

    # Usando como chave os nomes dos arquivos gerados, que são  baseado no prefixo
    # extraído do arquivo extraído e nos nomes dos municípios.
    prefixo = "-".join(path_texto_diario.split("-")[:-1])
    prefixo = prefixo.replace("-proc", "") # removendo sufixo "-proc" do nome do arquivo.
    nome_arquivo = f"{prefixo}-atos-{diario.id}.txt"
    with open(nome_arquivo, "w") as out_file:
        out_file.write(diario_serializado)
