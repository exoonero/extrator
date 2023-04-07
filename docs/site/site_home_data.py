import json
import glob
import os

lista_diarios = []
contagem_diarios = {}
for path in glob.glob("data/diarios/*-resumo-extracao.json"):
    with open(path, encoding="utf-8") as json_file:
        diarios = json.load(json_file)
        for diario in diarios:
            diario = json.loads(diario)
            data_str = os.path.basename(path).split('-resumo')[0]
            data = data_str.split("-")
            ano, mes, dia = int(data[0]), int(data[1]), int(data[2])
            # Json que será transformado em arquivo
            dict_diario = {}
            municipio = diario["municipio"]
            id = diario["id"]
            dict_diario["id"] = id
            dict_diario["nome"] = municipio
            if id not in contagem_diarios:
                contagem_diarios[id] = {}
            if (ano, mes) not in contagem_diarios[id]:
                contagem_diarios[id][(ano, mes)] = 0
            contagem_diarios[id][(ano, mes)] += 1
            dict_diario["detalhe"] = {
                "ano": ano,
                "mes": mes,
                "dia": dia,
                "diarios": {},
                "atos": {},
                "nomeacoes": {},
                "exoneracoes": {}
            }
            lista_diarios.append(dict_diario)

diarios_por_id = {}
for diario in lista_diarios:
    municipio = diario["id"]
    ano, mes, dia = diario["detalhe"]["ano"], diario["detalhe"]["mes"], diario["detalhe"]["dia"]
    diario["detalhe"]["diarios"]["qtd-diarios"] = contagem_diarios[municipio][(
        ano, mes)]
    if municipio not in diarios_por_id:
        diarios_por_id[municipio] = {"id": municipio, "nome": diario["nome"], "detalhe": []}
    diarios_por_id[municipio]["detalhe"].append(diario["detalhe"])

os.makedirs('./docs/site/diarios/2022', exist_ok=True)

for (id, diarios) in diarios_por_id.items():
    total_ano = sum(
        [contagem for _, contagem in contagem_diarios[id].items()])
    total_meses = {mes: contagem for (
        _, mes), contagem in contagem_diarios[id].items()}
    media_diarios_mes = total_ano / len(total_meses)
    info_total = {
        "resumo": {
            "total_diarios_ano": total_ano,
            "total_diarios_meses": total_meses,
            "media_diarios_mes": media_diarios_mes
        }
    }
    with open(f"./docs/site/diarios/2022/{id}-inicial.json", "w", encoding="utf-8") as json_file:
        json.dump({**diarios, **info_total}, json_file,
                  indent=2, default=str, ensure_ascii=False)