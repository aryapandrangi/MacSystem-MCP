# Dockerfile for MacSystem-Mcp Python FastMCP Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    procps \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastmcp \
    psutil \
    pillow \
    pypdf

# Copy application files
COPY mac_server.py .
COPY tools/ ./tools/
COPY tests/ ./tests/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command to start FastMCP server
CMD ["python3", "mac_server.py"]
