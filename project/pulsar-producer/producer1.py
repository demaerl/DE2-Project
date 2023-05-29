import os
import requests
from pulsar import Client, Producer

pulsar_service_url = "pulsar://pulsar-broker:6650"
topic = "github-repos-topic"

api_url = "https://api.github.com/search/repositories"
query_params = {
    "q": "language:java",  
    "per_page": 100,  
}
response = requests.get(api_url, params=query_params)
if response.status_code == 200:
    data = response.json()

    client = Client(pulsar_service_url)

    producer = client.create_producer(topic)

    for item in data["items"]:
        repo_name = item["name"]
        repo_url = item["html_url"]

        has_maven_build = False
        if requests.get(f"{repo_url}/blob/master/pom.xml").status_code == 200:
            has_maven_build = True

        has_junit_tests = False
        if requests.get(f"{repo_url}/blob/master/src/test/java/org/junit").status_code == 200:
            has_junit_tests = True

        if has_maven_build and has_junit_tests:
            message = f"{repo_name},{repo_url}".encode()
            producer.send(message)

    producer.close()
    client.close()

else:
    print("Error occurred while fetching repositories:", response.status_code)