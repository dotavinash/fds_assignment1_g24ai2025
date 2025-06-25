# Use Python base image
FROM python:3.9-slim

# Create and set working directory
WORKDIR /app

# Copy everything from ./src to /app
COPY src/ .

# Install Flask (needed for API)
RUN pip install flask

# Expose the port
EXPOSE 5000

# Command to run the service
CMD ["python3", "node.py"]
