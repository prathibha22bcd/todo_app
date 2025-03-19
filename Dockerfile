# Use an official lightweight Python image
FROM python:3.9-slim  

# Set the working directory inside the container
WORKDIR /app  

# Copy only necessary files first (to leverage Docker's layer caching)
COPY requirements.txt .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application code
COPY . .  

# Expose the required port
EXPOSE 5000  

# Define the command to run the application
CMD ["python", "app.py"]
