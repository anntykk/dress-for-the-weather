# syntax=docker/dockerfile:1

# Use python base image
FROM python:3.9-slim

# Create Docker working directory
WORKDIR /app

# Copy files in local working directory to Docker working directory
COPY . .

# Install requirements
RUN pip install -r requirements.txt

# Instruct Docker to run app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]