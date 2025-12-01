# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV REFLEX_ENV prod

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        gnupg \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy the project requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Reflex specifically
RUN pip install reflex

# Copy the rest of the application code
COPY . .

# Install frontend dependencies and compile the app
RUN reflex export --frontend-only

# Expose the port that the app runs on
EXPOSE 8000

# Run the application
CMD ["reflex", "run", "--env", "prod"]