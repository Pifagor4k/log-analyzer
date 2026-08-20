# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Step 1: Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Copy the rest of the application
COPY src/ ./src/
COPY main.py .

# Set the default executable for the container
ENTRYPOINT ["python3", "main.py"]