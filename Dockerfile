# Use a slim version of Python 3.9 as the base image
FROM python:3.9-slim

# Update package lists and upgrade packages
RUN apt-get update && apt-get upgrade -y

# Install any necessary system dependencies (if needed)
RUN apt-get install -y some-package

# Set environment variables
ENV PYTHON_VERSION=3.9.21
ENV LANG=C.UTF-8

# Upgrade pip, setuptools, and flask
RUN pip install --upgrade pip setuptools flask

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the necessary port
EXPOSE 5000

# Command to run your application
CMD ["python", "app.py"]


