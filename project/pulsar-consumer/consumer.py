import pulsar
import os
import subprocess
from pulsar import ConsumerType

BROKER_IP = os.environ['BROKER_IP']

def run_tests(url: str):
    repo_name = url.split('/')[-1][:-4]
    try:
        subprocess.run(['/usr/bin/git', 'clone', url])
    except Exception as e:
        print(f'Error cloning repo {url}: {e}')
    
    os.chdir(repo_name)
    try:
        print(f'Running tests of repo {repo_name}')
        subprocess.run(['/usr/bin/mvn', 'test'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        os.chdir('..')
        print(f'Tests of repo {repo_name} finished')
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
        repo_name = repo_url.split('/')[-1][:-4]
        with open('/app/log.txt', 'a') as logfile:
            logfile.write(f'{repo_name}\n')

if __name__ == "__main__":
    main()