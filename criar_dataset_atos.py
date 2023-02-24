import json
import glob
import os.path
import zipfile

records = []
for path in glob.glob("data/diarios/*-atos.json"):
    with open(path) as json_file:
        # remove conteúdo desnecessário para a análise.
        # transforma json strings em dicts python para facilitar manipulação.
        # cria estrutura própria para manipulação dos dados.
        diarios = json.load(json_file)
        for diario in diarios:
            diario = json.loads(diario)
            data_quebrada = diario["data_publicacao"].split("-")
            for ato in diario["atos"]:
                ato = json.loads(ato)

                # adicionando campos para facilitar a análise.
                record = {}
                record["municipio"] = diario["id"]
                record["cod"] = ato["cod"]
                record["possui_nomeacoes"] = ato["possui_nomeacoes"]
                record["possui_exoneracoes"] = ato["possui_exoneracoes"]
                record["num_nomeacoes"] = len(ato["cpf_nomeacoes"])
                record["num_exoneracoes"] = len(ato["cpf_exoneracoes"])
                record["ano"] = int(data_quebrada[0])
                record["mes"] = int(data_quebrada[1])
                record["dia"] = int(data_quebrada[2])
                records.append(record)

with zipfile.ZipFile("df.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
    df_json = json.dumps(records, indent=2, default=str, ensure_ascii=False)
    zip_file.writestr("df.json", df_json)
    zip_file.testzip()
