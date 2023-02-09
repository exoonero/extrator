# Extrai atos a partir de um arquivo de texto com o texto de um diário municipal.

import sys
import json

import diario_municipal


if __name__ == "__main__":
    # Verificando argumentos passados para o programa.
    if len(sys.argv) < 2:
        print("Usage: python extrair_atos.py <caminho para arquivo texto com diário municipal>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r") as in_file:
        texto_diario = in_file.read()

    diario = diario_municipal.Diario.do_texto(texto_diario)
    diario.extrai_atos()
    print(json.dumps(diario.__dict__, indent=2, ensure_ascii=False, default=str))
