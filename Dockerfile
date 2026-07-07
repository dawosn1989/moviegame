# Use a lightweight, official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Expose the port the app runs on
EXPOSE 8005

# Command to run the application
CMD ["python", "server.py"]