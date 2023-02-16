# Extrai atos a partir de um arquivo de texto com o texto de um diário municipal.

import sys
import json

import atos
import diario_municipal


class asobject(object):
    def __init__(self, d):
        self.__dict__.update(d)


if __name__ == "__main__":
    # Verificando argumentos passados para o programa.
    if len(sys.argv) < 2:
        print("Usage: python extrair_atos.py <caminho para arquivo com resultado de extração>", file=sys.stderr)
        sys.exit(1)

    path_resultado = sys.argv[1]
    with open(path_resultado, "r", encoding="utf8") as in_file:
        resultados = json.load(in_file)

    res_atos = []
    for res in resultados:
        res = json.loads(res, object_hook=asobject)
        diario = diario_municipal.Diario(diario_municipal.Municipio(
            res.municipio), res.cabecalho, res.texto)
        diario.atos = atos.extrair(res.texto)
        # Removendo o texto para não deixar o arquivo muito grande.
        # Essa informação continua existindo no arquivo resumo-extração.json.
        del diario.texto
        res_atos.append(diario)

    nome_arquivo = path_resultado.replace(
        "-resumo-extracao.json", f"-atos.json")
    with open(nome_arquivo, "w", encoding="utf8") as out_file:
        json.dump(res_atos, out_file, indent=2,
                  default=str, ensure_ascii=False)
