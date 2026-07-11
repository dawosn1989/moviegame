# Use a lightweight, official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all of your code from the Pi into the container's /app folder
COPY . /app

# If your game uses external libraries, uncomment the line below to install them:
# RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8005

# Command to run the application
CMD ["python", "server.py"]