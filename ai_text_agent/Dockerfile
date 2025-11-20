# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY app ./app

# Expose port for HTTP
EXPOSE 8080

# Start the server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]