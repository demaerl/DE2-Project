import pulsar
import os
import subprocess
from pulsar import ConsumerType

BROKER_IP = '192.168.2.138'

def run_tests(url: str):
    repo_name = url.split('/')[-1][:-4]
    try:
        subprocess.run(['/usr/bin/git', 'clone', url])
    except Exception as e:
        print(f'Error cloning repo {url}: {e}')
    
    os.chdir(repo_name)
    try:
        print(f'Running tests of repo {repo_name}')
        subprocess.run(['/usr/bin/mvn', 'test'])
        os.chdir('..')
        subprocess.run(['rm', '-rf', repo_name])
    except Exception as e:
        print(f'Error running tests of repo {repo_name}: {e}')


def main():
    client = pulsar.Client(f'pulsar://{BROKER_IP}:6650')

    consumer = client.subscribe(
        'repo-URLs',
        'repo-sub',
        consumer_type=ConsumerType.Shared
    )

    while True:
        msg = consumer.receive()
        try:
            repo_url = msg.data().decode('utf-8')
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)
        print(f'Received repo URL: {repo_url}')
        run_tests(repo_url)

if __name__ == "__main__":
    main()