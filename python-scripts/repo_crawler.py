import requests
import os
import sys
import pulsar

TOKEN = os.environ['API_TOKEN']
HEADERS = {'Authorization': f'Bearer {TOKEN}'}
BROKER_IP = '192.168.2.138'

def init_producer():
    # Create a pulsar client by supplying ip address and port
    client = pulsar.Client(f'pulsar://{BROKER_IP}:6650')

    # Create a producer on the topic that consumer can subscribe to
    producer = client.create_producer('repo-URLs')

    return producer

def check_junit(download_url)  -> bool:
    response = requests.get(download_url)
    if response.status_code == 200:
        if 'junit' in (response.content).decode('utf-8'):
            return True
    return False


def check_maven_junit(repository_url):
    # Extract owner and repository name from the URL
    parts = repository_url.split('/')
    owner = parts[-2]
    repo = parts[-1]

    # Make a GET request to retrieve the repository contents
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(api_url, headers=HEADERS)
    
    if response.status_code == 200:
        # Check if any file has the name "pom.xml"
        contents = response.json()
        for item in contents:
            if item['name'] == 'pom.xml' and item['type'] == 'file':
                return check_junit(item['download_url'])
    return False
 

def main():
    producer = init_producer()

    for i in range(0,10):
        print(f'Round {i} of 10')
        # Create an API request 
        url = 'https://api.github.com/search/repositories?q=language:java&per_page=100&sort=stars&page='+ str(i)
        response = requests.get(url, headers=HEADERS)
        response_dict = response.json()
        # find total number of repositories
        repos_dicts = response_dict['items']
        # examine the first repository
        for j in range(0,len(repos_dicts)):
            repo_dict = repos_dicts[j]
            # Call the function to check if pom.xml exists in the repository
            clone_url = repo_dict['clone_url']
            if check_maven_junit(repo_dict['html_url']):
                print(f'Sending download url: {clone_url}')
                producer.send(clone_url.encode('utf-8'))
    
    producer.close()
    sys.exit(0)

if __name__ == "__main__":
    main()

