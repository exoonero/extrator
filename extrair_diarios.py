import json
import sys
from diario_ama import extrair_diarios_municipais


def cria_arquivos(nome_arquivo_preffix: str, diarios: dict):
    for diario in diarios:
        nome_arquivo = f"{nome_arquivo_preffix}-proc-{diario.id}.txt"
        with open(nome_arquivo, "w", encoding='utf-8') as out_file:
            out_file.write(diario.texto)


if __name__ == "__main__":
    # Verificando argumentos passados para o programa.
    if len(sys.argv) < 2:
        print("Usage: python extrair_diarios.py <caminho para arquivo texto extraído>", file=sys.stderr)
        sys.exit(1)

    path_texto_diario = sys.argv[1]
    texto_diario = ""
    with open(path_texto_diario, "r", encoding='utf-8') as in_file:
        texto_diario = in_file.read()

    diarios = extrair_diarios_municipais(texto_diario)
    # Usando como chave os nomes dos arquivos gerados, que são  baseado no prefixo
    # extraído do arquivo extraído e nos nomes dos municípios.
    prefixo = "-".join(path_texto_diario.split("-")[:-1])
    cria_arquivos(prefixo, diarios)

    nome_arquivo = f"{prefixo}-resumo-extracao.json"
    with open(nome_arquivo, "w", encoding='utf-8') as out_file:
        json.dump(diarios, out_file, indent=2, default=str, ensure_ascii=False)
