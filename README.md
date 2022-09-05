# IFAL - Querido Diário (OKBR)

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
curl -v -H "Content-Type: application/pdf" -T diario-completo-2022-08-29.pdf http://localhost:9998/tika
```
### Parando Contêiner

```sh
sudo docker stop tika
```
### Extrair texto do pdf e o salvando em um arquivo txt e html
```sh
#Com o apache tika rodando e estando dentro da pasta "extrair-para-arquivo":
#Para txt:
(Está com o problema de o texto ser extraído juntamente de tags html)
curl -v -H "Content-Type: application/pdf" -T diario-completo-2022-08-29.pdf http://localhost:9998/tika -o index.txt 

#Para html:

curl -v -H "Content-Type: application/pdf" -T diario-completo-2022-08-29.pdf http://localhost:9998/tika -o index.html
```

### Comandos
```sh
# docker build - constrói uma imagem docker
# docker pull - baixa uma imagem já existente
# docker run - roda uma imagem
```
