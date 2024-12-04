from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'exemplo-topico',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='grupo-consumidores'
)

for message in consumer:
    print(f"Recebida: {message.value.decode('utf-8')}")

