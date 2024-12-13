# Projeto Kafka - Laura Capssa e Vinícius Mattos

## Passos para Instalação

Este projeto utiliza o Apache Kafka em containers Docker para simular um ambiente distribuído de mensageria com múltiplos nós, incluindo a criação de tópicos, produção e consumo de mensagens, e testes de alta disponibilidade.

### Pré-requisitos
Antes de começar, você precisará ter os seguintes programas instalados:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

# Passo 1: Clonar o Repositório

Primeiro, clone o repositório para sua máquina local:

```bash
git clone https://github.com/laura-capssa/kafka-projeto
cd kafka-projeto
```

# Passo 2: Subir os Containers com Docker Compose

### 1. Navegue até o diretório do projeto
```bash
cd kafka-projeto
```

### 2. Suba os containers com o Docker Compose
```bash
docker-compose up -d
```
Isso irá iniciar os seguintes containers:
1. Zookeeper: Usado pelo Kafka para coordenação entre brokers.
2. Kafka: Brokers Kafka para armazenar e distribuir mensagens.
3. Kafdrop: Interface web para visualização de tópicos e mensagens do Kafka (disponível em http://localhost:9000).

### 3. Verifique se os containers estão em execução
```bash
docker ps
```
# Passo 3: Criação do Ambiente (Nodos, Partição, Fator de Replicação)
Para criar o ambiente com 4 nós Kafka, siga os passos abaixo:

O arquivo docker-compose.yml já está configurado para 4 nós Kafka (kafka1, kafka2, kafka3, kafka4), e um Zookeeper para coordenação.
As configurações de fator de replicação e partições são definidas automaticamente, mas podem ser alteradas nas configurações de criação de tópico no Kafka.
Para criar um tópico com 3 partições e fator de replicação 3, execute o seguinte comando em um dos containers Kafka:
```bash
docker exec -it kafka-projeto-kafka1-1 /bin/bash
kafka-topics.sh --create --topic test-topic --partitions 3 --replication-factor 3 --bootstrap-server kafka1:9092
```

**Produtor e Consumidor Normal** (Todos os Nodos On)
Para testar o produtor e consumidor com todos os nós em funcionamento, siga os seguintes passos:

**Produtor:**
Em um dos containers Kafka, execute o produtor:
```bash
docker exec -it kafka-projeto-kafka1-1 /bin/bash
kafka-console-producer.sh --broker-list kafka1:9092,kafka2:9093,kafka3:9094,kafka4:9095 --topic test-topic
```
**Consumidor:**
Em outro container Kafka, execute o consumidor:
```bash
docker exec -it kafka-projeto-kafka2-1 /bin/bash
kafka-console-consumer.sh --bootstrap-server kafka1:9092 --topic test-topic --from-beginning
```

Produtor e Consumidor com um dos Nodos Off (Derrubar um Nodo)
Para testar a resiliência do sistema, derrube um dos nós Kafka e verifique se a comunicação continua funcionando.

## 1. Derrubar um Nodo Kafka
Desligue um dos containers Kafka:
```bash
docker stop kafka-projeto-kafka1-1
```
## 2. Testar Produtor e Consumidor
Tente enviar e consumir mensagens novamente, como feito anteriormente. O Kafka deve continuar funcionando com o fator de replicação garantindo a disponibilidade.

# Passo 4: Produtor e Consumidor com um Nodo Novo (Adicionar um Nodo)
Para adicionar um novo broker ao cluster Kafka:

## 1. Adicionar Novo Nodo
Edite o arquivo docker-compose.yml para adicionar um novo container Kafka, alterando a configuração para um novo broker. Por exemplo:
```bash
kafka5:
  image: confluentinc/cp-kafka:latest
  environment:
    - KAFKA_BROKER_ID=5
    - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
    - KAFKA_LISTENER_SECURITY_PROTOCOL=PLAINTEXT
    - KAFKA_ADVERTISED_LISTENER=PLAINTEXT://kafka5:9096
  ports:
    - "9096:9092"
  networks:
    - kafka-net
```

## 2. Subir o Novo Nodo
Execute o comando para criar o novo broker Kafka:
```bash
docker-compose up -d kafka5
```
## 3. Testar Produtor e Consumidor
Após a adição do novo broker, teste novamente o produtor e consumidor para verificar se a comunicação ocorre corretamente com o novo nodo.

## 4. Consumidor com Leitura em Grupo
O Kafka suporta consumidores em grupos, o que permite que as mensagens sejam consumidas de forma balanceada entre os membros do grupo.

Para testar isso, você pode criar múltiplos consumidores em diferentes containers Kafka:
```bash
docker exec -it kafka-projeto-kafka2-1 /bin/bash
kafka-console-consumer.sh --bootstrap-server kafka1:9092 --topic test-topic --group test-group
```
Repita o comando em outro container Kafka. As mensagens enviadas pelo produtor serão consumidas pelos dois consumidores, balanceadas entre eles.

### Comando para listar o líder de um tópico

```bash
kafka-topics --bootstrap-server kafka1:9092 --describe --topic nome-do-topico | grep "Leader"
```

# Novidades em Relação ao Exemplo de Aula
Configuração de múltiplos brokers Kafka: No exemplo de aula, foi utilizado apenas um broker Kafka. Este projeto utiliza 4 brokers Kafka, distribuídos para fornecer maior resiliência e capacidade de escalabilidade.

Alta Disponibilidade: A configuração de replicação de tópicos foi implementada com o fator de replicação configurado como 3, garantindo que as mensagens sejam replicadas entre os brokers para maior disponibilidade e tolerância a falhas.

Adição de Novo Nodo Kafka: Foi incluída a capacidade de adicionar novos brokers ao cluster Kafka, com a modificação do docker-compose.yml para incluir um broker extra e reconfigurar o cluster de forma dinâmica.

Kafdrop para Monitoramento: A interface web Kafdrop foi configurada para permitir a visualização dos tópicos, consumidores e mensagens Kafka. Isso facilita a monitoração do sistema em tempo real.

Testes de Falha de Nodo: Foi realizado o teste de falha de um broker Kafka, derrubando um nodo para verificar se o Kafka ainda mantém sua operação com a alta disponibilidade garantida.

# Passo 5:  Acesse a interface do Kafdrop 
```bash
http://localhost:9000
```
Para visualizar os tópicos do Kafka.


# Passo 6: Prints
![Captura de tela 2024-12-06 194536](https://github.com/user-attachments/assets/81c57ce8-719c-41cf-894b-a555bf6f0e3c)

![Captura de tela 2024-12-06 195356](https://github.com/user-attachments/assets/8457bd01-bc77-49d2-9992-22c9c9652280)

![Captura de tela 2024-12-06 195423](https://github.com/user-attachments/assets/28183071-35e3-4254-8bee-3f3d313b42e0)

![Captura de tela 2024-12-06 200322](https://github.com/user-attachments/assets/93825414-0467-4748-9685-c6eab1b01967)

![Captura de tela 2024-12-06 202319](https://github.com/user-attachments/assets/7a9af42b-948f-4eff-9415-e2f0f2b10b18)

![Captura de tela 2024-12-06 204805](https://github.com/user-attachments/assets/cf328f4d-e656-47e3-ad6b-94f1a593c49c)


