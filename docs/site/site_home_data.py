import json
import glob
import os

contagem_diarios = {}
municipios = {}
for path in glob.glob("data/diarios/*-resumo-extracao.json"):
    with open(path, encoding="utf-8") as json_file:
        diarios = json.load(json_file)
        for diario in diarios:
            diario = json.loads(diario)
            data_str = os.path.basename(path).split('-resumo')[0]
            ano, mes = map(int, data_str.split("-")[:2])
            id = diario["id"]
            municipios[id] = diario["municipio"]
            if id not in contagem_diarios:
                contagem_diarios[id] = {}
            if (ano, mes) not in contagem_diarios[id]:
                contagem_diarios[id][(ano, mes)] = 0
            contagem_diarios[id][(ano, mes)] += 1

diarios_por_id = {}
for id, contagem in contagem_diarios.items():
    total_ano = sum(contagem.values())
    media_diarios_mes = total_ano / len(contagem)
    info_total = {
        "id": id,
        "nome": municipios[id],
        "resumo": {
            "total_diarios_ano": total_ano,
            "media_diarios_mes": media_diarios_mes
        },
        "detalhe": [
            {
                'ano': ano,
                'mes': mes,
                'diarios': {'qtd-diarios': qtd},
                'atos': {},
                'nomeacoes': {},
                'exoneracoes': {}
            } for (ano, mes), qtd in contagem.items()
        ]
    }
    diarios_por_id[id] = info_total

os.makedirs('./docs/site/diarios/2022', exist_ok=True)

for (id, diarios) in diarios_por_id.items():
    with open(f"./docs/site/diarios/2022/{id}-inicial.json", "w", encoding="utf-8") as json_file:
        json.dump(diarios, json_file, indent=2, default=str, ensure_ascii=False)