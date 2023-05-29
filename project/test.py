import os
import requests
import subprocess

# GitHub API endpoint for searching repositories
api_url = "https://api.github.com/search/repositories"

# Query parameters for repository search
query_params = {
    "q": "language:java",  # Programming language: Java
    "per_page": 100,  # Number of repositories per page (adjust as needed)
}

# Send the request to the GitHub API
response = requests.get(api_url, params=query_params)

# Check if the request was successful
if response.status_code == 200:
    # Extract the JSON data from the response
    data = response.json()

    # Process each repository in the search results
    for item in data["items"]:
        repo_name = item["name"]
        repo_url = item["html_url"]
        print(f"Repository: {repo_name}")
        print(f"URL: {repo_url}")

        # Clone the repository
        # clone repository if it is not alredy cloned
        if not os.path.exists(repo_name):
            subprocess.run(["git", "clone", "--depth", "1", repo_url])
        else:
            print("Repository already cloned")

        # Check if the repository has a Maven build system
        is_maven_project = False
        if os.path.exists(f"{repo_name}/pom.xml"):
            is_maven_project = True
            print("Build system: Maven")
        else:
            # delete the cloned repository
            subprocess.run(["rm", "-rf", repo_name])
            print("No Maven build system found")
            continue
        
            # Add your code here to handle Maven-based projects

        # Check if the repository uses the JUnit framework
        has_junit_tests = False
        for root, dirs, files in os.walk(repo_name):
            if any(file.startswith("Test") and file.endswith(".java") for file in files):
                has_junit_tests = True
                break

        if has_junit_tests:
            print("Unit testing framework: JUnit")
        else:
            # delete the cloned repository
            subprocess.run(["rm", "-rf", repo_name])
            print("No JUnit tests found")
            continue
        
        # if the repository has maven and junit
        if is_maven_project and has_junit_tests:
            os.chdir(repo_name)
            # run maven test
            subprocess.run(["mvn", "test"])
            os.chdir("..")
            # delete the cloned repository
            subprocess.run(["rm", "-rf", repo_name])
            # run JUnit test
            subprocess.run(["java", "-jar", "junit-4.13.2.jar", "--class-path", f"{repo_name}/target/test-classes", "--scan-class-path"])
            
            

        print("\n")

else:
    print("Error occurred while fetching repositories:", response.status_code)
