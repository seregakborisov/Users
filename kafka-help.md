1. `docker exec -it kafka sh` - вызвать терминал внутри контейнера кафки
2. `cd opt/kafka/bin/` - перейти в папку со скриптами кафки (можно сделать ls и удивиться сколько их)
3. `./kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic my-topic` - создание
4. `./kafka-console-producer.sh --bootstrap-server kafka:9092 --topic my-topic` - создать продюсера (интерактивная запись данных в топик)
