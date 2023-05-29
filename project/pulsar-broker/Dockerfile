# Use a base image with Java and other necessary dependencies
FROM openjdk:11

# Set the working directory
WORKDIR /pulsar

# Install Pulsar broker dependencies
RUN apt-get update && apt-get install -y wget

# Download and extract Pulsar binary package
RUN wget https://archive.apache.org/dist/pulsar/pulsar-2.8.1/apache-pulsar-2.8.1-bin.tar.gz \
    && tar xvfz apache-pulsar-2.8.1-bin.tar.gz --strip-components=1 \
    && rm apache-pulsar-2.8.1-bin.tar.gz

# Set environment variables
ENV PULSAR_HOME /pulsar

# Expose necessary ports
EXPOSE 6650 8080

# Define the entry point command to start the Pulsar broker
CMD ["/pulsar/bin/pulsar", "standalone"]