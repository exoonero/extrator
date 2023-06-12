import json
import glob
import os

os.makedirs("./docs/site/dados", exist_ok=True)

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
            detalhe_ano_mes = detalhe_ano.get(mes, {})
            detalhe_ano_mes["num_diarios"] = detalhe_ano_mes.get("num_diarios", 0) + 1
            for ato in diario["atos"]:
                ato = json.loads(ato)
                detalhe_ano_mes["num_nomeacoes"] = detalhe_ano_mes.get(
                    "num_nomeacoes", 0) + len(ato["cpf_nomeacoes"])
                detalhe_ano_mes["num_exoneracoes"] = detalhe_ano_mes.get(
                    "num_exoneracoes", 0) + len(ato["cpf_exoneracoes"])
            detalhe_ano[mes] = detalhe_ano_mes
            detalhe[ano] = detalhe_ano

            inicial[id_municipio] = {
                "id": id_municipio,
                "nome": nome_municipio,
                "detalhe": detalhe,
            }

# Atualizando seção de resumo
for id_municipio, dado in inicial.items():
    num_diarios = 0
    num_exoneracoes = 0
    num_nomeacoes = 0

    for ano, detalhe in dado["detalhe"].items():
        for mes, mes_detalhe in detalhe.items():
            num_diarios += mes_detalhe["num_diarios"]
            num_exoneracoes += mes_detalhe.get("num_exoneracoes", 0)
            num_nomeacoes += mes_detalhe.get("num_nomeacoes", 0)

    inicial[id_municipio]["resumo"] = {
        "num_diarios": num_diarios,
        "num_exoneracoes": num_exoneracoes,
        "num_nomeacoes": num_nomeacoes,
    }

# Salvando dados para renderização da página inicial.
for id_municipio, dado in inicial.items():
    with open(f"./docs/site/dados/{id_municipio}.json", "w", encoding="utf-8") as json_file:
        json.dump(dado, json_file, indent=2, default=str, ensure_ascii=False)