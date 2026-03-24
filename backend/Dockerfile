# Use the official Python lightweight image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Prevent Python from writing .pyc files to disk and keep stdout unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (Uncomment if you need packages like psycopg2 for PostgreSQL)
# RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code
COPY . .

# Expose the port your application runs on (8000 is standard for FastAPI)
EXPOSE 8000

# Command to run the application in production 
# (Assuming FastAPI with Uvicorn. If you use Flask, you would use Gunicorn instead)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]