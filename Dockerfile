# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script into the container
COPY analyzer.py .

# Set the default executable for the container
ENTRYPOINT ["python3", "analyzer.py"]
