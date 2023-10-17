
<h1 align="center">
  <br>
  <a href="https://exoonero.org"><img src="https://exoonero.org/favicon.ico" alt="Exoonero logo" width="200"></a>
  <br>
  Exoonero - Extrator
  <br>
</h1>

<h4 align="center">Extrator das nomeações e exonerações de Alagoas e segmentador dos diários e atos do <a href="https://www.diariomunicipal.com.br/ama/" target="_blank">Diário Oficial AMA</a>.</h4>

<p align="center">
    <img src="https://img.shields.io/badge/python-%230095D5.svg?&style=for-the-badge&logo=python&logoColor=white"/>
</p>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#fluxo-de-processamento">Fluxo de Processamento</a> •
  <a href="#como-usar">Como Usar</a> •
  <a href="#testes">Testes</a> 
</p>

## Sobre

O projeto tem como principal objetivo coletar, transformar em texto e separar em municípios os diários oficiais municipais da Associação dos Municípios Alagoanos (AMA). Além da separação do conteúdo por município, o texto do diário de cada ente estadual é separado em atos normativos. Também iremos utilizar algoritmos computacionais para classificar e extrair informações dos atos normativos dos diários de cada município. Mais especificamente, o nosso foco será em nomeações e exonerações.

## Fluxo de Processamento

![image](https://github.com/exoonero/extrator/assets/89322317/853fc4e4-c44c-4557-a59b-cd6152a4b825)<br>
### Manual
```
PDF de Diário -> Apache Tika -> Arquivo Extraído -> extrair_diarios.py -> Arquivo(s) Processados dos Diários -> extrair_atos.py -> Arquivo(s) Processados dos Atos de um Diário.
```
### Automático
```
./coleta_diarios.sh && ./coleta_atos.sh
```
> **Note**
> Se você está usando Windows, utilize os arquivos que contenham _windows através de um Git Bash.

### Sobre o Processamento (Gabarito)
Para dar início ao processamento dos dados, foi montado um gabarito para processar o texto dos diários levando em consideração os seguintes pontos:
- Remover linhas em branco até o cabeçalho
- O cabeçalho (que contém a data e o nome da AMA) vir no início de cada extração de município uma vez -- deve ser repetido para cada município
- Vamos deixar www.diariomunicipal.com.br/ama repetir como separador/marcador de página 
- Remover tudo depois do último código identificador

## Como Usar
Ao coletar algum PDF do diário do site da [AMA](https://www.diariomunicipal.com.br/ama/) realize os seguintes passos. <br><br>
<strong>1. Pull da Imagem do Apache Tika</strong><br>
```
sudo docker pull apache/tika:1.28.4
```
<strong>2. Rodar Imagem do Apache Tika</strong><br>
```
sudo docker run -d -p 9998:9998 --rm --name tika apache/tika:1.28.4
```

<strong>3. Extrair Texto do PDF Usando Apache Tika</strong><br>

```
curl -v -H "Accept: text/plain" -H "Content-Type: application/pdf" -T diario-exemplo-entrada.pdf http://localhost:9998/tika -o diario-exemplo-saida-extraido.txt
```
Após o primeiro -T, colocamos o caminho do pdf que queremos extrair o texto. E depois de -o colocamos o caminho, nome e extensão do arquivo extraido.

## Testes
Atualmente temos mais de 60 casos de teste, que aferem a corretude dos dados.

<strong>Executar os testes</strong><br>
```
python -m unittest integracao_test.py
```
Ou
```
python3 -m unittest integracao_test.py
```
## Related

[Exoonero](https://exoonero.org) - Website do Projeto onde os dados aqui capturados são exibidos.

Os dados exibidos no site estão na pasta: docs/site/dados <br>
E podem ser gerados executando o código docs/site_home_data.py <br>
Que é responsável por gerar arquivos jsons contabilizando diários, nomeações e exonerações com base nos arquivos  gerados com a execução do <strong>Fluxo de Processamento Automático</strong>, mostrado tópicos [acima](https://github.com/exoonero/extrator/edit/main/README.md#autom%C3%A1tico).
