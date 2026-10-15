import json
import socket
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'localhost:9095',   # Kafka broker(s)
    'client.id': socket.gethostname(),
    'acks': 'all',                           # Wait for all replicas (durability)
}

producer = Producer(conf)

def delivery_report(err, msg):
    """Callback called once for each produced message."""
    if err is not None:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

def send_message(topic, key, value):
    """Send a single JSON message."""
    producer.produce(
        topic,
        key=key.encode('utf-8'),
        value=json.dumps(value).encode('utf-8'),
        callback=delivery_report,
    )
    # Serve delivery callbacks without blocking
    producer.poll(0)

if __name__ == '__main__':
    topic = 'my-topic'

    for i in range(5):
        send_message(
            topic,
            key=f'key-{i}',
            value={'id': i, 'message': f'hello {i}'},
        )

    # Wait for all messages to be delivered
    producer.flush()
    print('All messages flushed.')