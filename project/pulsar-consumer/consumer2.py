from pulsar import Client, Consumer, Message

pulsar_service_url = "pulsar://pulsar-broker:6650"
topic = "my-test-topic"
subscription = "my-test-subscription"

client = Client(pulsar_service_url)
consumer = client.subscribe(topic, subscription)

while True:
    message: Message = consumer.receive()

    try:
        print(f"Received message: {message.data().decode()}")
        consumer.acknowledge(message)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        consumer.negative_acknowledge(message)

    consumer.close()
    client.close()