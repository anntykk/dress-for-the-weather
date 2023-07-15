# syntax=docker/dockerfile:1

# Use python base image
FROM python:3.9-slim

# Create Docker working directory
WORKDIR /app

# Copy files in local working directory to Docker working directory
COPY . .

# Install requirements
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside the container
EXPOSE 5000

# Instruct Docker to run app
CMD ["python", "app.py"]