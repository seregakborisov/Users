import json
import signal
import sys
from confluent_kafka import Consumer, KafkaError

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9095',
    'group.id': 'my-consumer-group-2',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
    'client.id': 'my-consumer-1',
}

consumer = Consumer(conf)
consumer.subscribe(['my-topic'])

running = True

def shutdown(sig, frame):
    global running
    print('\nShutting down...')
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

try:
    while running:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition, not an error
                continue
            else:
                print(f'Consumer error: {msg.error()}')
                break

        print(msg.topic())
        print(msg.offset())
        print(msg.timestamp())
        print(msg.value())

        # Commit offset after successful processing
        consumer.commit(asynchronous=False)

finally:
    # Close consumer, committing final offsets
    consumer.close()
    print('Consumer closed.')