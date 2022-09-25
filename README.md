# IFAL - Querido Diário (OKBR)

# Fluxo de Processamento
PDF -> Tika -> Arquivo Extraído -> post_proc.py -> Arquivo(S) Proc <> Arquivo(S) Gabarito
O post_proc realiza o processamento do texto extraído para textos processados.
## Manuseando Contêiner Apache Tika

Observação: Para funcionar, é necessário utilizar a versão mais recente do apache tika. A versão que está no dockerfile do Querido Diário está desatualizado. Para obter a imagem mais recente, fizemos o pull de uma imagem docker.

### Executando Passo a Passo
```sh
# Realizar pull da imagem do apache tika
sudo docker pull apache/tika:1.28.4
# Rodar imagem mais recente do apache/tika
sudo docker run -d -p 9998:9998 --rm --name tika apache/tika:1.28.4
```

### Contêiner logs

```sh
sudo docker logs tika
```

### Entrando no Contêiner
```sh
docker exec -it tika bash
```

### Invocando Tika Manualmente

```sh
curl -v -H "Accept: text/plain" -H "Content-Type: application/pdf" -T diario-anadia-2022-08-29.pdf http://localhost:9998/tika
```
### Parando Contêiner

```sh
sudo docker stop tika
```
### Extrair texto do pdf e o salvando em um arquivo txt (sem tags html) e html
```sh
#Com o apache tika rodando
#Para txt:

curl -v -H "Accept: text/plain" -H "Content-Type: application/pdf" -T diario-anadia-2022-08-29.pdf http://localhost:9998/tika -o diario-anadia-2022-08-29-extraido.txt 

#Para html:

curl -v -H "Accept: text/html" -H "Content-Type: application/pdf" -T diario-anadia-2022-08-29.pdf http://localhost:9998/tika -o diario-anadia-2022-08-29-extraido.html
```


### Comandos
```sh
# docker build - constrói uma imagem docker
# docker pull - baixa uma imagem já existente
# docker run - roda uma imagem
```

### Como montamos o gabarito

- Remover linhas em branco até o cabeçalho
- Remover preâmbulo (parte em azul no diário)
- O cabeçalho (que contém a data e o nome da AMA) vir no início de cada extração de município **uma vez** -- deve ser repetido para cada município
- Vamos deixar `www.diariomunicipal.com.br/ama` repetir como separador/marcador de página (só não tocar nele, já está certinho)
- Remover tudo depois do último código identificador
