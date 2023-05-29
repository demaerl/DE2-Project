# Use a base image with Maven and JDK
FROM maven:3.8.4-jdk-11

ARG TOKEN

ENV API_TOKEN=$TOKEN

# Set the working directory
WORKDIR /app

# Copy the application code into the Docker image
COPY . /app

RUN apt-get update && apt-get install -y python3-pip

# install python
RUN apt-get install -y python3

RUN pip install -r requirements.txt

# Expose necessary ports
EXPOSE 6650 8080

# Define the entry point command
CMD [ "python3", "producer.py"]
