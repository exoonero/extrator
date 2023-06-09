import json
import glob
import os

os.makedirs("./docs/site/dados/inicial", exist_ok=True)
os.makedirs("./docs/site/dados/municipio", exist_ok=True)

# Dicionário que guarda dados para renderização da página inicial.
inicial = {}
municipio = {}
geral = {
    "detalhe": {},
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
            mes = int(data_quebrada[1])
            dia = int(data_quebrada[2])

            # Atualizando seção de detalhes do municipio
            dado_municipio = inicial.get(id_municipio, {})
            detalhe = dado_municipio.get("detalhe", {})
            detalhe_ano = detalhe.get(ano, {})
            detalhe_ano["num_diarios"] = detalhe_ano.get("num_diarios", 0) + 1
            for ato in diario["atos"]:
                ato = json.loads(ato)
                detalhe_ano["num_nomeacoes"] = detalhe_ano.get(
                    "num_nomeacoes", 0) + len(ato["cpf_nomeacoes"])
                detalhe_ano["num_exoneracoes"] = detalhe_ano.get(
                    "num_exoneracoes", 0) + len(ato["cpf_exoneracoes"])
            detalhe[ano] = detalhe_ano

            inicial[id_municipio] = {
                "id": id_municipio,
                "nome": nome_municipio,
                "detalhe": detalhe,
            }

            dado_municipio_mes = municipio.get(id_municipio, {})
            dado_municipio_mes[ano] = dado_municipio_mes.get(ano, {})
            dado_municipio_mes[ano][mes] = dado_municipio_mes[ano].get(mes, {})
            dado_municipio_mes[ano][mes]["num_diarios"] = dado_municipio_mes[ano][mes].get("num_diarios", 0) + 1
            for ato in diario["atos"]:
                ato = json.loads(ato)
                dado_municipio_mes[ano][mes]["num_nomeacoes"] = dado_municipio_mes[ano][mes].get(
                    "num_nomeacoes", 0) + len(ato["cpf_nomeacoes"])
                dado_municipio_mes[ano][mes]["num_exoneracoes"] = dado_municipio_mes[ano][mes]["num_exoneracoes"] = dado_municipio_mes[ano][mes].get(
                    "num_exoneracoes", 0) + len(ato["cpf_exoneracoes"])
            municipio[id_municipio] = {
                "id": id_municipio,
                "nome": nome_municipio,
                ano: dado_municipio_mes[ano]
            }

            # Atualizando seção de detalhes geral.
            detalhe_geral = geral.get("detalhe", {})
            detalhe_geral_ano = detalhe_geral.get(ano, {})
            detalhe_geral_ano["num_diarios"] = detalhe_geral_ano.get(
                "num_diarios", 0) + 1
            detalhe_geral_ano["num_nomeacoes"] = detalhe_geral_ano.get(
                "num_nomeacoes", 0) + detalhe_ano.get("num_nomeacoes", 0)
            detalhe_geral_ano["num_exoneracoes"] = detalhe_geral_ano.get(
                "num_exoneracoes", 0) + detalhe_ano.get("num_exoneracoes", 0)
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
        num_diarios += detalhe["num_diarios"]
        num_exoneracoes += detalhe.get("num_exoneracoes", 0)
        num_nomeacoes += detalhe.get("num_nomeacoes", 0)

    inicial[id_municipio]["resumo"] = {
        "num_diarios": num_diarios,
        "num_exoneracoes": num_exoneracoes,
        "num_nomeacoes": num_nomeacoes,
    }

# Salvando dados para renderização da página inicial.
for id_municipio, dado in inicial.items():
    with open(f"./docs/site/dados/inicial/{id_municipio}-inicial.json", "w", encoding="utf-8") as json_file:
        json.dump(dado, json_file, indent=2, default=str, ensure_ascii=False)

# Salvando dados para renderização da página do municipio.
for id_municipio, dado in municipio.items():
    with open(f"./docs/site/dados/municipio/{id_municipio}.json", "w", encoding="utf-8") as json_file:
        json.dump(dado, json_file, indent=2, default=str, ensure_ascii=False)