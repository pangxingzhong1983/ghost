# Multi-stage build for Ghost C2 Framework
# Stage 1: Builder - install build dependencies and compile native extensions
FROM python:3.10-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    libssl-dev \
    swig \
    libmagic1 \
    libpcap-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime - minimal image with only runtime dependencies
FROM python:3.10-slim

WORKDIR /ghost

# Create non-root user for security
RUN groupadd -r ghost && useradd -r -g ghost ghost

# Install runtime dependencies (only what's needed at runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 \
    libmagic1 \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy Ghost source code
COPY . /ghost

# Ensure Python can find user-installed packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/ghost
ENV PYTHONUNBUFFERED=1

# Set ownership to non-root user
RUN chown -R ghost:ghost /ghost
USER ghost

# Default command
CMD ["python3", "ghost/cli/ghostsh.py"]