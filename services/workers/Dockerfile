FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY workers/requirements.txt .
COPY shared/requirements.txt ./shared-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r shared-requirements.txt

# Copy shared modules and application code
COPY shared /app/shared
COPY workers/app /app/workers

# Set PYTHONPATH to include /app so that 'shared' module can be found
ENV PYTHONPATH=/app

# Create non-root user
RUN useradd -m -u 1000 vetrai && \
    chown -R vetrai:vetrai /app

USER vetrai

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
WORKDIR /app/workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
