import requests
import os

TOKEN = os.environ['API_TOKEN']
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

def check_junit(download_url)  -> bool:
    response = requests.get(download_url)
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

    for i in range(1,10):
        # Create an API request 
        url = 'https://api.github.com/search/repositories?q=language:java&per_page=100&sort=stars&page='+ str(i)
        response = requests.get(url, headers=HEADERS)
        print("Status code: ", response.status_code)
        # In a variable, save the API response.
        response_dict = response.json()
        # Evaluate the results.
        print(response_dict.keys())

        print("Total repos:", response_dict['total_count'])
        # find total number of repositories
        repos_dicts = response_dict['items']
        print("Repos found:", len(repos_dicts))
        # examine the first repository
        repo_dict = repos_dicts[0]

        print("The following is some information regarding the first repository:")
        print('Name:', repo_dict['name'])  #print the project's name
        print('Language:', repo_dict['language'])
        print('Description:', repo_dict['description']) #print the repository’s description
        # Call the function to check if pom.xml exists in the repository
        download_url = check_pom_xml(repo_dict['html_url'])
        if download_url:
            print("pom.xml exists in the repository, checking for junit keyword.")
            if check_junit(download_url):
                print("pom.xml contains JUnit tests.")
        print('\n\n')

if __name__ == "__main__":
    main()