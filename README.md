# IFAL - Querido Diário (OKBR)

## Manuseando Contêiner Apache Tika

Observação: Para funcionar, é necessário utilizar a versão mais recente do apache tika. A versão que está no dockerfile do Querido Diário está desatualizado. Para obter a imagem mais recente, fizemos o pull de uma imagem docker.
```sh
sudo docker pull apache/tika:1.28.4
```
### Executando 

```sh
<<<<<<< HEAD
# Set up do dockerfile do querido diário (versão 1.24.1)
    #sudo docker build -t tika -f Dockerfile_apache_tika .
    #sudo docker run -d -p -p 9998:9998 --rm --name tika tika

# Rodar imagem mais recente do apache/tika
sudo docker run -d -p 9998:9998 --rm --name tika apache/tika:1.28.4
=======
sudo docker build -t tika -f Dockerfile_apache_tika .
sudo docker run -d -p 9998:9998 --rm --name tika tika
>>>>>>> dbdbcf9734a853b5d982410867af426a4d02d605
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
<<<<<<< HEAD
curl -v -H "Content-Type: application/pdf" -T diario-completo-2022-08-29.pdf http://localhost:9998/tika
=======
curl -H "Content-Type: application/pdf" -X PUT -d @diario-completo-2022-08-29.pdf http://localhost:9998/tika
>>>>>>> dbdbcf9734a853b5d982410867af426a4d02d605
```
### Parando Contêiner

```
sh
sudo docker stop tika
```

### Comandos
```sh
# docker build - constrói uma imagem docker
# docker pull - baixa uma imagem já existente
# docker run - roda uma imagem
```
