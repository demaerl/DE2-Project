import os
import subprocess
from pulsar import Client, Consumer, Message
import traceback

pulsar_service_url = "pulsar://pulsar-broker:6650"
topic = "github-repos-topic"
subscription = "github-repos-subscription"

client = Client(pulsar_service_url)

consumer = client.subscribe(topic, subscription)

try:
    while True:
        message: Message = consumer.receive()

        try:
            repo_info = message.data().decode().split(",")
            repo_name = repo_info[0]
            repo_url = repo_info[1]

            print(f"Repository: {repo_name}")
            print(f"URL: {repo_url}")

            if not os.path.exists(repo_name):
                subprocess.run(["git", "clone", "--depth", "1", repo_url])
            else:
                print("Repository already cloned")

            is_maven_project = False
            if os.path.exists(f"{repo_name}/pom.xml"):
                is_maven_project = True
                print("Build system: Maven")
            else:
                subprocess.run(["rm", "-rf", repo_name])
                print("No Maven build system found")
                continue

            os.chdir(repo_name)

            subprocess.run(["mvn", "test"])

            os.chdir("..")

            subprocess.run(["rm", "-rf", repo_name])

            consumer.acknowledge(message)

            print("\n")

        except Exception as e:
            print(f"Error processing message: {str(e)}")
            print(traceback.format_exc())
            consumer.negative_acknowledge(message)
            
finally:
    consumer.close()
    client.close()