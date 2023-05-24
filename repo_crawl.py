import requests
import os
import sys

TOKEN = os.environ['API_TOKEN']
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

def check_junit(download_url)  -> bool:
    response = requests.get(download_url)
    if response.status_code == 200:
        if 'junit' in (response.content).decode('utf-8'):
            return True
    return False


def check_pom_xml(repository_url):
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
                return item['download_url']
    return None
 

def main():
    repo_urls = []

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
            download_url = check_pom_xml(repo_dict['html_url'])
            if download_url:
                if check_junit(download_url):
                    repo_urls.append(repo_dict['clone_url'])
    
    print(f'Number of repos that use Maven and JUnit: {len(repo_urls)}')
    sys.exit(0)

if __name__ == "__main__":
    main()

