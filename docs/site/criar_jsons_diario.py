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
            dict_diario["nome"] = municipio
            if municipio not in contagem_diarios:
                contagem_diarios[municipio] = {}
            if (ano, mes) not in contagem_diarios[municipio]:
                contagem_diarios[municipio][(ano, mes)] = 0
            contagem_diarios[municipio][(ano, mes)] += 1
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

diarios_por_nome = {}
for diario in lista_diarios:
    municipio = diario["nome"]
    ano, mes, dia = diario["detalhe"]["ano"], diario["detalhe"]["mes"], diario["detalhe"]["dia"]
    diario["detalhe"]["diarios"]["qtd-diarios"] = contagem_diarios[municipio][(
        ano, mes)]
    if municipio not in diarios_por_nome:
        diarios_por_nome[municipio] = []
    diarios_por_nome[municipio].append(diario)

os.makedirs('./docs/site/diarios', exist_ok=True)
for nome, diarios in diarios_por_nome.items():
    total_ano = sum(
        [contagem for _, contagem in contagem_diarios[nome].items()])
    total_meses = {mes: contagem for (
        _, mes), contagem in contagem_diarios[nome].items()}
    info_total = {
        "total_ano": total_ano,
        "total_meses": total_meses
    }
    with open(f"./docs/site/diarios/{nome}.json", "w", encoding="utf-8") as json_file:
        json.dump(diarios + [info_total], json_file, indent=2,
                  default=str, ensure_ascii=False)
