import os
import requests
from pulsar import Client, Producer

def fetch_github_repos(session, url, params):
    response = session.get(url, params=params)
    response.raise_for_status()
    return response.json()

def check_file_exists(session, url):
    response = session.get(url)
    return response.status_code == 200

pulsar_service_url = "pulsar://pulsar-broker:6650"
topic = "github-repos-topic"
api_url = "https://api.github.com/search/repositories"
query_params = {
    "q": "language:java",  
    "per_page": 100,  
}

with requests.Session() as session:
    try:
        data = fetch_github_repos(session, api_url, query_params)

        client = Client(pulsar_service_url)
        producer = client.create_producer(topic)

        for item in data["items"]:
            repo_name = item["name"]
            repo_url = item["html_url"]

            has_maven_build = check_file_exists(session, f"{repo_url}/blob/master/pom.xml")
            has_junit_tests = check_file_exists(session, f"{repo_url}/blob/master/src/test/java/org/junit")

            if has_maven_build and has_junit_tests:
                message = f"{repo_name},{repo_url}".encode()
                producer.send(message)

        producer.close()
        client.close()
        
    except requests.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")