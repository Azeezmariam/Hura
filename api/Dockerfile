# Use specific version for better reproducibility
FROM python:3.10-slim

# Set environment variables early for better layer caching
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create user with permissions
RUN adduser --disabled-password --gecos "" appuser && \
    mkdir -p /data && \
    chown -R appuser:appuser /data

# Set persistent storage and PATH
ENV PERSISTENT_DIR=/data \
    PATH="/home/appuser/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY --chown=appuser:appuser requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files (after dependencies for better caching)
COPY --chown=appuser:appuser . .

# Set environment variables for the application
ENV VECTOR_DB_PATH=$PERSISTENT_DIR/vector_db \
    MODEL_CACHE=$PERSISTENT_DIR/models

# Create persistent directories
RUN mkdir -p $VECTOR_DB_PATH $MODEL_CACHE && \
    chown -R appuser:appuser $PERSISTENT_DIR

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Expose port
EXPOSE 7860

# Start application with proper signal handling
CMD ["uvicorn", "app_whatsapp:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"] 