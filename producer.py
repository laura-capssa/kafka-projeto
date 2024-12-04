from kafka import KafkaProducer

# Inicializa o produtor Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Envia 10 mensagens para o tópico
for i in range(10):
    message = f"Mensagem {i}".encode('utf-8')  # Codifica a mensagem
    producer.send('exemplo-topico', message)  # Envia a mensagem para o tópico
    print(f"Enviada: {message}")  # Confirma o envio no console

# Fecha o produtor para liberar recursos
producer.close()

