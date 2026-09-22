# Single-stage build for Ghost C2 Framework
FROM python:3.10-slim

WORKDIR /ghost

# Install system dependencies and build tools
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
    libssl3 \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies into system site-packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip cache purge

# Copy Ghost source code
COPY . /ghost

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/ghost
ENV HOME=/home/ghost

# Create non-root user and set ownership (optional security)
RUN groupadd -r ghost && useradd -r -g ghost ghost || true \
    && mkdir -p /home/ghost \
    && chown -R ghost:ghost /ghost /home/ghost

# Default command (run as ghost if possible)
USER ghost
CMD ["python3", "ghost/cli/ghostsh.py"]