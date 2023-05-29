from pulsar import Client, Producer

pulsar_service_url = "pulsar://pulsar-broker:6650"
topic = "my-test-topic"

client = Client(pulsar_service_url)
producer = client.create_producer(topic)

message = "Hello, Pulsar!".encode()
producer.send(message)

producer.close()
client.close()