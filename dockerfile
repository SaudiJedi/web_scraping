# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y firefox-esr && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver for Firefox
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    rm /tmp/geckodriver.tar.gz

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Define the command to run your script
CMD ["python", "script.py"]  # replace your_script.py with your actual script name
