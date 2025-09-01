# Use the official Python image from the Docker Hub
FROM python:3.10-alpine
RUN apk update && apk add busybox-extras
RUN adduser -D -s /bin/sh app

COPY .env /local-envs/.env

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY /app .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=America/Argentina/Mendoza

# Expose the port FastAPI will run on
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]