# Use an official Python image
FROM python:3.9-slim  

# Set the working directory
WORKDIR /app  

# Copy only dependencies first (for better caching)
COPY requirements.txt .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application
COPY . .  

# Expose the application port
EXPOSE 5000  

# Define the command to start the app
CMD ["python", "app.py"]

RUN pip install --upgrade pip flask setuptools

