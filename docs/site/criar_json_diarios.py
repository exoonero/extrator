import json
import glob
import os
from collections import defaultdict

lista_diarios = []
contagem_mensal = defaultdict(lambda: defaultdict(int))

for path in glob.glob("data/diarios/*-resumo-extracao.json"):
    with open(path, encoding="utf-8") as json_file:
        diarios = json.load(json_file)
        for diario in diarios:
            diario = json.loads(diario)
            data_str = os.path.basename(path).split('-resumo')[0]
            data = data_str.split("-")
            ano, mes, dia = int(data[0]), int(data[1]), int(data[2])
            municipio = diario["municipio"]
            contagem_mensal[municipio][(ano, mes)] += 1
            dict_diario = {}
            dict_diario["municipio"] = municipio
            # ALEX: Podemos adicionar o texto no json desmarcando essa linha
            # dict_diario["texto"] = diario["texto"]
            dict_diario["ano"] = ano
            dict_diario["mes"] = mes
            dict_diario["dia"] = dia
            lista_diarios.append(dict_diario)

for dict_diario in lista_diarios:
    municipio = dict_diario["municipio"]
    ano, mes = dict_diario["ano"], dict_diario["mes"]
    dict_diario["quantidade-diarios"] = contagem_mensal[municipio][(ano, mes)]

os.makedirs('./docs/site/diarios', exist_ok=True)

with open(f"./docs/site/diarios/{ano}.json", "w", encoding="utf-8") as json_file:
    json.dump(lista_diarios, json_file, indent=2, default=str, ensure_ascii=False)