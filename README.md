# IFAL - Querido Diário (OKBR)

## Manuseando Contêiner Apache Tika

### Executando

```sh
sudo docker build -t tika -f Dockerfile_apache_tika .
sudo docker run -d -p -p 9998:9998 --rm --name tika tika
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
curl -H "Content-Type: application/pdf" -X PUT -d @diario-completo-2022-08-29.pdf http://localhost:9998/tika

### Parando Contêiner

```sh
sudo docker stop tika
```