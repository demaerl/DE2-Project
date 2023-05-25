import pulsar
import os
import subprocess
from pulsar import ConsumerType

BROKER_IP = '192.168.2.138'

def run_tests(url: str):
    try:
        subprocess.run(["/usr/bin/git", "clone", url])
    except Exception as e:
        print(f'Error cloning repo {url}: {e}')

    # TODO

# def on_receive(consumer, msg):
#     try:
#         repo_url = msg.data().decode('utf-8')
#         consumer.acknowledge(msg)
#         print(f'Received repo URL: {repo_url}')
#         # run_tests(repo_url)
#     except:
#         consumer.negative_acknowledge(msg)

def main():
    client = pulsar.Client(f'pulsar://{BROKER_IP}:6650')

    consumer = client.subscribe(
        'repo-URLs',
        'repo-sub',
        consumer_type=ConsumerType.Shared
    )

    msg = consumer.receive()
    try:
        repo_url = msg.data().decode('utf-8')
        consumer.acknowledge(msg)
        print(f'Received repo URL: {repo_url}')
        # run_tests(repo_url)
    except:
        consumer.negative_acknowledge(msg)

if __name__ == "__main__":
    main()