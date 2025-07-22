# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app directory
COPY app ./app
COPY Frontend ./Frontend

# Create tmp directory for Excel output
RUN mkdir -p /app/app/tmp

# Expose the port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "app.Server:app", "--host", "0.0.0.0", "--port", "8000"]
