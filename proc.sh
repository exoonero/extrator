#!/bin/bash

# Importante para depurar a execução do script
set -x
set -e

echo "Fazendo pull da imagem do Apache Tika 1.28.4"
sudo docker pull apache/tika:1.28.4

echo "Executando imagem do Apache Tika 1.28.4"
sudo docker run -d -p 9998:9998 --rm --name tika apache/tika:1.28.4

echo "Esperando Apache Tika iniciar"
sleep 30

# O parâmetro passado é o diretório onde estão os arquivos a serem processados.
# Assumiremos que o diretório contém um arquivo com o mesmo nome, porém com a extensão .pdf.
echo "Convertendo PDF para texto"
curl \
-H "Accept: text/plain" -H "Content-Type: application/pdf" \
-T $1/$1.pdf \
http://localhost:9998/tika > $1/$1-extraido.txt

echo "Parando imagem do Apache Tika 1.28.4"
sudo docker stop tika

echo "Executando Processamento do texto extraído"
python3 post_proc.py $1/$1-extraido.txt
