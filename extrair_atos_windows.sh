#!/bin/bash

set -x  # debug
set -e  # exit on error

ROOT_DIR=${PWD}
DATA_DIR=${ROOT_DIR}/data
DOWNLOAD_DIR=${DATA_DIR}/diarios

cd ${DOWNLOAD_DIR}

for resultado in `dir -a *-resumo-extracao.json`
do
    python ${ROOT_DIR}/extrair_atos.py ${resultado}
done