import json
import glob
import os
import pandas as pd

os.makedirs("./docs/site/dados", exist_ok=True)

# Dicionário que guarda dados para renderização da página inicial.
inicial = {}
geral = {
    "detalhe": {},
    "ranking_nomeacoes": {},
    "ranking_exoneracoes": {}
}

for path in glob.glob("./data/diarios/*-atos.json"):
    with open(path, encoding="utf-8") as json_file:
        diarios = json.load(json_file)

        for diario in diarios:
            diario = json.loads(diario)
            id_municipio = diario["id"]
            nome_municipio = diario["municipio"]

            data_quebrada = diario["data_publicacao"].split("-")
            ano = int(data_quebrada[0])
            mes = int(data_quebrada[1])  # para uso futuro
            dia = int(data_quebrada[2])  # para uso futuro

            # Atualizando seção de detalhes do municipio
            dado_municipio = inicial.get(id_municipio, {})
            detalhe = dado_municipio.get("detalhe", {})
            detalhe_ano = detalhe.get(ano, {})
            detalhe_ano_resumo = detalhe_ano.get("resumo", {})
            detalhe_ano_mes = detalhe_ano.get(mes, {})
            detalhe_ano_resumo["num_diarios"] = detalhe_ano_resumo.get(
                "num_diarios", 0) + 1
            detalhe_ano_mes["num_diarios"] = detalhe_ano_mes.get(
                "num_diarios", 0) + 1
            for ato in diario["atos"]:
                ato = json.loads(ato)
                detalhe_ano_resumo["num_nomeacoes"] = detalhe_ano_resumo.get(
                    "num_nomeacoes", 0) + len(ato["cpf_nomeacoes"])

                detalhe_ano_resumo["num_exoneracoes"] = detalhe_ano_resumo.get(
                    "num_exoneracoes", 0) + len(ato["cpf_exoneracoes"])
                detalhe_ano_mes["num_nomeacoes"] = detalhe_ano_mes.get(
                    "num_nomeacoes", 0) + len(ato["cpf_nomeacoes"])

                detalhe_ano_mes["num_exoneracoes"] = detalhe_ano_mes.get(
                    "num_exoneracoes", 0) + len(ato["cpf_exoneracoes"])

            detalhe_ano[mes] = detalhe_ano_mes
            detalhe[ano] = detalhe_ano
            detalhe_ano["resumo"] = detalhe_ano_resumo
            nome_municipio = nome_municipio.title()
            nome_municipio = nome_municipio.replace(" De ", " de ")
            nome_municipio = nome_municipio.replace(" Da ", " da ")
            nome_municipio = nome_municipio.replace(" Do ", " do ")
            inicial[id_municipio] = {
                "id": id_municipio,
                "nome": nome_municipio,
                "detalhe": detalhe,
            }

            # Atualizando seção de detalhes geral.
            detalhe_geral = geral.get("detalhe", {})
            detalhe_geral_ano = detalhe_geral.get(ano, {
                "resumo": {
                    "num_diarios": 0,
                    "num_nomeacoes": 0,
                    "num_exoneracoes": 0
                }
            })
            detalhe_geral_ano_mes = detalhe_geral_ano.get(mes, {
                "num_diarios": 0,
                "num_nomeacoes": 0,
                "num_exoneracoes": 0,
            })

            detalhe_geral_ano_mes["num_diarios"] += 1
            for ato in diario["atos"]:
                ato = json.loads(ato)
                detalhe_geral_ano_mes["num_nomeacoes"] += len(ato["cpf_nomeacoes"])
                detalhe_geral_ano_mes["num_exoneracoes"] += len(ato["cpf_exoneracoes"])
                detalhe_geral_ano["resumo"]["num_nomeacoes"] += len(ato["cpf_nomeacoes"])
                detalhe_geral_ano["resumo"]["num_exoneracoes"] += len(ato["cpf_exoneracoes"])
            
            detalhe_geral_ano["resumo"]["num_diarios"] += 1
                
            
            detalhe_geral_ano[mes] = detalhe_geral_ano_mes
            detalhe_geral[ano] = detalhe_geral_ano

            inicial["geral"] = {
                "id": "geral",
                "detalhe": detalhe_geral,
            }

# Atualizando seção de resumo
for id_municipio, dado in inicial.items():
    num_diarios = 0
    num_exoneracoes = 0
    num_nomeacoes = 0
    for ano, detalhe in dado["detalhe"].items():
        resumo = detalhe.get("resumo", {})
        num_diarios += resumo.get("num_diarios", 0)
        num_exoneracoes += resumo.get("num_exoneracoes", 0)
        num_nomeacoes += resumo.get("num_nomeacoes", 0)

    inicial[id_municipio]["resumo"] = {
        "num_diarios": num_diarios,
        "num_exoneracoes": num_exoneracoes,
        "num_nomeacoes": num_nomeacoes,
    }


# Analisando municípios que mais nomearam e exoneraram
def top5(arg):
    df = pd.DataFrame.from_dict(inicial, orient='index')
    df = df[df['id'] != 'geral']
    df = df.sort_values(by=['resumo'], ascending=False,
                        key=lambda x: x.str.get(arg))
    top_4 = df.head(4)
    ranking = {}
    municipios = []
    for index, (municipio, row) in enumerate(top_4.iterrows()):
        ranking[index+1] = {
            "nome": row["nome"],
            "num": row['resumo'][arg]
        }
        municipios.append(municipio)
    outros = df[4:]['resumo'].apply(lambda x: x[arg]).sum()
    ranking[5] = {
        "nome": "Outros",
        "num": int(outros) 
    }
    
    return ranking

inicial['geral']['ranking_nomeacoes'] = top5("num_nomeacoes")
inicial['geral']['ranking_exoneracoes'] = top5(
    "num_exoneracoes")
# Salvando dados para renderização da página inicial.
for id_municipio, dado in inicial.items():
    with open(f"./docs/site/dados/{id_municipio}.json", "w", encoding="utf-8") as json_file:
        json.dump(dado, json_file, indent=2, default=str, ensure_ascii=False)
