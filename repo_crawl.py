import requests

def check_pom_xml(repository_url):
    # Extract owner and repository name from the URL
    parts = repository_url.split('/')
    owner = parts[-2]
    repo = parts[-1]

    # Make a GET request to retrieve the repository contents
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Check if any file has the name "pom.xml"
        contents = response.json()
        for item in contents:
            if item['name'] == 'pom.xml' and item['type'] == 'file':
                return True
    return False




for i in range(1,10):
    # Create an API request 
    url = 'https://api.github.com/search/repositories?q=language:java&per_page=100&sort=stars&page='+ str(i)
    response = requests.get(url)
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
    print('Owner:', repo_dict['owner']['login'])  #use the key owner and the the key login to get the dictionary describing the owner and the owner’s login name respectively.
    print('Stars:', repo_dict['stargazers_count'])  #print how many stars the project has earned
    print('Repository:', repo_dict['html_url'])  #print URL for the project’s GitHub repoitory
    print('Created:', repo_dict['created_at'])  #print when it was created
    print('Updated:', repo_dict['updated_at'])  #show when it was last updated
    print('Language:', repo_dict['language'])
    print('Description:', repo_dict['description']) #print the repository’s description
    # Call the function to check if pom.xml exists in the repository
    if check_pom_xml(repo_dict['html_url']):
        print("pom.xml exists in the repository.")
    else:
        print("pom.xml does not exist in the repository.")
    print('\n\n')



